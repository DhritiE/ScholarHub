import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"
UC_FILE = "uc-opportunities.json"
MED_FILE = "medical-opportunities.json"

QUERIES = [
    ("high school students", "Scholarship"), ("high school summer", "Summer Program"),
    ("high school research", "Research"), ("high school internship", "Summer Program"),
    ("high school senior", "Scholarship"), ("high school biomedical", "Research"),
    ("high school health", "Summer Program"), ("high school clinical", "Summer Program"),
    ("high school medicine", "Research"), ("high school stem", "Research"),
    ("secondary school", "Scholarship"), ("pre-college", "Summer Program"),
    ("upward bound", "Summer Program"), ("talent search", "Scholarship"),
    ("teen leadership", "Summer Program"), ("youth biomedical", "Research"),
    ("youth health careers", "Summer Program"), ("youth medical", "Research"),
    ("youth hospital", "Summer Program"), ("youth neuroscience", "Research"),
    ("youth stem", "Research"), ("youth science", "Research"),
    ("youth robotics", "Summer Program"), ("youth cybersecurity", "Summer Program"),
    ("youth arts", "Summer Program"), ("youth entrepreneurship", "Summer Program")
]

EXCLUDE_WORDS = [
    "postdoctoral", "postdoc", "doctoral", "phd", "ph.d.", "dissertation",
    "graduate student", "graduate fellowship", "graduate research", "faculty",
    "undergraduate only", "college sophomore", "college junior", "law school",
    "medical school", "residency", "veteran", "small business", "sbir", "sttr"
]

def is_valid_hs(title):
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
        payload = json.dumps({"keyword": kw, "oppStatuses": "posted|forecasted", "rows": 250}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                hits = json.loads(r.read().decode("utf-8")).get("data", {}).get("oppHits", [])
        except Exception as e:
            print(f"Skipping '{kw}': {e}")
            continue
        for item in hits:
            title = item.get("title", "").strip()
            oid = item.get("id", "")
            if title and oid and is_valid_hs(title):
                c = item.get("awardCeiling")
                award = f"Up to ${int(c):,}" if c and str(c).isdigit() and int(c) > 0 else "Federal Grant / Program"
                results.append({
                    "title": title, "category": cat,
                    "grades": [11, 12] if "senior" in kw else [9, 10, 11, 12],
                    "deadline": item.get("closeDate") or "Rolling / Check Site",
                    "amountOrCost": award,
                    "description": f"Sponsored by {item.get('agency', 'U.S. Federal Agency')}. Click below for high school eligibility and details.",
                    "link": f"https://www.grants.gov/search-results-detail/{oid}"
                })
        time.sleep(0.2)
    return results

if __name__ == "__main__":
    curated = load_json(UC_FILE) + load_json(MED_FILE)
    existing = [x for x in load_json(DATA_FILE) if isinstance(x, dict) and is_valid_hs(x.get("title", ""))]
    incoming = curated + fetch_grants()

    cleaned = []
    seen = set()
    for idx, item in enumerate(curated + existing + incoming, start=1):
        title = item.get("title", "").strip()
        k = title.lower()
        if title and k not in seen:
            item["id"] = idx
            cleaned.append(item)
            seen.add(k)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Done! Total opportunities: {len(cleaned)}")
