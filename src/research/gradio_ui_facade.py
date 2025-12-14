"""
Gradio UI Facade

Provides a clean interface for creating and managing the Gradio web UI.
All Gradio-specific code is encapsulated here, following the facade pattern.
"""

from typing import List, Optional, Callable, AsyncGenerator
import gradio as gr
from pathlib import Path


class GradioUIFacade:
    """Facade for managing the Gradio web interface."""
    
    def __init__(self, outputs_dir: Path) -> None:
        """
        Initialize the UI facade.
        Args:
            outputs_dir: Directory where reports are saved
        """
        self.outputs_dir: Path = outputs_dir
        self.outputs_dir.mkdir(exist_ok=True)
        self._deep_research_ui: Optional[gr.Blocks] = None
    
    def get_report_files(self) -> List[str]:
        """Get list of report files sorted by modification time (newest first)."""
        if not self.outputs_dir.exists():
            return []
        
        report_files: List[Path] = sorted(
            self.outputs_dir.glob("report_*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        return [f.name for f in report_files]
    
    def load_report(self, filename: Optional[str]) -> str:
        """Load a report file and return its content."""
        if not filename or filename == "":
            return "Select a report to view..."
        
        filepath: Path = self.outputs_dir / filename
        if not filepath.exists():
            return f"⚠️ Report file not found: {filename}"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"⚠️ Error reading report: {str(e)}"
    
    def create_ui(self, run_research_fn: Callable[[str], AsyncGenerator[str, None]]) -> None:
        """
        Create the Gradio interface.
        
        Args:
            run_research_fn: Async function that takes a query string and yields updates
        """
        with gr.Blocks() as deep_research_ui:
            gr.Markdown("""
            # 🔬 Deep Research Agent
            
            Enter a research question and get a comprehensive report automatically
            researched and synthesized by AI agents.
            
            **How it works:**
            1. 📋 Plans strategic web searches
            2. 🌐 Executes searches in parallel
            3. 📝 Synthesizes comprehensive report
            4. 💾 Saves report to file
            
            **Note:** Each research costs ~$0.13 in API calls.
            """)
            
            with gr.Tabs():
                # Tab 1: New Research
                with gr.Tab("🆕 New Research"):
                    with gr.Row():
                        with gr.Column():
                            query_textbox = gr.Textbox(
                                label="Research Query",
                                placeholder="e.g., Latest AI agent frameworks in 2025",
                                lines=3
                            )
                            
                            with gr.Row():
                                run_button = gr.Button("🚀 Start Research", variant="primary", scale=2)
                                clear_button = gr.Button("Clear", scale=1)
                    
                    report_output = gr.Markdown(
                        label="Research Report", 
                        value="",
                        height=600
                    )
                    
                    # Event handlers
                    run_button.click(
                        fn=run_research_fn, 
                        inputs=query_textbox, 
                        outputs=report_output
                    )
                    
                    query_textbox.submit(
                        fn=run_research_fn,
                        inputs=query_textbox,
                        outputs=report_output
                    )
                    
                    clear_button.click(
                        lambda: ("", ""), 
                        outputs=[query_textbox, report_output]
                    )
                
                # Tab 2: Past Reports
                with gr.Tab("📚 Past Reports"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            report_dropdown = gr.Dropdown(
                                label="Select Report",
                                choices=self.get_report_files(),
                                value=None,
                                interactive=True
                            )
                            
                            refresh_button = gr.Button("🔄 Refresh List", scale=1)
                        
                        with gr.Column(scale=3):
                            report_viewer = gr.Markdown(
                                label="Report Content",
                                value="Select a report from the dropdown to view it...",
                                height=600
                            )
                    
                    # Event handlers
                    report_dropdown.change(
                        fn=self.load_report,
                        inputs=report_dropdown,
                        outputs=report_viewer
                    )
                    
                    def refresh_on_select():
                        """Refresh the dropdown with updated report file list."""
                        return gr.update(choices=self.get_report_files(), value=None)
                    
                    refresh_button.click(
                        fn=refresh_on_select,
                        outputs=report_dropdown
                    )
                    
                    # Auto-refresh dropdown when tab is selected
                    deep_research_ui.load(
                        fn=refresh_on_select,
                        outputs=report_dropdown
                    )
        
        self._deep_research_ui = deep_research_ui
    
    def launch(
        self,
        server_name: str = "127.0.0.1",
        server_port: Optional[int] = None,
        share: bool = False,
        inbrowser: bool = True,
    ) -> None:
        """
        Launch the Gradio interface.
        
        Args:
            server_name: Server hostname
            server_port: Server port (None for auto)
            share: Whether to create a public link
            inbrowser: Whether to open in browser
        """
        if self._deep_research_ui is None:
            raise ValueError("UI not created. Call create_ui() first.")
        
        try:
            self._deep_research_ui.launch(
                server_name=server_name,
                server_port=server_port,
                share=share,
                inbrowser=inbrowser,
                theme=gr.themes.Default(primary_hue="sky")
            )
        except OSError as e:
            if "address already in use" in str(e).lower():
                print(f"\n⚠️  Port {server_port} is already in use. Trying next available port...")
                self._deep_research_ui.launch(
                    server_name=server_name,
                    server_port=None,
                    share=share,
                    inbrowser=inbrowser,
                    theme=gr.themes.Default(primary_hue="sky")
                )
            else:
                raise

