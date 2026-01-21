import requests
from typing import List
from config.settings import settings
from src.agents.state import SearchResult
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        self.api_key = settings.serper_api_key
        self.base_url = "https://google.serper.dev/search"
    
    def search(self, query: str, num_results: int = None) -> List[SearchResult]:
        """
        Search Google using Serper API
        """
        if num_results is None:
            num_results = settings.max_search_results
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results,
            'gl': 'us',
            'hl': 'en'
        }
        
        try:
            logger.info(f"Searching for: {query}")
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for idx, item in enumerate(data.get('organic', [])[:num_results]):
                results.append(SearchResult(
                    title=item.get('title', ''),
                    url=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    position=idx + 1
                ))
            
            logger.info(f"Found {len(results)} search results")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
