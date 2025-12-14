"""
Writer Agent - Report Synthesis

This agent takes multiple search summaries and synthesizes them
into a comprehensive, well-structured research report.

Key Features:
- Structured output with multiple fields
- Long-form content generation (1000+ words)
- Markdown formatting
- Includes summary and follow-up questions
"""

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words. Use proper headings, subheadings, and formatting."
)


class ReportData(BaseModel):
    """Structured report output with metadata."""
    
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )

    markdown_report: str = Field(
        description="The final report in markdown format, 1000+ words."
    )

    follow_up_questions: List[str] = Field(
        description="Suggested topics to research further, 3-5 questions."
    )


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData
)

