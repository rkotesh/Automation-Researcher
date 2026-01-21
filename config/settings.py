from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    serper_api_key: str = Field(..., env="SERPER_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    google_drive_credentials_path: str = Field(default="credentials.json", env="GOOGLE_DRIVE_CREDENTIALS_PATH")
    google_drive_token_path: str = Field(default="token.json", env="GOOGLE_DRIVE_TOKEN_PATH")
    google_drive_folder_id: Optional[str] = Field(default=None, env="GOOGLE_DRIVE_FOLDER_ID")
    max_search_results: int = Field(default=3, env="MAX_SEARCH_RESULTS")
    scraping_timeout: int = Field(default=30, env="SCRAPING_TIMEOUT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    llm_provider: str = Field(default="anthropic", env="LLM_PROVIDER")
    llm_model: str = Field(default="claude-3-sonnet-20240229", env="LLM_MODEL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
