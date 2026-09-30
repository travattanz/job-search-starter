#!/usr/bin/env python3
"""Render a resume HTML file to PDF with whatever Chromium-family browser exists.

Works on Windows, macOS and Linux — do not hand-write a Chrome path in the skill,
call this instead.

Usage:
  python resume_pdf.py path/to/resume.html
  python resume_pdf.py resume.html --out "Jane Doe - Resume.pdf"
  python resume_pdf.py resume.html --check      # only report staleness, render nothing

Exit codes: 0 rendered (or fresh, with --check), 1 no browser found or render
failed, 2 bad arguments.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

WINDOWS_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
]
MAC_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
LINUX_NAMES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "microsoft-edge", "microsoft-edge-stable", "brave-browser",
]


def find_browser():
    """Env override first, then the usual install locations, then PATH."""
    override = os.environ.get("RESUME_PDF_BROWSER")
    if override:
        if Path(override).exists():
            return override
        sys.stderr.write(f"RESUME_PDF_BROWSER set but not found: {override}\n")

    candidates = []
    if sys.platform.startswith("win"):
        candidates = WINDOWS_CANDIDATES
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates = candidates + [
                str(Path(local) / "Google/Chrome/Application/chrome.exe"),
                str(Path(local) / "Microsoft/Edge/Application/msedge.exe"),
            ]
    elif sys.platform == "darwin":
        candidates = MAC_CANDIDATES

    for path in candidates:
        if Path(path).exists():
            return path
    for name in LINUX_NAMES + ["chrome", "msedge"]:
        found = shutil.which(name)
        if found:
            return found
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="resume HTML file")
    ap.add_argument("--out", help="output PDF path (default: <html stem>.pdf beside it)")
    ap.add_argument("--check", action="store_true",
                    help="report whether the PDF is older than the HTML, render nothing")
    args = ap.parse_args(argv)

    html = Path(args.html).expanduser().resolve()
    if not html.is_file():
        sys.stderr.write(f"No such file: {html}\n")
        return 2

    out = Path(args.out).expanduser() if args.out else html.with_suffix(".pdf")
    if not out.is_absolute():
        out = (html.parent / out).resolve()

    stale = not out.exists() or out.stat().st_mtime < html.stat().st_mtime
    if args.check:
        print(f"{'STALE' if stale else 'fresh'}: {out}")
        return 0

    browser = find_browser()
    if not browser:
        sys.stderr.write(
            "No Chrome/Edge/Chromium found. Install one, or set RESUME_PDF_BROWSER "
            "to the executable path.\n")
        return 1

    # A file:// URL avoids Chrome treating a Windows path as a search term.
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-pdf-header-footer", f"--print-to-pdf={out}", html.as_uri(),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        sys.stderr.write("Browser timed out after 120s.\n")
        return 1

    # Headless Chrome prints noise to stderr and sometimes exits non-zero while
    # still writing a perfectly good PDF, so judge it by the file.
    if not out.exists() or out.stat().st_size == 0:
        sys.stderr.write(
            f"Render produced no PDF (exit {proc.returncode}).\n{proc.stderr[-1500:]}\n")
        return 1

    print(f"{out}  ({out.stat().st_size // 1024} KB, {browser})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
