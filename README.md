# ScholarHub

A centralized web directory helping high school students (Grades 9–12) discover **Scholarships**, **Research Opportunities**, and **Summer Programs** filtered by grade level.

## Files Included
- `index.html` — Main structure and filter controls
- `styles.css` — Responsive styling and card grid layout
- `script.js` — Dynamic filtering by grade level, category, keyword search, and saved bookmarks
- `scholarhub-opportunities.json` — Database of 25+ curated high school opportunities
- `favicon.svg` — Custom ScholarHub graduation cap icon

## How to Add More Opportunities
Open `scholarhub-opportunities.json` and append a new object following this template:

```json
{
  "id": 26,
  "title": "Program or Scholarship Name",
  "category": "Scholarship",
  "grades": [11, 12],
  "deadline": "January",
  "amountOrCost": "$5,000",
  "description": "Short summary of eligibility and benefits.",
  "link": "https://example.org"
}
```
