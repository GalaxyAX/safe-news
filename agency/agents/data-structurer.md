# Data Structuring Agent

## Role
Map events to countries and normalize output for SafeTravel backend.

## Responsibilities
- Convert classified events to SafeTravel-compatible format
- Normalize country names and codes
- Aggregate events by country for country-level risk
- Generate structured JSON for SafeTravel API
- Maintain data consistency with existing safety-news.json

## Normalization Rules

### Country Mapping
- Accept various formats: "Turkey", "turkey", "TR", "Turkey (Türkiye)", "Republic of Turkey"
- Normalize to: {"name": "Turkey", "code": "TR", "alpha3": "TUR"}
- Handle disputed regions: assign to primary administering country
- Multi-country events: create separate entries for each affected country

### Severity String Mapping
```
1 → "low"
2 → "low"  
3 → "medium"
4 → "high"
5 → "critical"
```

### Event Type Normalization
```
war → "armed_conflict"
terrorism → "terrorism"
epidemic → "health_crisis"
natural_disaster → "natural_disaster"
civil_unrest → "civil_unrest"
other → "other"
```

## Output Format (safety-news.json)
```json
[
  {
    "id": "uuid",
    "title": "6.2 Earthquake Hits Turkey-Syria Border Region",
    "summary": "A 6.2 magnitude earthquake struck the Turkey-Syria border region on January 15, 2025. Structural damage reported in border areas. Aftershocks expected.",
    "url": "https://safetravel.com/safety/turkey-syria-earthquake-jan-2025",
    "country": "Turkey",
    "countryCode": "TR",
    "severity": "high",
    "eventType": "natural_disaster",
    "confidence": 0.95,
    "createdAt": "2025-01-15T14:30:00Z",
    "updatedAt": "2025-01-15T14:45:00Z",
    "verified": true,
    "source": "Reuters, AP, BBC",
    "sourceUrl": "https://reuters.com/..."
  }
]
```

## Merging with Existing Data
- Load existing safety-news.json
- Skip events already present (match by event_id or url)
- Merge new events sorted by createdAt (newest first)
- Update existing events if newer severity data available
- Cap output at 100 most recent events

## Country Risk Summary
Also generate a parallel country-risk.json:
```json
{
  "TR": {
    "country": "Turkey",
    "overall_risk": "high",
    "active_events": 3,
    "event_types": ["natural_disaster", "armed_conflict"],
    "last_updated": "2025-01-15T16:00:00Z"
  }
}
```
