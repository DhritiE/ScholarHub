import json
import os
import urllib.request
import urllib.parse

DATA_FILE = "scholarhub-opportunities.json"

def load_existing():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_careeronestop_scholarships():
    """
    Fetches high school scholarships from the U.S. Department of Labor's
    CareerOneStop API if API credentials are configured in GitHub Secrets.
    Free API key signup: https://www.careeronestop.org/Developers/WebAPI/registration.aspx
    """
    user_id = os.environ.get("COS_USER_ID")
    api_token = os.environ.get("COS_API_TOKEN")

    if not user_id or not api_token:
        print("No CareerOneStop API keys found in environment. Skipping API fetch.")
        return []

    keyword = urllib.parse.quote("high school")
    url = f"https://api.careeronestop.org/v1/scholarship/{user_id}/{keyword}/0/100"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw_data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching from CareerOneStop API: {e}")
        return []

    fetched = []
    for item in raw_data.get("Scholarships", []):
        title = item.get("ScholarshipName", "").strip()
        link = item.get("WebAddress", "").strip()
        if not title or not link:
            continue

        if not link.startswith("http"):
            link = "https://" + link

        amount = item.get("AwardAmount") or "Varies"
        deadline = item.get("Deadline") or "Check Website"
        desc = (
            item.get("Purpose")
            or item.get("Qualifications")
            or "Verified national scholarship opportunity."
        ).strip()

        fetched.append({
            "title": title,
            "category": "Scholarship",
            "grades": [11, 12],
            "deadline": deadline,
            "amountOrCost": str(amount),
            "description": desc[:240] + ("..." if len(desc) > 240 else ""),
            "link": link
        })

    print(f"Fetched {len(fetched)} opportunities from CareerOneStop.")
    return fetched

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
    api_data = fetch_careeronestop_scholarships()
    updated_data = merge_and_deduplicate(current_data, api_data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2)
