from typing import Dict, Any
from .client import hindsight_service

async def reflect_memories(bank_id: str, query: str) -> Dict[str, Any]:
    """
    Reflects on memories in Hindsight to synthesize high-level relationship insights.
    """
    return await hindsight_service.reflect(bank_id=bank_id, query=query)

async def set_steering_mission(bank_id: str, mission: str) -> Dict[str, Any]:
    """
    Sets a durable steering mission for preference learning.
    """
    return await hindsight_service.set_mission(bank_id=bank_id, mission=mission)
