---
description: Ingest a new job listing. Prompts you to paste the job description, then saves it to disk.
argument-hint: <url>
allowed-tools: Read, Write, Glob
---

Ingest a new job listing into the Agentic CV Tailorer project.

The job URL (if provided) is: `$ARGUMENTS`

## What to do

1. Ask the user to paste the full job description text. Wait for their reply before continuing.

2. Extract from the pasted text:
   - `title` — exact job title as written
   - `company` — company name
   - `location` — location or "Remote"

3. Generate a job ID: `<company-slug>-<title-slug>-<YYYYMM>` using today's date.
   Lowercase, hyphens only. Example: `google-software-engineer-202605`.

4. Check for duplicates: Glob `jobs/<id>/`. If it already exists, warn the user and ask whether to continue or abort.

5. Create `jobs/<id>/job.json`:
```json
{
  "id": "<id>",
  "title": "<job title>",
  "company": "<company>",
  "location": "<location>",
  "url": "<url from arguments or empty string>",
  "date_added": "<YYYY-MM-DD>",
  "description": "<full pasted description>"
}
```

6. Read `state/seen_jobs.json`, add `"<id>": {"date_added": "<YYYY-MM-DD>", "status": "ingested"}`, write it back.

7. Tell the user the job was saved and to run `/do <id>` for the full pipeline, or `/analyze <id>` to start step by step.
