"""
Graph construction and compilation for the orchestrator-worker workflow.
Defines the execution flow and state management.
"""

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import InMemorySaver

from logger import get_logger
from schemas import GraphState
from nodes import OrchestratorNode, WorkerNode, CollectorNode

logger = get_logger(__name__)


class WorkflowGraph:
    """Builds and manages the orchestrator-worker workflow graph."""

    def __init__(
        self,
        llm: ChatOpenAI,
        max_workers: int = 4,
        enable_checkpointing: bool = True,
    ) -> None:
        """Initialize the workflow graph.

        Args:
            llm: The language model to use for all nodes.
            max_workers: Maximum number of concurrent workers.
            enable_checkpointing: Whether to enable state checkpointing.
        """
        self.llm = llm
        self.max_workers = max_workers
        self.enable_checkpointing = enable_checkpointing
        self.logger = get_logger(__class__.__name__)

        self._graph = None
        self._nodes = None

    def build(self):
        """Build the workflow graph.

        Returns:
            CompiledGraph: The compiled workflow graph.
        """
        self.logger.info("Building workflow graph...")

        # Initialize nodes
        orchestrator = OrchestratorNode(self.llm)
        worker = WorkerNode(self.llm, max_workers=self.max_workers)
        collector = CollectorNode(self.llm)

        self._nodes = {
            "orchestrator": orchestrator,
            "worker": worker,
            "collector": collector,
        }

        # Create graph
        builder = StateGraph(GraphState)
        builder.add_node("orchestrator", orchestrator)
        builder.add_node("worker", worker)
        builder.add_node("collector", collector)

        # Add edges
        builder.add_edge(START, "orchestrator")
        builder.add_edge("orchestrator", "worker")
        builder.add_edge("worker", "collector")
        builder.add_edge("collector", END)

        # Compile graph
        checkpointer = InMemorySaver() if self.enable_checkpointing else None
        self._graph = builder.compile(checkpointer=checkpointer)

        self.logger.info("Workflow graph built successfully")
        return self._graph

    def get_graph(self):
        """Get the compiled graph.

        Returns:
            CompiledGraph: The compiled workflow graph.

        Raises:
            RuntimeError: If graph has not been built yet.
        """
        if self._graph is None:
            raise RuntimeError(
                "Graph has not been built yet. Call build() first.",
            )
        return self._graph

    def visualize(self, output_path: str = "workflow_graph.png") -> None:
        """Generate a visualization of the workflow graph.

        Args:
            output_path: Path to save the graph visualization.
        """
        if self._graph is None:
            raise RuntimeError(
                "Graph has not been built yet. Call build() first.",
            )

        try:
            self.logger.info(
                f"Generating graph visualization to {output_path}",
            )
            self._graph.get_graph().draw_mermaid_png(
                output_file_path=output_path,
            )
            self.logger.info(f"Visualization saved to {output_path}")
        except Exception as e:
            self.logger.warning(f"Failed to generate visualization: {str(e)}")
