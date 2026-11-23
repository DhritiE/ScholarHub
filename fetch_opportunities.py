import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"

QUERIES = [
    ("high school", "Scholarship"), ("secondary school", "Scholarship"),
    ("students", "Scholarship"), ("student", "Scholarship"),
    ("scholarship", "Scholarship"), ("fellowship", "Research"),
    ("internship", "Summer Program"), ("summer", "Summer Program"),
    ("youth", "Summer Program"), ("teen", "Summer Program"),
    ("adolescent", "Summer Program"), ("k-12", "Research"),
    ("pre-college", "Summer Program"), ("college prep", "Scholarship"),
    ("college readiness", "Scholarship"), ("upward bound", "Summer Program"),
    ("talent search", "Scholarship"), ("mentorship", "Summer Program"),
    ("leadership", "Summer Program"), ("stem", "Research"),
    ("science", "Research"), ("mathematics", "Research"),
    ("engineering", "Research"), ("technology", "Research"),
    ("computer science", "Research"), ("robotics", "Summer Program"),
    ("cybersecurity", "Summer Program"), ("artificial intelligence", "Research"),
    ("biomedical", "Research"), ("medical", "Research"),
    ("health careers", "Summer Program"), ("public health", "Research"),
    ("clinical", "Summer Program"), ("hospital", "Summer Program"),
    ("neuroscience", "Research"), ("cancer research", "Research"),
    ("environmental", "Research"), ("climate", "Research"),
    ("marine science", "Research"), ("space", "Research"),
    ("arts", "Summer Program"), ("humanities", "Summer Program"),
    ("civic engagement", "Summer Program"), ("entrepreneurship", "Summer Program")
]

EXCLUDE_WORDS = [
    "postdoctoral", "postdoc", "doctoral", "phd", "ph.d.", "dissertation",
    "faculty", "law school", "residency", "sbir", "sttr"
]

def is_allowed(title):
    t = title.lower()
    return not any(bad in t for bad in EXCLUDE_WORDS)

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def fetch_grants():
    url = "https://api.grants.gov/v1/api/search2"
    results = []
    for kw, cat in QUERIES:
        payload = json.dumps({"keyword": kw, "oppStatuses": "posted|forecasted", "rows": 500}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        })
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                hits = json.loads(r.read().decode("utf-8")).get("data", {}).get("oppHits", [])
        except Exception as e:
            print(f"Skipping '{kw}': {e}")
            continue
        for item in hits:
            title = item.get("title", "").strip()
            oid = item.get("id", "")
            if title and oid and is_allowed(title):
                c = item.get("awardCeiling")
                award = f"Up to ${int(c):,}" if c and str(c).isdigit() and int(c) > 0 else "Grant / Program"
                results.append({
                    "title": title,
                    "category": cat,
                    "grades": [11, 12] if "senior" in title.lower() else [9, 10, 11, 12],
                    "deadline": item.get("closeDate") or "Rolling / Check Site",
                    "amountOrCost": award,
                    "description": f"Sponsored by {item.get('agency', 'U.S. Federal Agency')}. Click below for eligibility and application details.",
                    "link": f"https://www.grants.gov/search-results-detail/{oid}"
                })
        time.sleep(0.15)
    return results

if __name__ == "__main__":
    existing = load_json(DATA_FILE)
    incoming = fetch_grants()

    merged = []
    seen = set()
    for idx, item in enumerate(existing + incoming, start=1):
        if not isinstance(item, dict):
            continue
        title = item.get("title", "").strip()
        k = title.lower()
        if title and k not in seen:
            item["id"] = idx
            merged.append(item)
            seen.add(k)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    print(f"Done! Total opportunities: {len(merged)}")
