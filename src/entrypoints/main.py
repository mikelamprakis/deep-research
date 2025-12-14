"""
Entry point for running the Deep Research Web Application.

Run this script as a module from the project root:
    python -m src.entrypoints.main
"""

# Import and run the app
if __name__ == "__main__":
    import os
    from src.research.app import deep_research_ui
    
    # Get port from environment variable or use default
    port = int(os.environ.get("GRADIO_SERVER_PORT", "7860"))
    print(f"🚀 Starting Deep Research Agent...")
    print(f"   Port: {port} (or next available if in use)")
    print(f"   (Set GRADIO_SERVER_PORT environment variable to use a specific port)")
    print()
    
    # Use the facade to launch
    deep_research_ui.launch(server_port=port)

