# Automated Opportunity Updates Setup

This package adds a weekly GitHub Action (`update.yml`) and Python script (`fetch_opportunities.py`) that automatically fetch new high school scholarships from the U.S. Department of Labor's **CareerOneStop API**, remove duplicates, and update `scholarhub-opportunities.json`.

## Step 1: Upload Files to Your Repository
1. Extract `ScholarHub-Automation.zip`.
2. Upload `fetch_opportunities.py` to the root folder of your `ScholarHub` repository.
3. Upload `.github/workflows/update.yml` (if uploading via browser, click **Add file > Create new file**, type `.github/workflows/update.yml` as the filename, and paste the contents of `update.yml`).

## Step 2: Add Your Free CareerOneStop API Key
1. Request a free student/developer API key at: https://www.careeronestop.org/Developers/WebAPI/registration.aspx
2. In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret** and add two secrets:
   - `COS_USER_ID` — your CareerOneStop User ID
   - `COS_API_TOKEN` — your CareerOneStop API Token

## Step 3: Run It Now
1. Go to the **Actions** tab in your repository.
2. Click **Auto-Update ScholarHub Opportunities** on the left, then click **Run workflow**.
3. Once it finishes, your `scholarhub-opportunities.json` file will automatically update with new listings and redeploy to your live site!
