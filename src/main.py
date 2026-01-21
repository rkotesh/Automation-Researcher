import sys
from src.agents.graph import create_research_graph
from src.agents.state import ResearchState
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_research(topic: str) -> ResearchState:
    """
    Run the automated research workflow
    """
    logger.info(f"Starting research for topic: {topic}")
    
    # Initialize state
    initial_state: ResearchState = {
        "topic": topic,
        "search_results": [],
        "scraped_contents": [],
        "briefing_document": "",
        "document_url": None,
        "error": None,
        "current_step": "initializing"
    }
    
    # Create and run graph
    app = create_research_graph()
    final_state = app.invoke(initial_state)
    
    return final_state

def main():
    """
    CLI entry point
    """
    if len(sys.argv) < 2:
        print("Usage: python -m src.main \"Your research topic\"")
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    
    try:
        result = run_research(topic)
        
        if result.get("error"):
            logger.error(f"Research failed: {result['error']}")
            print(f"\n[Error] Research failed: {result['error']}")
            sys.exit(1)
        
        print(f"\n[Success] Research completed successfully!")
        print(f"Document URL: {result.get('document_url')}")
        print(f"Sources analyzed: {len(result.get('scraped_contents', []))}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n[Error] Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
