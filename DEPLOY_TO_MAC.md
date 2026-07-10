# Deploy Atlas to Your Mac

**Complete guide to get Atlas running on your Mac laptop from this GitHub repo**

---

## Step 1: Download from GitHub

### Option A: Direct Download (Easiest)

1. Go to: https://github.com/nlevarun/atlas
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract to your Mac
5. Rename folder to `atlas` if needed
6. Move to home directory: `~/atlas`

### Option B: Git Clone (If you have git)

```bash
cd ~
git clone https://github.com/nlevarun/atlas.git
cd atlas
```

---

## Step 2: Install Prerequisites

### Install Homebrew (Mac Package Manager)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. Takes ~5 minutes.

### Install Python 3.12

```bash
brew install python@3.12
python3.12 --version  # Should show: Python 3.12.x
```

### Install Node.js 20

```bash
brew install node@20
node --version   # Should show: v20.x.x
npm --version    # Should show: 10.x.x
```

### Install Docker Desktop

```bash
brew install --cask docker
```

Then:
1. Open Spotlight (Cmd+Space)
2. Type "Docker"
3. Open Docker Desktop
4. Wait for it to fully start (whale icon in menu bar should be calm)

Verify:
```bash
docker --version
docker compose version
```

---

## Step 3: Run Automated Setup

```bash
cd ~/atlas
chmod +x *.sh
./setup_mac.sh
```

This script will:
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies (~15 packages)
- ✅ Install all Node.js dependencies (~200 packages, this is normal)
- ✅ Make helper scripts executable
- ✅ Create .env file

Takes ~5 minutes depending on your internet speed.

---

## Step 4: Start Atlas

```bash
./start_all.sh
```

This will:
1. Start Docker services (Postgres, Redis, etc.)
2. Start backend API on port 8000
3. Start frontend on port 3000
4. Automatically open browser to http://localhost:3000

Wait ~30 seconds for everything to initialize.

---

## Step 5: Test!

You should see the Atlas search page.

1. Type: **Anthropic**
2. Click: **"Start Research"**
3. Watch: 4 agents execute in real-time
4. Result: ~15-20 evidence items in 5-10 seconds

**What you'll see:**
- 🤖 news_agent → 3 news articles
- 🤖 financial_agent → 3 financial metrics
- 🤖 hiring_agent → 5 job postings
- 🤖 github_agent → 3 repositories
- 📝 Synthesis → Professional narrative

---

## Step 6: (Optional) Add API Keys for Real Data

Atlas works perfectly with mock data (no setup needed!). But for real company intelligence:

```bash
cd ~/atlas
nano .env  # or use any text editor
```

Add your keys:

```bash
# Real news search (optional)
TAVILY_API_KEY=tvly-xxxxx

# Real LLM synthesis (optional)
OPENAI_API_KEY=sk-xxxxx

# Better GitHub rate limits (optional)
GITHUB_TOKEN=ghp_xxxxx

# SEC Edgar (no key needed, just add user agent)
SEC_EDGAR_USER_AGENT="YourName your@email.com"
```

Then restart backend:
```bash
./restart_backend.sh
```

### Where to Get API Keys

**Tavily**: https://tavily.com (1,000 free searches/month)
**OpenAI**: https://platform.openai.com (pay-as-you-go, ~$0.10/run)
**GitHub**: https://github.com/settings/tokens (free, 5,000/hour)

---

## Daily Use

### Start Atlas
```bash
cd ~/atlas
./start_all.sh
```

### Stop Atlas
```bash
./stop_all.sh
```

### Check Status
```bash
./status.sh
```

### View Logs
```bash
tail -f backend.log    # Backend
tail -f frontend.log   # Frontend
```

---

## Troubleshooting

### "Docker daemon not running"

**Solution:**
```bash
open -a Docker
# Wait 30 seconds
```

### "Port already in use"

**Solution:**
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### "Module not found" errors

**Solution:**
```bash
cd ~/atlas
source venv/bin/activate
cd apps/api
pip install -r requirements.txt
```

### Need fresh start?

**Solution:**
```bash
./reset_all.sh
```

This deletes all data and resets to clean state.

---

## What's Included

### Code (34 files)
- 14 Python files (backend)
- 10 TypeScript/React files (frontend)
- 10 Config files

### Documentation (9 files)
- README.md - Main overview
- README_MAC.md - Quick start
- MAC_SETUP.md - Detailed setup
- OPERATIONS_MANUAL.md - How to use
- USER_GUIDE.md - Research tips
- ARCHITECTURE.md - System design
- PHASE_0_COMPLETE.md - Phase 0 details
- PHASE_1_COMPLETE.md - Phase 1 details
- DEPLOY_TO_MAC.md - This file

### Helper Scripts (6 files)
- setup_mac.sh - One-time setup
- start_all.sh - Start everything
- stop_all.sh - Stop everything
- status.sh - Check status
- restart_backend.sh - Restart backend
- reset_all.sh - Fresh start

---

## File Structure

```
~/atlas/
├── apps/
│   ├── api/              # FastAPI backend
│   └── web/              # Next.js frontend
├── packages/
│   ├── schemas/          # Data models
│   ├── agents/           # 4 research agents
│   ├── orchestrator/     # Workflow
│   ├── synthesis/        # LLM synthesis
│   └── llm/              # LLM abstraction
├── infra/
│   ├── docker-compose.yml
│   └── postgres/init.sql
├── docs/
│   └── ARCHITECTURE.md
├── *.sh                  # Helper scripts
├── *.md                  # Documentation
└── .env.example          # Config template
```

---

## Next Steps

After Atlas is running:

1. **Read**: [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md) - Learn how to use it
2. **Read**: [USER_GUIDE.md](USER_GUIDE.md) - Research best practices
3. **Test**: Run research on 5-10 companies you know
4. **Customize**: Add API keys for real data
5. **Integrate**: Use for your actual work

---

## Performance on Mac

**M1/M2/M3 (Apple Silicon):**
- Excellent! Docker runs natively
- Fast startup (~10 seconds)
- Low resource usage (2-4GB RAM)
- Efficient battery usage

**Intel Mac:**
- Good! Docker runs smoothly
- Slightly slower startup (~15 seconds)
- Higher resource usage (4-6GB RAM)

Both work great!

---

## Cost Estimate

**Without API keys:** $0
- Uses realistic mock data
- Perfect for testing and evaluation
- Fully functional

**With API keys:** ~$0.25 per research run
- Tavily news: $0.05
- OpenAI synthesis: $0.10
- GitHub: Free
- SEC Edgar: Free
- **Total: ~$0.15-$0.25**

**Monthly for 100 companies:** ~$25

Compare to:
- Manual research: $100+ per company (2 hours @ $50/hr)
- Research platforms: $1,000-10,000/month
- **Atlas: $25/month** (100 companies)

---

## System Requirements

**Minimum:**
- macOS 12.0+ (Monterey)
- 8GB RAM
- 10GB free disk space
- Internet connection

**Recommended:**
- macOS 13.0+ (Ventura) or 14.0+ (Sonoma)
- 16GB RAM
- 20GB free disk space
- Fast internet

---

## Support

**Setup Issues:**
- See [MAC_SETUP.md](MAC_SETUP.md) troubleshooting section
- Check Docker is running: `docker ps`
- Verify ports are free: `lsof -ti:8000` and `lsof -ti:3000`

**Usage Questions:**
- See [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md)
- See [USER_GUIDE.md](USER_GUIDE.md)

**Technical Issues:**
- Check logs: `tail -f backend.log frontend.log`
- Restart: `./stop_all.sh && ./start_all.sh`
- Reset: `./reset_all.sh`

**GitHub:**
- https://github.com/nlevarun/atlas
- Open an issue for bugs or questions

---

## Success Checklist

- [ ] Prerequisites installed (Python, Node, Docker)
- [ ] Atlas downloaded and extracted to `~/atlas`
- [ ] Setup script completed (`./setup_mac.sh`)
- [ ] Docker Desktop running
- [ ] Atlas started (`./start_all.sh`)
- [ ] Browser opens to http://localhost:3000
- [ ] Search for "Anthropic" works
- [ ] 4 agents execute successfully
- [ ] Report displays with evidence

If all checked: **You're ready to research!** 🚀

---

**Welcome to Atlas!**

You now have a complete AI research system running on your Mac. Fast, reliable, evidence-backed company intelligence at your fingertips.

Happy researching! 📊
