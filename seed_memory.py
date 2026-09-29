import os
import sys
import asyncio
import logging

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.hindsight.client import hindsight_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_memory")

RAHUL_MEMORIES = [
    {
        "content": "Kickoff Meeting with Rahul Sharma (VP Engineering, Acme Cloud). We discussed the core REST API integration schema. Rahul explicitly promised to deliver the OpenAPI/Swagger documentation by September 20, 2026. Alex (our side) promised to review Acme's rate limiting specifications by September 25.",
        "timestamp": "2026-09-12T10:00:00Z",
        "metadata": {"type": "meeting", "contact": "Rahul Sharma", "company": "Acme Cloud"},
        "tags": ["meeting", "commitment", "deadline", "api-docs"]
    },
    {
        "content": "Architecture Sync with Rahul Sharma. Major decision change: Acme Cloud is shifting its authentication framework from OAuth2 Bearer Tokens to API Key headers. Rahul noted this change will simplify partner developer onboarding and reduce OAuth server latency.",
        "timestamp": "2026-09-18T14:30:00Z",
        "metadata": {"type": "decision", "contact": "Rahul Sharma", "topic": "auth-architecture"},
        "tags": ["decision", "architecture", "oauth2", "api-keys"]
    },
    {
        "content": "Slack Check-in with Rahul Sharma. Rahul mentioned the OpenAPI documentation delivery (originally promised for Sept 20) is delayed due to an internal InfoSec security audit. The docs were not sent by the Sept 20 deadline and remain outstanding.",
        "timestamp": "2026-09-22T16:00:00Z",
        "metadata": {"type": "update", "contact": "Rahul Sharma", "status": "delayed"},
        "tags": ["commitment-delayed", "overdue", "api-docs", "infosec"]
    }
]

PRIYA_MEMORIES = [
    {
        "content": "Partnership kickoff with Priya Patel (Nexus Systems). Priya requested a custom 99.99% uptime SLA clause and dedicated support tier. Promised to send draft agreement terms by Sept 23.",
        "timestamp": "2026-09-20T11:00:00Z",
        "metadata": {"type": "meeting", "contact": "Priya Patel"},
        "tags": ["meeting", "sla", "contract"]
    },
    {
        "content": "Email from Priya Patel: Sent draft contract with 99.99% SLA. Awaiting our legal team review.",
        "timestamp": "2026-09-24T11:00:00Z",
        "metadata": {"type": "email", "contact": "Priya Patel"},
        "tags": ["contract", "review"]
    }
]

DAVID_MEMORIES = [
    {
        "content": "Tech sync with David Chen (DataSync Corp). Discussed migration to PostgreSQL 16 partition indexing. David agreed to prepare test benchmarks by Sept 26.",
        "timestamp": "2026-09-19T16:15:00Z",
        "metadata": {"type": "meeting", "contact": "David Chen"},
        "tags": ["meeting", "architecture", "database"]
    }
]


async def seed():
    logger.info("Starting Hindsight memory seeding...")
    
    bank_rahul = "contact_rahul_sharma"
    for mem in RAHUL_MEMORIES:
        res = await hindsight_service.retain(
            bank_id=bank_rahul,
            content=mem["content"],
            timestamp=mem["timestamp"],
            metadata=mem["metadata"],
            tags=mem["tags"]
        )
        logger.info(f"Retained Rahul memory: {res}")
        
    bank_priya = "contact_priya_patel"
    for mem in PRIYA_MEMORIES:
        await hindsight_service.retain(
            bank_id=bank_priya,
            content=mem["content"],
            timestamp=mem["timestamp"],
            metadata=mem["metadata"],
            tags=mem["tags"]
        )

    bank_david = "contact_david_chen"
    for mem in DAVID_MEMORIES:
        await hindsight_service.retain(
            bank_id=bank_david,
            content=mem["content"],
            timestamp=mem["timestamp"],
            metadata=mem["metadata"],
            tags=mem["tags"]
        )

    logger.info("Memory seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
