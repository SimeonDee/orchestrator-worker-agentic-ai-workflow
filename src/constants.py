"""
Constants used throughout the orchestrator-worker agentic AI workflow.
"""

# LLM Configuration
DEFAULT_LLM_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7

# Graph Configuration
DEFAULT_THREAD_ID = "1"
DEFAULT_MAX_WORKERS = 4

# Prompts
ORCHESTRATOR_SYSTEM_PROMPT = (
    "You are an orchestrator agent that breaks down a complex query "
    "into smaller, manageable tasks. Provide a list of clear, specific tasks "
    "that need to be executed to answer the user's query."
)

ORCHESTRATOR_USER_PROMPT = (
    "Given the query: {query}, break it down into a list of tasks."
)

COLLECTOR_SYSTEM_PROMPT = (
    "You are a collector agent that synthesizes and summarizes results "
    "obtained from worker agents. Provide a comprehensive, well-structured "
    "summary."
)

COLLECTOR_USER_PROMPT = (
    "Given the following results: {results}, provide a comprehensive summary."
)

WORKER_TASK_PROMPT_TEMPLATE = "Perform the following task: {task}"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Error Messages
ERROR_MISSING_API_KEY = (
    "OPENAI_API_KEY is not set in the environment " "variables."
)  # noqa
ERROR_EMPTY_TASKS = "Orchestrator produced no tasks from the query."
ERROR_EXECUTION_FAILED = "Failed to execute task: {task}"
