---
description: Fetch a LinkedIn job listing by URL and save it to disk. Usage: /add-job <url>
argument-hint: <linkedin-job-url>
allowed-tools: Bash, Read
---

Fetch and ingest the LinkedIn job at: `$ARGUMENTS`

## What to do

1. Run:
   ```
   python src/fetch_job.py $ARGUMENTS
   ```

2. Parse the output to get the `job-id` (printed as `job-id: <value>` on the last line).

3. Handle errors:
   - `ModuleNotFoundError` for `requests` or `bs4` → tell user: `pip install requests beautifulsoup4`
   - Rate-limited → tell user to wait 1–2 minutes and retry
   - HTTP error or empty description → tell user LinkedIn may have blocked the request; they can retry or paste the description manually

4. On success, tell the user the job was saved and to run `/do <job-id>` to generate the tailored CV, or `/analyze <job-id>` to start step by step.
