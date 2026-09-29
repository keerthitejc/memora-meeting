from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MemoryItem(BaseModel):
    id: str
    content: str
    timestamp: str
    metadata: Dict[str, Any] = {}
    tags: List[str] = []

class PreferenceSetting(BaseModel):
    bank_id: str
    instruction: str
    created_at: str
