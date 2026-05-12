---
description: Generate a tailored cv.md for a job using your master profile. Run after /analyze.
argument-hint: <job-id>
allowed-tools: Read, Write, Glob
---

Generate a tailored CV for job `$ARGUMENTS`.

## NON-NEGOTIABLE RULE
**Never invent facts.** Every skill, bullet, date, project, and credential must exist in `profile/master.yaml`.
You may reword, reorder, and emphasise — you may NOT add experience, tools, or qualifications that are not in the profile.
If the job requires something the profile lacks, omit it silently. Do not fabricate it.

## What to do

1. Read these three files:
   - `profile/master.yaml` — source of truth
   - `jobs/$ARGUMENTS/analysis.json` — job requirements (run `/analyze $ARGUMENTS` first if missing)
   - `jobs/$ARGUMENTS/job.json` — company name and title for context

2. Match profile facts to job requirements:
   - Which experience bullets are most relevant to the `required_skills` and `keywords`?
   - Which projects are worth including (max 2–3 most relevant)?
   - Which skills subcategories matter most for this `domain`?
   - Should experience sections be reordered for relevance?

3. Write `jobs/$ARGUMENTS/cv.md` using exactly this format:

```
# <Full Name>
<email> | <phone> | <location> | [LinkedIn](<url>) | [GitHub](<url>)

## Summary
<2 tight sentences max. Lead with your strongest relevant fact, end with your value to this specific role. No filler.>

## Experience

### <Title> — <Company>
*<Mon YYYY> – <Mon YYYY or Present> | <Location>*
- <bullet emphasising relevance to this job>
- <bullet>

## Skills
**<Category>:** <comma-separated items>

## Education

### <Degree> — <Institution>
*<YYYY> – <YYYY> | GPA: <gpa>, <honors>*

## Projects

### [<Project Name>](<github or project url>)
*<date or range>*
- <bullet>

## Languages
<Language> (<proficiency>), <Language> (<proficiency>)
```

Omit any section (Projects, Languages, etc.) if it adds no value for this particular job.

4. Tell the user the CV is at `jobs/$ARGUMENTS/cv.md` and they can run `/render $ARGUMENTS` to produce a .docx.
