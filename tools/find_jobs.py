#!/usr/bin/env python3
"""Fetch and rank job postings from employer job boards, with no model tokens spent.

This is the cheap half of the skill. It queries the public JSON APIs of the four
big applicant-tracking systems for every employer listed in `boards.json`, filters
by keyword, location and salary, drops anything already in `tracker.json`, ranks
what's left, and writes a small shortlist the agent can read in one gulp.

The agent reads `shortlist.json` — a few hundred tokens — instead of a hundred
job-board pages.

Setup: `boards.json` lives next to this script and maps employers to their board.
Seed it once with target employers (the agent does this during setup) and add to
it whenever a new employer turns up. Format:

    {"companies": [
      {"name": "Acme",  "ats": "greenhouse", "token": "acme"},
      {"name": "Globex","ats": "lever",      "token": "globex"},
      {"name": "Initech","ats": "ashby",     "token": "initech"},
      {"name": "Umbrella","ats": "workable", "token": "umbrella"},
      {"name": "Stark", "ats": "smartrecruiters", "token": "Stark"}
    ]}

The `token` is the employer's slug in their careers URL:
  boards.greenhouse.io/ACME -> acme          jobs.lever.co/GLOBEX -> globex
  jobs.ashbyhq.com/INITECH -> initech        apply.workable.com/UMBRELLA -> umbrella
  careers.smartrecruiters.com/STARK -> Stark (case-sensitive here)

Usage:
  python find_jobs.py --dry-run                 # list boards, fetch nothing
  python find_jobs.py                           # fetch, rank, write shortlist.json
  python find_jobs.py --keywords "test engineer,controls" --limit 8
  python find_jobs.py --company Acme            # one employer only

Stdlib only — no pip install, nothing to break on a fresh machine.
"""

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAREER = HERE.parent
BOARDS = HERE / "boards.json"
CONFIG = CAREER / "config.json"
TRACKER = CAREER / "applications" / "tracker.json"
OUT = CAREER / "shortlist.json"

UA = "Mozilla/5.0 (compatible; job-search-and-apply/1.0)"
TIMEOUT = 25

ENDPOINTS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{t}/jobs?content=true",
    "lever": "https://api.lever.co/v0/postings/{t}?mode=json",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{t}?includeCompensation=true",
    "workable": "https://apply.workable.com/api/v1/widget/accounts/{t}?details=true",
    "smartrecruiters": "https://api.smartrecruiters.com/v1/companies/{t}/postings?limit=100",
}


# ---------------------------------------------------------------- plumbing

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def strip_html(text):
    # Greenhouse returns the description entity-escaped, so unescape before
    # stripping tags or the tags survive as literal text. Unescape again after,
    # for entities that were double-encoded.
    text = html.unescape(text or "")
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


# ---------------------------------------------------------------- per-ATS

def norm_greenhouse(company, data):
    for j in data.get("jobs", []):
        yield {
            "company": company, "title": j.get("title", ""),
            "location": (j.get("location") or {}).get("name", ""),
            "url": j.get("absolute_url", ""),
            "posted": (j.get("updated_at") or "")[:10],
            "text": strip_html(j.get("content", "")),
        }


def norm_lever(company, data):
    for j in data:
        cats = j.get("categories") or {}
        yield {
            "company": company, "title": j.get("text", ""),
            "location": cats.get("location", ""),
            "url": j.get("hostedUrl", ""),
            "posted": datetime.fromtimestamp(
                j["createdAt"] / 1000, timezone.utc).date().isoformat()
                if j.get("createdAt") else "",
            "text": strip_html(j.get("descriptionPlain") or j.get("description", "")),
        }


def norm_ashby(company, data):
    for j in data.get("jobs", []):
        yield {
            "company": company, "title": j.get("title", ""),
            "location": j.get("location", ""),
            "url": j.get("jobUrl") or j.get("applyUrl", ""),
            "posted": (j.get("publishedAt") or "")[:10],
            "text": strip_html(j.get("descriptionHtml") or j.get("descriptionPlain", "")),
            "comp": j.get("compensation") or {},
        }


def norm_workable(company, data):
    for j in data.get("jobs", []):
        yield {
            "company": company, "title": j.get("title", ""),
            "location": ", ".join(x for x in (j.get("city"), j.get("state"),
                                              j.get("country")) if x),
            "url": j.get("url") or j.get("application_url", ""),
            "posted": (j.get("published_on") or "")[:10],
            "text": strip_html(j.get("description", "") + " " + (j.get("requirements") or "")),
        }


def norm_smartrecruiters(company, data):
    for j in data.get("content", []):
        loc = j.get("location") or {}
        yield {
            "company": company, "title": j.get("name", ""),
            "location": ", ".join(x for x in (loc.get("city"), loc.get("region"),
                                              loc.get("country")) if x),
            "url": f"https://jobs.smartrecruiters.com/{j.get('company', {}).get('identifier', '')}"
                   f"/{j.get('id', '')}",
            "posted": (j.get("releasedDate") or "")[:10],
            "text": "",  # SmartRecruiters needs a second call per posting; skip it here.
        }


NORMALIZERS = {
    "greenhouse": norm_greenhouse, "lever": norm_lever, "ashby": norm_ashby,
    "workable": norm_workable, "smartrecruiters": norm_smartrecruiters,
}


# ---------------------------------------------------------------- filtering

SALARY_RE = re.compile(
    r"\$\s?(\d{2,3})(?:,(\d{3}))?(?:\s?[kK])?\s?(?:-|–|—|to)\s?\$?\s?(\d{2,3})(?:,(\d{3}))?(?:\s?[kK])?")


def salary_floor_from_text(text):
    """Lowest annual figure the posting states, or None. Deliberately conservative:
    a missed salary means the agent reads the posting itself, which is fine. A
    wrong one would filter out a good job silently."""
    m = SALARY_RE.search(text or "")
    if not m:
        return None
    low = int(m.group(1) + (m.group(2) or ""))
    if low < 1000:            # "$95k" style
        low *= 1000
    return low if 20000 <= low <= 800000 else None


def hourly_to_annual(text):
    m = re.search(r"\$\s?(\d{2,3}(?:\.\d{1,2})?)\s?(?:/|\s?per\s?)h", text or "", re.I)
    return int(float(m.group(1)) * 2080) if m else None


def score(job, keywords, cities, remote_ok):
    """Cheap relevance score. Title matches count far more than body mentions,
    because a body mention is often a different team's requirement."""
    title = job["title"].lower()
    body = job["text"].lower()
    loc = job["location"].lower()
    s = 0
    for kw in keywords:
        kw = kw.lower().strip()
        if not kw:
            continue
        if kw in title:
            s += 10
        elif kw in body:
            s += 2
    if any(c.lower() in loc for c in cities if c):
        s += 6
    if remote_ok and "remote" in loc:
        s += 4
    if re.search(r"\b(senior|staff|principal|lead|director|manager|vp)\b", title):
        s -= 3       # entry and mid roles are the usual target; the agent can override
    if re.search(r"\b(intern|internship|co-op)\b", title):
        s -= 8
    if job["posted"]:
        try:
            age = (date.today() - datetime.strptime(job["posted"], "%Y-%m-%d").date()).days
            s += 4 if age <= 7 else (2 if age <= 21 else 0)
        except ValueError:
            pass
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keywords", default="",
                    help="comma-separated; defaults to config.json search_keywords")
    ap.add_argument("--cities", default="", help="comma-separated location matches")
    ap.add_argument("--min-salary", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0,
                    help="shortlist size; default applications_per_run x candidate_multiplier")
    ap.add_argument("--company", action="append", help="restrict to these employers")
    ap.add_argument("--dry-run", action="store_true", help="list boards, fetch nothing")
    ap.add_argument("--json", action="store_true", help="print the shortlist too")
    args = ap.parse_args(argv)

    cfg = load_json(CONFIG, {})
    boards = load_json(BOARDS, {}).get("companies", [])
    if args.company:
        wanted = {c.lower() for c in args.company}
        boards = [b for b in boards if b.get("name", "").lower() in wanted]

    keywords = [k for k in (args.keywords or ",".join(
        cfg.get("search_keywords", []))).split(",") if k.strip()]
    cities = [c for c in (args.cities or ",".join(cfg.get("search_cities", []))).split(",") if c.strip()]
    min_salary = args.min_salary or int(cfg.get("min_salary") or 0)
    remote_ok = bool(cfg.get("remote_ok", True))
    limit = args.limit or (int(cfg.get("applications_per_run", 2))
                           * int(cfg.get("candidate_multiplier", 3)))

    if not boards:
        print(f"No boards configured. Add employers to {BOARDS} — see the docstring "
              f"at the top of this file for the format.")
        return 1

    if args.dry_run:
        print(f"{len(boards)} board(s) configured; would query:")
        for b in boards:
            ats = b.get("ats", "?")
            ok = "ok " if ats in ENDPOINTS else "UNSUPPORTED"
            print(f"  [{ok}] {b.get('name','?'):<24} {ats:<16} {b.get('token','?')}")
        print(f"\nkeywords={keywords or '(none — everything ranks equally)'}")
        print(f"cities={cities or '(any)'}  min_salary={min_salary or '(any)'}  limit={limit}")
        print("No requests made.")
        return 0

    # Already-applied URLs and company/role pairs never come back.
    tracker = load_json(TRACKER, {}).get("applications", [])
    seen_urls = {(a.get("url") or "").split("?")[0] for a in tracker}
    seen_roles = {((a.get("company") or "").lower(), (a.get("role") or "").lower())
                  for a in tracker}

    jobs, errors = [], []
    for b in boards:
        ats, token, name = b.get("ats"), b.get("token"), b.get("name") or b.get("token")
        if ats not in ENDPOINTS:
            errors.append(f"{name}: unsupported ats '{ats}'")
            continue
        try:
            data = get_json(ENDPOINTS[ats].format(t=token))
        except (OSError, ValueError) as e:
            # OSError covers URLError, HTTPError and socket timeouts. One dead
            # board never stops the run — it gets reported and skipped.
            errors.append(f"{name} ({ats}/{token}): {e}")
            continue
        try:
            jobs.extend(NORMALIZERS[ats](name, data))
        except (KeyError, TypeError, AttributeError) as e:
            errors.append(f"{name}: unexpected payload shape ({e})")

    kept = []
    for j in jobs:
        if j["url"].split("?")[0] in seen_urls:
            continue
        if (j["company"].lower(), j["title"].lower()) in seen_roles:
            continue
        stated = salary_floor_from_text(j["text"]) or hourly_to_annual(j["text"])
        if min_salary and stated and stated < min_salary:
            continue
        j["stated_salary_floor"] = stated
        j["score"] = score(j, keywords, cities, remote_ok)
        kept.append(j)

    kept.sort(key=lambda j: -j["score"])
    top = kept[:limit]
    for j in top:
        # The agent gets a snippet, not the whole posting. It fetches the full
        # text only for the ones it actually decides to apply to.
        j["snippet"] = j["text"][:600]
        del j["text"]
    for j in kept[limit:]:
        j.pop("text", None)

    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "boards_queried": len(boards),
        "postings_seen": len(jobs),
        "after_filters": len(kept),
        "shortlist": top,
        "errors": errors,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"{len(jobs)} postings from {len(boards)} boards -> {len(kept)} pass filters "
          f"-> top {len(top)} written to {OUT}")
    for j in top:
        sal = f"${j['stated_salary_floor']:,}+" if j["stated_salary_floor"] else "salary n/s"
        print(f"  {j['score']:>3}  {j['company']:<18} {j['title'][:52]:<52} "
              f"{j['location'][:26]:<26} {sal}")
    for e in errors:
        print(f"  ! {e}", file=sys.stderr)
    if args.json:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
