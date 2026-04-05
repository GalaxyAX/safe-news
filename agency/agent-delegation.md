# Agent Delegation Plan

## Agent Roster and Responsibilities

### Agent 1: osint-collector
**Stage**: Collection (Stage 1)
**Schedule**: Every 15 minutes
**Input**: RSS feeds, government alerts, NGO reports, social signals
**Output**: raw_events.jsonl

**Responsibilities**:
- Poll Reuters, AP, BBC, Al Jazeera RSS feeds
- Monitor WHO, US State Dept, FEMA government feeds
- Track ReliefWeb and NGO humanitarian reports
- Extract: headline, summary, source, URL, location hint, timestamp
- Deduplicate by URL before appending
- Tag with category hint (war, terrorism, epidemic, natural_disaster, civil_unrest)

### Agent 2: verification
**Stage**: Verification (Stage 2)
**Schedule**: Every 30 minutes
**Input**: raw_events.jsonl
**Output**: verified_events.jsonl

**Responsibilities**:
- Cross-reference events across multiple sources
- Assign confidence scores (0.0-1.0) based on source reliability tiers
- Deduplicate events matching same incident within 6-hour window
- Merge duplicate sources into single high-confidence event
- Drop events with confidence < 0.30
- Flag 0.30-0.50 for review, auto-pass > 0.75

### Agent 3: risk-analyst
**Stage**: Analysis (Stage 3)
**Schedule**: Every 60 minutes
**Input**: verified_events.jsonl
**Output**: classified_events.jsonl

**Responsibilities**:
- Classify event type: war, terrorism, epidemic, natural_disaster, civil_unrest
- Assign severity 1-5 and risk level: low/medium/high/critical
- Map locations to ISO 3166-1 alpha-2 country codes
- Assess escalation risk (low/medium/high)
- Generate analytical summary for each event
- Identify multi-country affected areas

### Agent 4: seo-writer
**Stage**: Publishing (Stage 4)
**Schedule**: Every 60 minutes (when new classified events exist)
**Input**: classified_events.jsonl
**Output**: published_articles.jsonl

**Responsibilities**:
- Write SEO-optimized articles for severity 3+ events
- Generate headline (50-65 chars), summary (150-160 chars), body
- Create URL-safe slugs and extract 3-7 keywords
- Score SEO 0-100 based on optimization criteria
- Maintain factual, neutral, non-sensational tone
- Include traveler impact and safety guidance

### Agent 5: monitoring
**Stage**: Monitoring (Stage 5)
**Schedule**: Every 4 hours
**Input**: All pipeline outputs
**Output**: trends.json, alerts.jsonl

**Responsibilities**:
- Detect geographic hotspots and event clusters
- Track escalation/de-escalation per country
- Alert immediately on critical (severity 5) events
- Watch for 3+ high-severity events in same country within 24h
- Generate 24-hour trend reports with category breakdowns
- Monitor rate of change against baseline

### Agent 6: quality-control
**Stage**: Quality Control (Stage 6a)
**Schedule**: Every 8 hours
**Input**: All pipeline outputs
**Output**: Validation report, quarantined_events.jsonl

**Responsibilities**:
- Validate JSON schema compliance at each stage
- Verify confidence scores, severity scores, country codes
- Check SEO scores meet minimum threshold (60)
- Detect anomalies: severity jumps, future timestamps, invalid codes
- Quarantine invalid events with logged reasons
- Report validation metrics (pass rate, failure count)

### Agent 7: data-structurer
**Stage**: Data Structuring (Stage 6b)
**Schedule**: Every 8 hours (after QC)
**Input**: QC-validated events
**Output**: safety-news.json (final), country-risk.json

**Responsibilities**:
- Normalize country names and codes
- Map severity 1-5 to string labels (low/medium/high/critical)
- Merge with existing safety-news.json (skip duplicates)
- Sort by createdAt newest first, cap at 100 events
- Generate country risk summary with overall risk per country
- Ensure JSON compatibility with SafeTravel backend API
