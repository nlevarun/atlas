# Atlas - For Your Mac

**Complete AI Research System - Ready to Run on macOS**

---

## Quick Start (First Time Setup - 10 minutes)

### 1. Install Prerequisites

Open Terminal and run:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12, Node.js 20, and Docker
brew install python@3.12 node@20
brew install --cask docker

# Start Docker Desktop
open -a Docker
# Wait for Docker to fully start (whale icon in menu bar)
```

### 2. Extract Atlas

1. Extract the downloaded zip to your home directory
2. Rename folder to just `atlas` if needed
3. Should be at: `~/atlas`

### 3. Run Setup

```bash
cd ~/atlas
chmod +x *.sh
./setup_mac.sh
```

This takes ~5 minutes and installs all dependencies.

### 4. Start Atlas

```bash
./start_all.sh
```

Wait 30 seconds, then browser opens automatically to http://localhost:3000

### 5. Test!

Search for: **Anthropic**

Watch 4 agents research the company in real-time! ✨

---

## Daily Use

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

---

## Documentation

- **[MAC_SETUP.md](MAC_SETUP.md)** - Detailed setup guide
- **[OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md)** - How to use Atlas
- **[USER_GUIDE.md](USER_GUIDE.md)** - Research best practices
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design

---

## What You Get

✅ **4 Real Research Agents**
- News Agent (recent articles)
- Financial Agent (SEC filings)
- Hiring Agent (job postings)
- GitHub Agent (repository metrics)

✅ **Real-Time Updates**
- WebSocket streaming
- Live agent feed
- Watch research happen

✅ **Professional Reports**
- 15-20 evidence items per company
- Cited sources
- Confidence scores
- 5-10 second execution

✅ **Works Without API Keys**
- Intelligent mock data fallback
- Zero setup required
- Add keys later for real data

---

## Optional: Add API Keys for Real Data

Edit `~/atlas/.env`:

```bash
# Real news (optional)
TAVILY_API_KEY=tvly-xxxxx

# Real AI synthesis (optional)
OPENAI_API_KEY=sk-xxxxx

# Better GitHub limits (optional)
GITHUB_TOKEN=ghp_xxxxx
```

Cost: ~$0.25 per research run with real APIs

---

## Helper Scripts

All scripts are in `~/atlas/`:

- `setup_mac.sh` - One-time setup
- `start_all.sh` - Start everything
- `stop_all.sh` - Stop everything
- `status.sh` - Check what's running
- `restart_backend.sh` - Restart just backend
- `reset_all.sh` - Delete all data (fresh start)

---

## Troubleshooting

**Can't start Docker?**
```bash
open -a Docker
# Wait 30 seconds
```

**Port already in use?**
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

**Need fresh start?**
```bash
./reset_all.sh
```

More help: See [MAC_SETUP.md](MAC_SETUP.md)

---

## Support

- Setup issues → [MAC_SETUP.md](MAC_SETUP.md)
- Usage questions → [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md)
- Research tips → [USER_GUIDE.md](USER_GUIDE.md)

---

**Your Mac is the perfect platform for Atlas!** 🚀

Everything runs natively, fast, and smooth on Apple Silicon.

Enjoy! 📊
