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
    ("high school stem", "Research"), ("high school science", "Research"),
    ("high school engineering", "Research"), ("high school coding", "Summer Program"),
    ("secondary school", "Scholarship"), ("pre-college", "Summer Program"),
    ("upward bound", "Summer Program"), ("talent search", "Scholarship"),
    ("teen leadership", "Summer Program"), ("youth stem", "Research"),
    ("youth science", "Research"), ("youth robotics", "Summer Program"),
    ("youth biomedical", "Research"), ("youth environmental", "Research"),
    ("youth cybersecurity", "Summer Program"), ("youth arts", "Summer Program"),
    ("youth entrepreneurship", "Summer Program"), ("k-12 stem", "Research")
]

INCLUDE_WORDS = [
    "high school", "secondary school", "pre-college", "precollege", "teen",
    "youth", "k-12", "upward bound", "talent search", "9th", "10th", "11th", "12th",
    "uc ", "ucla", "ucsd", "uci", "ucsb", "ucsf", "berkeley", "cosmos", "regents", "blue and gold"
]

EXCLUDE_WORDS = [
    "postdoctoral", "postdoc", "doctoral", "phd", "ph.d.", "dissertation",
    "graduate student", "graduate fellowship", "graduate research", "faculty",
    "undergraduate only", "college sophomore", "college junior", "law school",
    "medical school", "residency", "veteran", "small business", "sbirs", "sttr"
]

def is_high_school(title):
    t = title.lower()
    if any(bad in t for bad in EXCLUDE_WORDS):
        return False
    return any(good in t for good in INCLUDE_WORDS)

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
            if title and oid and is_high_school(title):
                c = item.get("awardCeiling")
                award = f"Up to ${int(c):,}" if c and str(c).isdigit() and int(c) > 0 else "Federal Grant / Program"
                results.append({
                    "title": title, "category": cat,
                    "grades": [11, 12] if "senior" in title.lower() else [9, 10, 11, 12],
                    "deadline": item.get("closeDate") or "Rolling / Check Site",
                    "amountOrCost": award,
                    "description": f"Sponsored by {item.get('agency', 'U.S. Federal Agency')}. Click below for high school eligibility and details.",
                    "link": f"https://www.grants.gov/search-results-detail/{oid}"
                })
        time.sleep(0.2)
    return results

if __name__ == "__main__":
    uc_items = load_json(UC_FILE)
    existing = [x for x in load_json(DATA_FILE) if isinstance(x, dict) and is_high_school(x.get("title", ""))]
    incoming = uc_items + fetch_grants()

    cleaned = []
    seen = set()
    for idx, item in enumerate(uc_items + existing + incoming, start=1):
        title = item.get("title", "").strip()
        k = title.lower()
        if title and k not in seen:
            item["id"] = idx
            cleaned.append(item)
            seen.add(k)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Done! High school opportunities: {len(cleaned)}")
