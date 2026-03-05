"""
Tests for the schemas module.
"""

import pytest

from schemas import GraphState, OrchestratorLLMOutput


class TestGraphState:
    """Test cases for GraphState model."""

    def test_valid_graph_state(self):
        """Test creating a valid GraphState."""
        state = GraphState(query="What is AI?")
        assert state.query == "What is AI?"
        assert state.tasks == []
        assert state.results == []
        assert state.summary == ""

    def test_graph_state_with_all_fields(self):
        """Test GraphState with all fields populated."""
        state = GraphState(
            query="What is AI?",
            tasks=["Task 1", "Task 2"],
            results=["Result 1", "Result 2"],
            summary="Summary",
        )
        assert state.query == "What is AI?"
        assert len(state.tasks) == 2
        assert len(state.results) == 2
        assert state.summary == "Summary"

    def test_empty_query_raises_error(self):
        """Test that empty query raises validation error."""
        with pytest.raises(ValueError):
            GraphState(query="")

    def test_whitespace_only_query_raises_error(self):
        """Test that whitespace-only query raises validation error."""
        with pytest.raises(ValueError):
            GraphState(query="   ")

    def test_query_is_stripped(self):
        """Test that query is stripped of leading/trailing whitespace."""
        state = GraphState(query="  What is AI?  ")
        assert state.query == "What is AI?"


class TestOrchestratorLLMOutput:
    """Test cases for OrchestratorLLMOutput model."""

    def test_valid_orchestrator_output(self):
        """Test creating valid orchestrator output."""
        output = OrchestratorLLMOutput(tasks=["Task 1", "Task 2"])
        assert len(output.tasks) == 2
        assert output.tasks == ["Task 1", "Task 2"]

    def test_empty_tasks_raises_error(self):
        """Test that empty tasks list raises validation error."""
        with pytest.raises(ValueError):
            OrchestratorLLMOutput(tasks=[])

    def test_whitespace_only_task_raises_error(self):
        """Test that whitespace-only tasks raise validation error."""
        with pytest.raises(ValueError):
            OrchestratorLLMOutput(tasks=["  ", "Task 2"])

    def test_tasks_are_stripped(self):
        """Test that tasks are stripped of leading/trailing whitespace."""
        output = OrchestratorLLMOutput(tasks=["  Task 1  ", "  Task 2  "])
        assert output.tasks == ["Task 1", "Task 2"]
