"""
Research Manager - Multi-Agent Orchestrator

This class coordinates the agents to execute the complete
research workflow: plan → search → write → save.
"""

from typing import AsyncGenerator, List, Optional
from agents import Agent, Runner
from agents.result import RunResult
from agents.tracing import trace, gen_trace_id
from src.research.agents.planner_agent import WebSearchItem, WebSearchPlan
from src.research.agents.writer_agent import ReportData
import asyncio
from pathlib import Path
from datetime import datetime


class ResearchManager:
    """Orchestrates the deep research workflow across multiple agents."""

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """Execute the complete research workflow and yield the final report."""
        trace_id: str = gen_trace_id()
        print(f"🔍 Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
        
        with trace("Deep Research", trace_id=trace_id):
            from src.research.agents.planner_agent import planner_agent
            from src.research.agents.search_agent import search_agent
            from src.research.agents.writer_agent import writer_agent
            
            print(f"📋 Planning searches...")
            search_plan: WebSearchPlan = await self.plan_searches(query, planner_agent)
            print(f"✅ Planned {len(search_plan.searches)} searches")
            
            print(f"🌐 Executing {len(search_plan.searches)} searches...")
            search_results: List[str] = await self.perform_searches(search_plan, search_agent)
            print(f"✅ Completed {len(search_results)} searches")
            
            print(f"📝 Writing report...")
            report: ReportData = await self.write_report(query, search_results, writer_agent)
            print(f"✅ Report complete ({len(report.markdown_report)} chars)")
            
            saved_path: str = await self.save_report(query, report)
            print(f"💾 Saved: {saved_path}\n")
            
            yield report.markdown_report

    async def plan_searches(self, query: str, planner_agent: Agent) -> WebSearchPlan:
        """Generate a search plan using the planner agent."""
        result: RunResult = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan, search_agent: Agent) -> List[str]:
        """Execute all searches in parallel."""
        tasks: List[asyncio.Task[Optional[str]]] = [
            asyncio.create_task(self.search(item, search_agent))
            for item in search_plan.searches
        ]
        
        results: List[str] = []
        for task in asyncio.as_completed(tasks):
            result: Optional[str] = await task
            if result is not None:
                results.append(result)
        
        return results

    async def search(self, item: WebSearchItem, search_agent: Agent) -> Optional[str]:
        """Perform a single web search."""
        input_text: str = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result: RunResult = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"⚠️ Search failed: {item.query} - {e}")
            return None

    async def write_report(self, query: str, search_results: List[str], writer_agent: Agent) -> ReportData:
        """Synthesize search results into a comprehensive report."""
        input_text: str = f"Original query: {query}\n\nSummarized search results:\n{search_results}"
        result: RunResult = await Runner.run(writer_agent, input_text)
        return result.final_output_as(ReportData)
    
    async def save_report(self, query: str, report: ReportData) -> str:
        """Save report to a markdown file."""
        project_root: Path = Path(__file__).parent.parent.parent
        outputs_dir: Path = project_root / "outputs"
        outputs_dir.mkdir(exist_ok=True)
        
        timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_query: str = "".join(c for c in query[:50] if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
        filename: str = f"report_{timestamp}_{safe_query}.md"
        filepath: Path = outputs_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Research Report\n\n**Query:** {query}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
            f.write(f"## Summary\n\n{report.short_summary}\n\n---\n\n")
            f.write(f"{report.markdown_report}\n\n---\n\n## Follow-up Questions\n\n")
            f.write("\n".join(f"- {q}" for q in report.follow_up_questions))
        
        return str(filepath)

