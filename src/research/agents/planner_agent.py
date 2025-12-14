"""
Planner Agent - Strategic Search Planning

This agent takes a user's research query and generates a strategic plan
of multiple web searches to comprehensively answer the query.

Key Features:
- Structured output (Pydantic models)
- Generates multiple search terms with reasoning
- Configurable number of searches
"""

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

# Configuration: How many searches to plan
HOW_MANY_SEARCHES: int = 5

INSTRUCTIONS = f"""You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.

Think strategically:
- Cover different aspects of the topic
- Include specific and broad searches
- Consider recent developments vs. foundational information
- Look for data, opinions, and comparisons
"""


class WebSearchItem(BaseModel):
    """A single web search with reasoning."""
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    """A complete plan of multiple web searches."""
    searches: List[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)

