# 🔬 Deep Research Agent

A multi-agent AI system that automates comprehensive research by orchestrating specialized agents to plan, search, synthesize, and deliver research reports.

## 🎯 What This Does

Transforms a simple research query into a comprehensive markdown report:

```
Input:  "Latest AI agent frameworks in 2025"
         ↓
Output: Comprehensive report saved to outputs/ and displayed in UI
```

## 🏗️ Architecture Overview

This system uses a **multi-agent architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         Entry Points                    │
│  (Web UI / CLI)                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Research Manager                   │
│  (Orchestration Engine)                 │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Planner│ │Search │ │Writer │
│ Agent │ │ Agent │ │ Agent │
└───────┘ └───────┘ └───────┘
```

### Key Components

1. **Entry Points** (`src/entrypoints/`)
   - `main.py` - Web UI (Gradio)
   - `run_research.py` - CLI interface

2. **Research Layer** (`src/research/`)
   - `research_manager.py` - Orchestrates agents
   - `app.py` - Application logic
   - `gradio_ui_facade.py` - UI facade pattern

3. **Agents** (`src/research/agents/`)
   - **Planner Agent** - Generates strategic search plans
   - **Search Agent** - Executes web searches in parallel
   - **Writer Agent** - Synthesizes comprehensive reports

### Workflow

1. **Plan** → Planner Agent generates 5 strategic search queries
2. **Search** → Search Agent executes all searches in parallel
3. **Synthesize** → Writer Agent creates comprehensive report
4. **Save** → Report saved as markdown in `outputs/` directory

**See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.**

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.13+
- OpenAI API key

### 2. Setup

```bash
# Clone the repository
cd deep-research-demo

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-key-here
```

### 4. Run

#### Option A: Web Interface (Recommended)

```bash
python -m src.entrypoints.main
```

Opens browser at `http://localhost:7860` (or next available port).

**Features:**
- Interactive web UI
- Real-time report generation
- View past reports
- Report browsing and selection

#### Option B: CLI Interface

Edit `src/entrypoints/run_research.py` to set your query:

```python
RESEARCH_QUERY: str = "Your research query here"
```

Then run:

```bash
python -m src.entrypoints.run_research
```

#### Option C: Programmatic Usage

```python
from src.research.research_manager import ResearchManager
import asyncio

async def main():
    manager = ResearchManager()
    async for report in manager.run("Your research query"):
        print(report)

asyncio.run(main())
```

## 📁 Project Structure

```
deep-research-demo/
│
├── src/                           # Source code
│   ├── entrypoints/               # Application entry points
│   │   ├── main.py               # Web UI entry point
│   │   └── run_research.py       # CLI entry point
│   │
│   └── research/                  # Core research system
│       ├── app.py                # Application logic
│       ├── research_manager.py   # Orchestration engine
│       ├── gradio_ui_facade.py   # UI facade
│       └── agents/               # Specialized agents
│           ├── planner_agent.py  # Search planning
│           ├── search_agent.py   # Web search execution
│           └── writer_agent.py   # Report synthesis
│
├── outputs/                       # Generated reports (markdown)
│
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md           # Architecture details
│   ├── OPENAI_SDK.md             # OpenAI SDK reference
│   └── OPENAI_AGENTS.md          # openai-agents module reference
│
├── requirements.txt               # Python dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # This file
```

## 🎓 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - System architecture, design patterns, data flow
- **[OpenAI SDK Reference](docs/OPENAI_SDK.md)** - OpenAI SDK usage and best practices
- **[OpenAI Agents Reference](docs/OPENAI_AGENTS.md)** - openai-agents module documentation

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-your-key-here
```

### Code Configuration

**Number of searches:**
Edit `src/research/agents/planner_agent.py`:
```python
HOW_MANY_SEARCHES: int = 5  # Change to 3, 7, etc.
```

**Search detail level:**
Edit `src/research/agents/search_agent.py`:
```python
WebSearchTool(search_context_size="low")  # Options: low, medium, high
```

## 💰 Cost Considerations

**Per research run: ~$0.13**

- Planner Agent: ~$0.001
- Search Agent (5 searches): ~$0.125 (~$0.025 each)
- Writer Agent: ~$0.005

**To reduce costs:**
- Reduce `HOW_MANY_SEARCHES` from 5 to 3
- Use `search_context_size="low"` (already set)
- Use `gpt-4o-mini` model (already configured)

## 🎨 Features

- ✅ **Multi-Agent Architecture** - Specialized agents working together
- ✅ **Parallel Execution** - Searches run concurrently for speed
- ✅ **Structured Outputs** - Type-safe responses with Pydantic
- ✅ **Web UI** - Gradio-based interface with report browsing
- ✅ **CLI Interface** - Command-line usage
- ✅ **Report Persistence** - Reports saved as markdown files
- ✅ **Strong Typing** - Full type hints throughout codebase
- ✅ **Clean Architecture** - Separation of concerns, facade pattern

## 🏛️ Design Patterns

- **Facade Pattern** - `GradioUIFacade` encapsulates UI complexity
- **Orchestrator Pattern** - `ResearchManager` coordinates agents
- **Dependency Injection** - Agents passed as parameters for testability

## 📊 Example Queries

**Technology:**
- "Latest developments in quantum computing hardware"
- "AI agent frameworks comparison 2025"
- "Blockchain scalability solutions"

**Business:**
- "Electric vehicle market trends in Europe"
- "SaaS pricing strategies for B2B startups"
- "Remote work tools adoption post-2024"

**Science:**
- "Recent advances in renewable energy storage"
- "CRISPR gene therapy clinical trials 2025"
- "Climate change mitigation technologies"

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
Ensure `.env` file exists with your API key:
```bash
OPENAI_API_KEY=sk-...
```

### Port already in use
The app automatically tries the next available port. Or set a specific port:
```bash
GRADIO_SERVER_PORT=7861 python -m src.entrypoints.main
```

### Import errors
Run as a module from the project root:
```bash
python -m src.entrypoints.main
```

### Searches taking long
- Normal: WebSearchTool takes ~5-10 seconds per search
- Searches run in parallel, so 5 searches ≈ 10 seconds total
- This is expected behavior

## 🔑 Key Technologies

- **Python 3.13+** - Programming language
- **openai-agents** - Multi-agent framework
- **OpenAI API** - LLM and web search
- **Gradio 6.x** - Web UI framework
- **Pydantic** - Structured output validation
- **asyncio** - Async/parallel execution

## 💼 Use Cases

- Market research
- Competitive intelligence
- Literature reviews
- Trend analysis
- Investment research
- Content creation
- Due diligence

## 🧪 Testing

The codebase is structured for testing:
- Agents can be tested in isolation
- ResearchManager can be tested with mock agents
- Use dedicated test files (no `__name__ == "__main__"` blocks in production code)

## 📝 Development

### Code Style

- **Strong Typing** - All functions and variables are type-hinted
- **Direct Imports** - No `__init__.py` files, imports show origin clearly
- **Clean Architecture** - Separation of concerns
- **Type Safety** - Pydantic models for structured data

### Running from Source

Always run as a module from the project root:
```bash
python -m src.entrypoints.main
python -m src.entrypoints.run_research
```

## 🙏 Acknowledgments

Based on OpenAI Agents course materials and the OpenAI Agents SDK.

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [OpenAI Platform](https://platform.openai.com/)

---

