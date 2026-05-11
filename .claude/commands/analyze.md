---
description: Analyze a job listing and extract structured requirements into analysis.json. Run before /tailor.
argument-hint: <job-id>
allowed-tools: Read, Write, Glob
---

Analyze the job listing `$ARGUMENTS` and save a structured breakdown to `analysis.json`.

## What to do

1. Read `jobs/$ARGUMENTS/job.json`. If it doesn't exist, tell the user to run `/add-job` first and stop.

2. Analyze the `description` field and extract:
   - `required_skills` — explicitly required technologies, tools, languages
   - `preferred_skills` — nice-to-have / bonus qualifications
   - `responsibilities` — 4–6 core responsibilities in plain language
   - `seniority` — "junior" / "mid" / "senior" / "lead" / "staff"
   - `domain` — primary domain: e.g. "sysadmin", "security", "data science", "backend", "devops"
   - `keywords` — terms to weave into the CV for ATS matching
   - `must_haves` — hard requirements that would disqualify a candidate if missing
   - `culture_signals` — up to 3 values or culture hints from the description

3. Write to `jobs/$ARGUMENTS/analysis.json`.

4. Tell the user the analysis is done and to run `/tailor $ARGUMENTS` next.
