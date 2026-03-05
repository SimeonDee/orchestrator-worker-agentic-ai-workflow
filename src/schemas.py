"""
Data schemas and models for the orchestrator-worker agentic AI workflow.
Uses Pydantic for validation and serialization.
"""

from pydantic import BaseModel, Field, validator


class OrchestratorLLMOutput(BaseModel):
    """Output schema for the orchestrator LLM node.

    Attributes:
        tasks: A list of actionable tasks extracted from the user query.
    """

    tasks: list[str] = Field(
        ...,
        description="A list of tasks to be performed by worker agent.",
        min_items=1,
    )

    @validator("tasks")
    def validate_tasks(cls, v: list[str]) -> list[str]:
        """Validate that tasks are non-empty strings."""
        if not v:
            raise ValueError("Tasks list cannot be empty")
        if any(not task.strip() for task in v):
            raise ValueError("All tasks must be non-empty strings")
        return [task.strip() for task in v]


class GraphState(BaseModel):
    """State model for the orchestrator-worker graph.

    Attributes:
        query: The initial user query.
        tasks: Decomposed list of tasks from the orchestrator.
        results: Results from executing each task.
        summary: Final summary of all results from the collector.
    """

    query: str = Field(
        ...,
        description="The original query or task to be performed.",
        min_length=1,
    )
    tasks: list[str] = Field(
        default_factory=list,
        description="A list of tasks to be performed by worker agent.",
    )
    results: list[str] = Field(
        default_factory=list,
        description="A list of results from executing the tasks.",
    )
    summary: str = Field(
        default="",
        description="A comprehensive summary of all results.",
    )

    @validator("query")
    def validate_query(cls, v: str) -> str:
        """Validate and clean the query string."""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


# Backward compatibility aliases
Orchestrator_LLM_Output = OrchestratorLLMOutput
Graph_State = GraphState
