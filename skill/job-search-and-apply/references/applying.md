# Running one application session

Read this at the start of an "Apply: …" session, before touching a form. It
covers filling and submitting one application, signing in, escalating, and
closing out. For form mechanics, read `application-ui.md` in this same folder.

Your whole job is one application. Don't search for other jobs, don't read other
application folders, don't refresh the tracker dashboard. That's the budget.

## Filling and submitting

1. Open the posting and start the application.
2. Fill every field from `profile.md`. Match each work-experience title and date
   to the tailored resume exactly — a mismatch is a background-check problem, not
   a typo.
3. **Before submitting, confirm the attached resume filename and date are this
   job's tailored PDF.** Sites reuse whatever was uploaded last. Read the
   filename back off the page.
4. Check stored profile data — address, legal name, phone — against
   `profile.md`. Stale values persist from old applications.
5. Save the draft after each section. Long forms expire, and so do plan windows.
6. Submit, then capture the confirmation text or number.

If `auto_submit` is false in `config.json`, stop before the submit button, flag
the session, and wait:

```
sessions(action: "patch", statusNote: "Filled and ready — press submit", attention: "hand", ttlMinutes: 240)
```

Any free text you write yourself — screening answers, "why this job", recruiter
replies — goes through `human-writing.md` and its self-check first, against
`memory/career/voice.md`. Keep it under `max_free_text_words` unless the form
demands more. Never claim anything that isn't ✅ in `memory/career/skills.md`.

Most of your answers should already be in the brief, pre-written. Use them. Only
draft fresh text for questions the brief didn't anticipate.

## Job-site sign-in and account creation

Follow `profile.md` → **Job-site sign-in**. It says one of two things:

- **Create accounts as needed** — use the job-hunt email and the password at the
  location recorded there. Read it when you need it, type it straight into the
  form, and never write it into notes, a file, or chat.
- **Never sign in** — leave the browser open on the sign-in page, say which page
  is waiting, and stop.

Either way, these always stop for the human: a 2FA code, a CAPTCHA, a rejected
password, a Google-or-Microsoft-only login. Never ask for a password in chat.

## Load `sessions` before using it

`sessions(action: "patch", ...)` is a deferred tool; a fresh session has no
schema for it and the call raises `InputValidationError`. That silently skips the
rename.

Run `ToolSearch` with `query: "select:mcp__openclaw__sessions"` before the first
`sessions(...)` call, and again on any later `InputValidationError`. Never drop
the rename or the escalation flag because of it.

## When to stop and ask

Escalate instead of guessing when:

- A required answer isn't in `profile.md`
- A **legal attestation** you can't establish from the files — citizenship,
  clearance, criminal history, licensure, government service, right to work.
  Never guess one of these. A wrong answer on a signed application is a
  rescinded offer.
- A login wall the sign-in policy can't clear
- An operating-system permission dialog — leave it for the human, never grant
  access on their behalf
- The posting turns out to contradict the brief: wrong salary band, wrong
  location, seniority far off, or it's been taken down. Say so and stop rather
  than applying to something they'd have skipped.

To escalate, post every open question in **your own session** as one batched
message, and flag the sidebar:

```
sessions(action: "patch", statusNote: "Blocked: <short question>", attention: "hand", ttlMinutes: 120)
```

**Never text or message the user** on any channel — not for blocks, not for
progress. They watch the sessions directly.

Then wait for the answer rather than guessing or abandoning the application.

## After a confirmed submission

1. Rename the session:
   `sessions(action: "patch", label: "Applied: <Company> — <Role>")`. Never
   rename a blocked or unconfirmed one — the rename is the signal that nothing is
   left to do.
2. Append to the folder's `notes.md`: `Submitted: YYYY-MM-DD`, the confirmation
   text or number, the resume filename used, and anything the form asked that
   wasn't already saved.
3. Update the folder's entry in `applications/tracker.json`: `status` to
   `submitted` and `applied` to today's date. That date is what the application
   caps count, so only ever set it on a real confirmation.
4. Add every new standing answer to `profile.md` and every newly confirmed or
   denied skill to `skills.md`, so the next application autofills. This is the
   single biggest saving available — an employer's second application should be
   nearly free.
5. Add any application cap the site or confirmation email stated to
   `application-limits.json`, with the source quoted.
