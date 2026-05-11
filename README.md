# Agentic CV Tailorer

Paste a LinkedIn job URL, get a tailored `.docx` CV. Every CV is grounded in your master profile — no hallucinated experience.

## How it works

1. `/add-job <url>` — fetches the job listing, analyzes requirements, tailors a CV from your profile, and renders a `.docx`. One command, full pipeline.
2. All your personal history lives in `profile/master.yaml`. The tailorer only uses what's in there.
3. Each job gets its own folder under `jobs/` with the analysis, markdown CV, and final docx.

## Setup

**Requirements:** Python 3.9+, a Claude Pro account (uses Claude Code slash commands — no separate API key needed).

```bash
git clone https://github.com/GiladFisher/Agentic-CV-Tailorer
cd Agentic-CV-Tailorer
pip install -r requirements.txt
```

Copy the profile template and fill it in:

```bash
cp profile/master.yaml.example profile/master.yaml
# edit profile/master.yaml with your real details
```

Then open Claude Code from the project folder:

```bash
claude
```

## Commands

| Command | What it does |
|---------|-------------|
| `/add-job <url>` | Full pipeline: fetch → analyze → tailor → render |
| `/analyze <id>` | Extract requirements from a saved job |
| `/tailor <id>` | Generate `cv.md` from profile + analysis |
| `/render <id>` | Convert `cv.md` to `cv.docx` |
| `/do <id>` | Run analyze + tailor + render on an already-fetched job |
| `/list-jobs` | Show all jobs and pipeline status |

## Project structure

```
profile/
  master.yaml          # your full history — source of truth (gitignored)
  master.yaml.example  # schema template to copy from
jobs/
  <id>__<company>__<title>/
    job.json           # raw job data
    analysis.json      # extracted requirements and keywords
    cv.md              # tailored CV in markdown
    cv.docx            # final output
state/
  seen_jobs.json       # ingested jobs (gitignored)
  applied.json         # jobs you've submitted (gitignored)
templates/             # base .docx template (optional)
src/
  fetch_job.py         # scrapes LinkedIn job page
  render_docx.py       # converts cv.md → cv.docx
.claude/commands/      # slash command definitions
```

## Notes

- `profile/master.yaml` and `jobs/` are gitignored — your personal data stays local.
- LinkedIn scraping uses the guest API endpoint. If you hit a rate limit, wait a minute and retry.
- To re-tailor an existing job with updated profile info, run `/do <id>` again.
