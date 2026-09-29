# MEMORA — AI Relationship Memory & Meeting Intelligence Agent

> *"Most meeting assistants remember the meeting. MEMORA remembers the relationship."*

MEMORA is an autonomous meeting-intelligence agent built for hackathons powered by **Hindsight** (by Vectorize). Before every meeting, MEMORA continuously **retains** memory about interactions, decisions, and promises, then **recalls** relevant history and **reflects** on it to generate a grounded prep briefing — including overdue commitments, changed decisions, and suggested questions.

---

## 🌟 Core Features

1. **Login Page:** Soft white background with blurred indigo/violet/teal gradient depth, email/password login, and a 1-click **Guest / Demo Login** button for judges.
2. **Dashboard:** Personalized greeting, "Hero Next Meeting" card with `✨ Prepare Me` CTA, and relationship stats (Active Contacts, Retained Memory Units, Open Commitments, Overdue Promises).
3. **Prepare Me Workflow (Centerpiece Agent Pipeline):** Visible step-by-step 3-stage animated agent execution:
   - **1. Hindsight Recall:** Querying multi-strategy memory index (semantic + keyword + entity graph + temporal filtering).
   - **2. Hindsight Reflect:** Synthesizing relationship trajectory, changed decisions (e.g. shifts in auth architecture), and overdue promises.
   - **3. Build Briefing:** Groq LLM turning Hindsight reflection into a structured brief.
4. **Memory ON vs Memory OFF Toggle Switch:** Re-runs meeting prep grounded in Hindsight memory vs a generic ungrounded LLM call, visually highlighting the dramatic before/after contrast.
5. **"Why?" Evidence Drill-Down:** Grounded follow-up query box under briefings (e.g., *"Why are you saying the documentation is overdue?"*) that re-queries Hindsight memory banks and cites exact historical memories with dates rather than re-generated guesses.
6. **Memory Graph Explorer:** Visual graph view (Contact at center, branching to Meetings, Decisions, and Deliverables nodes).
7. **Relationship Timeline:** Vertical date-based chronological stream of all retained memories about a contact.
8. **Commitment Tracker:** Cross-contact table of open/overdue promises, sortable and filterable by status.
9. **Preference Learning & Steering:** Settings panel allowing users to set custom instructions (e.g. *"keep briefs short, focus on unresolved items"*), stored as durable Hindsight steering missions (`aset_mission`).

---

## 🏗️ Architecture & Tech Stack

```
memora/
├── backend/
│   ├── main.py                  # FastAPI REST API endpoints
│   ├── agents/                  # Autonomous Meeting, Memory & Briefing Agents
│   │   ├── meeting_agent.py
│   │   ├── memory_agent.py
│   │   └── briefing_agent.py
│   ├── hindsight/               # Hindsight Cloud & Fallback Client (Retain, Recall, Reflect)
│   │   ├── client.py
│   │   ├── retain.py
│   │   ├── recall.py
│   │   └── reflect.py
│   ├── models/                  # Pydantic schemas (Contact, Meeting, Briefing, Memory)
│   └── services/                # Meeting and briefing data services
├── demo/                        # Seed data (Rahul Sharma 3-interaction timeline & seed script)
│   ├── contacts.json
│   ├── meetings.json
│   └── seed_memory.py
├── frontend/                    # Vite + React + Tailwind CSS + Framer Motion dashboard
│   └── src/
│       ├── components/          # PipelineAnimation, BriefingView, WhyDrilldown, MemoryExplorer, etc.
│       └── pages/               # LoginPage, DashboardPage, PreparePage
├── .env
└── README.md
```

### Technology Highlights
- **Memory Layer:** Hindsight (by Vectorize) — `aretain`, `arecall`, `areflect`, `aset_mission`.
- **LLM:** Groq (`openai/gpt-oss-120b` with fallback to `qwen/qwen3-32b`).
- **Backend:** Python 3.14 + FastAPI + Pydantic + Uvicorn.
- **Frontend:** React 18 + Vite + Tailwind CSS + Framer Motion + Lucide Icons.

---

## 🚀 Quick Start & Setup

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_WORKSPACE_ID=memora-workspace
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install hindsight-client groq fastapi uvicorn pydantic python-dotenv requests httpx

# Seed demo memories into Hindsight
python demo/seed_memory.py

# Start FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🎬 Hackathon 60-Second Judge Demo Walkthrough

1. **Login:** Click **"Try the demo (One-Click Guest Login)"** on the login card.
2. **Dashboard:** Click **`✨ Prepare Me for Next Meeting`** on the hero card for **Rahul Sharma** (VP of Engineering @ Acme Cloud).
3. **Agent Pipeline:** Watch the 3-step live pipeline animate (**1. Recall → 2. Reflect → 3. Build Briefing**).
4. **Inspect Grounded Brief:**
   - **Objective:** Address overdue OpenAPI documentation and finalize API Key auth shift.
   - **Previous Discussion:** Sept 12 kickoff (OpenAPI promised for Sept 20), Sept 18 decision shift (OAuth2 → API Keys), Sept 22 Slack update (InfoSec audit delay).
   - **Commitments Table:** See 🔴 Overdue, 🟡 In Progress, ⚪ Open items.
5. **Memory ON vs Memory OFF Toggle:** Click the top toggle to **Memory OFF**. Observe how the brief changes to a generic, ungrounded LLM output. Toggle back to **Memory ON** to show the Hindsight relationship grounding.
6. **"Why?" Evidence Drill-Down:** Click the preset chip *"Why are you saying the documentation is overdue?"*. View exact retained memory citations with dates (Sept 12, Sept 22).
7. **Memory Explorer & Timeline:** Navigate tabs to view the node graph and vertical relationship stream.
