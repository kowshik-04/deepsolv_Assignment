from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Follower(BaseModel):
    page_id: str
    profile_id: str
    name: Optional[str] = None
    profile_url: Optional[str] = None
    relation: str  # "follower" or "following"
    followed_at: datetime = datetime.utcnow()
