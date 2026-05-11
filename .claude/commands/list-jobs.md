---
description: List all jobs in the project and show which pipeline stages are complete.
allowed-tools: Glob, Read
---

List all jobs in the `jobs/` directory and show their pipeline status.

## What to do

1. Glob `jobs/*/job.json` to find all jobs.

2. For each job:
   - Read `job.json` → get `title`, `company`, `date_added`
   - Check existence of `analysis.json`, `cv.md`, `cv.docx` using Glob
   - Mark each stage: ✓ (exists) or ✗ (missing)

3. Print a table:

```
ID                                  | Company  | Title               | Added      | Analyzed | Tailored | Rendered
------------------------------------|----------|---------------------|------------|----------|----------|----------
google-software-engineer-202605     | Google   | Software Engineer   | 2026-05-11 | ✓        | ✓        | ✗
```

4. End with a one-line summary: e.g. "3 jobs — 3 analyzed, 2 tailored, 1 rendered."

If `jobs/` is empty, tell the user to run `/add-job <url>` to add their first listing.
