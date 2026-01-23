import requests
from bs4 import BeautifulSoup
from typing import List
from config.settings import settings
from src.agents.state import SearchResult, ScrapedContent
from src.utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

class ScraperService:
    def __init__(self):
        self.timeout = settings.scraping_timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape_url(self, url: str, title: str) -> ScrapedContent:
        """
        Scrape content from a single URL using BeautifulSoup
        """
        try:
            logger.info(f"Scraping: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
                script.decompose()
            
            # Get text
            # Prefer article body if possible
            article_body = soup.find('article')
            if article_body:
                text = article_body.get_text(separator='\n\n')
            else:
                # Fallback to body
                text = soup.body.get_text(separator='\n\n') if soup.body else ""
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n\n'.join(chunk for chunk in chunks if chunk)
            
            if not text_content or len(text_content) < 100:
                logger.warning(f"Insufficient content for {url}")
                return ScrapedContent(
                    url=url,
                    title=title,
                    content="",
                    success=False,
                    error_message="Insufficient content extracted"
                )
            
            return ScrapedContent(
                url=url,
                title=title,
                content=text_content[:15000], # Limit content size
                success=True
            )
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            return ScrapedContent(
                url=url,
                title=title,
                content="",
                success=False,
                error_message=str(e)
            )
    
    def scrape_multiple(self, search_results: List[SearchResult]) -> List[ScrapedContent]:
        """
        Scrape multiple URLs
        """
        scraped_contents = []
        for result in search_results:
            scraped = self.scrape_url(result.url, result.title)
            scraped_contents.append(scraped)
        
        successful = [s for s in scraped_contents if s.success]
        logger.info(f"Successfully scraped {len(successful)}/{len(search_results)} URLs")
        
        return scraped_contents
