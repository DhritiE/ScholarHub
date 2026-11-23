import json
import os
import urllib.parse
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"
UC_FILE = "uc-opportunities.json"
MED_FILE = "medical-opportunities.json"

NSF_QUERIES = [
    "high school students",
    "high school summer",
    "high school research",
    "secondary school stem",
    "pre-college",
    "youth stem",
    "high school internship",
    "high school robotics",
    "high school computer science",
    "high school biomedical"
]

EXCLUDE_WORDS = [
    "postdoctoral", "postdoc", "doctoral", "phd", "dissertation",
    "graduate student", "graduate fellowship", "faculty", "undergraduate only"
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

def fetch_nsf_programs():
    results = []
    for kw in NSF_QUERIES:
        q = urllib.parse.quote(kw)
        url = f"https://api.nsf.gov/services/v1/awards.json?keyword={q}&printFields=id,title,agency,fundsObligatedAmt,expDate,awardeeName"
        req = urllib.request.Request(url, headers={"User-Agent": "ScholarHub/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                awards = json.loads(r.read().decode("utf-8")).get("response", {}).get("award", [])
        except Exception as e:
            print(f"NSF skip '{kw}': {e}")
            continue

        for item in awards:
            title = item.get("title", "").strip()
            aid = item.get("id", "")
            if not title or not aid or not is_valid_hs(title):
                continue
            org = item.get("awardeeName", "National Science Foundation Partner")
            amt = item.get("fundsObligatedAmt", "")
            award_str = f"Funded (${int(amt):,})" if str(amt).isdigit() and int(amt) > 0 else "NSF Youth STEM Program"
            cat = "Summer Program" if any(w in title.lower() for w in ["summer", "camp", "internship"]) else "Research"
            results.append({
                "title": title,
                "category": cat,
                "grades": [9, 10, 11, 12],
                "deadline": item.get("expDate") or "Annual / Check Program Site",
                "amountOrCost": award_str,
                "description": f"NSF-funded youth/high school STEM program hosted by {org}.",
                "link": f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={aid}"
            })
    return results

if __name__ == "__main__":
    curated = load_json(UC_FILE) + load_json(MED_FILE)
    existing = [x for x in load_json(DATA_FILE) if isinstance(x, dict) and is_valid_hs(x.get("title", ""))]
    incoming = curated + fetch_nsf_programs()

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
