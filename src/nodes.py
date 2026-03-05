"""
Graph node definitions for the orchestrator-worker agentic AI workflow.
Each node represents a step in the processing pipeline.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from logger import get_logger
from schemas import GraphState, OrchestratorLLMOutput
from constants import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    ORCHESTRATOR_USER_PROMPT,
    COLLECTOR_SYSTEM_PROMPT,
    COLLECTOR_USER_PROMPT,
    WORKER_TASK_PROMPT_TEMPLATE,
)

logger = get_logger(__name__)


class OrchestratorNode:
    """Orchestrator node that breaks down queries into tasks."""

    def __init__(self, llm: ChatOpenAI) -> None:
        """Initialize the orchestrator node.

        Args:
            llm: The language model to use for task decomposition.
        """
        self.llm = llm
        self.llm_with_output = llm.with_structured_output(
            schema=OrchestratorLLMOutput,
        )
        self.logger = get_logger(__class__.__name__)

    def __call__(self, state: GraphState) -> GraphState:
        """Execute the orchestrator node.

        Args:
            state: The current graph state.

        Returns:
            GraphState: Updated state with decomposed tasks.

        Raises:
            ValueError: If LLM fails to produce tasks.
        """
        query = state.query
        self.logger.info(f"Orchestrating query: {query[:100]}...")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", ORCHESTRATOR_SYSTEM_PROMPT),
                ("user", ORCHESTRATOR_USER_PROMPT),
            ]
        )

        orchestrator_chain = prompt | self.llm_with_output
        response = orchestrator_chain.invoke({"query": query})

        self.logger.info(f"Generated {len(response.tasks)} tasks")
        return state.model_copy(update={"tasks": response.tasks})


class WorkerNode:
    """Worker node that executes tasks in parallel."""

    def __init__(self, llm: ChatOpenAI, max_workers: int = 4) -> None:
        """Initialize the worker node.

        Args:
            llm: The language model to use for task execution.
            max_workers: Maximum number of concurrent workers.
        """
        self.llm = llm
        self.max_workers = max_workers
        self.logger = get_logger(__class__.__name__)

    def execute_task(self, task: str) -> str:
        """Execute a single task.

        Args:
            task: The task to execute.

        Returns:
            str: The result of the task execution.

        Raises:
            Exception: If task execution fails.
        """
        try:
            self.logger.debug(f"Executing task: {task[:100]}...")
            response = self.llm.invoke(
                WORKER_TASK_PROMPT_TEMPLATE.format(task=task),
            )
            self.logger.debug("Task completed successfully")
            return response.content
        except Exception as e:
            self.logger.error(f"Failed to execute task: {str(e)}")
            raise

    def __call__(self, state: GraphState) -> GraphState:
        """Execute the worker node.

        Args:
            state: The current graph state.

        Returns:
            GraphState: Updated state with task results.
        """
        from concurrent.futures import ThreadPoolExecutor

        tasks = state.tasks
        self.logger.info(
            f"Processing {len(tasks)} tasks with {self.max_workers} workers",
        )

        results = []
        with ThreadPoolExecutor(
            max_workers=min(self.max_workers, len(tasks))
        ) as executor:
            results = list(executor.map(self.execute_task, tasks))

        self.logger.info(f"All tasks completed. Got {len(results)} results")
        return state.model_copy(update={"results": results})


class CollectorNode:
    """Collector node that summarizes task results."""

    def __init__(self, llm: ChatOpenAI) -> None:
        """Initialize the collector node.

        Args:
            llm: The language model to use for summarization.
        """
        self.llm = llm
        self.logger = get_logger(__class__.__name__)

    def __call__(self, state: GraphState) -> GraphState:
        """Execute the collector node.

        Args:
            state: The current graph state.

        Returns:
            GraphState: Updated state with summary.
        """
        results = state.results
        self.logger.info(f"Collecting {len(results)} results")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", COLLECTOR_SYSTEM_PROMPT),
                ("user", COLLECTOR_USER_PROMPT),
            ]
        )

        collector_chain = prompt | self.llm
        response = collector_chain.invoke({"results": results})

        self.logger.info("Results collected and summarized")
        return state.model_copy(update={"summary": response.content})
