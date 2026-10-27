#!/usr/bin/env python3
"""Per-company application-cap check.

Reads Career/application-limits.json and applications/tracker.json and
reports, per company, how many applications went out inside the rolling window
and how many slots are left.

Usage:
  python check_limits.py                    # every company with history or a rule
  python check_limits.py Acme Globex       # just these
  python check_limits.py --json
  python check_limits.py --check Acme=3     # room for 3 more Acme applications?

Exits 1 when a --check request would breach a hard cap, so a shell step can gate
on it. An empty tracker prints nothing and exits 0 — that is correct, not broken.
"""

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

CAREER = Path(__file__).resolve().parent.parent
LIMITS = CAREER / "application-limits.json"
TRACKER = CAREER / "applications" / "tracker.json"

# A submitted application counts against a cap however it ended. "prepared"
# never went out; "withdrawn" was pulled back.
NON_COUNTING = {"prepared", "withdrawn"}


def load():
    limits = json.loads(LIMITS.read_text(encoding="utf-8")) if LIMITS.exists() else {}
    apps = []
    if TRACKER.exists():
        apps = json.loads(TRACKER.read_text(encoding="utf-8")).get("applications", [])
    return limits, apps


def real_keys(d):
    """Keys that are data. Anything starting with _ is documentation."""
    return {k: v for k, v in (d or {}).items() if not k.startswith("_")}


def canon(name, aliases):
    return aliases.get((name or "").strip().lower(), (name or "").strip())


def rule_for(company, limits):
    company_rules = real_keys(limits.get("companies"))
    if company in company_rules:
        r = dict(company_rules[company])
        r["kind"] = "hard"
        return r
    r = dict(limits.get("soft_cap") or limits.get("default") or {})
    r["kind"] = "soft" if r.get("max_per_window") else "none"
    return r


def parse_day(value):
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def build(today=None):
    limits, apps = load()
    aliases = {k.lower(): v for k, v in real_keys(limits.get("aliases")).items()}
    today = today or date.today()

    submitted = {}
    for a in apps:
        if a.get("status") in NON_COUNTING:
            continue
        day = parse_day(a.get("applied"))
        if not day:
            continue
        submitted.setdefault(canon(a.get("company"), aliases), []).append(
            (day, a.get("role", "")))

    report = {}
    for company in sorted(set(submitted) | set(real_keys(limits.get("companies")))):
        rule = rule_for(company, limits)
        window = int(rule.get("window_days") or 30)
        cutoff = today - timedelta(days=window - 1)
        rows = sorted(submitted.get(company, []))
        in_window = [r for r in rows if r[0] >= cutoff]
        cap = rule.get("max_per_window")

        # A slot frees the day after the oldest in-window application drops out.
        next_slot = None
        if cap and len(in_window) >= cap:
            frees = sorted(d for d, _ in in_window)[: len(in_window) - cap + 1][-1]
            next_slot = (frees + timedelta(days=window)).isoformat()

        report[company] = {
            "kind": rule["kind"],
            "cap": cap,
            "window_days": window,
            "window_start": cutoff.isoformat(),
            "used": len(in_window),
            "remaining": None if cap is None else max(0, cap - len(in_window)),
            "over_by": 0 if cap is None else max(0, len(in_window) - cap),
            "total_ever": len(rows),
            "next_slot_opens": next_slot,
            "confirmed": rule.get("confirmed", True),
            "source": rule.get("source", ""),
            "note": rule.get("note", ""),
            "in_window": [{"applied": d.isoformat(), "role": r} for d, r in in_window],
        }
    return report


def line(company, r):
    cap = "no cap" if r["cap"] is None else f"{r['used']}/{r['cap']}"
    tag = {"hard": "HARD", "soft": "soft", "none": "-"}[r["kind"]]
    bits = [f"{company:<22} {cap:>8}  per {r['window_days']}d  [{tag}]"]
    if r["remaining"] == 0:
        bits.append("FULL")
        if r["next_slot_opens"]:
            bits.append(f"next slot {r['next_slot_opens']}")
    elif r["remaining"] is not None:
        bits.append(f"{r['remaining']} left")
    if r["over_by"]:
        bits.append(f"OVER by {r['over_by']}")
    if not r["confirmed"]:
        bits.append("(cap unconfirmed)")
    return "  ".join(bits)


def main(argv):
    as_json = "--json" in argv
    checks = [a[len("--check="):] for a in argv if a.startswith("--check=")]
    if "--check" in argv:
        i = argv.index("--check")
        checks += argv[i + 1: i + 2]
    names = [a for a in argv if not a.startswith("-") and a not in checks]

    report = build()
    if names:
        wanted = {n.lower() for n in names}
        shown = {k: v for k, v in report.items() if k.lower() in wanted}
    else:
        shown = report

    if as_json:
        print(json.dumps(shown, indent=2))
    else:
        for company, r in sorted(shown.items(), key=lambda kv: -kv[1]["used"]):
            if r["kind"] == "none" and not r["used"]:
                continue
            print(line(company, r))

    breach = False
    for spec in checks:
        company, _, n = spec.partition("=")
        n = int(n or 1)
        r = report.get(company)
        if not r:
            print(f"\n{company}: no history and no rule - {n} is fine.")
            continue
        if r["cap"] is None:
            print(f"\n{company}: no cap; {n} more is fine.")
            continue
        room = r["remaining"]
        verdict = "OK" if n <= room else ("BREACH" if r["kind"] == "hard" else "over soft cap")
        print(f"\n{company}: want {n}, room for {room} "
              f"({r['used']}/{r['cap']} per {r['window_days']}d) -> {verdict}")
        if r["next_slot_opens"] and n > room:
            print(f"  next slot opens {r['next_slot_opens']}")
        if n > room and r["kind"] == "hard":
            breach = True

    return 1 if breach else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
