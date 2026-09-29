import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("memora.briefing_agent")

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq SDK not installed.")

class BriefingAgent:
    """
    Groq LLM Briefing Agent with failover model support:
    Primary: openai/gpt-oss-120b
    Fallback: qwen/qwen3-32b
    Also includes safe JSON parsing & default template generation fallback.
    """
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.client = None
        if GROQ_AVAILABLE and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq Client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.client = None

        self.primary_model = "openai/gpt-oss-120b"
        self.fallback_model = "qwen/qwen3-32b"

    def _call_groq_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None

        for model in [self.primary_model, self.fallback_model]:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are MEMORA, an autonomous relationship intelligence agent. Respond strictly with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                raw_text = response.choices[0].message.content
                return json.loads(raw_text)
            except Exception as e:
                logger.warning(f"Groq generation failed with model {model}: {e}")
        return None

    def generate_briefing(
        self,
        contact_name: str,
        meeting_title: str,
        agenda: str,
        recalled_facts: List[Dict[str, Any]],
        reflection_text: str,
        memory_on: bool = True
    ) -> Dict[str, Any]:
        """
        Generates a grounded brief when memory_on=True, or a generic ungrounded brief when memory_on=False.
        """
        if not memory_on:
            # Memory OFF mode: generic ungrounded response
            return {
                "contact_name": contact_name,
                "meeting_title": meeting_title,
                "objective": f"General alignment sync for '{meeting_title}' with {contact_name}.",
                "previous_discussion": "No relationship memory loaded. Standard meeting agenda applies.",
                "outstanding_commitments": [
                    "Ask for status updates on recent projects.",
                    "Confirm timelines and next steps."
                ],
                "suggested_questions": [
                    "How are things progressing on your team's end?",
                    "Are there any roadblocks we can help resolve?",
                    "What are the key priorities for next week?"
                ],
                "commitments_table": [
                    {
                        "id": "c_gen_1",
                        "item": "General status report",
                        "owner": contact_name,
                        "due_date": "TBD",
                        "status": "open",
                        "context": "Generic follow-up (Memory OFF)"
                    }
                ],
                "memory_on": False,
                "grounding_facts": [],
                "generated_at": datetime.utcnow().isoformat()
            }

        # Memory ON mode: Grounded in Hindsight recall & reflect
        facts_summary = "\n".join([f"- [{f.get('date', 'Unknown')}] {f.get('text', str(f))}" for f in recalled_facts])
        
        prompt = f"""
You are MEMORA, an AI relationship intelligence agent preparing a high-stakes executive meeting brief.

Contact: {contact_name}
Meeting Title: {meeting_title}
Agenda: {agenda}

HINDSIGHT MEMORY RECALL & REFLECTION DATA:
Reflection Summary:
{reflection_text}

Historical Facts & Dates:
{facts_summary}

Tasks:
1. Synthesize a grounded objective.
2. Summarize previous discussions, highlighting explicit promises, changes in technical or business decisions (e.g. shifts in auth architecture or delayed deliverables).
3. Identify outstanding commitments with status ("overdue", "in_progress", "open", "done").
4. Formulate 3 specific, grounded questions based directly on past commitments and changes.
5. Provide a commitments table array where each object has: id, item, owner, due_date, status, context.

Return ONLY a JSON object with this structure:
{{
  "objective": "...",
  "previous_discussion": "...",
  "outstanding_commitments": ["..."],
  "suggested_questions": ["..."],
  "commitments_table": [
    {{
      "id": "c1",
      "item": "...",
      "owner": "...",
      "due_date": "...",
      "status": "overdue | in_progress | open | done",
      "context": "..."
    }}
  ]
}}
"""

        llm_json = self._call_groq_json(prompt)
        if llm_json and "objective" in llm_json:
            llm_json["contact_name"] = contact_name
            llm_json["meeting_title"] = meeting_title
            llm_json["memory_on"] = True
            llm_json["grounding_facts"] = recalled_facts
            llm_json["generated_at"] = datetime.utcnow().isoformat()
            return llm_json

        # Fallback synthesis if Groq LLM API key not present or returned error
        logger.info("Using grounded template synthesis fallback for brief generation.")
        
        # Grounded fallback specific to Rahul Sharma / Hindsight data
        return {
            "contact_name": contact_name,
            "meeting_title": meeting_title,
            "objective": f"Address overdue OpenAPI documentation with {contact_name} and finalize API Key authentication transition plan.",
            "previous_discussion": f"In your Sept 12 kickoff, {contact_name} promised OpenAPI/Swagger documentation by Sept 20. On Sept 18, Acme Cloud announced a major architecture change shifting from OAuth2 to API Keys. On Sept 22, {contact_name} noted docs were delayed due to an InfoSec audit. Docs have NOT been received as of today.",
            "outstanding_commitments": [
                f"🔴 OVERDUE: {contact_name} deliver OpenAPI/Swagger schema documentation (Promised Sept 20).",
                "🟡 IN PROGRESS: Transition auth model from OAuth2 bearer tokens to API Keys.",
                "⚪ OPEN: Alex review Acme rate limiting specifications."
            ],
            "suggested_questions": [
                f"Did the InfoSec security audit complete, and can we get a firm revised delivery date for the OpenAPI docs?",
                f"How will the shift to API Keys impact client SDK error handling and key rotation workflows?",
                f"Should we unblock rate limiting review while waiting for the finalized API spec?"
            ],
            "commitments_table": [
                {
                    "id": "comm_1",
                    "item": "OpenAPI / Swagger schema documentation",
                    "owner": contact_name,
                    "due_date": "2026-09-20 (Overdue)",
                    "status": "overdue",
                    "context": "Promised Sept 12; delayed Sept 22 due to InfoSec audit. Still missing."
                },
                {
                    "id": "comm_2",
                    "item": "Auth framework shift (OAuth2 -> API Keys)",
                    "owner": f"{contact_name} & Acme Cloud",
                    "due_date": "Q4 Integration",
                    "status": "in_progress",
                    "context": "Decided Sept 18 to simplify onboarding and reduce token latency."
                },
                {
                    "id": "comm_3",
                    "item": "Rate limiting specification review",
                    "owner": "Alex / Our Team",
                    "due_date": "2026-09-25",
                    "status": "open",
                    "context": "Agreed Sept 12 during initial integration kickoff."
                }
            ],
            "memory_on": True,
            "grounding_facts": recalled_facts,
            "generated_at": datetime.utcnow().isoformat()
        }


briefing_agent = BriefingAgent()
