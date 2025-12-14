"""
Deep Research Web Application

Provides a clean interface to the research system using the Gradio UI facade.
"""

from typing import AsyncGenerator
from dotenv import load_dotenv
from pathlib import Path
from src.research.research_manager import ResearchManager
from src.research.gradio_ui_facade import GradioUIFacade

load_dotenv(override=True)

# Outputs directory - relative to project root
OUTPUTS_DIR: Path = Path(__file__).parent.parent.parent / "outputs"


async def run_research(query: str) -> AsyncGenerator[str, None]:
    """Execute research and yield the final report."""
    if not query or query.strip() == "":
        yield "⚠️ Please enter a research query"
        return
    
    manager: ResearchManager = ResearchManager()
    async for report in manager.run(query):
        yield report


def create_deep_research_ui() -> GradioUIFacade:
    """
    Create and configure the Gradio UI facade.
    
    Returns:
        Configured GradioUIFacade instance
    """
    ui_facade: GradioUIFacade = GradioUIFacade(outputs_dir=OUTPUTS_DIR)
    ui_facade.create_ui(run_research_fn=run_research)
    return ui_facade


# Expose deep_research_ui for backward compatibility with entrypoints
deep_research_ui: GradioUIFacade = create_deep_research_ui()
