# SafeTravel Autonomous OSINT Intelligence Agency

## Mission
Collect, verify, analyze, and publish global safety intelligence covering wars, terrorism, epidemics, and natural disasters. Operate 24/7 as an automated pipeline feeding structured data to the SafeTravel platform.

## Agency Structure

```
                    CEO (Strategy & Coordination)
                              |
        +----------+----------+----------+----------+
        |          |          |          |          |
   COLLECTION   VERIFICATION  ANALYSIS   PUBLISHING  MONITORING
        |          |          |          |          |
   OSINT      Fact-Check    Risk       SEO        Trend Detector
   Collector  Agent         Analyst    Writer     Alert Engine
   (News)   (Dedup)        (Classify) (Articles) (Escalation)
   (Gov)    (Confidence)   (Severity) (SEO)      (Patterns)
   (Social) (Source Rank)  (Geo)      (Schema)   (Thresholds)
   (RSS)
        |          |          |          |          |
        +----------+----------+----------+----------+
                              |
                     QUALITY CONTROL
                     (Accuracy + Compliance)
                              |
                     DATA STRUCTURING
                     (JSON Normalization)
```

## Agent Pipeline (6-Stage Workflow)

### Stage 1: COLLECTION - OSINT Collector Agent
- **Input**: RSS feeds, news APIs, government alerts, NGO reports
- **Output**: Raw intelligence events (`raw_events.jsonl`)
- **Sources**: NewsAPI, GDELT, RSS feeds (Reuters, AP, BBC), government feeds (State Dept, WHO, FEMA)

### Stage 2: VERIFICATION - Verification Agent
- **Input**: Raw events from Stage 1
- **Output**: Verified events (`verified_events.jsonl`)
- **Processes**: Deduplication, source cross-referencing, confidence scoring (0.0-1.0), fake detection

### Stage 3: ANALYSIS - Risk Analyst Agent
- **Input**: Verified events from Stage 2
- **Output**: Classified risks (`classified_events.jsonl`)
- **Processes**: Event type classification, severity rating (1-5), geographic mapping, impact assessment

### Stage 4: PUBLISHING - SEO News Writer Agent
- **Input**: Classified events from Stage 3
- **Output**: Published articles (`published_articles.jsonl`)
- **Processes**: Article generation, SEO optimization, slug creation, keyword extraction

### Stage 5: MONITORING - Monitoring Agent
- **Input**: All pipeline outputs
- **Output**: Trend reports and alerts (`trends.json`, `alerts.jsonl`)
- **Processes**: Trend detection, escalation tracking, threshold alerts, pattern recognition

### Stage 6: QUALITY CONTROL & DATA STRUCTURING
- **Input**: All outputs from previous stages
- **Output**: Final structured data (`safety-news.json`)
- **Processes**: Accuracy checks, consistency validation, JSON normalization, SafeTravel backend format mapping

---

## Execution Schedule

```
Every 15 minutes:  Stage 1 (Collection) sweep
Every 30 minutes:  Stages 2-3 (Verification + Analysis)
Every 60 minutes:  Stage 4 (Publishing) if new classified events exist
Every 4 hours:     Stage 5 (Monitoring) trend analysis
Every 8 hours:     Stage 6 (QC + Data structuring) full pipeline audit
```

---

## Data Flow Format

### Raw Event (Stage 1 Output)
```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "source": "string",
  "source_url": "string",
  "headline": "string",
  "summary": "string",
  "location_raw": "string",
  "collected_at": "ISO-8601"
}
```

### Verified Event (Stage 2 Output)
```json
{
  "event_id": "uuid",
  "confidence": 0.0-1.0,
  "source_count": int,
  "duplicate_of": "event_id|null",
  "verified_at": "ISO-8601"
}
```

### Classified Event (Stage 3 Output)
```json
{
  "event_id": "uuid",
  "event_type": "war|terrorism|epidemic|natural_disaster|civil_unrest|other",
  "severity": 1-5,
  "country_code": "ISO-3166-1 alpha-2",
  "region": "string",
  "risk_level": "low|medium|high|critical"
}
```

### Published Article (Stage 4 Output)
```json
{
  "article_id": "uuid",
  "event_id": "uuid",
  "headline": "string",
  "summary": "string",
  "body": "string",
  "slug": "string",
  "keywords": ["string"],
  "seo_score": 0-100
}
```

### SafeTravel Backend Event (Stage 6 Output)
```json
{
  "id": "uuid",
  "title": "string",
  "summary": "string",
  "url": "string",
  "country": "string",
  "countryCode": "string",
  "severity": "low|medium|high|critical",
  "eventType": "string",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "verified": true
}
```

---

## Directory Layout

```
agency/
  AGENT.md              - This file
  config/
    sources.yaml        - Data source configurations
    thresholds.yaml     - Alert thresholds and severity rules
    countries.yaml      - Country code mappings
  agents/
    osint-collector.md  - OSINT Collector Agent spec
    verification.md     - Verification Agent spec
    risk-analyst.md     - Risk Analyst Agent spec
    seo-writer.md       - SEO News Writer Agent spec
    monitoring.md       - Monitoring Agent spec
    quality-control.md  - Quality Control Agent spec
    data-structurer.md  - Data Structuring Agent spec
  data/
    raw_events.jsonl    - Stage 1 output
    verified_events.jsonl - Stage 2 output
    classified_events.jsonl - Stage 3 output
    published_articles.jsonl - Stage 4 output
  output/
    safety-news.json    - Final structured output
    trends.json         - Trend analysis
    alerts.jsonl        - Active alerts
  logs/
    pipeline.log        - Pipeline execution log
  scripts/
    pipeline.sh         - Main pipeline orchestrator