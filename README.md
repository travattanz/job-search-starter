# Job Search Starter for Codex

A local-first job-search workspace. Open this folder in Codex, attach your resume, and answer a short guided setup. You do not need to inspect or edit project files.

## Start here

1. Download or clone this repository, then open the folder in Codex.
2. In the chat box, type:

   **Set up my job search. Ask me for my resume first, then guide me through the yes/no setup.**

3. Drop in your resume when Codex asks. Codex will create a private `Career` folder on your Desktop and use short yes/no, multiple-choice, and factual questions to fill it in.
4. When setup is complete, type:

   **Find jobs for me today.**

Codex will search public postings using your selected search mode, check results against your must-haves and deal-breakers, rank the remaining jobs using your preferences, and show the results in chat. If you choose no specific employers, Codex uses broad public-web search.

## What setup asks

The 10–15 minute interview uses a resume to prefill facts, then confirms them with you. It covers target job titles, location and work mode, pay floor, schedule, must-haves, deal-breakers, optional preferences, and employers to include or exclude. It avoids broad “what’s your dream job?” questions. You can answer **Yes**, **No**, **Skip**, choose from a list, or correct a fact.

Codex shows a summary in chat when finished, including the Career folder location and the exact prompt for your first search. Setup asks where you want login credentials kept and whether you want to keep auto-apply enabled.

## Your private Career folder

Setup creates `Desktop/Career` on macOS or Windows and stores your profile, resume copy, search settings, application tracker, and job materials there. On Windows it checks common OneDrive Desktop locations too. The setup helper preserves existing files and can be run again safely. If Codex cannot access the Desktop, it will ask you to choose a folder or grant access; it will not save personal information in this repository.

## What it does

- Searches approved public Greenhouse, Lever, Ashby, Workable, and SmartRecruiters boards, or searches public postings broadly on the web when no employers are specified.
- Applies must-haves and deal-breakers, then ranks by your preferences.
- Tracks applications and checks per-company caps.
- Prepares tailored resume and application materials using only confirmed facts.
- Auto-apply is enabled by default after setup. Codex creates a dedicated chat for each application, saves approved reusable answers, and pauses for missing answers, login, multi-factor checks, CAPTCHA, or legal attestations.
- Can render a PDF resume with Chrome or Edge.

## Requirements

Python 3.9 or newer for the scripts. No packages or API keys are needed. Chrome or Edge is needed only for PDF rendering. A live search needs network access to the public job-board APIs.

## Privacy

Personal files live in `Desktop/Career`, outside the cloned repository. Job searches send requests to the public job-board APIs or web search. Passwords never belong in the repository, Career files, or chat; choose an OS or password-manager vault during setup. Codex does not retrieve vault entries unless an approved integration is available; otherwise you sign in manually in the browser. Applications may be submitted automatically when auto-apply is enabled, the job matches your confirmed criteria, a supported browser is available, and all non-attestation answers are known. Codex pauses when a human decision is required.

## For Codex

The conversational workflow is defined in `SETUP.md` and `.agents/skills/job-search-and-apply/`. Codex reads these instructions for you; they are not a checklist you need to open. The project skill works while this folder is open in Codex and does not install anything globally.

MIT License.
