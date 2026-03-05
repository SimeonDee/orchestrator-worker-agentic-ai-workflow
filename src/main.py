"""
Main entry point for the orchestrator-worker agentic AI workflow.
Demonstrates the multi-agent workflow with proper error handling and logging.
"""

from langchain_openai import ChatOpenAI

from config import get_config
from logger import setup_logger
from graph import WorkflowGraph
from schemas import GraphState


def main() -> None:
    """Run the orchestrator-worker workflow with a sample query."""
    # Load configuration
    config = get_config()

    # Setup logging
    logger = setup_logger(
        "orchestrator-worker",
        level=config.logging.level,
        log_format=config.logging.format,
    )

    logger.info("Starting orchestrator-worker agentic AI workflow")

    try:
        # Initialize LLM
        logger.info(f"Initializing LLM with model: {config.llm.model}")
        llm = ChatOpenAI(
            api_key=config.llm.api_key,
            model=config.llm.model,
            temperature=config.llm.temperature,
        )

        # Build workflow graph
        workflow = WorkflowGraph(
            llm=llm,
            max_workers=config.worker.max_workers,
            enable_checkpointing=True,
        )
        graph = workflow.build()

        # Generate graph visualization
        logger.info("Generating workflow visualization")
        workflow.visualize(
            output_path="orchestrator_worker_graph_architecture.png",
        )

        # Create initial state
        initial_state = GraphState(
            query=(
                "What is the capital of USA and what is the "
                "population of USA? Also, how many states do we have "
                "in Nigeria and what is Nigeria's capital?"
            ),
        )

        logger.info(f"Processing query: {initial_state.query}")

        # Execute workflow
        config_dict = {"configurable": {"thread_id": "1"}}

        for idx, chunk in enumerate(
            graph.stream(
                initial_state,
                stream_mode="updates",
                config=config_dict,
            ),
            1,
        ):
            logger.info(f"Step {idx}: {chunk}")
            print(f"\n{'='*80}")
            print(f"Step {idx}:")
            print(f"{'='*80}")
            print(chunk)

        logger.info("Workflow completed successfully")

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error during workflow execution: {str(e)}",
            exc_info=True,
        )
        raise


if __name__ == "__main__":
    main()
