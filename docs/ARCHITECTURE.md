# 🏗️ Architecture Documentation

## Overview

The Deep Research Agent is a multi-agent system that automates comprehensive research tasks by orchestrating specialized AI agents. The system follows a clean architecture pattern with clear separation of concerns.

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
├─────────────────────────────┬───────────────────────────────────┤
│    Web UI (Gradio)          │    CLI Interface                  │
│  src/entrypoints/main.py    │  src/entrypoints/run_research.py  │
└─────────────┬───────────────┴──────────────┬────────────────────┘
              │                              │
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼──────────────┐
              │    Research Manager         │
              │  src/research/              │
              │  research_manager.py        │
              └──────────────┬──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│ Planner Agent  │  │  Search Agent  │  │  Writer Agent  │
│                │  │                │  │                │
│ - Plans 5      │  │ - Web Search   │  │ - Synthesizes  │
│   searches     │  │ - Summarizes   │  │   report       │
│ - Structured   │  │ - Parallel     │  │ - Markdown     │
│   output       │  │   execution    │  │   formatted    │
└────────────────┘  └────────────────┘  └────────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │      OpenAI API             │
              │  (Agents + WebSearchTool)   │
              └─────────────────────────────┘
```

## Project Structure

```
deep-research-demo/
│
├── src/                          # Source code root
│   │
│   ├── entrypoints/              # Application entry points
│   │   ├── main.py              # Web UI entry point (Gradio)
│   │   └── run_research.py      # CLI entry point
│   │
│   └── research/                 # Core research system
│       │
│       ├── app.py               # Research application logic
│       ├── research_manager.py  # Orchestration engine
│       ├── gradio_ui_facade.py  # UI facade (Facade pattern)
│       │
│       └── agents/              # Specialized agents
│           ├── planner_agent.py # Strategic search planning
│           ├── search_agent.py  # Web search execution
│           └── writer_agent.py  # Report synthesis
│
├── outputs/                      # Generated reports (markdown)
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md          # This file
│   ├── OPENAI_SDK.md            # OpenAI SDK reference
│   └── OPENAI_AGENTS.md         # openai-agents module reference
│
├── requirements.txt             # Python dependencies
├── .env.example                # Environment configuration template
└── README.md                    # Project overview
```

## Component Architecture

### 1. Entry Points Layer

**Purpose:** Provide different interfaces for running the research system.

#### `src/entrypoints/main.py`
- **Type:** Web UI Entry Point
- **Technology:** Gradio
- **Responsibilities:**
  - Launch Gradio web interface
  - Handle port configuration
  - Expose UI to users

#### `src/entrypoints/run_research.py`
- **Type:** CLI Entry Point
- **Responsibilities:**
  - Accept static query from code
  - Run research workflow
  - Print results to console

### 2. Research Layer

#### `src/research/app.py`
- **Purpose:** Application logic layer
- **Responsibilities:**
  - Bridge between UI and research manager
  - Handle async research execution
  - Provide `run_research()` function

#### `src/research/research_manager.py`
- **Purpose:** Orchestration engine
- **Design Pattern:** Orchestrator Pattern
- **Responsibilities:**
  - Coordinate all agents
  - Manage workflow: plan → search → write → save
  - Handle async/parallel execution
  - Error handling and logging
  - File I/O for report saving

**Workflow:**
```
1. Plan Searches
   ↓
2. Execute Searches (Parallel)
   ↓
3. Write Report
   ↓
4. Save Report
```

#### `src/research/gradio_ui_facade.py`
- **Purpose:** UI Facade (Facade Design Pattern)
- **Technology:** Gradio
- **Responsibilities:**
  - Encapsulate all Gradio-specific code
  - Create and manage UI components
  - Handle report file loading
  - Provide clean interface to UI logic

### 3. Agents Layer

#### Planner Agent (`src/research/agents/planner_agent.py`)
- **Model:** `gpt-4o-mini`
- **Output:** Structured `WebSearchPlan` (Pydantic model)
- **Functionality:**
  - Analyzes research query
  - Generates 5 strategic search queries
  - Provides reasoning for each search
  - Returns structured plan

**Data Models:**
```python
class WebSearchItem:
    reason: str  # Why this search is important
    query: str   # Search term

class WebSearchPlan:
    searches: List[WebSearchItem]  # List of planned searches
```

#### Search Agent (`src/research/agents/search_agent.py`)
- **Model:** `gpt-4o-mini`
- **Tools:** `WebSearchTool` (OpenAI hosted)
- **Configuration:**
  - `tool_choice="required"` (must use search tool)
  - `search_context_size="low"` (cost optimization)
- **Functionality:**
  - Executes web search via OpenAI API
  - Summarizes search results
  - Returns concise summaries (2-3 paragraphs, <300 words)
  - **Cost:** ~$0.025 per search

#### Writer Agent (`src/research/agents/writer_agent.py`)
- **Model:** `gpt-4o-mini`
- **Output:** Structured `ReportData` (Pydantic model)
- **Functionality:**
  - Synthesizes all search results
  - Creates comprehensive report
  - Generates markdown-formatted content
  - Provides short summary
  - Suggests follow-up questions

**Data Models:**
```python
class ReportData:
    short_summary: str              # Brief overview
    markdown_report: str            # Full report in markdown
    follow_up_questions: List[str]  # Suggested next questions
```

## Data Flow

### Complete Research Workflow

```
User Query
    ↓
[Entry Point] (main.py or run_research.py)
    ↓
[ResearchManager.run()]
    │
    ├─→ [1] Planner Agent
    │       Input: User query
    │       Output: WebSearchPlan (5 searches)
    │
    ├─→ [2] Search Agent (Parallel Execution)
    │       Input: WebSearchItem (query + reason)
    │       Tool: WebSearchTool
    │       Output: Search summary (string)
    │       (Executed 5 times in parallel)
    │
    ├─→ [3] Writer Agent
    │       Input: Original query + all search summaries
    │       Output: ReportData (full report)
    │
    └─→ [4] Save Report
            Output: Markdown file in outputs/
    ↓
Final Report (Markdown)
```

### Parallel Search Execution

```
ResearchManager.perform_searches()
    │
    ├─→ Search 1 (async task) ──┐
    ├─→ Search 2 (async task) ──┤
    ├─→ Search 3 (async task) ──┼─→ asyncio.as_completed()
    ├─→ Search 4 (async task) ──┤   (results as they finish)
    └─→ Search 5 (async task) ──┘
            ↓
    [All results collected]
```

## Design Patterns

### 1. Facade Pattern
**Location:** `src/research/gradio_ui_facade.py`

Encapsulates complex Gradio UI logic behind a simple interface:
```python
class GradioUIFacade:
    def create_ui(...)    # Create UI
    def load_report(...)  # Load report files
    def launch(...)       # Start server
```

### 2. Orchestrator Pattern
**Location:** `src/research/research_manager.py`

Coordinates multiple agents to achieve a complex task:
- Manages agent execution order
- Handles data flow between agents
- Manages async/parallel execution

### 3. Dependency Injection
**Pattern:** Agent instances passed as parameters

```python
async def plan_searches(self, query: str, planner_agent: Agent) -> WebSearchPlan
async def perform_searches(self, search_plan: WebSearchPlan, search_agent: Agent)
async def write_report(self, query: str, search_results: List[str], writer_agent: Agent)
```

This makes methods testable and dependencies explicit.

## Technology Stack

### Core Technologies
- **Python 3.13+** - Programming language
- **openai-agents** - Multi-agent framework
- **OpenAI API** - LLM and web search capabilities
- **Gradio 6.x** - Web UI framework
- **Pydantic** - Structured output validation
- **asyncio** - Async/parallel execution

### Key Libraries
- **python-dotenv** - Environment variable management
- **pathlib** - Modern file path handling

## Concurrency Model

The system uses Python's `asyncio` for concurrent execution:

1. **Async Functions:** All agent calls are async
2. **Parallel Searches:** `asyncio.create_task()` + `asyncio.as_completed()`
3. **Non-blocking:** UI remains responsive during research

**Example:**
```python
tasks = [asyncio.create_task(self.search(item, search_agent)) 
         for item in search_plan.searches]

for task in asyncio.as_completed(tasks):
    result = await task
    results.append(result)
```

## Error Handling

1. **Agent Failures:** Search agent failures are caught and logged, but don't stop the workflow
2. **File I/O:** Try-except blocks for file operations
3. **Graceful Degradation:** System continues even if some searches fail

## File Organization Principles

1. **No `__init__.py` files:** Direct imports for clarity
2. **Strong Typing:** All functions and variables are type-hinted
3. **Separation of Concerns:** Each module has a single responsibility
4. **Entry Points:** Separate entry points for different use cases
5. **Clean Imports:** Direct module imports show origin clearly

## Configuration

### Environment Variables (`.env`)
- `OPENAI_API_KEY` - Required for all agents

### Code Configuration
- `HOW_MANY_SEARCHES` - Number of searches to plan (planner_agent.py)
- `search_context_size` - Search detail level (search_agent.py)
- `tool_choice` - Force tool usage (search_agent.py)

## Output Format

Reports are saved as Markdown files in `outputs/` directory:

```
report_YYYY-MM-DD_HH-MM-SS_QueryName.md

Format:
- Header with query and timestamp
- Short summary
- Full markdown report
- Follow-up questions
```

## Performance Characteristics

- **Parallel Searches:** 5 searches execute concurrently (~10 seconds total vs ~50 seconds sequential)
- **Cost per Research:** ~$0.13
  - Planner: ~$0.001
  - Searches (5x): ~$0.125
  - Writer: ~$0.005
- **Average Execution Time:** 30-60 seconds (depends on search complexity)

## Extension Points

1. **New Agents:** Add to `src/research/agents/`
2. **New Entry Points:** Add to `src/entrypoints/`
3. **UI Modifications:** Modify `src/research/gradio_ui_facade.py`
4. **Workflow Changes:** Modify `src/research/research_manager.py`

## Testing Strategy

- **Unit Tests:** Test individual agents in isolation
- **Integration Tests:** Test ResearchManager orchestration
- **No `__name__ == "__main__"` blocks:** Use dedicated test files instead

