# {{PREFERRED_NAME}} — Career Profile

Everything the job-search skill needs to know. Read top to bottom before any
job search, resume edit, or application. Edited by hand any time — it's read
fresh on every run.

Last updated: {{TODAY}}

## Targets

- **Titles and level:** {{TARGET_ROLES}}
- **Work to seek:** {{WORK_TO_SEEK}}
- **Industries / employer types:** {{INDUSTRIES}}
- **Must-haves:** {{MUST_HAVES}}
- **Preferences:** {{PREFERENCES}}
- **Deal-breakers:** {{DEAL_BREAKERS}}
- **Salary floor:** {{SALARY_FLOOR}} — include currency and pay period. Treat as a hard filter only if the user confirms it is one.
- **Location:** {{CITY_STATE}}; commute/travel limit {{COMMUTE_RADIUS}}.
- **Work setup:** {{ONSITE_HYBRID_REMOTE}}
- **Schedule:** {{SCHEDULE}}
- **Relocation:** {{RELOCATION}}
- **Target employers:** {{TARGET_COMPANIES}}
- **Excluded employers:** {{EXCLUDED_COMPANIES}}
- **Applications per run:** {{APPS_PER_RUN}} (also in `config.json`)

<!-- Keep must-haves, preferences, and deal-breakers separate. Never promote a
     preference to a hard filter. If a script cannot check a criterion, Codex
     reviews the full posting and explains the result in chat. -->

## Background

{{BACKGROUND_SUMMARY}}

<!-- Two or three sentences: years of experience, the domain, the kind of work
     they actually do day to day. This is what the skill uses to judge whether a
     posting is a real match or a keyword coincidence. -->

### Work history

{{WORK_HISTORY}}

<!-- Employer — Title — Mon YYYY to Mon YYYY (or Present), one line each, in the
     exact wording that goes on an application form. Dates must match the resume
     exactly; a mismatch is a background-check problem. -->

### Education

{{EDUCATION}}

<!-- Degree, school, Mon YYYY. Add "GPA: X.XX" only if they said to use it. -->

## Contact

- **Legal name (applications):** {{LEGAL_NAME}}
- **Goes by:** {{PREFERRED_NAME}}
- **Email:** {{EMAIL}}
- **Phone:** {{PHONE}}
- **City, state:** {{CITY_STATE}} — city and state only on a resume, never a
  street address. Forms with an address field get {{ADDRESS_FOR_FORMS}}.
- **LinkedIn:** {{LINKEDIN}}
- **Portfolio / GitHub:** {{PORTFOLIO}}

## Credential storage and auto-apply

- **Preferred credential store:** {{CREDENTIAL_STORAGE}} (Apple Keychain, Windows Credential Manager, password-manager app, or manual sign-in).
- **Auto-apply:** {{AUTO_APPLY_STATUS}} (from `config.json`; default on after explicit setup confirmation).
- **Dedicated job chat:** {{JOB_CHAT_STATUS}} (create a separate Codex chat for each application when the thread tool is available).
- **Reusable application answers:** {{SAVE_REUSABLE_ANSWERS}} (save user-confirmed answers with date and reuse scope; request separate consent for sensitive answers).

Never put passwords, access tokens, recovery codes, or cookies in this profile, chat, or an application folder. If the selected password manager cannot be accessed through an approved integration, ask the user to sign in manually.

## Standard application answers

Reuse these only when the question and context match. Record the user's exact
confirmed answer, confirmation date, and whether it is general or employer-
specific. Sensitive answers require explicit permission to store. Do not ask
again for a current reusable answer unless the user changes it or the context
differs.

| Question | Confirmed answer | Confirmed on | Reuse scope |
| --- | --- | --- | --- |

No reusable answers yet. Add a row only after the user confirms the answer; ask
before storing sensitive answers.

### Voluntary EEO questions

{{EEO_ANSWERS}}

<!-- Either their specific selections, or: "Decline all — select 'I don't wish
     to answer' / 'I decline to self-identify' on every one." Declining is a
     real answer. Never guess these from a name or a resume. -->

### Licenses and certifications

- **Hold:** {{LICENSES_HELD}}
- **In progress, do NOT list as held:** {{LICENSES_IN_PROGRESS}}

## Off limits

{{OFF_LIMITS}}

<!-- Employers not to contact, an address not to use, a former name, anything
     that must not appear on a form. -->

## Resume rules

- Base resume: `Career/resume.html`; PDF via
  `tools/resume_pdf.py`, regenerated right before every application.
- PDF filename: `{{LEGAL_NAME}} - Resume.pdf`
- City and state only, no street address.
- Nothing on it that isn't ✅ in `skills.md`.
- No license or certification listed as held unless it's in **Hold** above.
- One page unless 10+ years of experience.
- Cover letters: {{COVER_LETTER_POLICY}}

## Open questions

{{TODO_LIST}}

<!-- Every "TODO — ask" item. The skill surfaces this list when it's blocked, so
     keep it honest and delete lines as they're answered. -->
