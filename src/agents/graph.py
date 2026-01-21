from langgraph.graph import StateGraph, END
from src.agents.state import ResearchState
from src.agents.nodes import ResearchNodes
from src.utils.logger import get_logger

logger = get_logger(__name__)

def create_research_graph():
    """
    Create the LangGraph workflow for automated research
    """
    nodes = ResearchNodes()
    
    # Initialize graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("search", nodes.search_node)
    workflow.add_node("scrape", nodes.scrape_node)
    workflow.add_node("summarize", nodes.summarize_node)
    workflow.add_node("upload", nodes.upload_node)
    
    # Define edges
    workflow.set_entry_point("search")
    workflow.add_edge("search", "scrape")
    workflow.add_edge("scrape", "summarize")
    workflow.add_edge("summarize", "upload")
    workflow.add_edge("upload", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app
