import json
import os
import subprocess

DATA_FILE = "scholarhub-opportunities.json"
UC_FILE = "uc-opportunities.json"
MED_FILE = "medical-opportunities.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def recover_largest_from_git():
    best = load_json(DATA_FILE)
    try:
        commits = subprocess.check_output(
            ["git", "log", "--format=%H", "-n", "25", "--", DATA_FILE],
            text=True
        ).splitlines()
        for sha in commits:
            raw = subprocess.check_output(["git", "show", f"{sha}:{DATA_FILE}"], text=True)
            items = json.loads(raw)
            if isinstance(items, list) and len(items) > len(best):
                best = items
    except Exception as e:
        print(f"Git history check: {e}")
    return best

if __name__ == "__main__":
    curated = load_json(UC_FILE) + load_json(MED_FILE)
    historical = recover_largest_from_git()

    merged = []
    seen = set()
    for idx, item in enumerate(curated + historical, start=1):
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
    print(f"Done! Restored and merged total opportunities: {len(merged)}")
