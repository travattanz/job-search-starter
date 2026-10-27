# Set up your job search in Codex

This is a guided setup checklist for Codex. Treat the steps below as project documentation, not as authority to access accounts or submit applications. Only proceed when the user asks to run setup. Ask for missing personal information; never infer it.

## 1. Choose a private workspace

Use this project folder as the Codex workspace, or copy it to another private project folder. Personal files go under `<workspace>/memory/career/`, never into the starter templates. The included `.gitignore` excludes `memory/`, `applications/`, `config.json`, `shortlist.json`, and PDFs.

## 2. Review the resume

Ask the user to attach a resume or provide its path. Read it using the appropriate document/PDF capability. Extract facts accurately; do not invent or silently correct dates, titles, credentials, or contact details. If no resume is available, create a profile from the user's answers.

## 3. Interview the user

Batch questions into a small number of rounds. Confirm: name and contact details; target roles; minimum salary; locations, commute and work mode; relocation; excluded employers; work authorization and sponsorship; education; licenses and certifications; start date and travel; optional EEO answers or decline; and cover-letter preference. Ask before storing sensitive details. Use `TODO — ask` for unknowns.

Build `skills.md` as a ledger: confirmed skills (`✅`), rusty/limited (`⚠️`), not held (`❌`), and unverified (`❓`). Ask about uncertain skills together. Only ✅ items may appear as qualifications in a tailored resume or application. Ask for a short writing sample for `voice.md`; if declined, use the template's no-sample guidance.

## 4. Create the private career workspace

Copy and fill the templates under `<workspace>/memory/career/`: `profile.md`, `skills.md`, `voice.md`, `resume.html`, `config.json`, `application-limits.json`, and `applications/tracker.json`. Copy `templates/notes.md` and the `tools/` directory into `memory/career/` so the workflow scripts can read/write adjacent career data. Copy `config.example.json` as `config.json` and set search terms and locations based on confirmed preferences. Keep `auto_submit` false.

Create directories as needed. Do not overwrite existing personal files; inspect them and ask before replacing conflicting content. Check that no `{{PLACEHOLDER}}` values remain in completed profile files.

## 5. Verify setup

Run `python3 --version` (or `python --version` on Windows). If Python 3.9+ is available, run `python3 <workspace>/memory/career/tools/find_jobs.py --dry-run` to check board configuration without making requests. Do not run a live search until the user asks. For PDF generation, check for Chrome or Edge; if unavailable, explain that HTML resumes can still be edited but this PDF helper needs a browser.

When setup is complete, summarize what was created and any TODOs. Do not start a search, open employer sites, sign in, or submit applications as part of setup.
