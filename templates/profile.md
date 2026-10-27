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

## Job-site sign-in

{{SIGNIN_POLICY}}

<!-- One of:
  A) "Create accounts as needed with the job-hunt email above and the password
     at <where it lives>. Read it when needed; never write it into notes, a
     file, or chat."
  B) "Never sign in. Stop at every login wall, leave the browser open on the
     sign-in page, and say which page is waiting."
  Either way: 2FA, CAPTCHA and Google-only logins always stop for the human. -->

## Standard application answers

Reuse these verbatim. Every new answer a form asks for gets added here the same
day, so the next application autofills.

| Question | Answer |
| --- | --- |
| Authorized to work in {{COUNTRY}}? | {{WORK_AUTH}} |
| Need visa sponsorship, now or in future? | {{SPONSORSHIP}} |
| Citizen of {{COUNTRY}}? | {{CITIZENSHIP}} |
| Security clearance? | {{CLEARANCE}} |
| Earliest start date | {{START_DATE}} |
| Notice required | {{NOTICE}} |
| Willing to travel | {{TRAVEL}} |
| Willing to relocate | {{RELOCATION}} |
| Desired salary | {{DESIRED_SALARY}} |
| Currently employed | {{CURRENTLY_EMPLOYED}} |
| May we contact current employer | {{CONTACT_CURRENT_EMPLOYER}} |
| How did you hear about us | {{SOURCE_ANSWER}} |
| Previously applied here / worked here | {{PRIOR_RELATIONSHIP}} |
| Convicted of a felony | {{FELONY}} |
| Drug screen / background check consent | {{SCREENING_CONSENT}} |
| Referral name | {{REFERRAL}} |

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

- Base resume: `memory/career/resume.html`; PDF via
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
