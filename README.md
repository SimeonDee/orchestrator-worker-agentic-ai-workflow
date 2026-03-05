# orchestrator-worker-agentic-ai-workflow

[![Author](https://img.shields.io/badge/Author-Adedoyin%20Simeon%20Adeyemi-blue?logo=github&logoColor=white)](https://github.com/SimeonDee)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-v0.1+-green.svg)](https://github.com/langchain/langchain)
[![Langgraph](https://img.shields.io/badge/Langgraph-multi--agent-brightgreen.svg)](https://github.com/langgraph/langgraph)
[![OpenAI API](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)](https://openai.com)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/SimeonDee/orchestrator-worker-agentic-ai-workflow)

A sample Python project that demonstrates an **Orchestrator-Worker Agentic AI Workflow**. It leverages the
[Langgraph](https://github.com/langgraph/langgraph) and [LangChain](https://github.com/langchain/langchain) libraries
along with OpenAI's chat models to break down user queries, execute each task concurrently, and
collect a summarized response.

The repository contains a simple graph-based execution pipeline with three nodes:

1. **Orchestrator Node** - decomposes an incoming query into actionable tasks.
2. **Worker Node** - runs each task in parallel using a thread pool.
3. **Collector Node** - aggregates and summarizes the results returned by the workers.

## 🛠️ Tools & Technologies Used
- **Python 3.11+**
- **LangChain** for prompt templating and LLM orchestration
- **Langgraph** to build and run state graphs with checkpointing
- **OpenAI** (via `langchain_openai.ChatOpenAI`) as the LLM backend
- **dotenv** for environment variable management
- **concurrent.futures.ThreadPoolExecutor** for parallel task execution

## 🚀 Features
- Modular state graph architecture with clear node responsibilities
- Structured LLM output using Pydantic schemas (`schemas.py`)
- In-memory checkpointing for resuming graph execution (`InMemorySaver`)
- Example `main.py` demonstrating a multi-step query flow
- Configurable threading via the state graph configuration

## 📦 Getting Started

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SimeonDee/orchestrator-worker-agentic-ai-workflow.git
   cd orchestrator-worker-agentic-ai-workflow
   ```

2. **Create a Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and preferences
   ```

5. **Run the example**
   ```bash
   python src/main.py
   ```

### Development Setup

For development, install additional tools:

```bash
pip install -e ".[dev]"
```

**Available development commands:**

- **Run tests**
  ```bash
  pytest
  ```

- **Run tests with coverage**
  ```bash
  pytest --cov=src tests/
  ```

- **Format code**
  ```bash
  black src/ tests/
  isort src/ tests/
  ```

- **Lint code**
  ```bash
  flake8 src/ tests/
  pylint src/
  ```

- **Type checking**
  ```bash
  mypy src/
  ```

## 🧩 Project Structure

```
orchestrator-worker-agentic-ai-workflow/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # Project documentation
├── pyproject.toml           # Project configuration and dependencies
├── requirements.txt         # Direct dependencies (legacy)
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── schemas.py           # Pydantic data models and validation
│   ├── config.py            # Configuration management
│   ├── constants.py         # Application constants and prompts
│   ├── logger.py            # Logging setup and utilities
│   ├── nodes.py             # Graph node implementations
│   └── graph.py             # Graph construction and management
│
└── tests/
    ├── __init__.py
    ├── test_schemas.py      # Tests for data models
    ├── test_config.py       # Tests for configuration
    └── test_nodes.py        # Tests for graph nodes (optional)
```

### Key Modules

- **`main.py`** - Application entry point with orchestration logic
- **`schemas.py`** - Pydantic models for data validation (GraphState, OrchestratorLLMOutput)
- **`config.py`** - Configuration management from environment variables
- **`constants.py`** - Application-wide constants and prompt templates
- **`logger.py`** - Structured logging setup
- **`nodes.py`** - Graph node implementations (Orchestrator, Worker, Collector)
- **`graph.py`** - Graph construction and compilation

### Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini

# LLM Configuration
LLM_TEMPERATURE=0.7

# Worker Configuration
MAX_WORKERS=4

# Logging Configuration
LOG_LEVEL=INFO
```

## 🔍 Workflow Architecture

The workflow consists of three main nodes:

### 1. Orchestrator Node
- Accepts the user's query
- Uses LLM to break it down into smaller, manageable tasks
- Validates task output using Pydantic schemas
- Returns a list of tasks for parallel execution

### 2. Worker Node
- Receives tasks from the orchestrator
- Executes each task in parallel using ThreadPoolExecutor
- Configurable concurrency level via `MAX_WORKERS`
- Collects and returns results

### 3. Collector Node
- Receives all task results
- Uses LLM to synthesize and summarize results
- Provides comprehensive, structured summary
- Returns final summary to user

## 🛡️ Error Handling & Validation

This project includes robust error handling:

- **Configuration Validation** - Environment variables are validated on startup
- **Data Validation** - Pydantic models validate all inputs and outputs
- **Logging** - Comprehensive logging at all steps for debugging
- **Exception Handling** - Proper error propagation with informative messages

## 📝 Logging

Structured logging is enabled throughout the application. Control log levels via the `LOG_LEVEL` environment variable (DEBUG, INFO, WARNING, ERROR, CRITICAL).

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run the test suite and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✍️ Author

[![GitHub](https://img.shields.io/badge/GitHub-SimeonDee-181717?logo=github)](https://github.com/SimeonDee)
[![Email](https://img.shields.io/badge/Email-your.email%40example.com-red?logo=gmail&logoColor=white)](mailto:adeyemi.adedoyin.simeon@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/adedoyin-adeyemi-a7827b160)

---

Feel free to expand, adapt, or integrate this workflow into your own projects! Contributions and suggestions are welcome.
