import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import InMemorySaver

from schemas import Orchestrator_LLM_Output, Graph_State

load_dotenv()

# Ensuring the environment variable for OpenAI API key is set
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
else:
    print("OPENAI_API_KEY is set in the environment variables.")

# This is the main entry point for the
#  orchestrator-worker-agentic-ai-workflow project.

# LLM Initialization
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.7,
)

llm_with_output = llm.with_structured_output(schema=Orchestrator_LLM_Output)

# Checkpoint Saver Initialization
memory = InMemorySaver()

# Creating Graph Nodes
##############################


# Orchestrator Node: This node takes the initial query and breaks it down
# into tasks.
def orchestrator_node(state: Graph_State) -> Graph_State:
    """Orchestrator node that breaks down the query into tasks."""
    query = state.query
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an orchestrator agent that breaks down a query "
                "into tasks.",  # noqa
            ),
            (
                "user",
                "Given the query: {query}, break it down into a list "
                "of tasks.",  # noqa
            ),
        ]
    )
    orchestrator_chain = prompt | llm_with_output
    response = orchestrator_chain.invoke({"query": query})
    return state.model_copy(update={"tasks": response.tasks})


# Utility Function: This function to perform a specific task and
# return the results.
def execute_task(task: str) -> str:
    """Execute a specific task and return the result.

    Args:
        task (str): The task to be executed.

    Returns:
        str: The result of executing the task.
    """
    response = llm.invoke(f"Perform the following task: {task}")
    return response.content


# Worker Node: This node takes the tasks from the orchestrator
# and executes them in a thread.
def worker_node(state: Graph_State) -> Graph_State:
    """Worker node that executes the tasks provided by the orchestrator."""
    tasks = state.tasks
    results = []
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        results = list(executor.map(execute_task, tasks))
    return state.model_copy(update={"results": results})


def collector_node(state: Graph_State) -> Graph_State:
    """Collector node that summarizes the results obtained from the worker."""
    results = state.results
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a collector agent that summarizes the results "
                "obtained from the worker.",  # noqa
            ),
            (
                "user",
                "Given the following results: {results}, provide a summary.",
            ),
        ]
    )
    collector_chain = prompt | llm
    response = collector_chain.invoke({"results": results})
    return state.model_copy(update={"summary": response.content})


# Building the Graph
##############################
builder = StateGraph(Graph_State)
builder.add_node("orchestrator_node", orchestrator_node)
builder.add_node("worker_node", worker_node)
builder.add_node("collector_node", collector_node)

builder.add_edge(START, "orchestrator_node")
builder.add_edge("orchestrator_node", "worker_node")
builder.add_edge("worker_node", "collector_node")
builder.add_edge("collector_node", END)

graph = builder.compile(checkpointer=memory)

graph.get_graph().draw_mermaid_png(
    output_file_path="orchestrator_worker_graph_architecture.png"
)


def main():
    # Testing the graph with a sample query
    config = {"configurable": {"thread_id": "1"}}
    initial_state: Graph_State = Graph_State(
        query=(
            "What is the capital of USA and what is the "
            "population of USA. Also, How many states do we have "
            "in Nigeria and what is Nigeria's capital?"
        ),
        tasks=[],
        results=[],
        summary="",
    )

    for chunk in graph.stream(
        initial_state,
        stream_mode="updates",
        config=config,
    ):
        print(chunk)


if __name__ == "__main__":
    # Testing the Graph Agent
    main()
