# Job Search & Apply — starter kit

An OpenClaw skill that finds jobs for you, tailors your resume to each one, and
fills out the applications. This folder is the blank version: no one's personal
data in it. You run the setup once, answer some questions, and the skill knows
enough about you to work.

Built to run on a **$20 Claude plan**. See [Cheap mode](#cheap-mode).

## What you need

- A computer (Windows, macOS or Linux) with **Python 3.9+** and **Chrome or Edge**
- [OpenClaw](https://docs.openclaw.ai) installed and talking to Claude
- Your resume as a file — PDF, DOCX, or a LinkedIn profile export

## Three steps

1. **Install OpenClaw** and get to the point where you can chat with your agent.
2. **Put this folder in your OpenClaw workspace.** Default location:
   - Windows: `%USERPROFILE%\.openclaw\workspace\job-search-starter\`
   - macOS / Linux: `~/.openclaw/workspace/job-search-starter/`
3. **Tell your agent this, word for word:**

   ```
   Read job-search-starter/SETUP.md and run it.
   ```

The agent then interviews you — 15 minutes, mostly confirming things it read off
your resume — writes your profile into `memory/career/`, installs the skill, and
sets up the automations. When it's done you can say **"find me jobs"** or
**"apply for me"** and it works.

## What gets created

```
memory/career/
  profile.md              you: targets, contact, standard application answers
  skills.md               the ✅ / ❌ / ❓ ledger — what you can honestly claim
  voice.md                how you write, so answers don't read like a robot
  resume.html             your base resume, edited per job
  application-limits.json per-company application caps
  applications/           one folder per job, plus tracker.json
  tools/                  the scripts the skill runs
```

Nothing leaves your machine except the applications you submit.

## Cheap mode

A $20 Claude plan gives you a limited number of messages in a rolling 5-hour
window. An unthrottled job-application agent will eat the whole window in twenty
minutes. So this kit is throttled by default:

| Setting | Default | Why |
| --- | --- | --- |
| Applications per run | **2** | Two good applications beat six sloppy ones, and it fits the window. |
| Spacing between them | **~75 min** | Each application runs as its own scheduled session, so usage spreads across the day. |
| Model | **Sonnet** | Opus is roughly 5× the cost per message. Sonnet fills forms just as well. |
| Job search | **script, not model** | A Python script hits the job-board APIs and hands the model a ranked shortlist instead of raw web pages. |
| Cover letters | **only when required** | Long prose is the most expensive output there is. Stored short answers get reused. |

All five live in `config.json` (written during setup from
`config.example.json`). Raise them if you're on a bigger plan — set
`applications_per_run` to 5 and `stagger_minutes` to 0 and it behaves like an
unthrottled version.

If you hit your limit mid-application, nothing is lost. The session picks up
where it stopped when your window resets; the draft is saved on the job site.

## Honesty rules baked in

The skill will not put a skill on your resume unless you have confirmed you
actually have it. That's what `skills.md` is for — every claim traces to a line
you approved. It also won't submit anything with a legal attestation it had to
guess at; it stops and asks you.

## Windows notes

Commands in the skill are written for PowerShell first, with the macOS/Linux
equivalent beside them. The two things that differ in practice:

- **PDF generation** uses `tools/resume_pdf.py`, which finds Chrome or Edge
  itself on all three platforms. Don't hand-write a Chrome path.
- **Paths with spaces** need quoting in PowerShell too; the scripts handle it.

## Files in here

```
SETUP.md                      the interview + install script — this is what you run
config.example.json           cheap-mode knobs
skill/job-search-and-apply/   the skill itself, installed into your agent
  SKILL.md                    the procedure
  references/                 applying, form mechanics, browser fallback, writing, cheap mode
templates/                    blank profile.md, skills.md, voice.md, resume.html, tracker, limits
tools/                        find_jobs.py, new_application.py, resume_pdf.py, check_limits.py,
                              boards.json (the employer list find_jobs queries)
```

## Sharing it

Zip the folder and send it. The only thing the recipient needs to know is the
sentence in step 3 — everything else the agent handles. Nothing in here is
personal to whoever gave it to you; if you find a name or an address in it,
that's a bug.

## License

MIT. Do what you want with it.
