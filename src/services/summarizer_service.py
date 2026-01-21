from anthropic import Anthropic
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from typing import List
from config.settings import settings
from src.agents.state import ScrapedContent
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SummarizerService:
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model
        
        if self.provider == "anthropic":
            self.client = Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "openai":
            if not OpenAI:
                raise ImportError("OpenAI package is not installed. Please run `pip install openai`.")
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_briefing(self, topic: str, scraped_contents: List[ScrapedContent]) -> str:
        """
        Generate a comprehensive briefing document from scraped content
        """
        # Filter successful scrapes
        successful_scrapes = [s for s in scraped_contents if s.success and s.content]
        
        if not successful_scrapes:
            raise ValueError("No successfully scraped content available for summarization")
        
        # Prepare content for Claude
        sources_text = self._format_sources(successful_scrapes)
        
        prompt = f"""You are a professional research analyst. Generate a comprehensive briefing document on the topic: "{topic}"

Based on the following {len(successful_scrapes)} sources, create a well-structured briefing document that:

1. Provides an executive summary (2-3 paragraphs)
2. Identifies key trends and insights
3. Highlights important statistics and data points
4. Notes any conflicting information or different perspectives
5. Concludes with actionable takeaways

Format the document professionally with clear sections and headers.

SOURCES:
{sources_text}

Generate the briefing document now:"""

        try:
            logger.info(f"Generating briefing for topic: {topic}")
            
            briefing = self._generate_completion(prompt)
            
            logger.info("Briefing document generated successfully")
            return self._add_metadata(topic, briefing, successful_scrapes)
            
        except Exception as e:
            logger.error(f"Failed to generate briefing: {str(e)}")
            raise
    
    def _format_sources(self, scraped_contents: List[ScrapedContent]) -> str:
        """
        Format scraped content for the prompt
        """
        formatted = []
        for idx, content in enumerate(scraped_contents, 1):
            source = f"\n--- SOURCE {idx} ---\n"
            source += f"Title: {content.title}\n"
            source += f"URL: {content.url}\n"
            if content.author:
                source += f"Author: {content.author}\n"
            if content.publish_date:
                source += f"Published: {content.publish_date}\n"
            source += f"\nContent:\n{content.content[:5000]}\n"  # Limit content length
            formatted.append(source)
        
        return "\n".join(formatted)
    
    def _add_metadata(self, topic: str, briefing: str, sources: List[ScrapedContent]) -> str:
        """
        Add metadata header to the briefing
        """
        from datetime import datetime
        
        header = f"""# Research Briefing: {topic}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Sources Analyzed:** {len(sources)}

---

"""
        
        footer = f"""

---

## Sources

"""
        for idx, source in enumerate(sources, 1):
            footer += f"{idx}. [{source.title}]({source.url})\n"
        
        return header + briefing + footer

    def _generate_completion(self, prompt: str) -> str:
        """
        Generate completion using the configured provider
        """
        if self.provider == "anthropic":
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return message.content[0].text
            
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional research analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        
        raise ValueError(f"Unsupported provider: {self.provider}")
