from typing import Dict, Any, Optional, List
from .client import hindsight_service

async def retain_memory(bank_id: str, content: str, timestamp: Optional[str] = None, metadata: Optional[Dict[str, str]] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Retains interaction memory into Hindsight.
    Configured to prioritize: people/roles, decisions, commitments, deadlines, unresolved tasks.
    """
    return await hindsight_service.retain(
        bank_id=bank_id,
        content=content,
        timestamp=timestamp,
        metadata=metadata,
        tags=tags or ["meeting", "commitment", "decision"]
    )
