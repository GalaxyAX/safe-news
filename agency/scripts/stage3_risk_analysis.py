#!/usr/bin/env python3
"""
SafeTravel OSINT Pipeline - Stage 3: Risk Analysis
Reads verified_events.jsonl, classifies events by type/severity/location.
"""
import json
import hashlib
import os
from datetime import datetime, timezone

AGENCY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED_FILE = os.path.join(AGENCY_DIR, "data", "verified_events.jsonl")
CLASSIFIED_FILE = os.path.join(AGENCY_DIR, "data", "classified_events.jsonl")

# For loading from original safety-news.json as fallback
ORIGINAL_FILE = os.path.join(AGENCY_DIR, "..", "safety-news.json")

# Country mapping
COUNTRY_MAP = {
    "iraq": ("Iraq", "IQ"), "iran": ("Iran", "IR"), "israel": ("Israel", "IL"),
    "lebanon": ("Lebanon", "LB"), "baghdad": ("Iraq", "IQ"), "tehran": ("Iran", "IR"),
    "beirut": ("Lebanon", "LB"), "tel aviv": ("Israel", "IL"),
    "syria": ("Syria", "SY"), "yemen": ("Yemen", "YE"),
    "turkey": ("Turkey", "TR"), "egypt": ("Egypt", "EG"), "ethiopia": ("Ethiopia", "ET"),
    "japan": ("Japan", "JP"), "tokyo": ("Japan", "JP"),
    "norway": ("Norway", "NO"), "oslo": ("Norway", "NO"),
    "gaza": ("Palestine", "PS"), "palestine": ("Palestine", "PS"),
    "bangladesh": ("Bangladesh", "BD"), "india": ("India", "IN"),
    "north korea": ("North Korea", "KP"), "bahrain": ("Bahrain", "BH"),
    "uae": ("UAE", "AE"), "saudi arabia": ("Saudi Arabia", "SA"),
    "united states": ("United States", "US"), "usa": ("United States", "US"),
    "bushehr": ("Iran", "IR"), "mahshahr": ("Iran", "IR"),
    "strait of hormuz": ("Iran", "IR"), "nile": ("Egypt", "EG"),
    "red sea": ("Yemen", "YE"), "saifee hospital": ("Pakistan", "PK"),
    "pakistan": ("Pakistan", "PK"),
    "armenia": ("Armenia", "AM"), "azerbaijan": ("Azerbaijan", "AZ"),
    "ukraine": ("Ukraine", "UA"), "russia": ("Russia", "RU"),
}

# Event type classification keywords
TYPE_KEYWORDS = {
    "war": ["war", "military", "strike", "airstrike", "missile", "invasion", "attack",
            "shot down", "bomber", "fighter jet", "troops", "combat", "shelling",
            "f-15", "f-35", "iron dome", "idf", "hezbollah", "iran war", "iran-israel"],
    "terrorism": ["terrorist", "bombing", "militant", "extremist", "isis", "al-qaeda",
                  "hostage", "assassination", "suicide", "explosion", "car bomb",
                  "embassy attack", "arrested"],
    "epidemic": ["measles", "outbreak", "epidemic", "pandemic", "disease", "virus",
                 "quarantine", "who", "cdc", "cases surge"],
    "natural_disaster": ["earthquake", "flood", "hurricane", "tsunami", "wildfire",
                         "volcano", "cyclone", "magnitude", "seismic", "disaster",
                         "natural disaster"],
    "civil_unrest": ["protest", "protester", "rally", "demonstration", "riot", "coup",
                     "civil unrest", "march", "denounce", "gathered"],
}

def detect_country(text):
    """Detect country/location from text using keyword matching."""
    text_lower = text.lower()
    # Check multi-word entries first (longer keys first)
    for key in sorted(COUNTRY_MAP.keys(), key=len, reverse=True):
        if key in text_lower:
            return COUNTRY_MAP[key]
    return (None, None)

def classify_event_type(text):
    """Classify event type based on keyword matching."""
    text_lower = text.lower()
    scores = {}
    for event_type, keywords in TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[event_type] = score
    if not scores:
        return "other"
    return max(scores, key=scores.get)

def estimate_severity(event_type, text):
    """Estimate severity from event type and content."""
    text_lower = text.lower()
    if event_type == "war":
        if any(w in text_lower for w in ["killed", "dead", "casualties", "wounded", "destroyed", "civilian"]):
            return 5
        if any(w in text_lower for w in ["missile", "strike", "airstrike"]):
            return 4
        if any(w in text_lower for w in ["tension", "diplomatic", "warning"]):
            return 3
        return 4
    elif event_type == "terrorism":
        if any(w in text_lower for w in ["killed", "dead", "fatalities", "mass"]):
            return 5
        return 4
    elif event_type == "epidemic":
        if any(w in text_lower for w in ["surge", "outbreak", "emergency", "pandemic"]):
            return 4
        return 3
    elif event_type == "natural_disaster":
        if any(w in text_lower for w in ["magnitude", "tsunami", "major", "devastating"]):
            return 4
        return 2
    elif event_type == "civil_unrest":
        if any(w in text_lower for w in ["violence", "clash", "crackdown", "arrest"]):
            return 4
        if any(w in text_lower for w in ["protest", "rally", "demonstration"]):
            return 2
        return 2
    return 1

def severity_to_risk(severity):
    if severity >= 5: return "critical"
    if severity == 4: return "high"
    if severity == 3: return "medium"
    return "low"

def main():
    events = []

    # Try verified events first, fallback to original safety-news.json
    if os.path.exists(VERIFIED_FILE):
        with open(VERIFIED_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    elif os.path.exists(ORIGINAL_FILE):
        with open(ORIGINAL_FILE) as f:
            raw = json.load(f)
            for item in raw:
                # Convert to verified event format
                combined_text = f"{item.get('title', '')} {item.get('summary', '')} {item.get('content', '')}"
                events.append({
                    "event_id": item.get("id", str(hashlib.md5(item.get("slug", "").encode()).hexdigest()[:8])),
                    "timestamp": item.get("datePublished", datetime.now(timezone.utc).isoformat()),
                    "source": "SafeTravel Intelligence",
                    "source_url": f"https://github.com/GalaxyAX/safe-news/blob/main/image/{item.get('imageUrl', '').split('/')[-1]}" if item.get("imageUrl") else "",
                    "headline": item.get("title", ""),
                    "summary": item.get("summary", ""),
                    "full_content": item.get("content", ""),
                    "location_raw": item.get("category", ""),
                    "confidence": 0.85,  # Pre-verified articles
                    "source_count": 1,
                    "tags": item.get("tags", []),
                    "category_hint": item.get("category", "")
                })

    classified = []
    for event in events:
        combined = f"{event.get('headline', '')} {event.get('summary', '')} {event.get('full_content', '')} {' '.join(event.get('tags', []))}"
        country_name, country_code = detect_country(combined)
        event_type = classify_event_type(combined)
        severity = estimate_severity(event_type, combined)
        risk_level = severity_to_risk(severity)

        # Determine affected countries
        affected = [country_code] if country_code else []
        if country_code == "IR" and any(w in combined.lower() for w in ["israel", "lebanon"]):
            if "IL" not in affected: affected.append("IL")
            if "LB" not in affected: affected.append("LB")
        if country_code == "TR" and "syria" in combined.lower():
            if "SY" not in affected: affected.append("SY")

        c_event = {
            "event_id": event["event_id"],
            "timestamp": event.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "headline": event.get("headline", ""),
            "summary": event.get("summary", ""),
            "event_type": event_type,
            "severity": severity,
            "risk_level": risk_level,
            "country_code": country_code or "XX",
            "country_name": country_name or "Unknown",
            "affected_countries": affected if affected else [country_code or "XX"],
            "analysis": f"{event_type.replace('_', ' ').title()} event in {country_name or 'Unknown region'}. Severity {severity}/5, risk level {risk_level}.",
            "escalation_risk": "high" if severity >= 4 else "medium" if severity >= 3 else "low",
            "classified_at": datetime.now(timezone.utc).isoformat()
        }
        classified.append(c_event)

    os.makedirs(os.path.dirname(CLASSIFIED_FILE), exist_ok=True)
    with open(CLASSIFIED_FILE, "w") as f:
        for c in classified:
            f.write(json.dumps(c) + "\n")

    # Summary
    type_counts = {}
    risk_counts = {}
    for c in classified:
        type_counts[c["event_type"]] = type_counts.get(c["event_type"], 0) + 1
        risk_counts[c["risk_level"]] = risk_counts.get(c["risk_level"], 0) + 1

    print(json.dumps({
        "stage": 3,
        "status": "complete",
        "total_classified": len(classified),
        "by_type": type_counts,
        "by_risk": risk_counts
    }, indent=2))

if __name__ == "__main__":
    main()
