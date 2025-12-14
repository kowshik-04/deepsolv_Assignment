from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    page_id: str
    post_id: str
    content: str
    likes: int
    comments_count: int
    posted_at: datetime
