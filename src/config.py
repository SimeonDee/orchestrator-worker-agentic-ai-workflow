"""
Configuration management for the orchestrator-worker agentic AI workflow.
Handles environment variables and default configurations.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

from constants import (
    DEFAULT_LLM_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_WORKERS,
    ERROR_MISSING_API_KEY,
    LOG_LEVEL,
)


@dataclass
class LLMConfig:
    """Configuration for Language Model."""

    api_key: str
    model: str = DEFAULT_LLM_MODEL
    temperature: float = DEFAULT_TEMPERATURE

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ValueError(ERROR_MISSING_API_KEY)
        if not 0 <= self.temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")


@dataclass
class WorkerConfig:
    """Configuration for worker execution."""

    max_workers: int = DEFAULT_MAX_WORKERS

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.max_workers < 1:
            raise ValueError("max_workers must be at least 1")


@dataclass
class LogConfig:
    """Configuration for logging."""

    level: str = LOG_LEVEL
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class Config:
    """Application-wide configuration."""

    llm: LLMConfig
    worker: WorkerConfig = field(default_factory=WorkerConfig)
    logging: LogConfig = field(default_factory=LogConfig)

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables.

        Returns:
            Config: Application configuration loaded from environment.

        Raises:
            ValueError: If required environment variables are missing.
        """
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(ERROR_MISSING_API_KEY)

        llm_config = LLMConfig(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", DEFAULT_LLM_MODEL),
            temperature=float(
                os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE),
            ),
        )

        worker_config = WorkerConfig(
            max_workers=int(os.getenv("MAX_WORKERS", DEFAULT_MAX_WORKERS))
        )

        log_config = LogConfig(level=os.getenv("LOG_LEVEL", LOG_LEVEL))

        return cls(llm=llm_config, worker=worker_config, logging=log_config)


def get_config() -> Config:
    """Get the application configuration.

    Returns:
        Config: The application configuration.
    """
    return Config.from_env()
