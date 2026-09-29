import os
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("memora.meeting_service")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO_DIR = os.path.join(BASE_DIR, "demo")

class MeetingService:
    def __init__(self):
        self.contacts_file = os.path.join(DEMO_DIR, "contacts.json")
        self.meetings_file = os.path.join(DEMO_DIR, "meetings.json")

    def get_contacts(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_contact_by_id(self, contact_id: str) -> Optional[Dict[str, Any]]:
        contacts = self.get_contacts()
        for c in contacts:
            if c["id"] == contact_id:
                return c
        return None

    def get_meetings(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.meetings_file):
            with open(self.meetings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_next_meeting(self) -> Optional[Dict[str, Any]]:
        meetings = self.get_meetings()
        return meetings[0] if meetings else None

    def get_meeting_for_contact(self, contact_id: str) -> Optional[Dict[str, Any]]:
        meetings = self.get_meetings()
        for m in meetings:
            if m["contact_id"] == contact_id:
                return m
        return self.get_next_meeting()

    def get_commitments_all(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "comm_1",
                "contact_id": "c1",
                "contact_name": "Rahul Sharma",
                "company": "Acme Cloud",
                "item": "OpenAPI / Swagger schema documentation",
                "owner": "Rahul Sharma",
                "due_date": "2026-09-20",
                "status": "overdue",
                "context": "Promised Sept 12; delayed Sept 22 due to InfoSec audit. Missing."
            },
            {
                "id": "comm_2",
                "contact_id": "c1",
                "contact_name": "Rahul Sharma",
                "company": "Acme Cloud",
                "item": "Auth framework shift (OAuth2 -> API Keys)",
                "owner": "Rahul Sharma & Acme Cloud",
                "due_date": "Q4 Integration",
                "status": "in_progress",
                "context": "Decided Sept 18 to simplify onboarding and reduce token latency."
            },
            {
                "id": "comm_3",
                "contact_id": "c1",
                "contact_name": "Rahul Sharma",
                "company": "Acme Cloud",
                "item": "Rate limiting specification review",
                "owner": "Alex / Our Team",
                "due_date": "2026-09-25",
                "status": "open",
                "context": "Agreed Sept 12 during initial integration kickoff."
            },
            {
                "id": "comm_4",
                "contact_id": "c2",
                "contact_name": "Priya Patel",
                "company": "Nexus Systems",
                "item": "Draft 99.99% SLA commercial agreement terms",
                "owner": "Priya Patel",
                "due_date": "2026-09-23",
                "status": "done",
                "context": "Received Sept 24 via email, now under legal review."
            },
            {
                "id": "comm_5",
                "contact_id": "c3",
                "contact_name": "David Chen",
                "company": "DataSync Corp",
                "item": "PostgreSQL 16 partition index benchmarks",
                "owner": "David Chen",
                "due_date": "2026-09-26",
                "status": "in_progress",
                "context": "Agreed Sept 19 during database architecture sync."
            }
        ]

    def get_relationship_timeline(self, contact_id: str) -> List[Dict[str, Any]]:
        if contact_id == "c1":
            return [
                {
                    "id": "t1",
                    "date": "2026-09-12 10:00 AM",
                    "title": "API Kickoff Sync",
                    "type": "meeting",
                    "category": "Commitment Made",
                    "description": "Discussed core REST API integration schema. Rahul explicitly promised OpenAPI/Swagger schema documentation by Sept 20. Alex agreed to review rate limits by Sept 25.",
                    "tags": ["meeting", "commitment", "api-docs"]
                },
                {
                    "id": "t2",
                    "date": "2026-09-18 02:30 PM",
                    "title": "Architecture Alignment",
                    "type": "decision",
                    "category": "Decision Shift",
                    "description": "Major architecture pivot: Acme Cloud changed auth framework from OAuth2 Bearer Tokens to API Key headers to simplify partner developer onboarding.",
                    "tags": ["decision", "auth", "api-keys"]
                },
                {
                    "id": "t3",
                    "date": "2026-09-22 04:00 PM",
                    "title": "Slack Progress Check-in",
                    "type": "update",
                    "category": "Delay Warning",
                    "description": "Rahul reported that the promised OpenAPI documentation is delayed due to an internal InfoSec security audit. Sept 20 deadline missed.",
                    "tags": ["overdue", "infosec", "delay"]
                },
                {
                    "id": "t4",
                    "date": "Today, 02:00 PM",
                    "title": "Product Sync & Integration Review",
                    "type": "upcoming",
                    "category": "Upcoming Meeting",
                    "description": "Upcoming meeting to resolve OpenAPI docs delay and confirm API key rollout schedule.",
                    "tags": ["upcoming", "sync"]
                }
            ]
        elif contact_id == "c2":
            return [
                {
                    "id": "tp1",
                    "date": "2026-09-20 11:00 AM",
                    "title": "Partnership Kickoff",
                    "type": "meeting",
                    "category": "Negotiation",
                    "description": "Priya requested a custom 99.99% uptime SLA clause. Promised draft terms by Sept 23.",
                    "tags": ["meeting", "sla"]
                },
                {
                    "id": "tp2",
                    "date": "2026-09-24 11:00 AM",
                    "title": "Contract Delivery",
                    "type": "email",
                    "category": "Deliverable Received",
                    "description": "Priya emailed draft agreement terms. Sent to legal review.",
                    "tags": ["contract", "done"]
                }
            ]
        else:
            return [
                {
                    "id": "td1",
                    "date": "2026-09-19 04:15 PM",
                    "title": "Tech Sync",
                    "type": "meeting",
                    "category": "Technical",
                    "description": "Discussed PostgreSQL 16 partition index benchmarks. David promised test results by Sept 26.",
                    "tags": ["meeting", "db"]
                }
            ]

    def get_memory_explorer_graph(self, contact_id: str) -> Dict[str, Any]:
        contact = self.get_contact_by_id(contact_id) or {
            "id": "c1", "name": "Rahul Sharma", "role": "VP Engineering", "company": "Acme Cloud"
        }
        
        return {
            "center": {
                "id": contact["id"],
                "label": contact["name"],
                "sublabel": f"{contact['role']} @ {contact['company']}",
                "type": "contact"
            },
            "nodes": [
                {
                    "id": "n_meetings",
                    "label": "Meetings (3)",
                    "type": "category",
                    "color": "#6366F1",
                    "items": [
                        {"date": "2026-09-12", "title": "API Kickoff Sync", "detail": "Promised OpenAPI schema by Sept 20"},
                        {"date": "2026-09-18", "title": "Architecture Alignment", "detail": "Shifted OAuth2 to API Keys"},
                        {"date": "2026-09-22", "title": "Slack Sync", "detail": "InfoSec audit delay reported"}
                    ]
                },
                {
                    "id": "n_decisions",
                    "label": "Decisions (1)",
                    "type": "category",
                    "color": "#8B5CF6",
                    "items": [
                        {"date": "2026-09-18", "title": "Auth Architecture Change", "detail": "OAuth2 Bearer Tokens -> API Key headers"}
                    ]
                },
                {
                    "id": "n_commitments",
                    "label": "Commitments (3)",
                    "type": "category",
                    "color": "#EF4444",
                    "items": [
                        {"status": "overdue", "title": "OpenAPI Documentation", "detail": "Promised Sept 20, Overdue by 8 days"},
                        {"status": "in_progress", "title": "API Key Auth Transition", "detail": "Target: Q4 Integration"},
                        {"status": "open", "title": "Rate Limit Spec Review", "detail": "Target: Sept 25, Open"}
                    ]
                }
            ]
        }


meeting_service = MeetingService()
