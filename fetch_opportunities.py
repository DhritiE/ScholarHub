import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"
UC_FILE = "uc-opportunities.json"

QUERIES = [
    ("high school students", "Scholarship"), ("high school summer", "Summer Program"),
    ("high school research", "Research"), ("high school internship", "Summer Program"),
    ("high school senior", "Scholarship"), ("high school fellowship", "Research"),
    ("secondary school", "Scholarship"), ("teen leadership", "Summer Program"),
    ("adolescent youth", "Summer Program"), ("pre-college", "Summer Program"),
    ("college prep", "Scholarship"), ("college readiness", "Scholarship"),
    ("upward bound", "Summer Program"), ("talent search youth", "Scholarship"),
    ("youth stem", "Research"), ("youth science", "Research"),
    ("computer science youth", "Research"), ("coding youth", "Summer Program"),
    ("robotics youth", "Summer Program"), ("engineering high school", "Research"),
    ("mathematics youth", "Research"), ("biomedical youth", "Research"),
    ("health careers youth", "Summer Program"), ("environmental youth", "Research"),
    ("climate youth", "Research"), ("ocean science youth", "Research"),
    ("space education youth", "Research"), ("cybersecurity youth", "Summer Program"),
    ("youth civic engagement", "Summer Program"), ("youth arts", "Summer Program"),
    ("humanities youth", "Summer Program"), ("youth entrepreneurship", "Summer Program"),
    ("youth mentorship", "Summer Program"), ("student scholarship", "Scholarship"),
    ("summer institute high school", "Summer Program")
]

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
        payload = json.dumps({"keyword": kw, "oppStatuses": "posted|forecasted", "rows": 300}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                hits = json.loads(r.read().decode("utf-8")).get("data", {}).get("oppHits", [])
        except Exception:
            continue
        for item in hits:
            title = item.get("title", "").strip()
            oid = item.get("id", "")
            if title and oid:
                c = item.get("awardCeiling")
                award = f"Up to ${int(c):,}" if c and str(c).isdigit() and int(c) > 0 else "Federal Grant / Program"
                results.append({
                    "title": title, "category": cat,
                    "grades": [11, 12] if "senior" in kw else [9, 10, 11, 12],
                    "deadline": item.get("closeDate") or "Rolling / Check Site",
                    "amountOrCost": award,
                    "description": f"Sponsored by {item.get('agency', 'U.S. Federal Agency')}. Click below for details.",
                    "link": f"https://www.grants.gov/search-results-detail/{oid}"
                })
        time.sleep(0.2)
    return results

if __name__ == "__main__":
    existing = load_json(DATA_FILE)
    incoming = load_json(UC_FILE) + fetch_grants()
    seen = {x["title"].strip().lower() for x in existing if isinstance(x, dict) and "title" in x}
    max_id = max((x.get("id", 0) for x in existing if isinstance(x, dict)), default=0)
    for item in incoming:
        k = item["title"].strip().lower()
        if k not in seen:
            max_id += 1
            item["id"] = max_id
            existing.append(item)
            seen.add(k)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
    print(f"Done! Total: {len(existing)}")
