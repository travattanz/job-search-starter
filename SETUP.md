# SETUP — run this once

**You are the agent reading this.** This file is a script for you to execute, not
documentation for the user. Work through it top to bottom. At the end, the
`job-search-and-apply` skill is installed and knows enough about this person to
run.

Call the person **"you"** until Step 2 tells you their name; after that use it.

Ground rules for this whole setup:

- **Batch your questions.** Ask each numbered round as one message with a
  numbered list, and wait for one reply. Never drip one question at a time — it
  is slow and it burns a $20 plan's message budget.
- **Never invent an answer.** Anything you are not told stays out of the files,
  marked `TODO — ask` where it matters.
- **Read the resume before you ask anything.** Most of Round 2 is already in it.
- Write files with your file tools, not by echoing text through a shell.

Let `KIT` = the folder this file is in. Let `WS` = the OpenClaw workspace root
(the parent of `KIT`, normally `~/.openclaw/workspace`). Use absolute paths
everywhere; expand them yourself.

---

## Step 0 — Check the machine

Run these and note the answers. One message, then move on.

PowerShell (Windows):

```powershell
python --version
Get-Command chrome.exe, msedge.exe -ErrorAction SilentlyContinue | Select-Object Name, Source
```

bash (macOS / Linux):

```bash
python3 --version
ls /Applications/Google\ Chrome.app 2>/dev/null || which google-chrome chromium 2>/dev/null
```

You need Python **3.9+** and Chrome or Edge. If Python is missing, stop and tell
them to install it from python.org (Windows: tick "Add python.exe to PATH"), then
re-run this file. If neither browser is present, say so — the resume PDF step
needs one.

Record which Python command works (`python` on Windows, `python3` elsewhere) and
use it consistently for the rest of setup. Call it `PY`.

## Step 1 — Get the resume

Ask, as one message:

> Point me at your resume — drop the file in the chat, or give me the path to it.
> PDF, DOCX, or a LinkedIn "Save to PDF" export all work. If you don't have one,
> say so and I'll build one from scratch as we go.

Then read it:

- **PDF** — use your PDF reading tool. If that fails,
  `PY -c "import pypdf"` and install `pypdf` only if you must.
- **DOCX** — read it with the docx skill if you have one, otherwise
  `pip install python-docx` and script it.
- **No resume** — skip to Round 2 and expect to ask more.

Extract, verbatim where you can: name, city, email, phone, job titles with
employers and month/year ranges, degrees with school and year, licenses and
certifications, software and hardware named, and every bullet under each job.
Keep the bullets — they are the raw material for tailoring later.

Do not paraphrase dates or titles. A wrong date on an application is worse than
a missing one.

## Step 2 — Round 1: the essentials

Ask these as one numbered message. Fill in what you already know from the resume
and ask them to correct it rather than retype it.

1. **Name** as it should appear on an application, and the name you like to be
   called if it's different.
2. **City and state** you live in, and your phone and email. (I have
   `<from resume>` — right?)
3. **What roles are you going after?** Job titles, or a plain description. List
   two or three if you're open.
4. **Lowest salary you'd accept.** A number, not a range. I use it as a hard
   filter, so put it where you'd genuinely say yes.
5. **How far will you commute**, in miles or minutes, and are you open to
   remote, hybrid, on-site, or all three?
6. **Anywhere you'd relocate for?** Cities or "no".
7. **How many applications a day** do you want? Default is 2, which is what a
   $20 Claude plan comfortably supports. Say "default" if you don't care.
8. **Companies to skip** — anywhere you've already applied recently, been
   rejected by, or don't want to work.

## Step 3 — Round 2: the questions every application asks

Same deal — one message, numbered. Tell them up front: *"These are the boring
ones every form asks. Answer once and I'll never ask again."*

1. **Work authorization** — are you legally authorized to work in the country
   you're applying in, and will you now or in the future need visa sponsorship?
2. **Government / defense work** — do you hold or have you held a security
   clearance (which level, still active?), and are you a citizen of the country
   you're applying in? Several employers ask; I never guess at this one.
3. **Licenses and certifications** — anything you hold, with the number and
   state if it's a license. Also anything you're *studying for but don't hold
   yet* — I'll keep those off your resume, because claiming one you don't have
   is the fastest way to lose an offer.
4. **Education** — degree, school, graduation month/year, and your GPA if you
   want it used. Say "don't use GPA" and I won't.
5. **Earliest start date**, and notice you'd need to give.
6. **Willing to travel?** A rough percentage, and any hard no's.
7. **Veteran status, disability status, race/ethnicity, gender** — these are the
   voluntary EEO questions on US applications. Tell me what to select, or say
   **"decline"** and I'll pick "I don't wish to answer" every time. Your call
   and I won't ask again.
8. **Anything a form shouldn't say about you** — a previous employer you'd
   rather not be contacted, an address you don't want used, a name you don't go
   by.
9. **Do you want a cover letter** written when a form asks for one but doesn't
   require it? Default is no — they cost a lot of tokens and rarely change the
   outcome.

If they decline anything, write `declines to answer` in `profile.md`. That is a
real answer, not a gap.

## Step 4 — Round 3: the skills ledger

This is the round that makes the whole thing trustworthy, so explain why:

> Last one. I'm going to build a ledger of what you can honestly claim. I only
> put things on your resume that are in it. Anything I'm unsure about I'll ask
> before it goes anywhere.

Take every tool, language, standard, instrument and system you found in the
resume. Sort them yourself into three buckets and show the person the list:

- **Have it** — named in the resume with real work behind it
- **Not sure** — mentioned in passing, or a course, or you can't tell
- **Missing** — common in their target roles but absent from the resume

Then ask, as one message:

1. Here's what I read as yours: `<list>`. Anything in there you'd *not* want to
   be tested on in an interview?
2. These I'm unsure about: `<list>`. For each — solid, rusty, or never used it?
3. Roles like yours usually ask for these and I didn't see them: `<list>`. Any
   you actually have?

Write the result to `memory/career/skills.md` using `KIT/templates/skills.md`.
Every line gets `(confirmed YYYY-MM-DD)` with today's date. Rusty counts as
`⚠️`, not `✅`.

## Step 5 — Round 4: voice sample

The skill writes short answers in the person's own voice. Without a sample they
come out reading like a press release.

Ask:

> Paste me two or three emails you've actually sent — work ones are perfect,
> boring is perfect. I want your sentence rhythm, not your best writing. Or if
> you'd rather, answer this in your own words and I'll use it: *why are you
> looking for a new job right now?*

From what they give you, write `memory/career/voice.md` from
`KIT/templates/voice.md`. Record concretely: how they open and sign off, whether
they use contractions, whether they use em-dashes (count them — most people use
zero), typical sentence length, words they repeat, and their register. Quote two
or three real sentences as examples.

If they refuse or have nothing, write the file with
`No sample yet — keep answers short, plain and concrete` and move on.

## Step 6 — Write the career files

Create `WS/memory/career/` and fill it:

| Write | From | Notes |
| --- | --- | --- |
| `profile.md` | `KIT/templates/profile.md` | Rounds 1–3. Replace every `{{PLACEHOLDER}}`. |
| `skills.md` | `KIT/templates/skills.md` | Step 4. |
| `voice.md` | `KIT/templates/voice.md` | Step 5. |
| `application-limits.json` | `KIT/templates/application-limits.json` | Copy as-is. |
| `applications/tracker.json` | `KIT/templates/tracker.json` | Copy as-is. |
| `resume.html` | `KIT/templates/resume.html` | Step 7. |
| `templates/notes.md` | `KIT/templates/notes.md` | Copy as-is. `new_application.py` reads it from there. |
| `tools/` | `KIT/tools/` | Copy all three scripts **and** `boards.json`. |
| `config.json` | `KIT/config.example.json` | Step 10. |

Leave no `{{PLACEHOLDER}}` behind. Grep for it when you're done:

```powershell
Select-String -Path "$env:USERPROFILE\.openclaw\workspace\memory\career\*.md" -Pattern '{{'
```

```bash
grep -rn '{{' ~/.openclaw/workspace/memory/career/ || echo clean
```

Anything still there means you skipped a question. Go ask it.

## Step 7 — Build the base resume

Convert what you extracted into `WS/memory/career/resume.html`, starting from
`KIT/templates/resume.html` (a clean single-column layout that survives resume
parsers — no tables, no columns, no images, no icons).

Rules, which also apply every time the skill tailors it later:

- Only what the person confirmed. Nothing from the ❌ or ❓ buckets.
- **City and state only — never a street address.** Applications collect the
  address in a field; a resume with a home address on it gets circulated.
- Never list a license or certification as held when it isn't. In-progress goes
  in its own line saying so, or nowhere.
- Bullets start with a plain past-tense verb and carry a number where one exists.
- One page unless they have 10+ years of experience.

Then generate the PDF and confirm it exists:

```powershell
python "$env:USERPROFILE\.openclaw\workspace\memory\career\tools\resume_pdf.py" `
  "$env:USERPROFILE\.openclaw\workspace\memory\career\resume.html"
```

```bash
python3 ~/.openclaw/workspace/memory/career/tools/resume_pdf.py \
  ~/.openclaw/workspace/memory/career/resume.html
```

The script finds Chrome or Edge itself. It prints the output path — check the
file is non-zero and read the first page back to make sure nothing is cut off.
Show the person the path and ask them to open it before you go on. This is the
one artifact every employer sees; it's worth one round trip.

## Step 8 — Job-site accounts

Most job sites need an account. Ask:

> Job sites will make you create accounts. Two options:
>
> **A.** I create them as I go, using one email and one password you set aside
> for job hunting. Tell me where to find the password — a file path, or your
> password manager's name — and I'll read it when I need it and never write it
> into notes or chat.
>
> **B.** I stop at every sign-in wall and leave the page open for you to type it.
> Slower, but nothing of yours is stored anywhere.

Write their choice into `profile.md` under **Job-site sign-in**. If they pick A,
record *where* the credential lives, never the credential itself. If they give
you a password in chat anyway, use it for the session, note the path only, and
tell them once that chat isn't a good place for it.

2FA, CAPTCHA and Google-only logins always stop and wait for the human,
whichever option they chose.

## Step 8a — Seed the job boards

This is the one-time investment that makes every later run cheap. `find_jobs.py`
queries employer job boards directly instead of the agent reading search pages,
but it only knows the employers listed in `tools/boards.json`.

Spend a few searches now, once:

1. From their target roles and cities, name **20 to 40 real employers** who hire
   for that work in that area. Bias toward companies that actually post a lot.
2. For each, find which applicant-tracking system they use and its token. A
   single search per batch usually does it — the pattern is in the careers URL:
   `boards.greenhouse.io/<token>`, `jobs.lever.co/<token>`,
   `jobs.ashbyhq.com/<token>`, `apply.workable.com/<token>`,
   `careers.smartrecruiters.com/<Token>`.
3. Write them into `WS/memory/career/tools/boards.json` and delete the two
   examples.
4. Employers on **Workday** (`myworkdayjobs.com`) or **Taleo** have no open API.
   Don't guess a token for them — note them in `config.json` under
   `target_companies` and the skill will search those directly.

Then set in `config.json`: `search_keywords` from their target titles,
`search_cities` from the commutable cities they named, and `min_salary` from
their floor.

Verify the boards actually answer before you call it done:

```powershell
python "$env:USERPROFILE\.openclaw\workspace\memory\career\tools\find_jobs.py"
```

```bash
python3 ~/.openclaw/workspace/memory/career/tools/find_jobs.py
```

It prints one `!` line per board that failed. A failure is almost always a wrong
token — fix those now, because a silently dead board looks exactly like an
employer with no openings. Tell them how many live postings it found; that number
is the first real sign the thing works.

## Step 9 — Install the skill

Copy the skill into the workspace skills folder, where OpenClaw picks it up:

```powershell
$src = "$env:USERPROFILE\.openclaw\workspace\job-search-starter\skill\job-search-and-apply"
$dst = "$env:USERPROFILE\.openclaw\workspace\skills\job-search-and-apply"
New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
Copy-Item -Recurse -Force $src $dst
Get-ChildItem -Recurse $dst | Select-Object FullName
```

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R ~/.openclaw/workspace/job-search-starter/skill/job-search-and-apply \
      ~/.openclaw/workspace/skills/
find ~/.openclaw/workspace/skills/job-search-and-apply -type f
```

Expect `SKILL.md` plus five files under `references/`. If `references/` is empty
the copy didn't recurse — fix it now, because the skill points at those files
three times and a missing one fails silently at the worst moment.

## Step 10 — Write config.json

Copy `KIT/config.example.json` to `WS/memory/career/config.json` and set:

- `applications_per_run` — their Round 1 answer, default `2`
- `stagger_minutes` — `75`, or `0` if they said they're on a bigger plan
- `write_cover_letters` — their Round 3 answer, default `false`
- everything else as shipped

Then tell them in one sentence what those numbers mean for their plan.

## Step 11 — Automations

Create these with your `automations` tool. **Every one is silent** —
`delivery: {mode: "none"}`. An automation that messages someone about a job
application is a notification factory; they read the sessions instead.

1. **Daily job search** — ask first: *"Want me to look for jobs on my own every
   morning, or only when you ask?"* If yes, one `cron` job at their preferred
   time (default 08:00 local), payload `agentTurn`:

   > Run the job-search-and-apply skill. Find and apply to
   > `applications_per_run` jobs. Stay inside every company cap. Do not message
   > me; I'll read the sessions.

2. **Applied-session cleanup** — daily `cron` at 21:00, payload `agentTurn`:

   > Delete any session whose title starts with "Applied:" that was renamed
   > more than one day ago. Never delete a session titled "Apply:" — those are
   > unfinished.

Do not create an automation whose only purpose is to send a message.

## Step 12 — Prove it works

Run the two scripts that must work before the skill can:

```powershell
python "$env:USERPROFILE\.openclaw\workspace\memory\career\tools\check_limits.py"
python "$env:USERPROFILE\.openclaw\workspace\memory\career\tools\find_jobs.py" --dry-run
```

```bash
python3 ~/.openclaw/workspace/memory/career/tools/check_limits.py
python3 ~/.openclaw/workspace/memory/career/tools/find_jobs.py --dry-run
```

`check_limits.py` should print nothing and exit 0 on an empty tracker — that's
correct, not broken. `find_jobs.py --dry-run` should list the boards it would
query and exit without applying to anything.

Then confirm the skill is visible: it should now appear in your own skill list as
`job-search-and-apply`. If it doesn't, the copy in Step 9 went to the wrong place.

## Step 13 — Hand over

Report to them, short, in this session:

- Where their files live, and that `profile.md` and `skills.md` are theirs to
  edit any time
- The resume PDF path
- `applications_per_run` and `stagger_minutes`, and what that means for their
  plan's 5-hour window
- Which automations you created, and that all of them are silent
- Anything still marked `TODO — ask` in `profile.md`, as a short list
- That they can start with **"find me jobs"**, and that every application runs
  in its own session they can open and steer

Then say this, because it's the part people don't expect:

> One thing worth knowing: I won't put a skill, title, date or license on your
> resume unless it's in the ledger you just confirmed. If a posting wants
> something you don't have, I'll flag it as a gap instead of quietly claiming
> it. If that ever feels too strict, edit `skills.md` — but I'd rather you walk
> into an interview able to back every line.

Finally, delete nothing and do not run the setup again unless asked. If they want
to change an answer later, edit the file — `profile.md` and `skills.md` are read
fresh on every run.
