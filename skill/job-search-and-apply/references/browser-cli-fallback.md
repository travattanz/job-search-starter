# When the `browser` tool is broken

Read this the moment a `browser` tool call fails. It's a recovery path, not a
reason to stop.

## Recognising it

Every `browser` action — including `status` and `doctor`, which touch no page —
returns the same error. A real example:

```
Async work scope is closed
```

That's a stale async scope inside the running Gateway process. It is **not** a
login wall, a missing credential, a closed tab, or a stopped browser. Retrying the
tool won't clear it and neither will stopping and starting the browser; only an
OpenClaw restart does, and that's the human's to run.

**Don't report this as a blocker and don't abandon the application.** The browser
itself is fine. Drive it from the CLI.

## Switching to the CLI

Everything the tool does has a CLI equivalent that reaches the same managed
browser over the Gateway socket.

Windows (PowerShell) — put the OpenClaw-managed Node on `PATH` first, in every
call, or you get `openclaw: command not found`:

```powershell
$env:PATH = "$env:USERPROFILE\.openclaw\tools\node\bin;$env:PATH"
openclaw browser doctor
openclaw browser tabs
```

macOS / Linux:

```bash
export PATH="$HOME/.openclaw/tools/node/bin:$PATH"   # adjust to the installed version
openclaw browser doctor
openclaw browser tabs
```

If `openclaw` still isn't found, locate it rather than giving up:

```powershell
Get-ChildItem "$env:USERPROFILE\.openclaw\tools" -Recurse -Filter "openclaw*" -ErrorAction SilentlyContinue | Select-Object -First 5 FullName
```

```bash
ls ~/.openclaw/tools/*/bin/openclaw 2>/dev/null; which openclaw
```

`doctor` should report OK on gateway, plugin, profile and browser. Confirm that
before blaming anything else.

## Command map

| `browser` tool | CLI |
| --- | --- |
| `open` | `openclaw browser open <url>` |
| `navigate` | `openclaw browser navigate <url>` |
| `snapshot` | `openclaw browser snapshot` |
| `act` click | `openclaw browser click <ref>` (`--double`, `--button`) |
| `act` type | `openclaw browser type <ref> "<text>"` (`--submit`, `--slowly`) |
| `act` select | `openclaw browser select <ref> <value...>` |
| `act` press | `openclaw browser press <key>` |
| `act` fill | `openclaw browser fill --fields '[{"ref":"e12","value":"Jane"}]'` |
| `act` wait | `openclaw browser wait <selector>` / `--load networkidle` / `--fn <js>` |
| `act` evaluate | `openclaw browser evaluate --fn '<js>' [--ref <ref>]` |
| `act` batch | `openclaw browser batch --actions '[{"kind":"click","ref":"e12"}]'` |
| `upload` | `openclaw browser upload <path> --ref <ref>` — see below |
| `screenshot` | `openclaw browser screenshot` (prints the saved path) |
| `dialog` | `openclaw browser dialog --accept` |
| `tabs` / `close` / `focus` | `openclaw browser tabs` / `close <t1>` / `focus <t1>` |

Add `--json` for machine-readable output, and `--target-id <t1>` to pin a tab when
more than one is open.

`fill` with several fields in one call is both faster and cheaper than a type per
field. Use it.

## Uploading the tailored resume

This is the one place the CLI is stricter than the tool. `upload` refuses any path
outside the managed media directory:

```
Error: Invalid path: must stay within inbound media directory
```

So stage the PDF there first, keeping the exact filename the form should show:

```powershell
$staged = "$env:USERPROFILE\.openclaw\media\inbound\Jane Doe - Resume.pdf"
Copy-Item "<application folder>\Jane Doe - Resume.pdf" $staged
openclaw browser upload $staged --ref <file-input-ref>
```

```bash
STAGED="$HOME/.openclaw/media/inbound/Jane Doe - Resume.pdf"
cp "<application folder>/Jane Doe - Resume.pdf" "$STAGED"
openclaw browser upload "$STAGED" --ref <file-input-ref>
```

Use `--input-ref <ref>` to set an `<input type=file>` directly, or
`--element "<css>"` when the snapshot doesn't expose it. Read the filename and
date back off the page as `applying.md` requires, then delete the staged copy.

## Timeouts

Gateway calls can return `gateway timeout` well before the CLI's own default on
slow pages and file choosers. Raise both rather than treating a timeout as
failure:

```
openclaw --timeout 60000 browser <command> ...
openclaw browser upload "<staged>" --ref <ref> --timeout-ms 30000
```

## Refs still go stale

Refs (`e12`, `t1`) come from the last `snapshot`. Re-run
`openclaw browser snapshot` after every page change, and never reuse a ref across
a navigation.

## Before you finish

Note in the folder's `notes.md` that the `browser` tool was down and the CLI was
used, so the failure stays visible even though the application went through.
Mention the Gateway restart in your own session — as a thing worth doing, not as
something that stopped the work.
