from src.agents.state import ResearchState
from src.services.search_service import SearchService
from src.services.scraper_service import ScraperService
from src.services.summarizer_service import SummarizerService
from src.services.drive_service import DriveService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ResearchNodes:
    def __init__(self):
        self.search_service = SearchService()
        self.scraper_service = ScraperService()
        self.summarizer_service = SummarizerService()
        self.drive_service = DriveService()
    
    def search_node(self, state: ResearchState) -> ResearchState:
        """
        Node: Search Google for articles on the topic
        """
        try:
            logger.info(f"Step 1: Searching for '{state['topic']}'")
            state["current_step"] = "searching"
            
            search_results = self.search_service.search(state["topic"])
            state["search_results"] = search_results
            
            return state
        except Exception as e:
            state["error"] = f"Search failed: {str(e)}"
            return state
    
    def scrape_node(self, state: ResearchState) -> ResearchState:
        """
        Node: Scrape content from top search results
        """
        try:
            logger.info("Step 2: Scraping article content")
            state["current_step"] = "scraping"
            
            scraped_contents = self.scraper_service.scrape_multiple(state["search_results"])
            state["scraped_contents"] = scraped_contents
            
            return state
        except Exception as e:
            state["error"] = f"Scraping failed: {str(e)}"
            return state
    
    def summarize_node(self, state: ResearchState) -> ResearchState:
        """
        Node: Generate briefing document from scraped content
        """
        try:
            logger.info("Step 3: Generating briefing document")
            state["current_step"] = "summarizing"
            
            briefing = self.summarizer_service.generate_briefing(
                state["topic"],
                state["scraped_contents"]
            )
            state["briefing_document"] = briefing
            
            return state
        except Exception as e:
            state["error"] = f"Summarization failed: {str(e)}"
            return state
    
    def upload_node(self, state: ResearchState) -> ResearchState:
        """
        Node: Upload briefing document to Google Drive
        """
        try:
            logger.info("Step 4: Uploading to Google Drive")
            state["current_step"] = "uploading"
            
            filename = f"Research_Briefing_{state['topic'].replace(' ', '_')}"
            document_url = self.drive_service.upload_document(
                state["briefing_document"],
                filename
            )
            state["document_url"] = document_url
            state["current_step"] = "completed"
            
            return state
        except Exception as e:
            state["error"] = f"Upload failed: {str(e)}"
            return state
