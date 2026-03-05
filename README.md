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
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/orchestrator-worker-agentic-ai-workflow.git
   cd orchestrator-worker-agentic-ai-workflow
   ```
2. **Create a Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key**
   Create a `.env` file in the project root with:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o-mini  # optional
   ```
4. **Run the example**
   ```bash
   python src/main.py
   ```
   You should see the orchestrator breaking the query into tasks, workers executing them in parallel, and a summary output.

## 🧩 Project Structure
```
LICENSE
pyproject.toml
README.md
requirements.txt
src/
    main.py
    schemas.py
    __pycache__/
```

- `src/main.py` contains the graph definition and sample execution driver.
- `src/schemas.py` defines Pydantic models used for structured output.

## ✍️ Author

[![GitHub](https://img.shields.io/badge/GitHub-SimeonDee-181717?logo=github)](https://github.com/SimeonDee)
[![Email](https://img.shields.io/badge/Email-your.email%40example.com-red?logo=gmail&logoColor=white)](mailto:adeyemi.adedoyin.simeon@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/adedoyin-adeyemi-a7827b160)

---

Feel free to expand, adapt, or integrate this workflow into your own projects! Contributions and suggestions are welcome.
