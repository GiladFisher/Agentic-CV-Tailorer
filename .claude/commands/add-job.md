---
description: Fetch a LinkedIn job by URL and produce a tailored CV in one shot.
argument-hint: <linkedin-job-url>
allowed-tools: Bash, Read, Write, Glob
---

Full pipeline: fetch the job at `$ARGUMENTS`, analyze it, tailor a CV, and render to .docx.

## NON-NEGOTIABLE RULE
**Never invent facts.** Every skill, bullet, date, and credential in the CV must come from `profile/master.yaml`. Reword and emphasise — never fabricate.

## Stage 1 — Fetch

Run:
```
python src/fetch_job.py $ARGUMENTS
```

Parse the output for the `job-id` line (`job-id: <value>`). Stop and report the error if the script fails.

## Stage 2 — Analyze

Read `jobs/<job-id>/job.json`. Analyze the `description` field and write `jobs/<job-id>/analysis.json` with:
- `required_skills`, `preferred_skills`, `responsibilities` (4–6 items)
- `seniority`, `domain`, `keywords`, `must_haves`, `culture_signals`

## Stage 3 — Tailor

Read `profile/master.yaml` and `jobs/<job-id>/analysis.json`.

Match profile facts to job requirements. Write `jobs/<job-id>/cv.md` using this format:

```
# <Full Name>
<email> | <phone> | <location> | [LinkedIn](<url>) | [GitHub](<url>)

## Summary
<Check profile/master.yaml for a summaries entry whose key matches the job domain (security / sysadmin / data_science / fullstack). If one exists, adapt it to this specific role and company in one sentence. If none matches or the result would only repeat what's in the bullets, omit this section entirely.>

## Experience

### <Title> — <Company>
*<Mon YYYY> – <Mon YYYY or Present> | <Location>*
- <bullet>

## Skills
**<Category>:** <list>

## Education

### <Degree> — <Institution>
*<YYYY> – <YYYY> | GPA: <gpa>, <honors>*

## Projects

### [<Project Name>](<github or project url>)
*<date>*
- <bullet>

## Languages
<Language> (<proficiency>), ...
```

Omit sections that add no value for this job.

## Stage 4 — Render

Run:
```
python src/render_docx.py <job-id>
```

## Done

Tell the user where to find the output: `jobs/<job-id>/cv.docx` and `jobs/<job-id>/cv.md`.
