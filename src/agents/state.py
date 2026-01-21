from typing import TypedDict, List, Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    position: int

class ScrapedContent(BaseModel):
    url: str
    title: str
    content: str
    author: Optional[str] = None
    publish_date: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None

class ResearchState(TypedDict):
    topic: str
    search_results: List[SearchResult]
    scraped_contents: List[ScrapedContent]
    briefing_document: str
    document_url: Optional[str]
    error: Optional[str]
    current_step: str
