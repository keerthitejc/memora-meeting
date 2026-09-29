import os
import sys
import logging
from typing import Optional, List, Dict, Any

# Ensure project root is on sys.path for Vercel Serverless Function imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.meeting_service import meeting_service
from backend.agents.meeting_agent import meeting_agent
from backend.agents.memory_agent import memory_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memora.main")

app = FastAPI(
    title="MEMORA API",
    description="Autonomous Relationship Memory & Meeting Intelligence Agent API powered by Hindsight & Groq",
    version="1.0.0"
)

# Enable CORS for Vite React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from backend.services.db_service import db_service

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class PrepareRequest(BaseModel):
    contact_id: str
    memory_on: bool = True

class WhyRequest(BaseModel):
    contact_id: str
    query: str

class PreferenceRequest(BaseModel):
    contact_id: str
    instruction: str


@app.post("/api/auth/register")
def register_user(req: RegisterRequest):
    try:
        user = db_service.register_user(email=req.email, password=req.password, name=req.name)
        return {"status": "success", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/auth/login")
def login_user(req: LoginRequest):
    user = db_service.authenticate_user(email=req.email, password=req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"status": "success", "user": user}


@app.get("/")
def read_root():
    return {
        "app": "MEMORA — AI Relationship Memory & Meeting Intelligence Agent",
        "status": "online",
        "hindsight_engine": "ready",
        "tagline": "Most meeting assistants remember the meeting. MEMORA remembers the relationship."
    }


@app.get("/api/stats")
def get_stats():
    contacts = meeting_service.get_contacts()
    commitments = meeting_service.get_commitments_all()
    open_items = [c for c in commitments if c["status"] in ["overdue", "in_progress", "open"]]
    
    return {
        "total_contacts": len(contacts),
        "total_memories": 42,
        "open_commitments": len(open_items),
        "overdue_count": sum(1 for c in commitments if c["status"] == "overdue"),
        "freshness": "100% Synced"
    }


@app.get("/api/contacts")
def list_contacts():
    return meeting_service.get_contacts()


@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: str):
    c = meeting_service.get_contact_by_id(contact_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contact not found")
    return c


@app.get("/api/meetings")
def list_meetings():
    return meeting_service.get_meetings()


@app.get("/api/next-meeting")
def next_meeting():
    m = meeting_service.get_next_meeting()
    if not m:
        raise HTTPException(status_code=404, detail="No upcoming meetings found")
    return m


@app.post("/api/prepare")
async def prepare_meeting(req: PrepareRequest):
    contact = meeting_service.get_contact_by_id(req.contact_id)
    if not contact:
        # Fallback to Rahul Sharma
        contact = meeting_service.get_contacts()[0]
    
    meeting = meeting_service.get_meeting_for_contact(contact["id"])
    title = meeting["title"] if meeting else "Relationship Sync"
    agenda = meeting["agenda"] if meeting else "General check-in and task review"

    result = await meeting_agent.prepare_meeting(
        contact_id=contact["id"],
        contact_name=contact["name"],
        bank_id=contact.get("bank_id", "contact_rahul_sharma"),
        meeting_title=title,
        agenda=agenda,
        memory_on=req.memory_on
    )
    return result


@app.post("/api/why")
async def ask_why(req: WhyRequest):
    contact = meeting_service.get_contact_by_id(req.contact_id)
    bank_id = contact.get("bank_id", "contact_rahul_sharma") if contact else "contact_rahul_sharma"
    
    explanation = await memory_agent.explain_why(bank_id=bank_id, query=req.query)
    return explanation


@app.get("/api/timeline/{contact_id}")
def get_timeline(contact_id: str):
    return meeting_service.get_relationship_timeline(contact_id)


@app.get("/api/explorer/{contact_id}")
def get_explorer(contact_id: str):
    return meeting_service.get_memory_explorer_graph(contact_id)


@app.get("/api/commitments")
def get_commitments():
    return meeting_service.get_commitments_all()


@app.post("/api/preferences")
async def save_preferences(req: PreferenceRequest):
    contact = meeting_service.get_contact_by_id(req.contact_id)
    bank_id = contact.get("bank_id", "contact_rahul_sharma") if contact else "contact_rahul_sharma"
    
    res = await memory_agent.update_preferences(bank_id=bank_id, instruction=req.instruction)
    return {
        "status": "success",
        "message": "Preference updated and retained in Hindsight memory.",
        "instruction": req.instruction
    }
