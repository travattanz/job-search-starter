# Driving application forms

Read this before the first form interaction.

## Use the browser tool, not desktop control

The `browser` tool works on a text snapshot of the page. Desktop control works on
screenshots. The snapshot costs a fraction as much and doesn't misclick, so the
order of preference is not close:

1. `browser` tool against a managed profile — default
2. `openclaw browser` CLI — when the tool itself is broken, see
   `browser-cli-fallback.md`
3. Desktop control — only when the application is already open in the person's
   own browser and moving it would lose form state

```
browser(action: "snapshot")      # refs like e12 come from here
browser(action: "act", request: { kind: "type", ref: "e12", text: "Jane" })
browser(action: "act", request: { kind: "click", ref: "e34" })
```

**Refs go stale.** Any navigation, submit, or dynamic re-render invalidates them,
and a stale ref clicks nothing or clicks the wrong thing. Re-snapshot after every
page change and never reuse a ref across a navigation.

## Which browser holds the session

The person's real logins live in their own browser, which has no remote debugging
port. The OpenClaw-managed browser is a separate profile and usually doesn't hold
an application session already in progress.

```
browser(action: "profiles")     # what profiles exist
browser(action: "tabs")         # what's open in the managed one
```

If the application is in the managed browser, use the tool with that `profile`.
If it's in the person's own browser, use desktop control — and **do not restart
their browser to add a debug port**, because that destroys in-progress form
state.

Signing in fresh in the managed profile is almost always better than fighting for
control of an existing tab. It persists, so you only do it once per site.

## Desktop control rules

Only when there's no alternative. These are the things that cost time when
guessed wrong:

- **Coordinates are in the last screenshot's pixel space**, not physical screen
  pixels. A 1710×1107 screen may return a 1200×777 image; passing screen
  coordinates clicks the wrong place.
- **Take a screenshot immediately before every coordinate action.** Frames
  invalidate whenever the screen changes.
- **The first click focuses the window; a second click activates the control.**
  Budget two clicks when the browser wasn't frontmost.
- Use JPEG at low quality. Full-size PNG screenshots can exceed 1 MiB and break
  the reply.
- Browsers don't expose page content to the accessibility tree reliably, so the
  accessibility tree won't show form fields.
- OS automation permission prompts are the human's to answer. Never accept one on
  their behalf.

## File uploads

The resume upload is the step most likely to go wrong.

- Set the `<input type="file">` directly when the snapshot exposes it — far more
  reliable than clicking through a native file picker.
- Windows file pickers: the path goes in the filename box. Paste it rather than
  typing; put it on the clipboard first (`Set-Clipboard "<path>"` on Windows,
  `pbcopy` on macOS).
- Quote paths with spaces, which every resume filename has.
- **Confirm the upload** by reading the new filename and date off the page, not by
  assuming the click worked.

## Common form systems

**Greenhouse, Lever, Ashby** — plain forms, the easy case. The `browser` tool
handles them start to finish. Resume upload is a real file input.

**Workday** — a multi-page wizard with its own account per employer, and it
re-asks work history even after parsing the resume. Expect 6–8 pages. Save at
every step; the session expires. Its dropdowns are real widgets: click, wait for
the list, click the option.

**SuccessFactors** (many utilities and large employers) — dropdowns look native
but are **autocomplete text inputs**. Type the value, wait for the suggestion row,
then click the suggestion. Typing alone leaves raw text in the field. Uploads save
server-side immediately; typed fields do not. Sessions expire in about an hour;
the draft comes back under Candidate Profile → Saved Applications. The footer has
**Save**, **Apply** and **Delete Application** side by side — be deliberate.

**Taleo** — old, slow, and it often requires an account before showing the form.
Expect to create one.

**iCIMS** — usually fine, but it sometimes silently drops a resume upload. Check
the filename back.

## Before you submit

Read the review page and check, in this order: resume filename and date, legal
name, email, phone, work-history dates against the resume, every legal
attestation, and the EEO selections. Then submit and capture the confirmation.
