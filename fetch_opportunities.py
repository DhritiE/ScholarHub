import json
import os
import urllib.parse
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"

NSF_TOPICS = [
    ("high school students", "Research"),
    ("high school summer", "Summer Program"),
    ("high school internship", "Summer Program"),
    ("high school research", "Research"),
    ("secondary school", "Scholarship"),
    ("pre-college", "Summer Program"),
    ("youth stem", "Research"),
    ("youth science", "Research"),
    ("youth biomedical", "Research"),
    ("youth health", "Summer Program"),
    ("youth engineering", "Research"),
    ("youth computer science", "Research"),
    ("youth robotics", "Summer Program"),
    ("youth cybersecurity", "Summer Program"),
    ("youth environmental", "Research"),
    ("upward bound", "Scholarship"),
    ("talent search", "Scholarship"),
    ("k-12 stem", "Research")
]

EXCLUDE_WORDS = [
    "postdoctoral", "postdoc", "doctoral", "phd", "ph.d.",
    "dissertation", "faculty", "law school", "residency"
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

def fetch_nsf():
    results = []
    for kw, cat in NSF_TOPICS:
        q = urllib.parse.quote(kw)
        url = (
            f"https://api.nsf.gov/services/v1/awards.json?keyword={q}"
            "&rpp=100&printFields=id,title,fundsObligatedAmt,expDate,awardeeName,awardeeCity,awardeeStateCode"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "ScholarHub/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                awards = json.loads(r.read().decode("utf-8")).get("response", {}).get("award", [])
        except Exception as e:
            print(f"Skipping '{kw}': {e}")
            continue

        for item in awards:
            title = item.get("title", "").strip()
            aid = item.get("id", "")
            if not title or not aid or any(bad in title.lower() for bad in EXCLUDE_WORDS):
                continue
            amt = item.get("fundsObligatedAmt", "")
            org = item.get("awardeeName", "NSF Partner Institution")
            city = item.get("awardeeCity", "")
            state = item.get("awardeeStateCode", "")
            loc = f" ({city}, {state})" if city and state else ""
            results.append({
                "title": title,
                "category": cat,
                "grades": [9, 10, 11, 12],
                "deadline": item.get("expDate") or "Annual / Check Program Site",
                "amountOrCost": f"Funded (${int(amt):,})" if str(amt).isdigit() and int(amt) > 0 else "NSF Youth Program",
                "description": f"NSF-funded high school/youth program hosted by {org}{loc}.",
                "link": f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={aid}"
            })
    return results

if __name__ == "__main__":
    existing = load_json(DATA_FILE)
    incoming = fetch_nsf()

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
