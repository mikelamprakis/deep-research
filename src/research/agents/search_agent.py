"""
Search Agent - Web Research and Summarization

This agent performs web searches using OpenAI's WebSearchTool
and produces concise summaries of the results.

Key Features:
- Uses WebSearchTool (hosted by OpenAI)
- Forces tool usage (no hallucinations)
- Concise, focused summaries
- Costs ~$0.025 per search

Note: This tool costs money! See OpenAI pricing for WebSearchTool.
"""

from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],  # "low" is cheaper, "high" is more comprehensive
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),  # Always use the tool!
)

