import logging
import asyncio
from typing import Dict, Any, Optional
from backend.agents.memory_agent import memory_agent
from backend.agents.briefing_agent import briefing_agent

logger = logging.getLogger("memora.meeting_agent")

class MeetingAgent:
    """
    Core Autonomous Meeting Agent: orchestrates Recall -> Reflect -> Build Brief pipeline.
    """
    async def prepare_meeting(
        self,
        contact_id: str,
        contact_name: str,
        bank_id: str,
        meeting_title: str,
        agenda: str,
        memory_on: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the centerpiece agent pipeline.
        Returns the briefing along with pipeline execution trace for UI animation.
        """
        pipeline_steps = []
        
        if not memory_on:
            # Memory OFF mode
            pipeline_steps.append({
                "step": "bypass",
                "status": "completed",
                "label": "Memory OFF Mode",
                "detail": "Bypassing Hindsight relationship recall. Generating generic LLM prep."
            })
            brief = briefing_agent.generate_briefing(
                contact_name=contact_name,
                meeting_title=meeting_title,
                agenda=agenda,
                recalled_facts=[],
                reflection_text="",
                memory_on=False
            )
            return {
                "briefing": brief,
                "pipeline_steps": pipeline_steps
            }

        # Step 1: Hindsight Recall
        pipeline_steps.append({
            "step": "recall",
            "status": "in_progress",
            "label": "1. Hindsight Recall",
            "detail": f"Querying multi-strategy memory index (semantic + keyword + temporal) for bank '{bank_id}'..."
        })
        
        memory_ctx = await memory_agent.get_contact_memory_context(bank_id=bank_id, contact_name=contact_name)
        recalled_facts = memory_ctx.get("recalled_facts", [])
        
        pipeline_steps[0]["status"] = "completed"
        pipeline_steps[0]["result"] = f"Retrieved {len(recalled_facts)} memory units & timeline facts."

        # Step 2: Hindsight Reflect
        pipeline_steps.append({
            "step": "reflect",
            "status": "in_progress",
            "label": "2. Hindsight Reflect",
            "detail": "Synthesizing relationship trajectory, changed decisions, and overdue promises..."
        })
        
        reflection_text = memory_ctx.get("reflection", "")
        pipeline_steps[1]["status"] = "completed"
        pipeline_steps[1]["result"] = "Reflected on past interactions and decision shifts."

        # Step 3: Build Briefing
        pipeline_steps.append({
            "step": "brief",
            "status": "in_progress",
            "label": "3. Build Briefing",
            "detail": "Groq LLM turning Hindsight reflection into structured meeting brief..."
        })
        
        brief = briefing_agent.generate_briefing(
            contact_name=contact_name,
            meeting_title=meeting_title,
            agenda=agenda,
            recalled_facts=recalled_facts,
            reflection_text=reflection_text,
            memory_on=True
        )

        pipeline_steps[2]["status"] = "completed"
        pipeline_steps[2]["result"] = "Grounded briefing generated with commitments & suggested questions."

        return {
            "briefing": brief,
            "pipeline_steps": pipeline_steps
        }


meeting_agent = MeetingAgent()
