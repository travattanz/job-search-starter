# Job Search Starter for Codex

A local-first job search workspace with a Codex skill, public job-board discovery scripts, resume/application templates, and an honest skills ledger. Adapted from the OpenClaw starter kit for Codex.

## Use it in Codex

1. Open this folder as a project in Codex (desktop: open the folder; CLI: `cd` here and start Codex).
2. Say: **“Read SETUP.md and help me set up my job search.”** The setup interview will ask before writing personal profile data.
3. After setup, ask **“Find jobs for me”** or **“Prepare an application for [role]”**.

Codex discovers the project skill in `.agents/skills/job-search-and-apply/`. The skill works in this project; it does not install anything globally. Keep your personal data in `memory/career/`, which is excluded from Git.

## What it does

- Searches configured public Greenhouse, Lever, Ashby, Workable, and SmartRecruiters boards using `tools/find_jobs.py`.
- Tracks applications, checks per-company caps, and creates one folder per role.
- Tailors an HTML resume using only claims backed by your approved skills ledger.
- Generates a PDF using Chrome or Edge via `tools/resume_pdf.py`.
- Keeps you in control of sign-in, legal attestations, and final submission. The default workflow stops before submitting.

## Requirements

Python 3.9+ for the scripts. Chrome or Edge is needed to render resume PDFs. The discovery script needs network access to public ATS APIs. No API key or third-party AI provider is required.

## Privacy

Personal data, tracker files, shortlist output, and generated PDFs are gitignored. Review `.gitignore` before adding files. Job discovery sends requests to public job-board APIs. Nothing is submitted to an employer unless you explicitly complete the final submission step.

## Files

- `.agents/skills/job-search-and-apply/` — Codex skill and workflow references
- `SETUP.md` — one-time profile and workspace setup interview
- `config.example.json` — search and review-first settings
- `templates/` — blank profile, tracker, resume, voice, and cap templates
- `tools/` — job discovery, application folder, cap, and PDF scripts

MIT License.
