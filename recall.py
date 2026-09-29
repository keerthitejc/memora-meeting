from typing import Dict, Any, Optional, List
from .client import hindsight_service

async def recall_memories(bank_id: str, query: str, types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Recalls memories from Hindsight using mixed strategy (semantic + keyword + graph + temporal).
    """
    return await hindsight_service.recall(bank_id=bank_id, query=query, types=types)
