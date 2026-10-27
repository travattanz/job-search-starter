# Application site interaction

Codex may not have a browser connected in every session. Check for an available browser capability before interacting with a site. Do not assume a browser, shell automation, or access to the user's saved-password store.

Use only public pages and normal site flows. Do not bypass CAPTCHA, MFA, rate limits, login walls, or other access restrictions. Never inspect browser profiles, cookies, or password databases.

Use an authenticated browser session or the user's selected password-manager integration only. Never ask the user to paste a password or token into chat, and never save it in `Career/`, an application folder, logs, or the repository. If login is needed and no approved secure method is available, ask the user to sign in manually in the browser and resume after they confirm.

If auto-submit is enabled and the user explicitly confirmed it, ordinary form fields may be completed with confirmed profile facts and reusable answers. Pause in the dedicated job chat when a question is unknown, ambiguous, sensitive without storage consent, or asks for an attestation, certification, or consent. Never click an attestation or make a legal representation for the user.

Before submitting, recheck the employer, role, job link, role criteria, all answers, and application caps. Submit only when the user authorized auto-apply and the form contains no unresolved field or human-only checkpoint. Record submission only after the employer site confirms it.
