"""
Command-line interface for deep research with static prompts.

Edit the RESEARCH_QUERY variable below to set your research question.

Run this script as a module from the project root:
    python -m src.entrypoints.run_research
"""

# ============================================================================
# CONFIGURATION: Set your research query here
# ============================================================================
RESEARCH_QUERY: str = "Latest AI agent frameworks in 2025"

# ============================================================================

import asyncio
from dotenv import load_dotenv
from src.research.research_manager import ResearchManager

load_dotenv(override=True)


async def main() -> None:
    """Run research with the static query defined above."""
    query: str = RESEARCH_QUERY
    
    if not query or not query.strip():
        print("❌ Error: RESEARCH_QUERY is empty. Please set it in the code.")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🔬 DEEP RESEARCH AGENT")
    print("="*70)
    print(f"\nQuery: {query}")
    print(f"\nEstimated cost: ~$0.13")
    print("\n" + "="*70 + "\n")
    
    manager: ResearchManager = ResearchManager()
    
    async for update in manager.run(query):
        print(update)
    
    print("\n" + "="*70)
    print("✅ Research complete! Check the outputs/ directory for the full report.")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

