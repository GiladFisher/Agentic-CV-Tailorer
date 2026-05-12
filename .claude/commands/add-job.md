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
<You MUST use one of the summaries defined in profile/master.yaml under the summaries key. Pick the entry whose key best matches the job domain. You may lightly adapt the wording to fit the specific role, but do not write a new summary from scratch. If the chosen summary would only repeat what is already in the bullets below, omit this section entirely.>

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
