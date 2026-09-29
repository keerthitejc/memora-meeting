from pydantic import BaseModel, Field
from typing import Optional, List

class Contact(BaseModel):
    id: str
    name: str
    role: str
    company: str
    email: str
    avatar: Optional[str] = None
    relationship_status: str
    last_interaction: str
    bank_id: str
