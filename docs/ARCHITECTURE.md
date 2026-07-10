# Atlas Architecture

## Overview

Atlas is an AI operating system for company and market intelligence, built on evidence-backed research principles and multi-agent orchestration.

## Core Principles

### 1. Evidence-First Architecture

Every claim in Atlas must be:
- Backed by a specific source (`source_url`)
- Time-stamped (`retrieved_at`)
- Include verbatim excerpt (`raw_excerpt`)
- Never fabricated or interpolated

### 2. Structured Schemas

All data flows through Pydantic models:
- **Evidence**: Atomic facts with attribution
- **AgentReport**: Agent output with evidence list
- **CompanyProfile**: Synthesized narrative with citations
- **DebateResult**: Multi-agent deliberation output
- **Prediction**: Forecasts with confidence scores

### 3. Agent Orchestration

**Fan-out/Fan-in Pattern:**
```
Query → Orchestrator → [Agent 1, Agent 2, ..., Agent N] → Synthesis → Report
```

Agents execute in parallel, return structured reports, and synthesis combines them into coherent narratives.

### 4. Temporal Knowledge Graph

Evidence accumulates over time:
- Neo4j stores entity relationships
- Time-indexed edges track changes
- Graph queries enable trend detection
- Diff detection highlights material changes

## System Components

### Backend Services

**1. FastAPI Application (`apps/api/`)**
- REST endpoints for research requests
- WebSocket server for live streaming
- Background task orchestration
- In-memory storage (Phase 0), Postgres (Phase 1+)

**2. Agent System (`packages/agents/`)**
- `BaseAgent`: Abstract interface
- Specialized agents (News, Financial, Hiring, GitHub, etc.)
- Each returns `AgentReport` with evidence
- Validates sources and excerpts

**3. Orchestrator (`packages/orchestrator/`)**
- LangGraph state machine
- Fan-out to agents in parallel
- Collect and validate reports
- Stream events via WebSocket
- Error handling and retries

**4. LLM Abstraction (`packages/llm/`)**
- `LLMProvider` interface
- Adapters for OpenAI, Anthropic, Gemini
- Redis cache layer (TTL-based)
- Token counting and cost tracking

**5. Synthesis Engine (`packages/synthesis/`)**
- Convert evidence to narrative
- Enforce citation requirements
- Generate structured sections (Strategy, Growth, Risks)
- Validate all claims reference evidence IDs

**6. Debate System (`packages/debate/`)**
- Multi-agent deliberation
- Turn-based argumentation
- Consensus detection
- Confidence scoring

### Frontend Application

**Next.js App (`apps/web/`)**

**1. Search Page (`/`)**
- Simple input for company name/ticker
- Submit → POST to backend → redirect to dossier

**2. Dossier Page (`/dossier/[runId]`)**
- WebSocket connection to backend
- Live agent activity feed
- Report rendering (sections, evidence, sources)
- Evidence tooltips with excerpts

**3. Agent Feed Component**
- Real-time event stream
- Visual indicators per event type
- Confidence scores
- Timestamps

### Data Layer

**1. Postgres**
- `runs`: Research run metadata
- `agent_reports`: Agent output
- `evidence`: Atomic evidence items
- `api_costs`: LLM usage tracking
- `company_profiles`: Synthesized profiles
- `debates`: Multi-agent debate results
- `predictions`: Forecasts and outcomes

**2. Neo4j**
- Entity nodes (Company, Person, Product, Event)
- Temporal edges with timestamps
- Graph queries for relationships
- Diff detection over time

**3. Qdrant**
- Evidence embeddings
- Semantic search
- Duplicate detection
- Similarity scoring

**4. Redis**
- LLM response cache
- Rate limiting
- Session storage
- WebSocket pub/sub

**5. Temporal**
- Workflow orchestration
- Agent execution activities
- Retry logic
- Monitoring and observability

## Data Flow

### Phase 0: Basic Pipeline

```
User → FastAPI → Orchestrator → DummyAgent → WebSocket → Frontend
         ↓
    In-memory storage
```

### Phase 1+: Full Pipeline

```
User → FastAPI → Temporal Workflow
                      ↓
                 Orchestrator
                      ↓
         [Agent 1, Agent 2, ..., Agent N]
                      ↓ (parallel execution)
         [Report 1, Report 2, ..., Report N]
                      ↓
              Synthesis Engine
                      ↓
              Postgres + Neo4j
                      ↓
            WebSocket → Frontend
```

## Agent Lifecycle

1. **Initialization**: Agent receives `company_id` and `run_id`
2. **Research**: Agent queries APIs, scrapes data, runs searches
3. **Evidence Collection**: Each fact → `Evidence` object with source
4. **Validation**: Ensure all evidence has required fields
5. **Report Generation**: Compile evidence into `AgentReport`
6. **Broadcast**: Send events via WebSocket
7. **Storage**: Persist to Postgres

## Evidence Requirements

Every `Evidence` object must include:

```python
{
    "id": "uuid",
    "agent": "agent_name",
    "claim": "Single factual sentence",
    "source_url": "https://...",
    "source_type": "news" | "sec_filing" | ...,
    "retrieved_at": "2025-01-15T10:30:00Z",
    "confidence": 0.95,
    "raw_excerpt": "Verbatim text from source..."
}
```

**Null Policy**: If data unavailable, set to `null`. Never fabricate.

## LLM Usage Patterns

### 1. Synthesis
- Input: List of `Evidence` objects
- Output: Narrative sections with citation footnotes
- Model: GPT-4 or Claude Opus
- Cache: 1 hour TTL

### 2. Classification
- Input: Text snippet
- Output: Category label
- Model: GPT-3.5 or Claude Haiku (fast)
- Cache: 24 hours TTL

### 3. Debate
- Input: Claim + opposing evidence
- Output: Argument for/against
- Model: GPT-4 or Claude Sonnet
- No cache (context-dependent)

### 4. Embedding
- Input: Evidence text
- Output: Vector (1536 or 1024 dim)
- Model: text-embedding-3-small or Voyage
- Cache: Permanent (keyed by text hash)

## Cost Management

Track all LLM calls:
```sql
INSERT INTO api_costs (run_id, agent, provider, model, tokens_in, tokens_out, cost_usd)
```

Aggregate by run:
```sql
SELECT run_id, SUM(cost_usd) FROM api_costs GROUP BY run_id
```

## WebSocket Protocol

### Client → Server
- `ping`: Keep-alive

### Server → Client
- `connected`: Connection established
- `run_started`: Research initiated
- `agent_started`: Agent began
- `evidence_found`: New evidence
- `agent_completed`: Agent finished
- `synthesis_started`: Narrative generation began
- `run_completed`: Research done
- `run_failed`: Error occurred

## Scaling Strategy

**Phase 0-2**: Single-server monolith
**Phase 3+**: Service decomposition
- API Gateway
- Agent Workers (horizontal scaling)
- Temporal cluster
- Postgres replication
- Redis cluster
- CDN for frontend

## Security Considerations

1. **API Keys**: Never log or expose
2. **Rate Limiting**: Per-user limits on research requests
3. **Input Validation**: Sanitize company names
4. **CORS**: Restrict to known origins
5. **Authentication**: OAuth + JWT (Phase 2+)
6. **Data Privacy**: Respect scraping robots.txt

## Monitoring

**Key Metrics:**
- Research runs per minute
- Agent success/failure rates
- Average evidence per agent
- Synthesis latency
- LLM API costs per run
- WebSocket connection count

**Logging:**
- All agent executions
- LLM API calls
- Errors and retries
- User actions

## Future Enhancements

- [ ] Real-time company alerts (webhook-driven)
- [ ] Competitive intelligence comparisons
- [ ] Market trend detection via graph queries
- [ ] Export to Notion, Obsidian, etc.
- [ ] Chrome extension for inline fact-checking
- [ ] Slack/Discord bot integration

---

**Version**: 0.1.0 (Phase 0)
**Last Updated**: 2026-07-09
