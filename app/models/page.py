from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class Page(BaseModel):
    page_id: str = Field(..., description="LinkedIn Page ID")
    name: str
    url: str
    linkedin_internal_id: Optional[str]
    profile_picture: Optional[str]
    description: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    followers: int
    head_count: int
    specialties: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_scraped_at: datetime = Field(default_factory=datetime.utcnow)
