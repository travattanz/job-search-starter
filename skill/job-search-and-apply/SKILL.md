---
name: "job-search-and-apply"
description: "Find jobs, tailor a resume to each, and run the application sessions. Use for \"find me jobs\", \"apply for me\", \"job hunt\", resume tailoring, and filling out or submitting a job application form."
---

# Job Search And Apply

Find jobs, tailor the resume to each, and submit the applications. Each
application runs in **its own session** so the user can open it, watch it, and
steer it.

Runs on a $20 Claude plan. That constraint shapes the whole skill: it applies to
a small number of jobs per run, spaces them out across the day, and does every
mechanical step in Python instead of in model turns. Read
`references/cheap-mode.md` before the first run and follow the budget in
`config.json`.

**Never invent a skill, title, date, or credential.** Everything that goes on a
resume or into a form comes from `memory/career/skills.md` (✅ lines only) or
`memory/career/profile.md`. If it isn't in one of those, it's a gap — write the
gap down, don't launder it into a claim.

If `memory/career/profile.md` doesn't exist, setup never ran. Say so and point at
`job-search-starter/SETUP.md`; don't improvise a profile.

## Paths and commands

Absolute paths, always — a child session sees only the text of its brief.

- Windows: `%USERPROFILE%\.openclaw\workspace\memory\career\`, Python is `python`
- macOS / Linux: `~/.openclaw/workspace/memory/career/`, Python is `python3`

Every command below is written for PowerShell first. `$C` / `$CAREER` is the
career folder:

```powershell
$C = "$env:USERPROFILE\.openclaw\workspace\memory\career"
```

```bash
C=~/.openclaw/workspace/memory/career
```

## Writing rule — it has to read like the user wrote it

Every piece of free text written for an application — cover letters, "why this
job" answers, screening questions, recruiter replies, rewritten resume bullets —
must read as a person's writing. Before writing any of it, read
`references/human-writing.md` (the method and the self-check) and
`memory/career/voice.md` (how this person actually writes, taken from their own
messages). Run the self-check before anything goes into a form.

Short version: no corporate vocabulary (delve, leverage, robust, seamless,
passionate about, excited for this opportunity); at most one em-dash per page;
sentence length that varies hard; contractions; every claim tied to something
specific in `posting.md`. Generic enthusiasm is the giveaway. Detectors are
noisy, so never promise anyone a score.

## Step 1 — Load context

Read, in order:

- `config.json` — the budget: how many applications, what spacing, which model
- `profile.md` — targets, contact, standard application answers, resume rules,
  job-site sign-in policy
- `skills.md` — the ✅ / ⚠️ / ❌ / ❓ ledger
- `voice.md` — match it in every free-text answer
- `applications/tracker.json` — what's already gone out, so you don't repeat one
- `application-limits.json` — per-company caps

Don't read individual application folders at this stage. `tracker.json` has what
you need and the folders are where the tokens go.

Done when you can state the salary floor, commute radius, role direction, and
`applications_per_run` without guessing.

## Step 2 — Find candidate jobs

Let `N` = `applications_per_run` from `config.json` (default 2). Build a
shortlist of `N × candidate_multiplier` postings, then cut to N. Cutting from a
wider pool is what makes the picks good.

**When `search_mode` is `"script"` (the default), don't search the web.** Run:

```powershell
python "$C\tools\find_jobs.py"
```

```bash
python3 $C/tools/find_jobs.py
```

It queries every employer board in `tools/boards.json`, filters on keywords,
location and salary, drops anything already in `tracker.json`, ranks what's left,
and writes `shortlist.json`. Read that file — a few hundred tokens instead of a
hundred job-board pages.

If the shortlist comes back thin (fewer than N good matches), then and only then
search the web yourself, and **add every new employer you find to
`tools/boards.json`** so the script covers them for free next time. That file
getting bigger is the whole point: the skill gets cheaper the longer it's used.

Filters, from `profile.md` rather than from this list:

- Salary at or above the stated floor — postings that state nothing still count
- Inside the commute radius, or remote if they're open to it
- The role direction they actually described
- Not already in `tracker.json`
- Not in their do-not-apply list
- **Inside the employer's application cap** — Step 2a, a hard cut, not a ranking
  tweak

For each finalist, fetch the live posting once and keep the text. If extraction
fails, plain-GET the page and parse the JSON-LD `JobPosting` block.

Done when you have N postings with title, employer, location, salary, and a
working link.

## Step 2a — Respect each employer's application cap

Some employers cap how many roles one person may apply to in a rolling window,
and going over costs more than the extra applications. It can sour the whole
batch, including the role they actually wanted. Caps live in
`application-limits.json`: a hard cap per company, plus a self-imposed
`soft_cap` covering every company with no published rule.

```powershell
python "$C\tools\check_limits.py"
python "$C\tools\check_limits.py" --check Acme=2   # room for 2 more? exits 1 on a hard breach
```

Then:

- **Hard cap full** — drop that company from the run. Report it in Step 7 with
  the date the next slot opens. Never spend a slot to see what happens.
- **Room for k, more than k candidates** — take the k best-matching roles only.
  One strong application beats three that trip a cap.
- **Soft cap reached** — ask before going over rather than skipping silently.
  They may well want to.
- **Prepared-but-unsent folders at a capped company** — don't submit them. Set
  `next_step` in `tracker.json` to
  `HOLD - <company> cap; do not submit before YYYY-MM-DD`.

**Record a cap the moment you see one.** Portals, confirmation pages and
auto-reply emails state them. The number is worthless in a transcript and
permanent in the file. Add the company to `application-limits.json` with
`max_per_window`, `window_days`, the `source` you read it from, and
`confirmed: true` only when you read the number verbatim instead of inferring
it. Tell the application sessions to do the same in their briefs.

## Step 3 — Create the application folder

One command per job, not a series of file writes:

```powershell
python "$C\tools\new_application.py" --company "Acme" --role "Test Engineer II" `
  --url "<posting url>" --salary "<salary>" --location "<location>" `
  --posting-file "<saved posting text file>"
```

It creates `applications/<company>-<role-slug>/` with `posting.md`, `notes.md`
and a copy of the base `resume.html`, registers a `prepared` entry in
`tracker.json`, and prints the absolute folder path. Keep that path.

Then fill in `notes.md`: the posting keywords you'll target, each mapped to a ✅
line in `skills.md`, and the honest gaps. Write the gaps down plainly — they
become interview prep and they stop you over-claiming two steps later.

## Step 4 — Resolve unknown skills before writing anything

Collect every ❓ skill the N postings ask for. Ask **all of them in one message**,
never one at a time, and never ask about something already ✅ or ❌. On a metered
plan a five-question drip is five times the cost of one message.

Record each answer in `skills.md` with `(confirmed YYYY-MM-DD)` and any new
standing application answer in `profile.md`. A skill stays off the resume until
it's ✅. Rusty is ⚠️, not ✅.

## Step 5 — Tailor a resume per job

Edit the `resume.html` already inside the application folder — never the base
copy. Mirror the posting's vocabulary.

Rules:

- Only ✅ ledger terms. A keyword with no ✅ backing goes in `notes.md` under
  gaps and nowhere else.
- Rewrite bullets in the posting's phrasing, for work they actually do, under the
  writing rule above.
- Reorder sections so the closest-matching experience reads first.
- City and state only — never a street address. Never list a license or
  certification as held unless it's under **Hold** in `profile.md`.
- Add a `<!-- Tailored for: <company> <role> YYYY-MM-DD -->` comment at the top.

Generate the PDF into the same folder:

```powershell
python "$C\tools\resume_pdf.py" "<folder>\resume.html" --out "<Legal Name> - Resume.pdf"
```

```bash
python3 $C/tools/resume_pdf.py "<folder>/resume.html" --out "<Legal Name> - Resume.pdf"
```

The script finds Chrome or Edge itself on all three platforms. Don't hand-write a
browser path.

**Always regenerate the PDF right before applying.** A PDF older than its
`resume.html` is the single most likely thing to go wrong. Check it:

```powershell
python "$C\tools\resume_pdf.py" "<folder>\resume.html" --check
```

Then verify nothing forbidden survived the edit — swap in whatever this person's
own forbidden terms are, from `profile.md`:

```powershell
Select-String -Path "<folder>\resume.html" -Pattern "<street address>","<license they don't hold>"
```

```bash
grep -n -e "<street address>" -e "<license they don't hold>" "<folder>/resume.html"
```

## Step 6 — Spawn one session per application, staggered

Do **not** apply from this session. Each application gets its own visible session
so the user can open, review, and answer it independently.

Read `stagger_minutes` from `config.json` (default 75). **Spawn the first
application now. Schedule each later one.** Spawning all N at once is what
empties a $20 plan's 5-hour window in twenty minutes.

First one:

```
sessions_spawn(
  visible: true,
  model: <config.model, default "anthropic/claude-sonnet-5">,
  label: "Apply: <Company> — <Role>",
  group: "Job applications",
  task: "<full standalone brief>"
)
```

Each later one, at `stagger_minutes × position` from now — and never inside
`quiet_hours`, push it to the morning instead:

```
automations(action: "add", job: {
  name: "Apply: <Company> — <Role>",
  schedule: { kind: "at", at: "<ISO timestamp>" },
  deleteAfterRun: true,
  delivery: { mode: "none" },
  payload: { kind: "agentTurn", message: "<the same standalone brief, prefixed: 'Spawn a visible session labelled \"Apply: <Company> — <Role>\" in group \"Job applications\" on <model> with this brief:'>" }
})
```

`delivery: {mode: "none"}` on every one. An automation that messages someone
about a job application is a notification factory.

The brief must stand alone — the child sees only that text. Expand every path.
Include:

- Absolute path to the application folder, and to the tailored PDF
- The posting URL
- Instruction to read `profile.md`, `skills.md`, `voice.md`, and the folder's
  `notes.md` first — and nothing else, to stay inside the budget
- Instruction to read `<skill>/references/applying.md` before starting, and
  `<skill>/references/application-ui.md` before touching a form
- Instruction to read `<skill>/references/browser-cli-fallback.md` **the moment
  any `browser` tool call fails**, and switch to the CLI rather than reporting a
  blocker
- Instruction to run the `references/human-writing.md` self-check on any free
  text it writes itself
- Instruction to add any application cap the site or a confirmation email states
  to `application-limits.json`, with the source
- Whether `auto_submit` is true — if false, fill everything, stop before submit,
  and flag the session
- **Your pre-written answers**, already past the self-check: the "why this job"
  answer and anything the posting obviously asks. Writing them here, once, on
  this session's model, is cheaper than the child drafting and revising them.

Then report the session list in this session.

## Step 7 — Report

Each child session applies, logs its own result, and renames itself on
confirmation, per `references/applying.md`. Don't apply from this session and
don't duplicate the child's logging.

Report here, as a short list: role, employer, salary, location, when its session
starts, and any job deliberately skipped with the reason — including any company
skipped for a cap, with the date its next slot opens.

**Never text or message the user about applications on any channel.** They read
the sessions.

## Pitfalls

These bite in the application sessions too; `references/applying.md` carries the
procedures.

- **Burning the whole plan window at once.** Spawn one, schedule the rest. If a
  session dies mid-application saying you're out of usage, nothing is lost — the
  job site holds the draft and the session resumes when the window resets.
- **Over-applying to one employer.** Run `check_limits.py` before cutting to N.
  Caps are per company and per rolling window, and a breach can taint
  applications they cared about. A company whose hard cap is full gets dropped
  from the run, not quietly retried.
- **A broken `browser` tool is not a blocker.** If every `browser` action fails,
  including `status` and `doctor`, that's a Gateway fault, not a login wall.
  Switch to the `openclaw browser` CLI per `references/browser-cli-fallback.md`.
- **Wrong resume attached.** Sites reuse whatever was uploaded last. Always
  replace it and read the filename and date back off the page.
- **Stale PDF.** Regenerate right before the brief goes out; `--check` tells you.
- **Text that reads generated.** Run the `human-writing.md` self-check on every
  free-text answer before pasting. Stock enthusiasm and even sentence length are
  the flags.
- **Silent over-claiming.** If a posting's keyword isn't ✅, it belongs in the
  gaps list, not the resume.
- **Searching the web when the script would do.** `find_jobs.py` first. Web
  search is the expensive fallback, and every employer it turns up belongs in
  `boards.json` afterwards.
- **Session timeouts.** Save the draft after each section.
- **`sessions(...)` not loaded yet.** Run
  `ToolSearch("select:mcp__openclaw__sessions")` before the first use, or the
  rename and the escalation flag both fail silently.
- **Windows paths.** Quote every path; `%USERPROFILE%` and `~` don't expand
  inside a child's brief. Write them out.
