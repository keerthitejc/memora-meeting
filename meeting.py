from pydantic import BaseModel
from typing import Optional, List, Any

class Meeting(BaseModel):
    id: str
    contact_id: str
    contact_name: str
    title: str
    time: str
    scheduled_date: str
    location: str
    agenda: str

class CommitmentItem(BaseModel):
    id: str
    item: str
    owner: str  # "Rahul", "Alex", "Them", "Us"
    due_date: str
    status: str  # "overdue", "in_progress", "open", "done"
    context: str

class PrepBriefing(BaseModel):
    contact_name: str
    meeting_title: str
    objective: str
    previous_discussion: str
    outstanding_commitments: List[str]
    suggested_questions: List[str]
    commitments_table: List[CommitmentItem]
    memory_on: bool = True
    grounding_facts: List[Dict[str, Any]] = []
    generated_at: str
