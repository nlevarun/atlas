# Atlas - Complete Training Summary for Claude

**Purpose:** This document provides comprehensive context for training a new Claude instance to understand and work with the Atlas project.

---

## Project Overview

**Atlas** is an AI Operating System for Company Intelligence that operates **100% FREE**. It uses 4 specialized research agents to gather evidence-backed intelligence about companies, then synthesizes it into professional reports with citations.

**Key Achievement:** Rebuilt from paid APIs to 100% free operation using template-based synthesis + optional free tier APIs.

---

## Core Architecture

### 1. Evidence-First Philosophy
- **Every claim must have:** `source_url`, `retrieved_at`, verbatim `raw_excerpt`
- **No fabrication:** Unknown data = `null`, never invented
- **Citations:** Evidence IDs embedded in narrative bullets like `[abc12345]`

### 2. Agent System (Fan-Out/Fan-In)
4 specialized agents run **in parallel**:
- **NewsAgent** - Tavily API (free tier) or mock data
- **FinancialAgent** - SEC Edgar (always free) + mock data
- **HiringAgent** - Job posting analysis (mock data only)
- **GitHubAgent** - GitHub API (free) or mock data

**Orchestrator pattern:**
```
Start → Fan out to 4 agents (parallel) → Collect evidence → Synthesize → Done
```

### 3. Synthesis Engine (100% FREE)
**Default:** Template-based synthesis
- Uses intelligent pattern matching
- Extracts strategy, growth signals, risks from evidence
- No LLM API required
- Instant results
- Works offline

**Optional:** Groq free tier (Llama 3.1 70B)
- 15 requests/minute free
- 6,000 requests/day free
- Still $0.00 cost
- Better quality synthesis

### 4. Real-Time Streaming
- WebSocket connections for live updates
- Events: `agent_started`, `evidence_found`, `agent_completed`, `synthesis_completed`
- Frontend shows live agent feed as research happens

### 5. Tech Stack
**Backend:**
- Python 3.12 + FastAPI
- Pydantic schemas at all boundaries
- Template-based synthesis (no paid LLM)
- Optional Groq adapter (free tier)

**Frontend:**
- Next.js 14 + React 18
- WebSocket client for real-time updates
- Tailwind CSS

**Infrastructure:**
- Docker Compose: Postgres, Neo4j, Qdrant, Redis, Temporal
- All run locally on Mac
- Python venv for isolation

---

## Critical Technical Decisions

### 1. Removed All Paid APIs
**Before:** OpenAI GPT-4, Anthropic Claude (cost: $0.08-$0.10/run)
**After:** Template-based synthesis (cost: $0.00)
**Rationale:** User explicitly requested: "i dont want to pay for any keys. free tiers are fine. open ai synthesis / anthropic i dont want. i want a free option."

### 2. Template-Based Synthesis Implementation
Located in: `packages/synthesis/synthesizer.py`

**How it works:**
- Groups evidence by type (news, sec_filing, github, job_posting)
- Pattern matching on claim text:
  - "partnership" → Strategic partnerships narrative
  - "launch" / "product" → Product development narrative
  - "funding" / "raised" → Capital strategy narrative
  - "expansion" → Market expansion narrative
- Generates 3 narrative sections:
  - **Current Strategy** - From news, financials, GitHub activity
  - **Growth Signals** - From hiring, revenue growth, product launches
  - **Risks & Challenges** - Inferred from growth signals (scaling risk, competition, execution)
- Each bullet references evidence IDs: `[abc12345]`

**Quality:** Good enough for structured company research. More formulaic than LLM, but instant and free.

### 3. Groq as Optional Upgrade
Located in: `packages/llm/groq_adapter.py`

**Why Groq:**
- FREE tier: 6,000 requests/day
- Fastest LLM inference in the world
- OpenAI-compatible API
- Llama 3.1 70B model (high quality)

**Integration:**
```python
use_groq = os.getenv("USE_GROQ_SYNTHESIS", "false").lower() == "true"
self.synthesizer = EvidenceSynthesizer(use_groq=use_groq)
```

Set `USE_GROQ_SYNTHESIS=true` in `.env` to enable.

### 4. Mock Data Fallbacks
Every agent has realistic mock data:
- **NewsAgent:** Fake press releases with realistic dates, URLs
- **FinancialAgent:** Fake SEC filings with revenue, funding data
- **HiringAgent:** Fake job postings (engineering, sales, etc.)
- **GitHubAgent:** Fake repository stats (stars, forks, commits)

**Why:** System works 100% without any API keys. Great for:
- Testing the system
- Demos
- Offline work
- Privacy (no external API calls)

### 5. Mac-Only Deployment
**Before:** Had Windows .bat files, Windows-specific paths
**After:** Removed all Windows files, Mac-only

**User feedback:** "that device is mac so if you can build this tailored to that, it would be great"

**Scripts created:**
- `setup_mac.sh` - One-time setup (venv, dependencies, .env)
- `start_all.sh` - Start all services (Docker, backend, frontend)
- `stop_all.sh` - Stop everything gracefully
- `status.sh` - Check service health
- `restart_backend.sh` - Restart just backend (fast iteration)
- `reset_all.sh` - Delete all data, fresh start

All scripts are executable (`chmod +x *.sh`).

---

## Repository Structure

```
atlas/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py             # Entry point
│   │   ├── routers/
│   │   │   ├── research.py     # Research endpoints
│   │   │   └── websocket.py    # WebSocket handler
│   │   └── requirements.txt    # Python dependencies
│   │
│   └── web/                    # Next.js frontend
│       ├── src/
│       │   ├── app/
│       │   │   ├── page.tsx              # Search page
│       │   │   └── dossier/[runId]/      # Report page
│       │   └── components/
│       │       └── AgentFeed.tsx         # Live agent feed
│       └── package.json
│
├── packages/
│   ├── schemas/                # Pydantic models
│   │   ├── evidence.py         # Evidence, AgentReport
│   │   └── company.py          # CompanyProfile, NarrativeSection
│   │
│   ├── agents/                 # Agent implementations
│   │   ├── base.py             # BaseAgent abstract class
│   │   ├── dummy.py            # Phase 0 dummy (for testing)
│   │   ├── news_agent.py       # NewsAgent (Tavily + mock)
│   │   ├── financial_agent.py  # FinancialAgent (SEC + mock)
│   │   ├── hiring_agent.py     # HiringAgent (mock only)
│   │   └── github_agent.py     # GitHubAgent (GitHub API + mock)
│   │
│   ├── orchestrator/           # Fan-out/fan-in orchestration
│   │   ├── graph.py            # ResearchOrchestrator
│   │   └── state.py            # ResearchState
│   │
│   ├── synthesis/              # Evidence → narrative
│   │   └── synthesizer.py      # EvidenceSynthesizer (template-based)
│   │
│   └── llm/                    # LLM abstraction
│       ├── provider.py         # LLMProvider interface
│       ├── groq_adapter.py     # Groq free tier adapter
│       └── cache.py            # Redis cache layer
│
├── infra/
│   ├── docker-compose.yml      # All services
│   └── postgres/
│       └── init.sql            # Database schema
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PHASE_0_COMPLETE.md
│   └── PHASE_1_COMPLETE.md
│
├── setup_mac.sh                # One-time setup
├── start_all.sh                # Start everything
├── stop_all.sh                 # Stop everything
├── status.sh                   # Check health
├── restart_backend.sh          # Restart backend
├── reset_all.sh                # Fresh start
│
├── .env.example                # Environment template (all free)
├── README.md                   # Main docs (emphasizes FREE)
├── README_MAC.md               # Mac quick start
├── FREE_TIER_GUIDE.md          # Complete free tier guide
├── MAC_SETUP.md                # Detailed Mac setup
├── OPERATIONS_MANUAL.md        # Daily usage
├── USER_GUIDE.md               # Research best practices
├── DEPLOYMENT_CHECKLIST.md     # Pre-deployment verification
└── CLAUDE_TRAINING_SUMMARY.md  # This file
```

**Total:** ~67 files, zero Windows files, 100% Mac-compatible.

---

## Key Code Patterns

### 1. Evidence Schema
```python
class Evidence(BaseModel):
    id: str                      # UUID
    agent: str                   # e.g. "news_agent"
    claim: str                   # Atomic fact, one sentence
    source_url: HttpUrl | None
    source_type: Literal["sec_filing", "news", "github", "job_posting", ...]
    retrieved_at: datetime
    confidence: float            # 0.0-1.0
    raw_excerpt: str             # Verbatim snippet
```

### 2. Agent Pattern
```python
class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """Execute research and return report with evidence."""
        pass
```

All agents inherit from `BaseAgent` and return `AgentReport` with list of `Evidence`.

### 3. Orchestrator Flow
```python
async def execute(self, state: ResearchState) -> ResearchState:
    # Start node
    state = await self._start_node(state)

    # Run agents node (fan-out, parallel)
    state = await self._run_agents_node(state)

    # Synthesize node (fan-in)
    state = await self._synthesize_node(state)

    return state
```

### 4. Template Synthesis Pattern
```python
def _extract_strategy_from_news(self, company_name: str, evidence: Evidence) -> str:
    claim = evidence.claim.lower()

    if "partnership" in claim:
        return f"{company_name} is pursuing strategic partnerships..."
    elif "launch" in claim:
        return f"{company_name} is actively developing and launching..."
    # ... more patterns
```

### 5. WebSocket Streaming
```python
# Backend broadcasts events
await self._broadcast_event(run_id, {
    "type": "evidence_found",
    "agent": agent_name,
    "claim": evidence.claim,
    "confidence": evidence.confidence
})

# Frontend listens
ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    setEvents(prev => [...prev, data])
}
```

---

## Free Tier Configuration

### .env.example Structure
```bash
# ALL KEYS ARE OPTIONAL - Atlas works 100% FREE without any keys!

# Groq (FREE tier: 15 req/min, 6000/day)
GROQ_API_KEY=
USE_GROQ_SYNTHESIS=false

# Tavily (FREE tier: 1,000 searches/month)
TAVILY_API_KEY=

# GitHub (FREE: 5000 requests/hour)
GITHUB_TOKEN=

# SEC Edgar (FREE, no key needed)
SEC_EDGAR_USER_AGENT=YourName your@email.com

# Infrastructure (Docker defaults)
DATABASE_URL=postgresql://atlas:atlas_dev@localhost:5432/atlas
NEO4J_URI=bolt://localhost:7687
# ... etc
```

**Default behavior:** Works with zero configuration. Just `./start_all.sh`.

---

## Cost Analysis

### Default (No API Keys)
| Component | Cost |
|-----------|------|
| Synthesis | $0.00 (templates) |
| News | $0.00 (mock) |
| Financial | $0.00 (SEC + mock) |
| Hiring | $0.00 (mock) |
| GitHub | $0.00 (mock) |
| **Total/month** | **$0.00** |

### With Free Tiers
| Component | Cost |
|-----------|------|
| Synthesis | $0.00 (Groq free) |
| News | $0.00 (Tavily 1000/mo) |
| Financial | $0.00 (SEC free) |
| Hiring | $0.00 (mock) |
| GitHub | $0.00 (GitHub API) |
| **Total/month** | **$0.00** |

**Savings:** $25-300/month vs paid alternatives (OpenAI, paid search APIs, etc.)

---

## Operational Workflows

### First-Time Setup on Mac
```bash
# 1. Prerequisites (5 min)
brew install python@3.12 node@20
brew install --cask docker
open -a Docker

# 2. Setup Atlas (5 min)
cd ~/atlas
chmod +x *.sh
./setup_mac.sh

# 3. Start (30 sec)
./start_all.sh
# Opens http://localhost:3000
```

### Daily Usage
```bash
# Start work
./start_all.sh

# Check status
./status.sh

# Restart backend (after code changes)
./restart_backend.sh

# Stop everything
./stop_all.sh

# Fresh start (delete all data)
./reset_all.sh
```

### Research Workflow
1. Open http://localhost:3000
2. Enter company name (e.g. "Anthropic")
3. Wait 5-10 seconds
4. See:
   - Live agent feed (4 agents working in parallel)
   - Evidence items appearing in real-time
   - Final synthesized report with citations
5. Cost: $0.00

---

## Common Issues & Solutions

### Issue: Docker not running
**Solution:** `open -a Docker` then wait 30 seconds

### Issue: Port 8000 or 3000 already in use
**Solution:** `./stop_all.sh` then `./start_all.sh`

### Issue: Backend crashes
**Solution:**
```bash
cd ~/atlas
source venv/bin/activate
cd apps/api
uvicorn main:app --reload
# Check logs for errors
```

### Issue: Frontend not connecting to backend
**Solution:** Check `.env` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### Issue: Groq synthesis not working
**Solution:**
1. Check `GROQ_API_KEY` in `.env`
2. Check `USE_GROQ_SYNTHESIS=true` in `.env`
3. Run `./restart_backend.sh`
4. Falls back to template synthesis on error (still works)

---

## Development Patterns

### Adding a New Agent
1. Create `packages/agents/my_agent.py`
2. Inherit from `BaseAgent`
3. Implement `async def execute(self, company_id: str, run_id: str) -> AgentReport`
4. Return `AgentReport` with list of `Evidence`
5. Add mock data fallback
6. Register in `packages/orchestrator/graph.py`:
   ```python
   self.agents = [
       NewsAgent(),
       FinancialAgent(),
       HiringAgent(),
       GitHubAgent(),
       MyAgent(),  # <-- Add here
   ]
   ```

### Modifying Synthesis
1. Edit `packages/synthesis/synthesizer.py`
2. Update template patterns in `_extract_strategy_from_*()` methods
3. Test: `./restart_backend.sh` then search a company
4. No API calls, instant feedback

### Adding WebSocket Events
1. Backend: Add event in `packages/orchestrator/graph.py`
   ```python
   await self._broadcast_event(run_id, {
       "type": "my_custom_event",
       "data": {...}
   })
   ```
2. Frontend: Handle in `apps/web/src/app/dossier/[runId]/page.tsx`
   ```typescript
   ws.onmessage = (event) => {
       const data = JSON.parse(event.data)
       if (data.type === "my_custom_event") {
           // Handle it
       }
   }
   ```

---

## Documentation Hierarchy

**Quick Start:**
1. `README.md` - Overview, emphasizes FREE
2. `README_MAC.md` - Mac quick start (5 min setup)

**Setup:**
3. `MAC_SETUP.md` - Detailed installation steps
4. `FREE_TIER_GUIDE.md` - All free tier options explained
5. `DEPLOYMENT_CHECKLIST.md` - Pre-deployment verification

**Operations:**
6. `OPERATIONS_MANUAL.md` - Daily usage, commands, troubleshooting
7. `USER_GUIDE.md` - Research best practices, interpreting reports

**Architecture:**
8. `docs/ARCHITECTURE.md` - System design, technical decisions
9. `docs/PHASE_0_COMPLETE.md` - Phase 0 implementation details
10. `docs/PHASE_1_COMPLETE.md` - Phase 1 (real agents) details

**Training:**
11. `CLAUDE_TRAINING_SUMMARY.md` - This file (complete context)

---

## User's Journey (Chronological)

### Initial Request
User provided comprehensive plan to build Atlas from scratch with full autonomy. Requested Phase 0 (scaffold) and Phase 1 (real agents).

### Pivot 1: Windows → Mac
**User feedback:** "that device is mac so if you can build this tailored to that, it would be great"
**Action:** Removed all Windows files (.bat, Windows paths), kept only Mac scripts (.sh)

### Pivot 2: Clean Repository
**User feedback:** "get rid of every addl file that contributes nothing"
**Action:** Consolidated docs, removed unnecessary files, kept only essentials

### Pivot 3: 100% FREE
**User feedback:** "i dont want to pay for any keys. free tiers are fine. open ai synthesis / anthropic i dont want. i want a free option."
**Action:**
- Completely rewrote synthesis engine to use templates
- Removed OpenAI and Anthropic dependencies
- Added Groq as optional free tier
- Updated all documentation to emphasize FREE
- Result: $0.00/month, works without any API keys

### Final State
- 100% FREE operation (with or without API keys)
- Mac-only deployment
- Clean repository structure
- Comprehensive documentation
- Ready for GitHub commit and Mac deployment

---

## Critical Files to Understand

### 1. `packages/synthesis/synthesizer.py`
**Why:** Core of the FREE operation. Template-based synthesis logic.
**Key methods:**
- `_generate_strategy_section()` - Extracts strategy from evidence
- `_generate_growth_section()` - Identifies growth signals
- `_generate_risks_section()` - Infers risks
- `_extract_strategy_from_news()` - Pattern matching on news
- `_extract_strategy_from_financials()` - Pattern matching on financials

### 2. `packages/orchestrator/graph.py`
**Why:** Orchestrates the entire research workflow
**Key flow:**
- Start node → broadcast start event
- Run agents node → fan out to 4 agents in parallel
- Collect evidence → broadcast evidence events
- Synthesize node → call EvidenceSynthesizer
- Broadcast completion

### 3. `packages/agents/base.py` + agent implementations
**Why:** Defines agent contract
**Pattern:** All agents inherit from `BaseAgent`, implement `execute()`, return `AgentReport`

### 4. `.env.example`
**Why:** Shows ALL configuration options (all optional, all free)
**Key:** Emphasizes "ALL KEYS ARE OPTIONAL"

### 5. `setup_mac.sh`
**Why:** Automates entire Mac setup
**Flow:**
- Check prerequisites (Python, Node, Docker)
- Create Python venv
- Install backend dependencies
- Install frontend dependencies
- Copy .env.example to .env
- Done in 5 minutes

### 6. `start_all.sh`
**Why:** One command to start everything
**Flow:**
- Start Docker Compose (Postgres, Neo4j, etc.)
- Wait for services to be ready
- Activate venv
- Start FastAPI backend
- Start Next.js frontend
- Open browser

---

## Testing & Verification

### Manual Testing
```bash
# 1. Start system
./start_all.sh

# 2. Check services
./status.sh

# 3. Test backend health
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# 4. Test research endpoint
curl -X POST http://localhost:8000/api/research/company \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Anthropic"}'
# Expected: {"run_id":"<uuid>","status":"started"}

# 5. Open frontend
# http://localhost:3000
# Search: "Anthropic"
# Expected: Live agent feed, evidence items, report in 5-10 seconds
```

### Expected Output
- 4 agents execute in parallel (NewsAgent, FinancialAgent, HiringAgent, GitHubAgent)
- 15-20 evidence items collected
- Template-based synthesis generates 3 sections:
  - Current Strategy (2-4 bullets)
  - Growth Signals (2-4 bullets)
  - Risks & Challenges (2-3 bullets)
- Each bullet references evidence IDs
- Total time: 5-10 seconds
- Cost: $0.00

---

## Future Enhancements (Not Yet Implemented)

### Phase 2: Persistence
- Save research runs to Postgres
- Query historical research
- Deduplicate evidence

### Phase 3: Multi-Agent Debate
- Agents debate findings
- Resolve conflicting evidence
- Improve synthesis quality

### Phase 4: Time-Series Analysis
- Track company changes over time
- Trend detection
- Prediction signals

### Phase 5: Knowledge Graph
- Neo4j for relationship mapping
- Company connections
- Market ecosystem visualization

### Phase 6: Evaluation Harness
- Automated testing of agent quality
- Benchmark against ground truth
- Cost/quality tradeoffs

**Current status:** Phase 0 + Phase 1 complete, 100% FREE operation proven.

---

## Key Insights for Claude

### 1. Always Prioritize Free Options
User explicitly rejected paid APIs. When suggesting improvements, always consider:
- Is there a free tier? (Groq, Tavily, GitHub)
- Can we use templates/patterns? (synthesis)
- Can we use mock data? (all agents)
- Is free good enough? (usually yes for personal research)

### 2. Mac-First Development
User is deploying on Mac. Always:
- Use `.sh` scripts, not `.bat`
- Test paths like `~/atlas`, not `C:\Users\...`
- Use `brew` for installation
- Use `open -a Docker` not Windows commands

### 3. Evidence-Backed Everything
Never suggest features that fabricate data. Always:
- Include `source_url` in Evidence
- Use `null` for unknown data
- Add `retrieved_at` timestamp
- Embed evidence IDs in narrative: `[abc12345]`

### 4. Template Synthesis Is Acceptable
User accepted template-based synthesis. It's:
- Good enough for structured research
- Instant (no API latency)
- Free forever
- Privacy-friendly (no external calls)
Don't push for LLM unless user asks.

### 5. Real-Time Streaming Matters
User cares about seeing agents work live. Always:
- Use WebSocket for long-running tasks
- Broadcast granular events (agent_started, evidence_found)
- Show progress, not just final result

### 6. Operational Excellence
User needs to easily operate the system. Always:
- Provide shell scripts for common tasks
- Document troubleshooting steps
- Make setup automated (./setup_mac.sh)
- Include status checking (./status.sh)

---

## Commands Reference

### Setup (One-Time)
```bash
chmod +x *.sh          # Make scripts executable
./setup_mac.sh         # Automated setup
```

### Daily Operations
```bash
./start_all.sh         # Start everything
./stop_all.sh          # Stop everything
./status.sh            # Check health
./restart_backend.sh   # Quick backend restart
./reset_all.sh         # Fresh start (delete data)
```

### Manual Operations
```bash
# Start Docker only
cd ~/atlas/infra && docker-compose up -d

# Start backend only
cd ~/atlas
source venv/bin/activate
cd apps/api
uvicorn main:app --reload

# Start frontend only
cd ~/atlas/apps/web
npm run dev

# Check Docker services
docker ps

# View backend logs
cd ~/atlas/apps/api
# (logs appear in terminal when running uvicorn)

# View Docker logs
docker-compose -f ~/atlas/infra/docker-compose.yml logs -f postgres
```

---

## Summary

**Atlas** is a 100% FREE AI Operating System for company intelligence that:
- Uses 4 specialized agents (News, Financial, Hiring, GitHub)
- Runs agents in parallel for speed
- Uses template-based synthesis (no paid LLM)
- Optionally supports Groq free tier (6000/day free)
- Streams results in real-time via WebSocket
- Deploys on Mac with 5-minute setup
- Costs $0.00/month forever (with or without API keys)

**Key technical achievement:** Rebuilt from paid OpenAI/Anthropic APIs to intelligent template-based synthesis, achieving 100% free operation while maintaining good quality for structured company research.

**Current status:** Phase 0 + Phase 1 complete. Ready for GitHub commit and Mac deployment.

**User's explicit requirements met:**
✅ 100% FREE operation (no paid APIs)
✅ Mac-only deployment (no Windows files)
✅ Clean repository structure
✅ Comprehensive documentation
✅ Operational scripts for daily use
✅ Easy transfer to new laptop

---

## Training Your Personal Claude

When training a new Claude instance on this project, provide:

1. **This file** - Complete context and patterns
2. **Key files to read:**
   - `README.md` - Project overview
   - `FREE_TIER_GUIDE.md` - Free tier strategy
   - `packages/synthesis/synthesizer.py` - Core synthesis logic
   - `packages/orchestrator/graph.py` - Orchestration pattern
   - `.env.example` - Configuration options

3. **User preferences to remember:**
   - "No paid APIs" - Always suggest free alternatives
   - "Mac deployment" - No Windows files or commands
   - "Evidence-backed" - Never fabricate data
   - "Template synthesis is acceptable" - Don't push LLM unnecessarily
   - "Clean repository" - Remove files that contribute nothing

4. **Key commands:**
   - `./setup_mac.sh` - First-time setup
   - `./start_all.sh` - Daily start
   - `./status.sh` - Health check
   - `./restart_backend.sh` - Quick iteration

5. **Architecture patterns:**
   - Evidence-first (source URL, timestamp, excerpt)
   - Fan-out/fan-in (parallel agents)
   - Template-based synthesis (no LLM)
   - WebSocket streaming (real-time)
   - Mock data fallbacks (works offline)

With this context, Claude can:
- Understand the full architecture
- Make changes consistent with user preferences
- Debug issues using documented patterns
- Add features following established conventions
- Maintain the 100% FREE operation principle

---

**End of Training Summary**

This document provides complete context for working with Atlas. Read it thoroughly before making any changes to the codebase.
