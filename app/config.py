from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedIn Insights Service"
    ENV: str = "development"

    DEMO_SCRAPER: bool = True  
    LINKEDIN_SESSION_COOKIE: Optional[str] = None  

    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "linkedin_insights"

    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL_SECONDS: int = 300

    OPENAI_API_KEY: Optional[str] = None
    SCRAPE_POST_LIMIT: int = 20

    class Config:
        env_file = ".env"

settings = Settings()