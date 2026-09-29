import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("memora.hindsight")

# Try importing official Hindsight Client
try:
    from hindsight_client import Hindsight, RecallResponse, ReflectResponse
    HINDSIGHT_AVAILABLE = True
except ImportError:
    HINDSIGHT_AVAILABLE = False
    logger.warning("hindsight-client not installed. Operating in fallback mode.")


class LocalMemoryStore:
    """
    Robust in-memory / persistent fallback engine that mimics Hindsight's
    Retain, Recall, and Reflect operations when live Hindsight API key is missing or offline.
    """
    def __init__(self):
        self.banks: Dict[str, List[Dict[str, Any]]] = {}
        self.missions: Dict[str, str] = {}
        self._bootstrap_seed_data()

    def _bootstrap_seed_data(self):
        # Auto-seed Rahul Sharma memories
        self.banks["contact_rahul_sharma"] = [
            {
                "id": "mem_1",
                "content": "Kickoff Meeting with Rahul Sharma (VP Engineering, Acme Cloud). We discussed the core REST API integration schema. Rahul explicitly promised to deliver the OpenAPI/Swagger documentation by September 20, 2026. Alex (our side) promised to review Acme's rate limiting specifications by September 25.",
                "timestamp": "2026-09-12T10:00:00Z",
                "metadata": {"type": "meeting", "contact": "Rahul Sharma", "company": "Acme Cloud"},
                "tags": ["meeting", "commitment", "deadline", "api-docs"]
            },
            {
                "id": "mem_2",
                "content": "Architecture Sync with Rahul Sharma. Major decision change: Acme Cloud is shifting its authentication framework from OAuth2 Bearer Tokens to API Key headers. Rahul noted this change will simplify partner developer onboarding and reduce OAuth server latency.",
                "timestamp": "2026-09-18T14:30:00Z",
                "metadata": {"type": "decision", "contact": "Rahul Sharma", "topic": "auth-architecture"},
                "tags": ["decision", "architecture", "oauth2", "api-keys"]
            },
            {
                "id": "mem_3",
                "content": "Slack Check-in with Rahul Sharma. Rahul mentioned the OpenAPI documentation delivery (originally promised for Sept 20) is delayed due to an internal InfoSec security audit. The docs were not sent by the Sept 20 deadline and remain outstanding.",
                "timestamp": "2026-09-22T16:00:00Z",
                "metadata": {"type": "update", "contact": "Rahul Sharma", "status": "delayed"},
                "tags": ["commitment-delayed", "overdue", "api-docs", "infosec"]
            }
        ]
        self.banks["contact_priya_patel"] = [
            {
                "id": "mem_p1",
                "content": "Partnership kickoff with Priya Patel (Nexus Systems). Priya requested a custom 99.99% uptime SLA clause and dedicated support tier. Promised to send draft agreement terms by Sept 23.",
                "timestamp": "2026-09-20T11:00:00Z",
                "metadata": {"type": "meeting", "contact": "Priya Patel"},
                "tags": ["meeting", "sla", "contract"]
            },
            {
                "id": "mem_p2",
                "content": "Email from Priya Patel: Sent draft contract with 99.99% SLA. Awaiting our legal team review.",
                "timestamp": "2026-09-24T11:00:00Z",
                "metadata": {"type": "email", "contact": "Priya Patel"},
                "tags": ["contract", "review"]
            }
        ]
        self.banks["contact_david_chen"] = [
            {
                "id": "mem_d1",
                "content": "Tech sync with David Chen (DataSync Corp). Discussed migration to PostgreSQL 16 partition indexing. David agreed to prepare test benchmarks by Sept 26.",
                "timestamp": "2026-09-19T16:15:00Z",
                "metadata": {"type": "meeting", "contact": "David Chen"},
                "tags": ["meeting", "architecture", "database"]
            }
        ]

    def retain(self, bank_id: str, content: str, timestamp: Optional[str] = None, metadata: Optional[Dict[str, str]] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        if bank_id not in self.banks:
            self.banks[bank_id] = []
        
        entry = {
            "id": f"mem_{len(self.banks[bank_id]) + 1}",
            "content": content,
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat()
        }
        self.banks[bank_id].append(entry)
        return {"status": "success", "id": entry["id"]}

    def recall(self, bank_id: str, query: str, types: Optional[List[str]] = None) -> Dict[str, Any]:
        memories = self.banks.get(bank_id, [])
        if not memories:
            return {"results": [], "source_facts": [], "count": 0}
        
        query_words = set(query.lower().split())
        scored = []
        for mem in memories:
            text = mem["content"].lower()
            tags_text = " ".join(mem.get("tags", [])).lower()
            match_score = sum(1 for w in query_words if w in text or w in tags_text)
            
            # Simple keyword + recency scoring
            scored.append((match_score, mem))
        
        # Sort descending by match score, then recency
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored]
        
        return {
            "results": results,
            "source_facts": [{"text": m["content"], "date": m["timestamp"], "id": m["id"]} for m in results],
            "count": len(results)
        }

    def reflect(self, bank_id: str, query: str) -> Dict[str, Any]:
        recall_res = self.recall(bank_id, query)
        facts = recall_res["source_facts"]
        mission = self.missions.get(bank_id, "Analyze contact commitments and relationship context.")
        
        fact_texts = "\n- ".join([f"[{f['date']}] {f['text']}" for f in facts])
        synthesis = f"Based on {len(facts)} historical interactions under steering instruction ('{mission}'):\n- {fact_texts}"
        
        return {
            "text": synthesis,
            "based_on": facts
        }

    def set_mission(self, bank_id: str, mission: str):
        self.missions[bank_id] = mission
        return {"status": "success", "mission": mission}


local_store = LocalMemoryStore()


class MemoraHindsightClient:
    """
    Unified Hindsight wrapper supporting both official Hindsight Cloud API
    and graceful fallback mode.
    """
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY", "").strip()
        self.workspace_id = os.getenv("HINDSIGHT_WORKSPACE_ID", "memora-default").strip()
        self.base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").strip()
        
        self.client = None
        if HINDSIGHT_AVAILABLE and self.api_key:
            try:
                self.client = Hindsight(base_url=self.base_url, api_key=self.api_key)
                logger.info("Initialized Hindsight Cloud Client")
            except Exception as e:
                logger.error(f"Failed to initialize Hindsight Client: {e}")
                self.client = None
        else:
            logger.info("Operating Memora Hindsight Client in local fallback mode")

    async def retain(self, bank_id: str, content: str, timestamp: Optional[str] = None, metadata: Optional[Dict[str, str]] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retain memory in Hindsight (prioritizing people/roles, decisions, commitments, deadlines).
        """
        bank = bank_id or self.workspace_id
        if self.client:
            try:
                ts = datetime.fromisoformat(timestamp) if timestamp else datetime.utcnow()
                res = await self.client.aretain(
                    bank_id=bank,
                    content=content,
                    timestamp=ts,
                    metadata=metadata or {},
                    tags=tags or ["interaction"]
                )
                return {"status": "success", "response": str(res)}
            except Exception as e:
                logger.warning(f"Hindsight Cloud retain failed ({e}). Falling back to local store.")
        
        return local_store.retain(bank_id=bank, content=content, timestamp=timestamp, metadata=metadata, tags=tags)

    async def recall(self, bank_id: str, query: str, types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Recall memories using Hindsight mixed retrieval (semantic + keyword + graph + temporal).
        """
        bank = bank_id or self.workspace_id
        if self.client:
            try:
                res = await self.client.arecall(
                    bank_id=bank,
                    query=query,
                    types=types,
                    include_chunks=True,
                    include_source_facts=True
                )
                
                # Extract results format
                source_facts = []
                results_list = []
                if hasattr(res, "source_facts") and res.source_facts:
                    source_facts = [fact.to_dict() if hasattr(fact, "to_dict") else str(fact) for fact in res.source_facts]
                if hasattr(res, "results") and res.results:
                    results_list = [r.to_dict() if hasattr(r, "to_dict") else str(r) for r in res.results]

                return {
                    "results": results_list,
                    "source_facts": source_facts,
                    "raw": str(res)
                }
            except Exception as e:
                logger.warning(f"Hindsight Cloud recall failed ({e}). Falling back to local store.")

        return local_store.recall(bank_id=bank, query=query, types=types)

    async def reflect(self, bank_id: str, query: str) -> Dict[str, Any]:
        """
        Reflect over retained memories to synthesize relationship insights.
        """
        bank = bank_id or self.workspace_id
        if self.client:
            try:
                res = await self.client.areflect(
                    bank_id=bank,
                    query=query,
                    budget="low"
                )
                based_on = getattr(res, "based_on", [])
                return {
                    "text": getattr(res, "text", str(res)),
                    "based_on": [b.to_dict() if hasattr(b, "to_dict") else str(b) for b in based_on] if based_on else []
                }
            except Exception as e:
                logger.warning(f"Hindsight Cloud reflect failed ({e}). Falling back to local store.")

        return local_store.reflect(bank_id=bank, query=query)

    async def set_mission(self, bank_id: str, mission: str) -> Dict[str, Any]:
        """
        Set durable steering instruction for preference learning.
        """
        bank = bank_id or self.workspace_id
        if self.client:
            try:
                await self.client.aset_mission(bank_id=bank, mission=mission)
                return {"status": "success", "mission": mission}
            except Exception as e:
                logger.warning(f"Hindsight Cloud set_mission failed ({e}). Setting local store mission.")
        
        return local_store.set_mission(bank_id=bank, mission=mission)


# Global singleton instance
hindsight_service = MemoraHindsightClient()
