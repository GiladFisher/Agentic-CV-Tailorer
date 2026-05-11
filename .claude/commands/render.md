---
description: Convert cv.md to cv.docx using the local render script. Requires python-docx (pip install python-docx).
argument-hint: <job-id>
allowed-tools: Bash, Glob
---

Render `jobs/$ARGUMENTS/cv.md` to `jobs/$ARGUMENTS/cv.docx`.

## What to do

1. Glob `jobs/$ARGUMENTS/cv.md`. If not found, tell the user to run `/tailor $ARGUMENTS` first and stop.

2. Run:
   ```
   python src/render_docx.py $ARGUMENTS
   ```

3. If it fails with `ModuleNotFoundError: No module named 'docx'`, tell the user to run `pip install python-docx` and retry.

4. Confirm the output path: `jobs/$ARGUMENTS/cv.docx`.
