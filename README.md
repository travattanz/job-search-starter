# Job Search Starter for Codex

A local-first job-search workspace. Drop the folder into Codex, start one guided conversation, and let Codex set up your private profile and search preferences with you. You do not need to open or edit the project files yourself.

## Start here

1. Download or clone this repository, then open the folder in Codex.
2. In the chat box, type:

   **Start my 10–15 minute job-search setup. Guide me through it, create my private profile, and show me a summary before the first search.**

3. Answer the short interview. Codex will use your resume if you provide one, explain any missing choices, save your private files, and show what it set up.
4. When you’re ready to search, type:

   **Find jobs for me today.**

Codex will search the public job boards you approved, rank the results against your preferences, and show the matches and any gaps in chat. Setup itself does not contact job boards.

## What the 10–15 minute setup covers

- Target job titles, level, industries, and the kind of work you want
- Must-haves, preferences, and deal-breakers, such as pay, location, schedule, and work mode
- Your resume, career facts, and which skills you confirm are current
- Employers to include or exclude, and how many jobs to review at a time
- Optional application details; sensitive answers can be skipped and left for later
- A final review of the search standard Codex will use

You can answer in your own words, skip a question, or say “not sure.” Codex will label unknowns instead of guessing. The setup summary appears in chat, including where private files were saved and the exact prompt for the first search.

## What it does

- Searches approved public Greenhouse, Lever, Ashby, Workable, and SmartRecruiters boards.
- Ranks roles against your target titles, confirmed requirements, location, work mode, pay floor, preferences, and deal-breakers.
- Tracks applications and checks per-company caps.
- Prepares tailored resume and application materials using only confirmed facts.
- Can render a PDF resume with Chrome or Edge.
- Stops before sign-in, legal attestations, or final submission; you review and submit.

## Requirements

Python 3.9 or newer for the scripts. No packages or API keys are needed. Chrome or Edge is needed only for PDF rendering. A live search needs network access to the public job-board APIs.

## Privacy

Personal files are kept in `memory/career/` and excluded from Git. Job searches send requests to the public job-board APIs you selected. Nothing is sent to an employer, and no application is submitted automatically.

## For Codex

The guided workflow is defined in `SETUP.md` and `.agents/skills/job-search-and-apply/`. Codex reads these instructions for you; they are not a checklist you need to open. The project skill works while this folder is open in Codex and does not install anything globally.

MIT License.
