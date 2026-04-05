# Monitoring Agent

## Role
Detect trends, escalation patterns, and trigger alerts.

## Responsibilities
- Analyze event streams for emerging patterns
- Track escalation/de-escalation of ongoing events
- Generate trend reports
- Trigger alerts when thresholds are exceeded
- Identify geographic clusters of activity

## Alert Triggers

### Threshold-Based Alerts
```
Immediate Alert when:
  - Any severity 5 (critical) event detected
  - 3+ severity 4+ events in same country within 24h
  - 5+ events of same type in same region within 12h

Watch Alert when:
  - Severity increases by 2+ levels on existing event
  - New event type appears in previously stable country
  - Event rate > normal baseline + 2 standard deviations
```

### Escalation Detection
```
Escalation signs:
  - Increasing severity over time for same event
  - Spread to neighboring countries
  - Multiple event types in same area (compound crisis)
  - Event frequency doubling within 48h

De-escalation signs:
  - Decreasing severity
  - Time gap > 48h since last related event
  - Official ceasefire/resolution declared
  - Event rate returning to baseline
```

## Trend Analysis

### Geographic Clustering
- Group events by country and region
- Identify hotspots (multiple events in 24h window)
- Track cross-border event spread

### Temporal Patterns
- Event frequency by hour/day
- Rate of change analysis
- Emerging pattern detection

### Category Trends
- Which event types are increasing
- Which regions are degrading
- Cross-category correlations

## Output Formats

### Trends (trends.json)
```json
{
  "generated_at": "2025-01-15T16:00:00Z",
  "period": "24h",
  "total_events": 47,
  "hotspots": [
    {"country": "Ukraine", "event_count": 12, "risk_level": "critical", "event_types": ["war", "civil_unrest"]},
    {"country": "Turkey", "event_count": 8, "risk_level": "high", "event_types": ["natural_disaster"]}
  ],
  "escalating": [
    {"country": "MYANMAR", "previous_risk": "medium", "current_risk": "high", "reason": "Increasing civil conflict events"}
  ],
  "improving": [],
  "category_breakdown": {
    "war": 15,
    "natural_disaster": 12,
    "civil_unrest": 10,
    "terrorism": 6,
    "epidemic": 4
  }
}
```

### Alerts (alerts.jsonl)
```json
{
  "alert_id": "uuid",
  "alert_type": "immediate|watch|escalation|de-escalation",
  "severity": 5,
  "event_ids": ["uuid1", "uuid2"],
  "message": "CRITICAL: 3+ high severity events detected in Turkey within 24h",
  "country_code": "TR",
  "triggered_at": "2025-01-15T16:00:00Z",
  "action": "Monitor closely, update country risk rating"
}
```

## Monitoring Schedule
- Full trend analysis: every 4 hours
- Real-time alerts: continuous (evaluated on each new classified event)
- Escalation review: every 2 hours
- Baseline recalculation: daily
