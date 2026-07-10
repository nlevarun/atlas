# Atlas Setup for Mac

**Complete setup guide for macOS (tested on macOS Sonoma/Ventura)**

---

## System Requirements

- macOS 12.0 (Monterey) or later
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Admin access (no security restrictions)

---

## One-Time Setup (30 minutes)

### Step 1: Install Homebrew (5 min)

Homebrew is the Mac package manager. Open **Terminal** and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. When done, verify:

```bash
brew --version
```

### Step 2: Install Python 3.12 (5 min)

```bash
# Install Python 3.12
brew install python@3.12

# Verify
python3.12 --version
# Should show: Python 3.12.x

# Set as default python3 (optional)
brew link python@3.12
```

### Step 3: Install Node.js 20 (5 min)

```bash
# Install Node.js 20 LTS
brew install node@20

# Link it
brew link node@20

# Verify
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

### Step 4: Install Docker Desktop (10 min)

```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop
open -a Docker
```

**Wait for Docker Desktop to fully start** (whale icon in menu bar should be calm, not animated).

Verify in Terminal:

```bash
docker --version
docker compose version
```

### Step 5: Clone/Copy Atlas to Mac (5 min)

**Option A: USB Transfer**
1. Copy the entire `atlas` folder from your Windows machine
2. Place it in your Mac home directory: `~/atlas`

**Option B: Git (if using version control)**
```bash
cd ~
git clone <your-repo-url> atlas
```

**Option C: Direct Download**
If you've packaged it, just extract to `~/atlas`

---

## Automated Setup Script

I've created an automated setup script. Just run:

```bash
cd ~/atlas
chmod +x setup_mac.sh
./setup_mac.sh
```

This script will:
1. ✅ Create Python virtual environment
2. ✅ Install all Python dependencies
3. ✅ Install all Node.js dependencies
4. ✅ Verify all services
5. ✅ Create shortcuts

Takes ~5 minutes.

---

## Manual Setup (if you prefer)

### Step 1: Create Virtual Environment

```bash
cd ~/atlas

# Create venv
python3.12 -m venv venv

# Activate venv
source venv/bin/activate

# You should see (venv) in your prompt
```

### Step 2: Install Python Dependencies

```bash
cd apps/api
pip install --upgrade pip
pip install -r requirements.txt

# Should install ~15 packages
```

### Step 3: Install Node.js Dependencies

```bash
cd ../web
npm install

# Should install ~200 packages (this is normal for React/Next.js)
```

---

## Starting Atlas (Every Time)

### Quick Start (Recommended)

I've created helper scripts. Open **3 Terminal tabs/windows**:

**Terminal 1 - Infrastructure:**
```bash
cd ~/atlas
./start_infrastructure.sh
```

**Terminal 2 - Backend:**
```bash
cd ~/atlas
./start_backend.sh
```

**Terminal 3 - Frontend:**
```bash
cd ~/atlas
./start_frontend.sh
```

**Then open browser:** http://localhost:3000

### Manual Start

**Terminal 1 - Infrastructure:**
```bash
cd ~/atlas/infra
docker compose up -d

# Wait 30 seconds for services to initialize
docker compose ps  # Check all are "Up"
```

**Terminal 2 - Backend:**
```bash
cd ~/atlas
source venv/bin/activate
cd apps/api
python main.py
```

You should see:
```
🚀 Atlas Phase 1: Using real agents (News, Financial, Hiring, GitHub)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 3 - Frontend:**
```bash
cd ~/atlas/apps/web
npm run dev
```

You should see:
```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
✓ Ready in 2.3s
```

---

## Testing Atlas

### Basic Test (Phase 1)

1. Open Safari/Chrome: **http://localhost:3000**

2. You should see a clean search page with "Atlas" header

3. Type: **Anthropic**

4. Click **"Start Research"**

5. You'll be redirected to a report page

6. Watch the magic:
   - 4 agents start (news_agent, financial_agent, hiring_agent, github_agent)
   - Evidence appears in real-time
   - ~15-20 evidence items total
   - Synthesis creates narrative
   - Complete in ~5-10 seconds

### What You Should See

**Live Agent Feed (left side):**
- 🚀 run_started
- 🤖 agent_started (news_agent)
- 🤖 agent_started (financial_agent)
- 🤖 agent_started (hiring_agent)
- 🤖 agent_started (github_agent)
- 🔍 evidence_found (15-20 times)
- ✅ agent_completed (4 times)
- 📝 synthesis_started
- ✅ synthesis_completed
- 🎉 run_completed

**Report (right side):**
- Summary from each agent
- Evidence cards with sources
- Confidence scores
- Source links

### Test Different Companies

- **Anthropic** - AI startup, recent news
- **OpenAI** - Well-documented, lots of data
- **Stripe** - Private company, hiring signals
- **Airbnb** - Public company, SEC filings

---

## Stopping Atlas

### Stop Services

**Press `Ctrl+C`** in backend and frontend terminals

**Stop Docker:**
```bash
cd ~/atlas/infra
docker compose down
```

**Or use helper script:**
```bash
cd ~/atlas
./stop_all.sh
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## Adding API Keys (Optional)

Atlas works perfectly with **mock data** (no API keys needed). But for **real data**:

### Create .env file

```bash
cd ~/atlas
cp .env.example .env
nano .env  # or use any editor
```

### Add Your Keys

```bash
# Real news search (optional)
TAVILY_API_KEY=tvly-xxxxx

# Real LLM synthesis (optional)
OPENAI_API_KEY=sk-xxxxx

# Or use Claude instead
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Better GitHub rate limits (optional)
GITHUB_TOKEN=ghp_xxxxx

# SEC Edgar (required by SEC, no key needed)
SEC_EDGAR_USER_AGENT="YourName your@email.com"
```

### Get API Keys

**Tavily (News):**
- Sign up: https://tavily.com
- Free tier: 1,000 searches/month
- Cost: $0.05 per search after

**OpenAI (Synthesis):**
- Sign up: https://platform.openai.com
- Pay-as-you-go
- Cost: ~$0.10 per research run

**Anthropic (Alternative):**
- Sign up: https://console.anthropic.com
- Pay-as-you-go
- Cost: ~$0.08 per research run

**GitHub (Repository Data):**
- Generate token: https://github.com/settings/tokens
- Free tier: 5,000 requests/hour
- Select scopes: `public_repo`, `read:org`

### Restart Backend

After adding keys:
```bash
# Stop backend (Ctrl+C)
# Start again
cd ~/atlas
./start_backend.sh
```

Keys are now active!

---

## Mac-Specific Tips

### Use iTerm2 (Better Terminal)

```bash
brew install --cask iterm2
```

Split panes: `Cmd+D` (vertical), `Cmd+Shift+D` (horizontal)

### Create Desktop Shortcuts

**Option 1: Automator Quick Action**

1. Open Automator
2. New Document → Application
3. Add "Run Shell Script"
4. Paste:
```bash
cd ~/atlas && ./start_infrastructure.sh && ./start_backend.sh && ./start_frontend.sh && open http://localhost:3000
```
5. Save as "Start Atlas" to Applications

**Option 2: Alfred Workflow** (if you use Alfred)

Create workflow with keyword "atlas" that runs the start scripts.

### Add to PATH (Optional)

Add to `~/.zshrc`:

```bash
# Atlas shortcuts
alias atlas-start="cd ~/atlas && ./start_all.sh"
alias atlas-stop="cd ~/atlas && ./stop_all.sh"
alias atlas-logs="cd ~/atlas/infra && docker compose logs -f"
alias atlas-status="cd ~/atlas/infra && docker compose ps"
```

Then:
```bash
source ~/.zshrc
atlas-start  # Start everything!
```

---

## Troubleshooting

### "Cannot connect to Docker daemon"

**Solution:** Start Docker Desktop
```bash
open -a Docker
# Wait 30 seconds
```

### "Port already in use" (8000 or 3000)

**Solution:** Find and kill the process
```bash
# Find process on port 8000
lsof -ti:8000 | xargs kill -9

# Find process on port 3000
lsof -ti:3000 | xargs kill -9
```

### "Module not found" errors

**Solution:** Reinstall dependencies
```bash
cd ~/atlas
source venv/bin/activate
cd apps/api
pip install -r requirements.txt
```

### Docker containers unhealthy

**Solution:** Restart Docker services
```bash
cd ~/atlas/infra
docker compose down -v  # Remove volumes
docker compose up -d    # Start fresh
```

### Frontend build errors

**Solution:** Clear cache and reinstall
```bash
cd ~/atlas/apps/web
rm -rf node_modules .next
npm install
```

### Python version issues

**Solution:** Ensure using Python 3.12
```bash
python3.12 -m venv venv --clear
source venv/bin/activate
pip install -r apps/api/requirements.txt
```

---

## Performance Optimization for Mac

### For M1/M2/M3 Macs (Apple Silicon)

Docker runs natively - excellent performance!

### Allocate More Resources to Docker

1. Open Docker Desktop
2. Settings → Resources
3. Set:
   - CPUs: 4-6
   - Memory: 8-12 GB
   - Swap: 2 GB
4. Apply & Restart

### Speed Up Node.js

```bash
# Use faster package manager
brew install pnpm

# In atlas/apps/web:
pnpm install  # Instead of npm install
```

---

## Backup & Updates

### Backup Your Data

```bash
# Backup Docker volumes (contains research data)
cd ~/atlas/infra
docker compose down
cp -r /var/lib/docker/volumes ~/atlas_backup

# Backup .env
cp ~/atlas/.env ~/atlas_backup/
```

### Update Atlas

```bash
cd ~/atlas
git pull  # If using git

# Or copy new files from updated version

# Update dependencies
source venv/bin/activate
pip install --upgrade -r apps/api/requirements.txt
cd apps/web && npm update
```

---

## Monitoring

### Check Service Status

```bash
cd ~/atlas/infra
docker compose ps
```

All should show "Up (healthy)"

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f postgres
docker compose logs -f redis

# Backend logs
# (Visible in Terminal 2)

# Frontend logs
# (Visible in Terminal 3)
```

### Check API Health

```bash
curl http://localhost:8000/health
# Should return: {"status":"ok"}
```

---

## Uninstall (if needed)

```bash
# Stop and remove all containers
cd ~/atlas/infra
docker compose down -v

# Remove Docker images
docker system prune -a

# Remove atlas directory
cd ~
rm -rf atlas

# Remove virtual environment
# (Already inside atlas directory)

# Uninstall software (optional)
brew uninstall docker node@20 python@3.12
```

---

## Next Steps

After setup works:

1. **Read**: [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md) - How to use Atlas
2. **Read**: [USER_GUIDE.md](USER_GUIDE.md) - Research best practices
3. **Add API keys** for real data (optional)
4. **Run research** on your target companies
5. **Export reports** (Phase 2 feature)

---

## Quick Reference Card

**Start Atlas:**
```bash
cd ~/atlas
./start_all.sh
```

**Stop Atlas:**
```bash
./stop_all.sh
```

**Check Status:**
```bash
./status.sh
```

**View Logs:**
```bash
cd infra && docker compose logs -f
```

**Reset Everything:**
```bash
./reset_all.sh
```

**Open Atlas:**
```
http://localhost:3000
```

---

## Support

- **Setup Issues**: See troubleshooting section above
- **Usage Questions**: See [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md)
- **Research Tips**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Architecture**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

**Mac users: You have the best setup for Atlas!** 🚀

Docker runs natively on M-series chips, everything is fast and smooth.

Enjoy researching! 📊
