# Atlas

AI operating system for company intelligence. Atlas runs four research agents in parallel, gathers evidence with citations, and synthesizes a report.

## What it does

Atlas researches a company across four angles at once:

- **News agent** - recent articles and announcements, via Tavily's free tier or mock data if no key is set
- **Financial agent** - SEC EDGAR filings, no key needed
- **Hiring agent** - job posting signals, mock data only for now
- **GitHub agent** - repository activity and stars, via the GitHub API

Results get combined into a written report. By default this uses template-based synthesis; if you add a Groq key, it uses an LLM instead. Every claim in the report links back to a source URL and excerpt. 

## Setup (Mac)

Install prerequisites:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12 node@20
brew install --cask docker
open -a Docker
```

Run the setup script:

```bash
cd ~/atlas
chmod +x *.sh
./setup_mac.sh
```

Start Atlas:

```bash
./start_all.sh
```

This opens `http://localhost:3000` automatically. Search a company name and you'll get a report in 5-10 seconds.

## Running for free

Atlas works with no API keys at all: agents fall back to realistic mock data, and synthesis uses templates instead of an LLM. To pull real data instead, add any of these free keys to `.env`:

| Service | What it enables | Free tier | Sign up |
|---|---|---|---|
| Groq | LLM-written synthesis instead of templates | 6,000 requests/day | console.groq.com |
| Tavily | Real news search | 1,000 searches/month | tavily.com |
| GitHub | Real repo stats, higher rate limits | 5,000 requests/hour | github.com/settings/tokens |
| SEC EDGAR | Real financial filings | Unlimited, no key | just add your name/email to `.env` |

None of these need a credit card. All are optional, and you can mix and match — add just a Tavily key, for instance, and everything else keeps using mock data.

## Commands

```bash
./setup_mac.sh          # one-time setup
./start_all.sh          # start everything
./stop_all.sh           # stop everything
./status.sh             # check what's running
./restart_backend.sh    # restart just the backend
./reset_all.sh          # wipe data and start fresh
```

## Requirements

- macOS 12 or later
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Python 3.12+, Node.js 20+, Docker Desktop

## Tech stack

**Backend:** Python 3.12, FastAPI, template-based synthesis with an optional Groq LLM.
**Frontend:** Next.js 14, React 18, Tailwind CSS, WebSocket updates for live agent status.
**Infrastructure:** Docker containers for Postgres, Neo4j, Qdrant, Redis, and Temporal, all running locally.

## Documentation

- [README_MAC.md](README_MAC.md) — Mac quick start
- [FREE_TIER_GUIDE.md](FREE_TIER_GUIDE.md) — free tier setup details
- [MAC_SETUP.md](MAC_SETUP.md) — detailed installation
- [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md) — day-to-day usage
- [USER_GUIDE.md](USER_GUIDE.md) — research tips
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system design, for contributors

## License

MIT
