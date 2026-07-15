# Atlas User Guide

**Research Best Practices & Tips for Maximum Value**

---

## Who This Guide Is For

- **Investors**: Due diligence, market research, competitive analysis 
- **Analysts**: Company intelligence, trend detection, report generation
- **Founders**: Competitive intelligence, market mapping, partnership research
- **Recruiters**: Company health assessment, team growth signals
- **Anyone**: Need fast, reliable company research

---

## Quick Start Checklist

Before your first research run:

- [ ] Atlas is running (`./start_all.sh`)
- [ ] Frontend loads at http://localhost:3000
- [ ] You understand what to search (company name or ticker)
- [ ] You know what to expect (15-20 evidence items in 5-10 seconds)
- [ ] You're ready to verify claims by clicking sources

---

## Research Workflow

### Step 1: Identify Target Company

**Best Searches:**
- ✅ **Full legal name**: "Anthropic PBC", "OpenAI LP"
- ✅ **Common name**: "Anthropic", "OpenAI", "Stripe"
- ✅ **Ticker symbol** (public companies): "TSLA", "MSFT", "GOOGL"

**Avoid:**
- ❌ Generic terms: "AI startup", "payments company"
- ❌ Misspellings: "Antrhopic", "Open AI"
- ❌ Overly specific: "Anthropic PBC Claude Team"

**Tips:**
- Check company's official website for exact name
- Try both full name and common name
- Use ticker for public companies (better financial data)

### Step 2: Run Research

1. **Enter company name** in search box
2. **Click "Start Research"**
3. **Don't refresh the page** - updates come automatically
4. **Watch live feed** - see agents work in real-time
5. **Wait 5-10 seconds** - research completes automatically

**What's Happening Behind the Scenes:**
- News Agent searches 100+ news sources
- Financial Agent queries SEC database
- Hiring Agent analyzes job boards
- GitHub Agent checks repository activity
- All agents run simultaneously (parallel)
- LLM synthesizes evidence into narrative

### Step 3: Review Results

**Start with Quick Scan (30 seconds):**
1. Check total evidence count (should be 15-20)
2. Skim narrative sections for key themes
3. Note confidence scores (90%+ is very reliable)
4. Identify surprising findings

**Deep Dive (5 minutes):**
1. Read each narrative section carefully
2. Click evidence IDs to see sources
3. Verify 2-3 high-impact claims
4. Note trends across multiple evidence items
5. Look for contradictions or gaps

**Critical Analysis (15 minutes):**
1. Click through to original sources
2. Read full articles, not just excerpts
3. Cross-reference multiple sources
4. Check publication dates (is it recent?)
5. Evaluate source credibility
6. Form your own conclusions

### Step 4: Take Action

**Export Key Findings:**
- Copy important quotes
- Screenshot evidence cards
- Save dossier URL (bookmark it)
- Note citations for reports

**Follow-Up Research:**
- Re-run weekly/monthly for updates
- Research competitors for comparison
- Dive deeper on specific claims
- Verify with additional sources

---

## Understanding Evidence Quality

### Confidence Scores Explained

**95-100% (Highest)**
- SEC filings (official financial documents)
- Company announcements (verified sources)
- Government databases
- **Trust level**: Can rely on these directly

**85-95% (Very High)**
- Major news outlets (Reuters, Bloomberg, WSJ)
- Reputable tech publications (TechCrunch, Verge)
- Company career pages (job postings)
- **Trust level**: Very reliable, minimal verification needed

**75-85% (High)**
- GitHub stats (public repository data)
- Secondary news sources
- Industry publications
- **Trust level**: Good, but verify important claims

**Below 75% (Medium)**
- Social media mentions
- User-generated content
- Aggregated data
- **Trust level**: Use as leads, always verify

### Source Types Ranked

**Most Reliable:**
1. **sec_filing** - Official regulatory filings (10-K, 10-Q, 8-K)
2. **press_release** - Official company communications
3. **patent** - USPTO records
4. **legal_filing** - Court documents

**Very Reliable:**
5. **news** - Major media outlets
6. **market_report** - Industry analysis firms

**Reliable:**
7. **job_posting** - Career page listings
8. **github** - Public repository data
9. **website_diff** - Company website changes

**Use Cautiously:**
10. **social** - Twitter, LinkedIn, etc.
11. **review** - User reviews, Glassdoor

### Red Flags to Watch For

⚠️ **Warning Signs:**
- All evidence from single source
- Conflicting claims in evidence
- No recent evidence (all >6 months old)
- Extremely low confidence scores (<70%)
- Vague or generic claims
- No source URLs provided

✅ **Green Flags:**
- Multiple independent sources
- Consistent claims across sources
- Recent evidence (<30 days)
- High confidence scores (>85%)
- Specific, detailed claims
- Verifiable source links

---

## Research Use Cases

### Due Diligence (Investors)

**Goal**: Assess investment opportunity

**Workflow:**
1. Run initial research on target company
2. Focus on financial evidence (revenue, funding, metrics)
3. Check growth signals (hiring, product launches)
4. Identify risks (competition, dependencies)
5. Compare to competitors (run research on 3-5 peers)
6. Re-run monthly to track progress

**Key Evidence to Look For:**
- Recent funding rounds (amounts, valuations, investors)
- Revenue growth trends
- Team expansion rate
- Product traction signals
- Customer acquisition
- Competitive positioning

**Questions to Answer:**
- Is the company growing?
- Are they hiring (and for what roles)?
- What's their strategic focus?
- Who are the key competitors?
- What are the major risks?

### Competitive Analysis

**Goal**: Understand competitive landscape

**Workflow:**
1. List 5-10 competitors
2. Run research on each
3. Compare evidence across companies
4. Identify trends and patterns
5. Map strategic differences
6. Spot opportunities and threats

**Comparison Framework:**
- **Team size**: Who's hiring more aggressively?
- **Product focus**: What are they building?
- **Market strategy**: Which segments are they targeting?
- **Funding**: Who has more runway?
- **Momentum**: Who has growing vs declining signals?

**Create Comparison Table:**
```
Company    | Team Growth | Funding | Product Focus | Momentum
-----------|-------------|---------|---------------|----------
Anthropic  | 50 hires    | $200M   | Enterprise AI | ↗ High
OpenAI     | 100 hires   | $10B    | Consumer AI   | ↗ High
Cohere     | 30 hires    | $270M   | Developer API | → Medium
```

### Market Mapping

**Goal**: Understand entire market segment

**Workflow:**
1. Identify 20-30 companies in space
2. Run research on top 10-15
3. Categorize by segment/approach
4. Identify leaders, challengers, niche players
5. Spot white space opportunities
6. Track quarterly for changes

**Market Map Example (AI Companies):**
```
Enterprise Focus:
- Anthropic (enterprise AI safety)
- OpenAI Enterprise
- Cohere (developer tools)

Consumer Focus:
- Character.AI
- Midjourney
- Jasper

Infrastructure:
- Hugging Face
- Weights & Biases
- Modal
```

### Partnership Research

**Goal**: Evaluate potential partners

**Workflow:**
1. Run research on potential partner
2. Assess financial health
3. Check strategic alignment
4. Identify complementary strengths
5. Spot potential conflicts
6. Evaluate partnership risks

**Evaluation Criteria:**
- **Financial stability**: Recent funding, revenue growth
- **Strategic fit**: Are goals aligned?
- **Reputation**: News sentiment, glassdoor reviews
- **Team quality**: Hiring for relevant roles?
- **Technology**: Compatible tech stacks?
- **Market position**: Strong enough to add value?

### Recruitment Research

**Goal**: Assess employer attractiveness

**Workflow:**
1. Research target company
2. Focus on hiring evidence
3. Check growth signals
4. Evaluate company momentum
5. Compare to other opportunities

**Key Signals:**
- **High hiring**: 20+ open roles = growing team
- **Senior roles**: Leadership hiring = maturity
- **Diverse roles**: Multiple functions = well-rounded growth
- **Recent funding**: Financial stability
- **Product launches**: Momentum and excitement

---

## Advanced Techniques

### Longitudinal Analysis

Track companies over time:

**Monthly Snapshots:**
```
Month 1: Anthropic
- Team: 150 people
- Funding: $200M Series D
- Product: Claude 2.0

Month 2: Anthropic
- Team: 170 people (+20)
- Funding: Same
- Product: Claude 2.1 launched

Month 3: Anthropic
- Team: 200 people (+30)
- Funding: $450M Series D extension
- Product: Claude 3.0 announced
```

**Trend Detection:**
- Accelerating hiring = scaling up
- Slowing hiring = stabilizing or struggling
- New product launches = momentum
- Funding rounds = validation and runway

### Cross-Referencing

Verify claims across multiple sources:

1. **Find claim in Atlas**: "Raised $200M Series D"
2. **Check multiple evidence items**: Should appear in news + SEC filing
3. **Click through to sources**: Read full articles
4. **Google search**: Find additional sources
5. **Company confirmation**: Check official press releases

**If claim appears in:**
- 1 source = Possible, needs verification
- 2 sources = Likely, worth noting
- 3+ sources = Confirmed, highly reliable

### Hypothesis Testing

Use Atlas to test specific hypotheses:

**Hypothesis**: "Company X is pivoting to enterprise from consumer"

**Evidence to look for:**
- Job postings for enterprise sales roles
- Press releases about enterprise products
- Partnerships with enterprise companies
- Shift in public messaging

**Research workflow:**
1. Run current research
2. Check hiring evidence (enterprise sales roles?)
3. Review news evidence (enterprise announcements?)
4. Compare to 3 months ago (what changed?)
5. Confirm or reject hypothesis

---

## Common Mistakes to Avoid

### 1. Taking Everything at Face Value

❌ **Wrong**: "Atlas says they raised $200M, so it must be true"
✅ **Right**: "Atlas found 3 sources saying $200M, let me click through to verify"

**Fix**: Always click source links for important claims

### 2. Ignoring Confidence Scores

❌ **Wrong**: Treating 60% confidence claim same as 95%
✅ **Right**: Focus on high-confidence claims, use low-confidence as leads

**Fix**: Sort by confidence, prioritize 85%+ claims

### 3. Not Checking Dates

❌ **Wrong**: Using 2-year-old evidence for current decisions
✅ **Right**: Focus on recent evidence (<6 months)

**Fix**: Check `retrieved_at` timestamp on each evidence item

### 4. Single-Source Reliance

❌ **Wrong**: Making decision based on one piece of evidence
✅ **Right**: Triangulate across multiple sources

**Fix**: Look for claim in multiple evidence items

### 5. Skipping Verification

❌ **Wrong**: Copying claims directly into reports without checking
✅ **Right**: Clicking through to verify original source

**Fix**: Budget time for verification (15min per company)

### 6. Over-Interpreting Signals

❌ **Wrong**: "10 job postings means they're crushing it!"
✅ **Right**: "10 job postings + funding + product launch = positive momentum"

**Fix**: Look for multiple corroborating signals

### 7. Ignoring Contradictions

❌ **Wrong**: Cherry-picking only positive signals
✅ **Right**: Investigating why evidence contradicts

**Fix**: Pay special attention to conflicting claims

---

## Power User Tips

### 1. Build Research Templates

Create standard checklists for your use case:

**Example: VC Due Diligence Checklist**
- [ ] Recent funding (amount, date, lead investor)
- [ ] Revenue metrics (if public)
- [ ] Team size and growth rate
- [ ] Key hires in past 3 months
- [ ] Product launches in past 6 months
- [ ] Competitor mentions in news
- [ ] Risk signals (lawsuits, layoffs, etc.)

### 2. Use Multiple Runs for Depth

Run 2-3 times if:
- First run has <10 evidence items
- Need more sources for verification
- Checking for updates (weekly research)

### 3. Compare to Competitors Immediately

Don't research in isolation:
1. Research Company A
2. Research Company B (main competitor)
3. Research Company C (alternative competitor)
4. Compare all three side-by-side

### 4. Track Trends, Not Snapshots

Single datapoint = interesting
Multiple datapoints = trend
Trends = actionable insights

### 5. Combine with Other Research

Atlas gives you:
- What's publicly known
- Recent developments
- Verifiable facts

Still need:
- Customer interviews
- Product trials
- Financial model analysis
- Private information

**Use Atlas as starting point, not end point.**

---

## Interpreting Results

### Strong Positive Signals

✅ Multiple funding announcements
✅ Aggressive hiring (20+ roles)
✅ Product launches with customer traction
✅ Partnerships with major companies
✅ Positive news sentiment across sources
✅ High confidence evidence (>90%)

**Interpretation**: Company is growing, has momentum, likely worth deeper look

### Mixed Signals

⚠️ Hiring + recent layoffs
⚠️ Funding + pivot announcement
⚠️ Product launch + executive departure
⚠️ Mix of positive and negative news

**Interpretation**: Company in transition, needs deeper investigation

### Weak/Negative Signals

❌ No recent news (>6 months old)
❌ Layoff announcements
❌ Executive departures
❌ Product shutdowns
❌ Lawsuits or regulatory issues
❌ Low evidence count (<5 items)

**Interpretation**: Company may be struggling, proceed with caution

### Inconclusive Results

❓ Very few evidence items (2-3)
❓ All from single source type
❓ Generic, vague claims
❓ Low confidence scores across board

**Interpretation**: Company too small/private, need alternative research methods

---

## When Atlas Isn't Enough

Atlas works best for:
- Companies with public presence
- Recent news/activity
- Public or growth-stage startups
- Tech companies with GitHub presence

Atlas struggles with:
- Very early stage (pre-seed)
- Stealth companies
- Non-tech industries (limited GitHub data)
- International companies (primarily English sources)
- Private, quiet companies

**Supplement Atlas with:**
- Crunchbase (funding data)
- PitchBook (private company data)
- LinkedIn Sales Navigator (employee data)
- Glassdoor (employee reviews)
- Customer interviews (qualitative insights)
- Financial models (projections)

---

## Research Frequency Guide

**New Opportunities:**
- Initial research: First time you hear about company
- Follow-up: 1 week later (check for missed signals)
- Update: Monthly until decision made

**Active Portfolio/Monitoring:**
- Growth companies: Weekly
- Stable companies: Monthly
- Mature companies: Quarterly

**Competitor Tracking:**
- Direct competitors: Weekly
- Broader market: Monthly
- Adjacent markets: Quarterly

**Trigger Events (Immediate Research):**
- Funding announcement
- Product launch
- Executive hire/departure
- Major partnership
- Negative news
- Earnings report (public companies)

---

## Ethical Research Guidelines

### Do:
- ✅ Verify claims before sharing
- ✅ Cite sources when using evidence
- ✅ Respect rate limits if adding API keys
- ✅ Use research for legitimate business purposes
- ✅ Keep sensitive findings confidential

### Don't:
- ❌ Share unverified claims as facts
- ❌ Use for illegal/unethical purposes
- ❌ Circumvent security measures
- ❌ Spam Atlas with excessive requests
- ❌ Share API keys with unauthorized users

---

## Getting Maximum Value

**Week 1: Learning**
- Run 10-20 searches
- Click through all sources
- Compare companies
- Learn what good evidence looks like

**Week 2: Applying**
- Use for real decisions
- Build your templates
- Develop verification workflow
- Integrate into your process

**Week 3: Optimizing**
- Add API keys for real data
- Set up regular monitoring
- Build comparison frameworks
- Share with team

**Ongoing: Mastery**
- Research 50-100 companies
- Spot patterns across industries
- Develop intuition for signals
- Become power user

---

## Next Steps

1. **Run your first research** on a company you know well
2. **Verify all claims** by clicking sources
3. **Compare to your knowledge** - did Atlas find things you didn't know?
4. **Run 10 more companies** to build intuition
5. **Read [OPERATIONS_MANUAL.md](OPERATIONS_MANUAL.md)** for technical details
6. **Add API keys** for real data when ready

---

**You're now ready to extract maximum value from Atlas!** 🎯

Remember: Atlas gives you the signals. You make the decisions. Always verify important claims and use multiple sources.

Happy researching! 📊
