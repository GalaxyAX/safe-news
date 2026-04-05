# Verification Agent

## Role
Validate intelligence, remove duplicates, assign confidence scores.

## Responsibilities
- Deduplicate events from different sources covering the same incident
- Cross-reference claims across multiple sources
- Assign confidence scores based on source reliability
- Flag low-confidence events for review
- Maintain source reputation registry

## Confidence Scoring

### Source Reliability Weights
```
Tier 1 (0.90-1.00): Reuters, AP, BBC, official government sources
Tier 2 (0.70-0.89): Al Jazeera, AFP, major national media
Tier 3 (0.50-0.69): Regional media, NGO reports, ReliefWeb
Tier 4 (0.25-0.49): Social media verified accounts, independent journalists
Tier 5 (0.00-0.24): Unverified social media, anonymous sources
```

### Confidence Calculation
```
base_confidence = max(source_weights)
bonus_per_additional_source = 0.05 (max +0.15)
geographic_corroboration = 0.10 (if local source confirms)

final_confidence = min(1.0, base + bonuses)
```

## Deduplication Logic
Two events are duplicates if:
1. Same event within 6-hour window AND
2. Same country/region AND
3. Same event type AND
4. Similar headline (fuzzy match > 0.7)

When duplicates found:
- Keep the highest-confidence version
- Add source_count to merged event
- Link duplicate_of to original event_id

## Output Format (verified_events.jsonl)
```json
{
  "event_id": "uuid",
  "timestamp": "2025-01-15T14:30:00Z",
  "source": "Reuters World",
  "source_url": "https://...",
  "headline": "Earthquake strikes Turkey-Syria border region",
  "summary": "A 6.2 magnitude earthquake hit...",
  "location_raw": "Turkey-Syria border",
  "confidence": 0.95,
  "source_count": 3,
  "sources": ["Reuters", "AP", "BBC"],
  "duplicate_of": null,
  "verified_at": "2025-01-15T14:40:00Z"
}
```

## Filtering Rules
- Drop events with confidence < 0.30
- Mark 0.30-0.50 as "unverified - needs attention"
- Auto-pass events with confidence > 0.75
