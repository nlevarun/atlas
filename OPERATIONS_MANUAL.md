# Atlas Operations Manual

**How to Actually Use Atlas - A Complete Guide**

---

## Table of Contents

1. [Starting Atlas](#starting-atlas)
2. [Running Research](#running-research)
3. [Understanding Results](#understanding-results)
4. [Advanced Features](#advanced-features)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Daily Operations](#daily-operations)

---

## Starting Atlas

### One-Command Start (Recommended)

```bash
cd ~/atlas
./start_all.sh
```

This starts:
- ✅ Docker infrastructure (Postgres, Redis, etc.)
- ✅ Backend API
- ✅ Frontend UI

Wait 30 seconds, then open: **http://localhost:3000**

### Manual Start (3 Terminals)

**Terminal 1:**
```bash
cd ~/atlas/infra
docker compose up -d
```

**Terminal 2:**
```bash
cd ~/atlas
source venv/bin/activate
cd apps/api
python main.py
```

**Terminal 3:**
```bash
cd ~/atlas/apps/web
npm run dev
```

### Verify It's Running

1. Backend: http://localhost:8000/health → Should show `{"status":"ok"}`
2. Frontend: http://localhost:3000 → Should show Atlas search page
3. Docker: `docker compose ps` → All services should be "Up (healthy)"

---

## Running Research

### Basic Company Research

1. **Open Atlas**: http://localhost:3000

2. **Enter Company Name**: Type in the search box
   - Examples: "Anthropic", "OpenAI", "Stripe", "Airbnb"
   - Works with: Full name, common name, or ticker symbol

3. **Click "Start Research"**

4. **Watch Live Progress**: You'll be redirected to the dossier page
   - Left side: Live agent feed (real-time updates)
   - Right side: Report (appears after synthesis)

5. **Wait 5-10 seconds**: Research completes automatically

6. **Review Report**: Scroll through evidence and narrative

### What Happens During Research

**Phase 1: Agent Execution (3-5 seconds)**
- News Agent searches recent articles
- Financial Agent queries SEC filings
- Hiring Agent analyzes job postings
- GitHub Agent checks repository activity

All agents run **in parallel** (simultaneously).

**Phase 2: Evidence Collection (0-1 second)**
- Each agent returns 3-5 evidence items
- Total: 15-20 pieces of evidence
- Each has: claim, source URL, confidence score, excerpt

**Phase 3: Synthesis (2-4 seconds)**
- LLM analyzes all evidence
- Generates narrative sections:
  - Current Strategy
  - Growth Signals
  - Risks & Challenges
- All claims cite evidence IDs

**Phase 4: Report Display (instant)**
- Professional report renders
- Evidence cards show sources
- Can click links to verify

---

## Understanding Results

### Agent Feed (Left Side)

Real-time event stream showing:

**🚀 run_started**
- Research initiated
- Shows company name and run ID

**🤖 agent_started**
- Individual agent begins
- You'll see 4 of these (one per agent)

**🔍 evidence_found**
- New evidence discovered
- Shows claim and confidence
- You'll see 15-20 of these

**✅ agent_completed**
- Agent finished
- Shows evidence count
- You'll see 4 of these

**📝 synthesis_started**
- LLM is generating narrative

**✅ synthesis_completed**
- Narrative ready
- Shows section counts

**🎉 run_completed**
- Research done!
- Shows total evidence count

### Evidence Cards (Right Side)

Each evidence item shows:

**Claim**: Single factual sentence
- Example: "Anthropic raised $200M Series D at $2B valuation."

**Source Type**: Where it came from
- 📰 news - Recent news articles
- 💰 sec_filing - SEC financial filings
- 👥 job_posting - Job board postings
- 💻 github - Repository activity

**Confidence**: How reliable (0-100%)
- 90-100%: Very high confidence (SEC filings, official sources)
- 80-90%: High confidence (reputable news, verified data)
- 70-80%: Medium confidence (job postings, GitHub stats)

**Source Link**: Click to verify
- Opens original source in new tab
- Always verify important claims!

**Excerpt**: Verbatim text from source
- Proof the claim is real
- Context for the claim

### Narrative Sections

**Current Strategy**
- Business positioning
- Key initiatives
- Market approach
- Strategic partnerships

**Growth Signals**
- Revenue growth
- Team expansion
- Product launches
- Market expansion
- Funding rounds

**Risks & Challenges**
- Competitive threats
- Market dynamics
- Operational challenges
- Dependencies

Each bullet point **references evidence IDs** in brackets: [evi_abc123]

---

## Advanced Features

### Phase 0 vs Phase 1

**Switch Modes:**

```bash
# Use Phase 1 (real agents, 15-20 evidence)
export USE_REAL_AGENTS=true
./start_backend.sh

# Use Phase 0 (dummy agent, 3 evidence, faster testing)
export USE_REAL_AGENTS=false
./start_backend.sh
```

Phase 0 is useful for:
- Testing the system
- Demos without API costs
- Development/debugging

Phase 1 is for:
- Real research
- Production use
- Actual company intelligence

### With vs Without API Keys

**Without API Keys (Default)**
- Uses realistic mock data
- Instant results (no API latency)
- Zero cost
- Good for testing and evaluation

**With API Keys**
- Real news from Tavily
- Real SEC filings from Edgar
- Real LLM synthesis from GPT-4/Claude
- Real GitHub data
- Cost: ~$0.25 per research run

To add keys, edit `~/atlas/.env`:
```bash
TAVILY_API_KEY=tvly-xxxxx
OPENAI_API_KEY=sk-xxxxx
GITHUB_TOKEN=ghp-xxxxx
```

Then restart backend.

### Checking Run History

**View All Runs:**
```bash
curl http://localhost:8000/api/research/runs
```

Returns JSON list of all research runs with:
- run_id
- company_name
- status
- started_at
- agent_count
- evidence_count

**Get Specific Run:**
```bash
curl http://localhost:8000/api/research/{run_id}/report
```

Returns complete report with all evidence.

**Via Frontend:**
- Open http://localhost:3000
- Click browser back button to see previous searches
- Bookmark dossier URLs to return later

---

## Best Practices

### Research Tips

**1. Use Specific Company Names**
- ✅ Good: "Anthropic", "OpenAI", "Stripe"
- ❌ Bad: "AI company", "payment startup"

**2. Try Ticker Symbols for Public Companies**
- ✅ "TSLA" (Tesla)
- ✅ "MSFT" (Microsoft)
- Works better for financial data

**3. Verify Important Claims**
- Click source links
- Read original articles
- Check multiple evidence items
- Look at confidence scores

**4. Compare Multiple Runs**
- Research evolves over time
- Run weekly/monthly for updates
- Compare evidence changes
- Track trend shifts

**5. Focus on High-Confidence Evidence**
- 90-100% confidence: Very reliable
- SEC filings are always 95%
- News from major outlets: 90-95%
- Job postings: 85-90%

### When to Run Research

**Initial Research:**
- New investment opportunity
- Competitive analysis
- Due diligence starting point
- Market mapping

**Regular Updates:**
- Weekly: Fast-moving startups
- Monthly: Established companies
- Quarterly: Slow-moving industries
- Before: Meetings, pitches, decisions

**Trigger Events:**
- Funding announcements
- Product launches
- Leadership changes
- Earnings reports
- News events

### Organizing Research

**Naming Convention:**
```
{company}_{date}_{run_id_short}
Example: anthropic_2026-07-09_abc123
```

**Create Research Log:**
```
Research_Log.md

## Anthropic
- 2026-07-09 (abc123): Initial research
  - Key finding: Series D $200M
  - Status: Growing rapidly
- 2026-08-01 (def456): Follow-up
  - New finding: Launched Claude 3.5
  - Status: Product momentum
```

---

## Troubleshooting During Operations

### Research Stuck

**Symptom:** Agent feed shows agents started but no evidence

**Solutions:**
1. Wait 30 seconds (APIs can be slow)
2. Check backend terminal for errors
3. Restart backend if frozen
4. Switch to Phase 0 to verify system works

### No Results Found

**Symptom:** Agents complete but 0 evidence

**Possible Causes:**
- Company name too generic
- Company too small/new (no public data)
- Typo in company name
- API rate limits hit

**Solutions:**
- Try alternative company name
- Add ticker symbol if public
- Try well-known company to test
- Check if API keys expired

### WebSocket Disconnected

**Symptom:** Live feed stops updating

**Solutions:**
1. Refresh browser page
2. Check backend is still running
3. Verify no proxy/firewall blocking WebSocket
4. Restart backend

### Slow Performance

**Symptom:** Taking >30 seconds

**Possible Causes:**
- API rate limits
- Network latency
- Insufficient Docker resources
- Too many concurrent requests

**Solutions:**
1. Check Docker resources (Settings → Resources)
2. Allocate more RAM to Docker (8-12 GB)
3. Run one research at a time
4. Use Phase 0 for testing (faster)

---

## Daily Operations

### Morning Startup Routine

```bash
# 1. Start Atlas
cd ~/atlas
./start_all.sh

# 2. Verify health
curl http://localhost:8000/health

# 3. Open frontend
open http://localhost:3000

# 4. Ready to research!
```

### During the Day

**Research Workflow:**
1. Enter company name
2. Start research
3. Review evidence while it runs
4. Export/copy important findings
5. Verify claims by clicking sources
6. Repeat for next company

**Tips:**
- Keep Atlas running all day
- No need to restart between searches
- Can run multiple searches (one at a time)
- Frontend handles all state

### End of Day Shutdown

```bash
# Stop all services
cd ~/atlas
./stop_all.sh

# Or keep running overnight (uses minimal resources)
```

**Docker uses ~2GB RAM when idle** - safe to keep running.

---

## Monitoring Operations

### Check System Health

```bash
# Backend health
curl http://localhost:8000/health

# Docker services
cd ~/atlas/infra
docker compose ps

# All should show "Up (healthy)"
```

### View Service Logs

```bash
# Backend logs (what agents are doing)
# Visible in Terminal 2

# Frontend logs (UI events)
# Visible in Terminal 3

# Docker logs (infrastructure)
cd ~/atlas/infra
docker compose logs -f postgres  # Database
docker compose logs -f redis     # Cache
```

### Resource Usage

```bash
# Docker stats (live)
docker stats

# Shows CPU, memory, network for each service
```

---

## Cost Tracking (With Real APIs)

### Per Research Run

**With API Keys:**
- Tavily news search: $0.05 (5 queries)
- OpenAI GPT-4 synthesis: $0.10 (3 calls)
- GitHub API: Free
- SEC Edgar: Free
- **Total: ~$0.15-$0.25 per run**

**Without API Keys:**
- Everything: $0.00
- Uses realistic mock data

### Monthly Budget

**Light Use (10 runs/month):**
- 10 × $0.25 = $2.50/month

**Medium Use (50 runs/month):**
- 50 × $0.25 = $12.50/month

**Heavy Use (200 runs/month):**
- 200 × $0.25 = $50/month

**Compare to:**
- Manual research: 2 hours × $50/hr = $100 per company
- Research platforms: $1,000-10,000/month
- Atlas: $2.50-50/month

**Atlas is 20-400x cheaper than alternatives.**

---

## Keyboard Shortcuts

### In Browser

- `Cmd+L` - Focus search box
- `Cmd+R` - Refresh page (reload report)
- `Cmd+T` - New tab (keep dossier open)
- `Cmd+Click` - Open source link in new tab

### In Terminal

- `Ctrl+C` - Stop backend/frontend
- `Cmd+T` - New terminal tab
- `Cmd+K` - Clear terminal
- `up arrow` - Previous command

---

## Exporting Results

### Copy Evidence (Manual)

1. Open dossier page
2. Select text from report
3. `Cmd+C` to copy
4. Paste into your notes/doc

### Screenshot Report

1. Open dossier page
2. `Cmd+Shift+3` - Full screen
3. `Cmd+Shift+4` - Selection
4. Image saved to Desktop

### API Export (Programmatic)

```bash
# Get report as JSON
curl http://localhost:8000/api/research/{run_id}/report > report.json

# Pretty print
curl http://localhost:8000/api/research/{run_id}/report | python -m json.tool
```

### Future: PDF Export (Phase 2)

Coming soon:
- One-click PDF generation
- Professional formatting
- Include all evidence
- Source citations

---

## Quick Command Reference

```bash
# Start everything
cd ~/atlas && ./start_all.sh

# Stop everything
./stop_all.sh

# Check status
./status.sh

# View logs
cd infra && docker compose logs -f

# Restart backend only
./restart_backend.sh

# Reset data (fresh start)
./reset_all.sh

# Test API
curl http://localhost:8000/health
```

---

## Next Steps

After mastering basic operations:

1. **[USER_GUIDE.md](USER_GUIDE.md)** - Research best practices
2. **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - How it works
3. **Add API keys** for real data
4. **Set up daily routine** for regular research
5. **Build research workflows** for your use case

---

## Support

**Operations Issues:**
- Check logs: `docker compose logs -f`
- Restart services: `./restart_all.sh`
- Read troubleshooting section above

**Usage Questions:**
- See [USER_GUIDE.md](USER_GUIDE.md)
- Check examples in this manual

**Technical Issues:**
- See [MAC_SETUP.md](MAC_SETUP.md)
- Check Docker resources
- Verify all services healthy

---

**You're now ready to operate Atlas like a pro!** 🚀

Research companies, gather intelligence, make informed decisions. Atlas handles the heavy lifting.

Happy researching! 📊
