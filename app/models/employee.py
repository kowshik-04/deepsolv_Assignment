from pydantic import BaseModel

class Employee(BaseModel):
    page_id: str
    name: str
    role: str
    profile_url: str
