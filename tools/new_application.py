#!/usr/bin/env python3
"""Create one application folder and register it in the tracker.

Saves the agent a handful of file operations per job, which is the point — every
step done in Python is a step not paid for in tokens.

Usage:
  python new_application.py --company "Acme" --role "Test Engineer II" \\
      --url "https://boards.greenhouse.io/acme/jobs/123" \\
      [--salary "$95,000-$120,000"] [--location "Long Beach, CA"] \\
      [--posting-file raw.txt]

Creates memory/career/applications/<company>-<role-slug>/ with posting.md,
notes.md and a copy of the base resume.html, then appends a `prepared` entry to
tracker.json. Re-running for the same folder updates posting.md and leaves
notes.md alone, so nothing you wrote by hand is lost.

Prints the absolute folder path on the last line — the agent puts that straight
into the application session's brief.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

CAREER = Path(__file__).resolve().parent.parent
APPS = CAREER / "applications"
TRACKER = APPS / "tracker.json"
BASE_RESUME = CAREER / "resume.html"
NOTES_TEMPLATE = CAREER / "templates" / "notes.md"


def slug(text, limit=60):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:limit].rstrip("-")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--company", required=True)
    ap.add_argument("--role", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--salary", default="not stated")
    ap.add_argument("--location", default="")
    ap.add_argument("--posting-file", help="file holding the full posting text")
    ap.add_argument("--posting-text", help="the full posting text inline")
    args = ap.parse_args(argv)

    today = date.today().isoformat()
    folder = APPS / f"{slug(args.company, 24)}-{slug(args.role)}"
    folder.mkdir(parents=True, exist_ok=True)

    body = ""
    if args.posting_file:
        body = Path(args.posting_file).read_text(encoding="utf-8", errors="replace")
    elif args.posting_text:
        body = args.posting_text
    else:
        body = ("TODO — paste the full posting text here. Tailoring against a "
                "summary produces generic bullets.")

    (folder / "posting.md").write_text(
        f"# {args.company} — {args.role}\n\n"
        f"- Link: {args.url}\n"
        f"- Fetched: {today}\n"
        f"- Salary: {args.salary}\n"
        f"- Location: {args.location or 'not stated'}\n\n"
        f"---\n\n{body}\n",
        encoding="utf-8")

    notes = folder / "notes.md"
    if not notes.exists():
        template = (NOTES_TEMPLATE.read_text(encoding="utf-8")
                    if NOTES_TEMPLATE.exists()
                    else "# {{COMPANY}} — {{ROLE}}\n\nPosting: {{URL}}\nFetched: {{TODAY}}\n")
        notes.write_text(template
                         .replace("{{COMPANY}}", args.company)
                         .replace("{{ROLE}}", args.role)
                         .replace("{{URL}}", args.url)
                         .replace("{{TODAY}}", today),
                         encoding="utf-8")

    resume = folder / "resume.html"
    if not resume.exists():
        if not BASE_RESUME.exists():
            print(f"WARNING: no base resume at {BASE_RESUME}", file=sys.stderr)
        else:
            shutil.copy2(BASE_RESUME, resume)

    # Tracker entry. One per folder; never a second for the same folder.
    data = {"applications": []}
    if TRACKER.exists():
        try:
            data = json.loads(TRACKER.read_text(encoding="utf-8"))
        except ValueError:
            print(f"WARNING: {TRACKER} is not valid JSON; not touching it", file=sys.stderr)
            print(folder)
            return 1
    apps = data.setdefault("applications", [])
    if not any(a.get("folder") == folder.name for a in apps):
        apps.append({
            "folder": folder.name,
            "company": args.company,
            "role": args.role,
            "url": args.url,
            "location": args.location,
            "salary": args.salary,
            "status": "prepared",
            "prepared": today,
            "applied": None,
            "next_step": "",
        })
        data["updated"] = today
        TRACKER.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
