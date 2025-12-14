# 🤝 OpenAI Agents Module Documentation

## Overview

The **`openai-agents`** package is a high-level Python library that simplifies building multi-agent AI systems. It provides abstractions for creating agents, running them, and managing their interactions.

**Package Name:** `openai-agents`  
**Installation:** `pip install openai-agents`

## Core Concepts

### 1. Agent

An **Agent** is a specialized AI assistant with:
- Instructions (system prompt)
- Model configuration
- Tools (functions it can call)
- Output type (structured output schema)

### 2. Runner

A **Runner** executes agents and manages their execution flow.

### 3. Tools

Functions that agents can call to interact with the world (e.g., web search, API calls).

## Creating an Agent

### Basic Agent

```python
from agents import Agent

agent = Agent(
    name="MyAgent",
    instructions="You are a helpful assistant.",
    model="gpt-4o-mini"
)
```

### Agent Parameters

#### `name`
- **Type:** `str`
- **Description:** Agent identifier
- **Example:** `"PlannerAgent"`

#### `instructions`
- **Type:** `str`
- **Description:** System prompt/instructions for the agent
- **Example:** `"You are a research assistant..."`

#### `model`
- **Type:** `str`
- **Description:** OpenAI model to use
- **Default:** `"gpt-4o-mini"`
- **Examples:** `"gpt-4o-mini"`, `"gpt-4o"`

#### `tools`
- **Type:** `List[Tool]`
- **Description:** Tools the agent can use
- **Example:** `[WebSearchTool(...)]`

#### `output_type`
- **Type:** `Type[BaseModel]` (Pydantic model)
- **Description:** Structured output schema
- **Example:** `WebSearchPlan`

#### `model_settings`
- **Type:** `ModelSettings`
- **Description:** Model configuration (temperature, tool_choice, etc.)

## Structured Outputs with Pydantic

The agents module integrates with Pydantic for type-safe structured outputs:

```python
from pydantic import BaseModel, Field
from agents import Agent

class SearchPlan(BaseModel):
    queries: List[str] = Field(description="List of search queries")
    priority: int = Field(description="Priority level")

agent = Agent(
    name="Planner",
    instructions="Plan searches",
    model="gpt-4o-mini",
    output_type=SearchPlan  # Enforces structured output
)
```

### Benefits

1. **Type Safety** - Guaranteed structure
2. **Validation** - Automatic validation of output
3. **IDE Support** - Autocomplete and type hints
4. **Documentation** - Field descriptions guide the model

## Running Agents

### Basic Execution

```python
from agents import Agent, Runner

agent = Agent(...)
result = await Runner.run(agent, "Your input query")
print(result.final_output)
```

### Async Execution

All agent runs are asynchronous:

```python
import asyncio

async def main():
    result = await Runner.run(agent, "Query")
    print(result.final_output)

asyncio.run(main())
```

### RunResult Object

The `Runner.run()` method returns a `RunResult` object:

```python
result = await Runner.run(agent, "Query")

# Access properties
result.final_output        # Final agent output
result.messages            # Conversation history
result.usage               # Token usage stats
result.trace_id            # Trace ID for debugging
```

### Structured Output Access

For agents with `output_type`:

```python
result = await Runner.run(agent, "Query")
plan = result.final_output_as(WebSearchPlan)  # Type-safe cast
print(plan.queries)
```

## Tools

### WebSearchTool (OpenAI Hosted)

Built-in tool for web search:

```python
from agents import Agent, WebSearchTool

agent = Agent(
    name="SearchAgent",
    tools=[WebSearchTool(search_context_size="low")],
    model_settings=ModelSettings(tool_choice="required")
)
```

#### WebSearchTool Parameters

- **`search_context_size`**
  - **Options:** `"low"`, `"medium"`, `"high"`
  - **Effect:** Amount of context returned
  - **Cost:** Higher = more expensive
  - **Recommendation:** Use `"low"` for cost efficiency

#### Tool Usage Control

```python
from agents import ModelSettings

# Force tool usage
ModelSettings(tool_choice="required")

# Let agent decide
ModelSettings(tool_choice="auto")

# Disable tools
ModelSettings(tool_choice="none")
```

### Custom Function Tools

Create custom tools using the `function_tool` decorator:

```python
from agents import function_tool
from pydantic import BaseModel

class WeatherParams(BaseModel):
    location: str

@function_tool
def get_weather(params: WeatherParams) -> str:
    """Get weather for a location."""
    # Your implementation
    return f"Weather in {params.location}: Sunny"

agent = Agent(
    tools=[get_weather],
    ...
)
```

## Tracing and Debugging

### Trace IDs

Every run generates a trace ID for debugging:

```python
from agents.tracing import gen_trace_id, trace

trace_id = gen_trace_id()

with trace("MyOperation", trace_id=trace_id):
    result = await Runner.run(agent, "Query")

# View trace at:
# https://platform.openai.com/traces/trace?trace_id={trace_id}
```

### Viewing Traces

1. Generate trace ID
2. Run your agent
3. Visit: `https://platform.openai.com/traces/trace?trace_id={trace_id}`
4. See detailed execution logs

## Model Settings

Configure agent behavior:

```python
from agents import ModelSettings

settings = ModelSettings(
    temperature=0.7,        # Randomness (0.0-2.0)
    tool_choice="required", # Tool usage policy
    max_tokens=2000         # Max output tokens
)

agent = Agent(
    model_settings=settings,
    ...
)
```

## Error Handling

```python
from agents import Agent, Runner

try:
    result = await Runner.run(agent, "Query")
except Exception as e:
    print(f"Agent execution failed: {e}")
    # Handle error
```

## Multi-Agent Workflows

Orchestrate multiple agents:

```python
# Agent 1: Planner
planner = Agent(name="Planner", output_type=SearchPlan, ...)
plan_result = await Runner.run(planner, query)
plan = plan_result.final_output_as(SearchPlan)

# Agent 2: Searcher (runs in parallel)
search_agent = Agent(name="Searcher", tools=[WebSearchTool()], ...)
results = await asyncio.gather(*[
    Runner.run(search_agent, item.query)
    for item in plan.searches
])

# Agent 3: Writer
writer = Agent(name="Writer", output_type=Report, ...)
report_result = await Runner.run(
    writer, 
    f"Query: {query}\nResults: {results}"
)
```

## Import Reference

### Common Imports

```python
# Core components
from agents import Agent, Runner
from agents.result import RunResult

# Tools
from agents import WebSearchTool, function_tool
from agents import ModelSettings

# Tracing
from agents.tracing import trace, gen_trace_id
```

### Module Structure

```
agents/
├── agent.py              # Agent class
├── run.py                # Runner class
├── result.py             # RunResult class
├── tools.py              # Tool classes
├── model_settings.py     # ModelSettings class
└── tracing/
    └── trace_api.py      # Trace utilities
```

## Best Practices

### 1. Use Structured Outputs

```python
# ✅ Good - Type-safe
agent = Agent(output_type=MyPydanticModel)

# ❌ Avoid - Unstructured
agent = Agent()  # No output_type
```

### 2. Explicit Tool Choice

```python
# ✅ Good - Explicit intent
ModelSettings(tool_choice="required")  # For search agents

# ⚠️ Caution - May skip tool
ModelSettings(tool_choice="auto")
```

### 3. Cost Optimization

```python
# ✅ Good - Cost-effective
WebSearchTool(search_context_size="low")
Agent(model="gpt-4o-mini")  # Cheaper model

# ⚠️ Higher cost
WebSearchTool(search_context_size="high")
Agent(model="gpt-4o")
```

### 4. Error Handling

```python
# ✅ Good - Graceful failure
try:
    result = await Runner.run(agent, query)
except Exception as e:
    logger.error(f"Agent failed: {e}")
    return None  # Continue workflow
```

### 5. Use Trace IDs

```python
# ✅ Good - Debuggable
trace_id = gen_trace_id()
print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
```

## How This Project Uses openai-agents

### Agent Creation Pattern

```python
# src/research/agents/planner_agent.py
from agents import Agent

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan
)
```

### Agent Execution Pattern

```python
# src/research/research_manager.py
from agents import Runner
from agents.result import RunResult

result: RunResult = await Runner.run(planner_agent, f"Query: {query}")
plan: WebSearchPlan = result.final_output_as(WebSearchPlan)
```

### Parallel Execution

```python
# Multiple agents run in parallel
tasks = [
    asyncio.create_task(Runner.run(search_agent, item.query))
    for item in plan.searches
]

results = await asyncio.gather(*tasks)
```

## Resources

- **Package:** https://pypi.org/project/openai-agents/
- **Documentation:** Check package README or source code
- **OpenAI Platform:** https://platform.openai.com/

## Differences from Direct OpenAI SDK

| Feature | OpenAI SDK | openai-agents |
|---------|-----------|---------------|
| **Abstraction Level** | Low-level API calls | High-level agent abstraction |
| **Structured Outputs** | Manual JSON parsing | Built-in Pydantic integration |
| **Tool Management** | Manual function calling | Declarative tool definition |
| **Multi-Agent** | Manual orchestration | Built-in patterns |
| **Tracing** | Manual implementation | Built-in trace support |
| **Use Case** | Custom implementations | Rapid agent development |

The `openai-agents` package is built on top of the OpenAI SDK and provides a higher-level, more Pythonic interface for building agent systems.

