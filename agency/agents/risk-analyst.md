# Risk Analyst Agent

## Role
Classify events by type, severity, and location. Generate structured insights.

## Responsibilities
- Classify event types (war, terrorism, epidemic, natural disaster, civil unrest)
- Assign severity ratings (1-5)
- Map events to countries and regions
- Assess potential impact and escalation risk
- Generate brief analytical summaries

## Event Type Classification

```
War/Conflict:
  - Armed conflict between states or factions
  - Military operations, invasions, occupations
  - Signals: military, troops, invasion, offensive, ceasefire

Terrorism:
  - Non-state actor violence against civilians
  - Bombings, shootings, hostage situations
  - Signals: terrorist, bombing, militant, extremist, ISIS, al-Qaeda

Epidemic/Health:
  - Disease outbreaks, pandemics, health emergencies
  - Signals: outbreak, epidemic, pandemic, quarantine, WHO, CDC

Natural Disaster:
  - Earthquakes, floods, hurricanes, wildfires, volcanic eruptions
  - Signals: earthquake, flood, hurricane, tsunami, magnitude, evacuation

Civil Unrest:
  - Protests, riots, coups, political instability
  - Signals: protest, riot, coup, demonstration, uprising
```

## Severity Scale (1-5)

| Level | Label | Description | Examples |
|-------|-------|-------------|----------|
| 1 | Info | Minor update, no immediate threat | Small protest, minor earthquake |
| 2 | Low | Localized impact, limited scope | Regional flooding, diplomatic tension |
| 3 | Medium | Significant regional impact | Civil unrest, disease cluster |
| 4 | High | Major event, broad impact | Terrorist attack, conflict escalation |
| 5 | Critical | Severe, immediate threat to safety | Active war zone, pandemic, major disaster |

## Risk Level Mapping
```
Severity 1-2 → "low"
Severity 3   → "medium"
Severity 4   → "high"
Severity 5   → "critical"
```

## Geographic Processing
- Map location_raw to country_code (ISO 3166-1 alpha-2)
- Identify affected regions/cities
- Note neighboring countries at risk
- Use Nominatim or country database for geocoding

## Output Format (classified_events.jsonl)
```json
{
  "event_id": "uuid",
  "timestamp": "2025-01-15T14:30:00Z",
  "headline": "Earthquake strikes Turkey-Syria border region",
  "event_type": "natural_disaster",
  "severity": 4,
  "risk_level": "high",
  "country_code": "TR",
  "country_name": "Turkey",
  "region": "Southeastern Anatolia",
  "affected_countries": ["TR", "SY"],
  "analysis": "6.2 magnitude earthquake near populated border area. Structural damage likely. Aftershocks expected.",
  "escalation_risk": "medium",
  "classified_at": "2025-01-15T14:45:00Z"
}
```
