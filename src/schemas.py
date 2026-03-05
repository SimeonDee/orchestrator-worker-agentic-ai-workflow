# from typing import Annotated
from pydantic import BaseModel, Field

# from langgraph.graph import add_messages


class Orchestrator_LLM_Output(BaseModel):
    tasks: list[str] = Field(
        ..., description="A list of tasks to be performed by worker agent."
    )


class Graph_State(BaseModel):
    query: str = Field(..., description="The query or task to be performed.")
    tasks: list[str] = Field(
        ..., description="A list of tasks to be performed by worker agent."
    )
    results: list[str] = Field(
        ...,
        description="A list of results from the worker agent after "
        "performing the tasks.",
    )
    summary: str = Field(
        ...,
        description="A summary of the results obtained by collector "
        "agent from the worker agent.",
    )
