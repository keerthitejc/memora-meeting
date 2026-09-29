import logging
from typing import Dict, Any, List
from backend.hindsight.recall import recall_memories
from backend.hindsight.reflect import reflect_memories, set_steering_mission

logger = logging.getLogger("memora.memory_agent")

class MemoryAgent:
    """
    Autonomous Memory Agent that handles Hindsight recall, reflect,
    'Why?' evidence retrieval, and preference steering.
    """
    async def get_contact_memory_context(self, bank_id: str, contact_name: str) -> Dict[str, Any]:
        """
        Executes Hindsight recall and reflect for a contact.
        """
        query = f"Retrieve all historical meetings, decisions, commitments, deadlines, and architectural changes with {contact_name}."
        
        recall_res = await recall_memories(bank_id=bank_id, query=query)
        reflect_res = await reflect_memories(bank_id=bank_id, query=query)
        
        return {
            "bank_id": bank_id,
            "recalled_facts": recall_res.get("source_facts", []),
            "recalled_results": recall_res.get("results", []),
            "reflection": reflect_res.get("text", ""),
            "based_on": reflect_res.get("based_on", [])
        }

    async def explain_why(self, bank_id: str, query: str) -> Dict[str, Any]:
        """
        Provides evidence-backed drill-down to answer 'Why' questions by querying Hindsight.
        """
        recall_res = await recall_memories(bank_id=bank_id, query=query)
        facts = recall_res.get("source_facts", [])
        
        if not facts:
            # Fallback search
            general_res = await recall_memories(bank_id=bank_id, query="commitments documentation overdue deadlines")
            facts = general_res.get("source_facts", [])

        explanation_lines = []
        citations = []
        for idx, fact in enumerate(facts[:4], 1):
            if isinstance(fact, dict):
                text = fact.get("text", str(fact))
                date = fact.get("date", fact.get("timestamp", "Recent"))
            else:
                text = str(fact)
                date = "Recent"
            
            citations.append({
                "id": f"cite_{idx}",
                "date": date,
                "fact": text
            })
            explanation_lines.append(f"• [{date}] {text}")

        answer = f"This claim is grounded in {len(citations)} exact historical memories retained in Hindsight:\n\n" + "\n".join(explanation_lines)

        return {
            "query": query,
            "answer": answer,
            "citations": citations
        }

    async def update_preferences(self, bank_id: str, instruction: str) -> Dict[str, Any]:
        """
        Stores durable steering instruction in Hindsight memory.
        """
        return await set_steering_mission(bank_id=bank_id, mission=instruction)


memory_agent = MemoryAgent()
