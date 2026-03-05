"""
Tests for the config module.
"""

import pytest

from config import LLMConfig, WorkerConfig, LogConfig, Config


class TestLLMConfig:
    """Test cases for LLMConfig."""

    def test_valid_llm_config(self):
        """Test creating valid LLMConfig."""
        config = LLMConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.model == "gpt-4o-mini"
        assert config.temperature == 0.7

    def test_llm_config_custom_values(self):
        """Test LLMConfig with custom values."""
        config = LLMConfig(api_key="test-key", model="gpt-4", temperature=0.5)
        assert config.api_key == "test-key"
        assert config.model == "gpt-4"
        assert config.temperature == 0.5

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises error."""
        with pytest.raises(ValueError):
            LLMConfig(api_key="")

    def test_invalid_temperature_raises_error(self):
        """Test that invalid temperature raises error."""
        with pytest.raises(ValueError):
            LLMConfig(api_key="test-key", temperature=2.5)


class TestWorkerConfig:
    """Test cases for WorkerConfig."""

    def test_valid_worker_config(self):
        """Test creating valid WorkerConfig."""
        config = WorkerConfig()
        assert config.max_workers == 4

    def test_worker_config_custom_workers(self):
        """Test WorkerConfig with custom max_workers."""
        config = WorkerConfig(max_workers=8)
        assert config.max_workers == 8

    def test_invalid_max_workers_raises_error(self):
        """Test that invalid max_workers raises error."""
        with pytest.raises(ValueError):
            WorkerConfig(max_workers=0)


class TestLogConfig:
    """Test cases for LogConfig."""

    def test_valid_log_config(self):
        """Test creating valid LogConfig."""
        config = LogConfig()
        assert config.level == "INFO"


class TestConfig:
    """Test cases for Config class."""

    def test_config_creation(self):
        """Test creating Config with sub-configs."""
        llm_config = LLMConfig(api_key="test-key")
        config = Config(llm=llm_config)
        assert config.llm.api_key == "test-key"
        assert isinstance(config.worker, WorkerConfig)
        assert isinstance(config.logging, LogConfig)
