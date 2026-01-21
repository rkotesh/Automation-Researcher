import requests
from bs4 import BeautifulSoup
from newspaper import Article
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape_url(self, url: str, title: str) -> ScrapedContent:
        """
        Scrape content from a single URL using newspaper3k
        """
        try:
            logger.info(f"Scraping: {url}")
            
            article = Article(url)
            article.download()
            article.parse()
            
            # Fallback to BeautifulSoup if newspaper3k fails
            if not article.text or len(article.text) < 100:
                logger.warning(f"Newspaper3k failed for {url}, trying BeautifulSoup")
                return self._scrape_with_bs4(url, title)
            
            return ScrapedContent(
                url=url,
                title=article.title or title,
                content=article.text,
                author=article.authors[0] if article.authors else None,
                publish_date=str(article.publish_date) if article.publish_date else None,
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
    
    def _scrape_with_bs4(self, url: str, title: str) -> ScrapedContent:
        """
        Fallback scraper using BeautifulSoup
        """
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text from paragraphs
        paragraphs = soup.find_all('p')
        content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        return ScrapedContent(
            url=url,
            title=title,
            content=content,
            success=True
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
