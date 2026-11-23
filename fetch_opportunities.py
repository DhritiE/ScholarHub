import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"

SEARCH_QUERIES = [
    # Core High School & Youth
    ("high school students", "Scholarship"),
    ("high school summer", "Summer Program"),
    ("high school research", "Research"),
    ("high school internship", "Summer Program"),
    ("high school senior", "Scholarship"),
    ("high school fellowship", "Research"),
    ("secondary school", "Scholarship"),
    ("teen leadership", "Summer Program"),
    ("adolescent youth", "Summer Program"),
    ("pre-college", "Summer Program"),
    ("college prep", "Scholarship"),
    ("college readiness", "Scholarship"),
    ("upward bound", "Summer Program"),
    ("talent search youth", "Scholarship"),

    # STEM, Coding, Engineering & Medicine
    ("youth stem", "Research"),
    ("youth science", "Research"),
    ("underrepresented youth stem", "Research"),
    ("computer science youth", "Research"),
    ("coding youth", "Summer Program"),
    ("robotics youth", "Summer Program"),
    ("engineering high school", "Research"),
    ("mathematics youth", "Research"),
    ("biomedical youth", "Research"),
    ("health careers youth", "Summer Program"),
    ("environmental youth", "Research"),
    ("climate youth", "Research"),
    ("ocean science youth", "Research"),
    ("space education youth", "Research"),
    ("cybersecurity youth", "Summer Program"),
    ("artificial intelligence education", "Research"),

    # Humanities, Arts, Civics & Leadership
    ("youth civic engagement", "Summer Program"),
    ("youth arts", "Summer Program"),
    ("humanities youth", "Summer Program"),
    ("youth journalism", "Summer Program"),
    ("youth entrepreneurship", "Summer Program"),
    ("financial literacy youth", "Scholarship"),
    ("youth mentorship", "Summer Program"),
    ("youth service", "Summer Program"),
    ("community service youth", "Scholarship"),
    ("youth agriculture", "Summer Program"),
    ("youth conservation", "Summer Program"),

    # General Student & Summer Institutes
    ("student scholarship", "Scholarship"),
    ("summer institute high school", "Summer Program"),
    ("summer academy youth", "Summer Program"),
    ("youth workforce", "Summer Program")
]

def load_existing():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize_item(title, default_category):
    t = title.lower()
    if any(word in t for word in ["summer", "camp", "internship", "academy", "institute", "mentorship", "workforce"]):
        return "Summer Program"
    if any(word in t for word in ["research", "science", "stem", "lab", "fellowship", "environmental", "biomedical", "engineering"]):
        return "Research"
    return default_category

def assign_grades(keyword, title):
    combined = f"{keyword} {title}".lower()
    if any(word in combined for word in ["senior", "college prep", "college readiness", "12th"]):
        return [11, 12]
    return [9, 10, 11, 12]

def format_award(item):
    ceiling = item.get("awardCeiling")
    if ceiling and str(ceiling).isdigit() and int(ceiling) > 0:
        return f"Up to ${int(ceiling):,}"
    return "Federal Grant / Program"

def fetch_grants_gov():
    """Fetches open and forecasted opportunities across 45 keywords from Grants.gov."""
    url = "https://api.grants.gov/v1/api/search2"
    all_fetched = []

    for keyword, default_cat in SEARCH_QUERIES:
        payload = json.dumps({
            "keyword": keyword,
            "oppStatuses": "posted|forecasted",
            "rows": 500
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

            agency = item.get("agency", "U.S. Federal Agency")
            opp_num = item.get("number", "")
            desc = f"Sponsored by {agency}"
            if opp_num:
                desc += f" (Opportunity #{opp_num})"
            desc += ". Click below for full eligibility requirements and application instructions."

            all_fetched.append({
                "title": title,
                "category": categorize_item(title, default_cat),
                "grades": assign_grades(keyword, title),
                "deadline": item.get("closeDate") or "Rolling / Check Site",
                "amountOrCost": format_award(item),
                "description": desc,
                "link": f"https://www.grants.gov/search-results-detail/{opp_id}"
            })

        time.sleep(0.5)

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

    print(f"Added {added_count} new unique opportunities. Total in database: {len(existing)}")
    return existing

if __name__ == "__main__":
    current_data = load_existing()
    new_data = fetch_grants_gov()
    updated_data = merge_and_deduplicate(current_data, new_data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2)
