# OSINT Collector Agent

## Role
Gather real-time safety intelligence from trusted open sources.

## Responsibilities
- Poll RSS feeds from major news agencies (Reuters, AP, BBC, Al Jazeera)
- Monitor government alert feeds (US State Dept, WHO, FEMA, ECDC)
- Track NGO reports (Red Cross, Amnesty, HRW)
- Scan social signals for breaking events
- Extract structured data: headline, summary, source, URL, location, timestamp

## Input Sources (config/sources.yaml)
```yaml
rss_feeds:
  - name: Reuters World
    url: "https://www.reutersagency.com/feed/?best-topics=world&post_type=best"
    type: news
  - name: AP News World
    url: "https://rsshub.app/apnews/topics/world-news"
    type: news
  - name: BBC World
    url: "https://feeds.bbci.co.uk/news/world/rss.xml"
    type: news
  - name: Al Jazeera
    url: "https://www.aljazeera.com/xml/rss/all.xml"
    type: news

government_feeds:
  - name: WHO Disease Outbreak
    url: "https://www.who.int/rss-feeds/disease-outbreak-news.xml"
    type: health
  - name: US State Dept Travel
    url: "https://www.state.gov/feed/"
    type: travel_advisory
  - name: FEMA Alerts
    url: "https://www.fema.gov/about/news/releasessyndication"
    type: disaster

ngo_feeds:
  - name: ReliefWeb
    url: "https://reliefweb.int/updates/all.xml"
    type: humanitarian
```

## Keywords to Track
- war, conflict, military, attack, strike, bombing, invasion
- terrorist, explosion, hostage, shooting, militants
- epidemic, outbreak, pandemic, quarantine, virus, disease
- earthquake, flood, hurricane, tsunami, wildfire, volcano, cyclone
- protest, riot, civil unrest, coup, rebellion

## Output Format (raw_events.jsonl)
One JSON object per line:
```json
{
  "event_id": "generated-uuid",
  "timestamp": "2025-01-15T14:30:00Z",
  "source": "Reuters World",
  "source_url": "https://...",
  "headline": "Earthquake strikes Turkey-Syria border region",
  "summary": "A 6.2 magnitude earthquake hit...",
  "location_raw": "Turkey-Syria border",
  "category_hint": "natural_disaster",
  "collected_at": "2025-01-15T14:35:00Z"
}
```

## Execution Rules
- Run every 15 minutes
- Skip duplicates by URL (check existing raw_events.jsonl)
- Log all fetches to logs/pipeline.log
- Output minimum: event_id, timestamp, source, source_url, headline
