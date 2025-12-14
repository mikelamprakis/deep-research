# 🤖 OpenAI SDK Documentation

## Overview

This project uses the **OpenAI Python SDK** as the foundation for interacting with OpenAI's API. The SDK provides the base client and models that power the agents system.

## Installation

```bash
pip install openai>=1.0.0
```

## Core Components

### OpenAI Client

The OpenAI SDK provides a client for interacting with the API:

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
```

### API Key Configuration

**Best Practice:** Store API keys in environment variables:

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

Or use `python-dotenv`:
```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## Chat Completions API

The core API for interacting with language models:

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Message Roles

- **`system`** - Sets the behavior and context for the assistant
- **`user`** - User queries and instructions
- **`assistant`** - Assistant responses (for conversation history)

### Common Parameters

#### `model`
- **Type:** `str`
- **Description:** Model identifier
- **Examples:**
  - `"gpt-4o"` - Latest GPT-4 model
  - `"gpt-4o-mini"` - Faster, cheaper version (used in this project)
  - `"gpt-3.5-turbo"` - Legacy model

#### `messages`
- **Type:** `List[ChatCompletionMessageParam]`
- **Description:** Conversation history
- **Required:** Yes

#### `temperature`
- **Type:** `float` (0.0 - 2.0)
- **Description:** Controls randomness
  - `0.0` - Deterministic, focused
  - `1.0` - Balanced (default)
  - `2.0` - Very creative
- **Default:** `1.0`

#### `max_tokens`
- **Type:** `int`
- **Description:** Maximum tokens in response
- **Default:** Model-dependent

#### `stream`
- **Type:** `bool`
- **Description:** Stream responses token-by-token
- **Default:** `False`

## Structured Outputs (JSON Mode)

The SDK supports structured outputs using JSON schema:

```python
response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "List 3 colors"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "colors_list",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "colors": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["colors"]
            }
        }
    }
)

colors = response.choices[0].message.parsed
print(colors.colors)  # ['red', 'blue', 'green']
```

## Function Calling / Tools

OpenAI supports function calling for structured tool usage:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    tools=tools,
    tool_choice="auto"  # or "required" or "none"
)
```

### Tool Choice Options

- **`"auto"`** - Model decides whether to use tools
- **`"required"`** - Model must use a tool
- **`"none"`** - Model cannot use tools

## Streaming Responses

For real-time responses:

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

## Error Handling

```python
from openai import OpenAI, APIError, RateLimitError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    print("Rate limit exceeded")
except APIError as e:
    print(f"API error: {e}")
```

### Common Error Types

- **`APIError`** - Base class for API errors
- **`RateLimitError`** - Rate limit exceeded
- **`APIConnectionError`** - Network/connection issues
- **`AuthenticationError`** - Invalid API key

## Response Structure

```python
response = client.chat.completions.create(...)

# Response object
response.id              # Request ID
response.model           # Model used
response.created         # Timestamp
response.choices         # List of completion choices

# Choice object
choice = response.choices[0]
choice.index            # Choice index
choice.message          # Message object
choice.finish_reason    # Why generation stopped

# Message object
message = choice.message
message.role           # "assistant"
message.content        # Generated text
message.tool_calls     # Tool calls (if any)
```

## Async API

For async/await support:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

import asyncio
asyncio.run(main())
```

## Cost Considerations

### Pricing (as of 2025)

- **GPT-4o-mini:**
  - Input: ~$0.15 per 1M tokens
  - Output: ~$0.60 per 1M tokens

- **GPT-4o:**
  - Input: ~$2.50 per 1M tokens
  - Output: ~$10.00 per 1M tokens

### Token Counting

```python
from tiktoken import encoding_for_model

encoding = encoding_for_model("gpt-4o-mini")
tokens = encoding.encode("Your text here")
print(f"Token count: {len(tokens)}")
```

## Best Practices

### 1. Use Environment Variables for API Keys
```python
# ❌ Bad
client = OpenAI(api_key="sk-...")

# ✅ Good
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### 2. Handle Errors Gracefully
```python
try:
    response = client.chat.completions.create(...)
except APIError as e:
    logger.error(f"API error: {e}")
    # Fallback logic
```

### 3. Use Appropriate Models
- Use `gpt-4o-mini` for simple tasks (cost-effective)
- Use `gpt-4o` for complex reasoning
- Choose based on requirements, not always the latest

### 4. Implement Rate Limiting
```python
import time
from openai import RateLimitError

def call_with_retry(client, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(*args, **kwargs)
        except RateLimitError:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### 5. Use Streaming for Long Responses
```python
# Better UX for long responses
stream = client.chat.completions.create(
    ...,
    stream=True
)
```

## Resources

- **Official Documentation:** https://platform.openai.com/docs
- **Python SDK Docs:** https://github.com/openai/openai-python
- **API Reference:** https://platform.openai.com/docs/api-reference
- **Pricing:** https://openai.com/pricing

## How This Project Uses OpenAI SDK

While this project primarily uses the `openai-agents` package (which wraps the OpenAI SDK), understanding the underlying SDK is important for:

1. **Custom implementations** - Building your own agent logic
2. **Debugging** - Understanding what's happening under the hood
3. **Advanced features** - Direct API access when needed
4. **Error handling** - Understanding SDK error types

The `openai-agents` package uses the OpenAI SDK internally for all API calls.

