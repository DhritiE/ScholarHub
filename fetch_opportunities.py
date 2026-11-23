import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"

SEARCH_QUERIES = [
    ("high school students", "Scholarship"),
    ("high school summer", "Summer Program"),
    ("high school research", "Research"),
    ("youth stem", "Research"),
    ("high school internship", "Summer Program"),
    ("secondary school scholarship", "Scholarship"),
    ("high school senior", "Scholarship"),
    ("high school fellowship", "Research"),
    ("teen leadership", "Summer Program"),
    ("youth science", "Research"),
    ("college prep", "Scholarship"),
    ("pre-college", "Summer Program"),
    ("youth internship", "Summer Program"),
    ("youth mentorship", "Summer Program"),
    ("youth civic engagement", "Summer Program"),
    ("youth arts", "Summer Program"),
    ("environmental youth", "Research"),
    ("student scholarship", "Scholarship"),
    ("summer institute high school", "Summer Program"),
    ("summer academy youth", "Summer Program"),
    ("adolescent education", "Scholarship"),
    ("underrepresented youth stem", "Research")
]

def load_existing():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize_item(title, default_category):
    t = title.lower()
    if any(word in t for word in ["summer", "camp", "internship", "academy", "institute", "mentorship"]):
        return "Summer Program"
    if any(word in t for word in ["research", "science", "stem", "lab", "fellowship", "environmental"]):
        return "Research"
    return default_category

def assign_grades(keyword):
    k = keyword.lower()
    if "senior" in k or "college prep" in k:
        return [11, 12]
    return [9, 10, 11, 12]

def fetch_public_grants():
    """Fetches open youth/high-school opportunities across 22 keywords from Grants.gov."""
    url = "https://api.grants.gov/v1/api/search2"
    all_fetched = []

    for keyword, default_cat in SEARCH_QUERIES:
        payload = json.dumps({
            "keyword": keyword,
            "oppStatuses": "posted|forecasted",
            "rows": 250
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                raw_data = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"Error fetching '{keyword}': {e}")
            continue

        hits = raw_data.get("data", {}).get("oppHits", [])
        print(f"Keyword '{keyword}': found {len(hits)} results.")

        for item in hits:
            title = item.get("title", "").strip()
            opp_id = item.get("id", "")
            if not title or not opp_id:
                continue

            all_fetched.append({
                "title": title,
                "category": categorize_item(title, default_cat),
                "grades": assign_grades(keyword),
                "deadline": item.get("closeDate") or "Check Website",
                "amountOrCost": "Federal Grant / Program",
                "description": f"Sponsored by {item.get('agency', 'U.S. Federal Agency')}. Click below for full eligibility and application details.",
                "link": f"https://www.grants.gov/search-results-detail/{opp_id}"
            })

        time.sleep(0.8)

    return all_fetched

def merge_and_deduplicate(existing, incoming):
    seen_titles = {item["title"].strip().lower() for item in existing}
    max_id = max((item.get("id", 0) for item in existing), default=0)

    added_count = 0
    for item in incoming:
        key = item["title"].strip().lower()
        if key not in seen_titles:
            max_id += 1
            item["id"] = max_id
            existing.append(item)
            seen_titles.add(key)
            added_count += 1

    print(f"Added {added_count} new unique opportunities. Total: {len(existing)}")
    return existing

if __name__ == "__main__":
    current_data = load_existing()
    new_data = fetch_public_grants()
    updated_data = merge_and_deduplicate(current_data, new_data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2)
        
