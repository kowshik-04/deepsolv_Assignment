from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Comment(BaseModel):
    page_id: str
    post_id: str
    comment_id: str
    author: Optional[str] = None
    content: str
    likes: int = 0
    posted_at: datetime
