---
description: Full pipeline for a job — analyze, tailor, and render in one go.
argument-hint: <job-id>
allowed-tools: Read, Write, Glob, Bash
---

Run the full CV tailoring pipeline for job `$ARGUMENTS`.

## NON-NEGOTIABLE RULE
**Never invent facts.** Every skill, bullet, date, and credential in the CV must come from `profile/master.yaml`.
Reword and emphasise — never fabricate.

## Stage 1 — Analyze

1. Read `jobs/$ARGUMENTS/job.json`. If not found, stop and tell the user to run `/add-job` first.

2. Analyze the job description and write `jobs/$ARGUMENTS/analysis.json` containing:
   `required_skills`, `preferred_skills`, `responsibilities`, `seniority`, `domain`,
   `keywords`, `must_haves`, `culture_signals`

## Stage 2 — Tailor

3. Read `profile/master.yaml` and `jobs/$ARGUMENTS/analysis.json`.

4. Match profile facts to job requirements. Identify the most relevant bullets, skills, and projects.

5. Write `jobs/$ARGUMENTS/cv.md` using this format:

```
# <Full Name>
<email> | <phone> | <location> | [LinkedIn](<url>) | [GitHub](<url>)

## Summary
<2 tight sentences max. Lead with your strongest relevant fact, end with your value to this specific role. No filler.>

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

## Stage 3 — Render

6. Run `python src/render_docx.py $ARGUMENTS`.
   If it fails with a missing `docx` module error, tell the user to `pip install python-docx` and re-run `/render $ARGUMENTS`.

7. Report what was created: `analysis.json`, `cv.md`, `cv.docx`.
