# Running this on a $20 plan

A Claude Pro plan gives a limited number of messages in a rolling 5-hour window.
An unthrottled job-application agent will spend the lot in twenty minutes and
leave the person unable to use Claude for anything else. Everything here exists
to stop that.

Read `config.json` at the start of every run and treat it as a budget, not a
suggestion.

## Where the money actually goes

In rough order, largest first:

1. **Reading raw web pages.** A job-board search page or a long posting is
   thousands of tokens, and most of it is boilerplate. `find_jobs.py` exists so
   the model reads a ranked shortlist instead.
2. **Writing long prose.** A cover letter costs more than filling an entire
   form. `write_cover_letters: false` means one gets written only when the form
   refuses to submit without it.
3. **Opus instead of Sonnet.** Roughly 5× per message for work Sonnet does
   equally well. Form filling is not a reasoning problem.
4. **Drip questions.** Five questions in five messages costs five times one
   message with five numbered questions. Always batch.
5. **Re-reading files.** `profile.md` and `skills.md` once per session, not once
   per step. Don't read application folders you aren't working on.
6. **Screenshot loops.** Desktop control burns a message per screenshot. Use the
   `browser` tool's snapshot instead wherever the page is reachable that way;
   it's text, and it's a fraction of the cost.

## The rules

- **N applications per run, from `applications_per_run`.** Default 2. Two
  applications with tailored resumes beat six copy-pastes, and it fits the
  window with room left over for the person's own work.
- **Stagger.** Spawn the first application session immediately; schedule the rest
  with one-shot `at` automations `stagger_minutes` apart. Usage spreads across
  the day instead of spiking.
- **Never inside `quiet_hours`.** Push a session that would land there to the
  next morning.
- **Script before model.** If a step is deterministic — folder creation, PDF
  rendering, cap checking, deduping, ranking — there's a script for it. Use it.
  Adding to the scripts is cheaper than doing the work in turns, every time.
- **One fetch per posting.** Fetch it once in Step 2, save the text into
  `posting.md`, and read it from there afterwards. Never re-fetch to check a
  detail.
- **Cap free text** at `max_free_text_words` unless the form states a longer
  minimum.
- **Snippets, not documents.** `shortlist.json` carries a 600-character snippet
  per posting on purpose. Fetch the full text only for the N you commit to.

## Running out mid-application

This will happen and it is not a failure.

The job site holds the draft — that's why `applying.md` says save after every
section. When usage resets, the session picks up where it stopped. What matters
is that the state lives in the application folder and on the job site, never only
in the conversation.

If a session dies with a usage error:

1. Don't respawn it. The same session resumes.
2. Leave `tracker.json` on `prepared`. Only a confirmed submission sets
   `applied`.
3. Flag it so the person knows: `sessions(action: "patch", statusNote: "Paused — plan limit; resumes when the window resets", ttlMinutes: 120)`

## When to spend more

Raise the budget deliberately, not by accident:

- **A role they really want.** Hand-write that one. Say so, and spend on it.
- **A first application at a new employer.** The screening answers get stored in
  `notes.md` and `profile.md`, so the second application there is nearly free.
- **A bigger plan.** `applications_per_run: 5`, `stagger_minutes: 0`, and it
  behaves like an unthrottled version.

## What not to cut

Cheapness has a floor. Don't save tokens by:

- Skipping the tailoring. An untailored resume is the one thing that makes the
  whole exercise pointless.
- Skipping the `human-writing.md` self-check.
- Guessing at a legal attestation instead of asking.
- Skipping `check_limits.py`. A tripped cap wastes far more than it saves.
