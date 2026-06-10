# Agentic CV Tailorer

Saves LinkedIn job listings and generates a tailored CV for each one, grounded strictly in `profile/master.yaml`.

## Folder structure

```
profile/master.yaml          # source of truth — gitignored, local only
profile/supporting/          # certs, transcripts, raw notes — gitignored
jobs/<id>__<company>__<title>/
  job.json                   # raw parsed job data
  analysis.json              # extracted requirements, keywords, skills
  cv.md                      # tailored CV in markdown
  cv.docx                    # rendered output
  notes.md                   # personal notes per job
state/seen_jobs.json         # job IDs already processed — gitignored
state/applied.json           # jobs submitted — gitignored
templates/                   # base .docx template
src/                         # Python utilities (docx rendering etc.)
.claude/commands/            # slash commands for each pipeline stage
```

## Non-negotiable tailoring rule

**Never invent facts.** Every bullet, date, skill, achievement, and credential in a generated CV must exist verbatim or by direct inference from `profile/master.yaml`. Rewrite, reorder, and emphasise — but never add experience, tools, or projects that are not in the profile.

## Slash commands

| Command | What it does |
|---------|-------------|
| `/add-job <url>` | Ingest a new job listing |
| `/analyze <id>` | Extract requirements + keywords → `analysis.json` |
| `/tailor <id>` | Generate `cv.md` from profile + analysis |
| `/render <id>` | Produce `cv.docx` from `cv.md` |
| `/do <id>` | Full pipeline: analyze + tailor + render |
| `/list-jobs` | Show all jobs and their current state |

## Git & environment notes

- **Shell:** PowerShell. Use PowerShell syntax — `$env:VAR`, backtick for line continuation, no `&&` operator (use `;` or `if ($?) { ... }` instead).
- **Path has spaces:** always quote — `"C:\Users\Brother printer\Documents\Projects\Agentic CV Tailorer"`.
- **gh CLI:** not always in PATH. Use the full path: `& "C:\Program Files\GitHub CLI\gh.exe"`.
- **git push:** uses HTTPS. The `credential-manager-core` warning on push is harmless — the push succeeds regardless.
- **Remote:** `https://github.com/GiladFisher/Agentic-CV-Tailorer.git`, branch `master`.
- **profile/master.yaml and jobs/ are gitignored** — never try to stage them.

## Job ID format

`<linkedin-job-id>` when scraped, or a short slug (e.g. `google-swe-2026-05`) for manually added jobs.
