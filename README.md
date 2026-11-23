# ScholarHub starter prototype

This is a free, responsive Progressive Web App (PWA) starter for the scholarship and educational-opportunity finder.

## What's included
- Responsive desktop and mobile layout
- Grade 9–12 browsing
- Search and filters for opportunity type, grade, and deadline
- Save/unsave opportunities using browser local storage
- PWA manifest and basic service worker
- Starter set of real, source-linked listings (checked November 23, 2026)

## Important
The included starter listings link to official provider pages. Eligibility, deadlines, costs, and availability can change. Confirm all details with the provider before applying. The initial database is intentionally small; expand it only with source-linked records and clear verification dates.

## Preview locally
Open `index.html` in a browser. Some PWA features require the app to be served over HTTPS or localhost.

## Free publishing path
1. Create a free GitHub account.
2. Create a public repository named `scholarhub`.
3. Upload all files in this folder.
4. In repository Settings, open Pages and configure deployment from the main branch.
5. GitHub Pages will provide a free `github.io` website address for the project.

Alternatively, deploy the folder using Cloudflare Pages' free tier.

## Next development steps
1. Replace fictional demo listings with verified opportunities.
2. Create a structured opportunity review process.
3. Add Supabase only when shared accounts and cloud-synced saved items are needed.
4. Add privacy protections and moderation before accepting student accounts or user submissions.

## Data fields recommended for each listing
id, title, provider, opportunity_type, eligible_grades, location, remote_status, amount_or_compensation, deadline, deadline_type, eligibility_summary, requirements, official_url, source_url, last_verified_at, status, notes.
