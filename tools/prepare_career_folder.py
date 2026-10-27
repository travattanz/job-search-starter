#!/usr/bin/env python3
"""Create the user's private Desktop/Career workspace without overwriting files.

Usage:
  python prepare_career_folder.py

The script is stdlib-only and safe to run again. It copies missing scripts and
templates from the repository into ~/Desktop/Career and reports the directory.
Existing profile, config, tracker, and application data are preserved.
"""

import json
import os
import shutil
import sys
from pathlib import Path


def desktop_dir():
    """Find the standard desktop, including common OneDrive Windows paths."""
    candidates = []
    if sys.platform == "win32":
        for key in ("OneDriveCommercial", "OneDriveConsumer", "OneDrive"):
            value = os.environ.get(key)
            if value:
                candidates.append(Path(value) / "Desktop")
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            candidates.append(Path(user_profile) / "Desktop")
    candidates.append(Path.home() / "Desktop")

    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    # Standard location if this account has not created a Desktop folder yet.
    return Path.home() / "Desktop"


def copy_missing(source, destination, created_files):
    if not source.is_file() or destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if os.name != "nt":
        destination.chmod(0o600)
    created_files.append(destination)


def main():
    source_root = Path(__file__).resolve().parents[1]
    career = desktop_dir() / "Career"
    created_files = []

    career.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        career.chmod(0o700)

    for dirname in ("tools", "templates", "applications"):
        folder = career / dirname
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.name != "nt":
            folder.chmod(0o700)

    for source in sorted((source_root / "tools").glob("*.py")):
        copy_missing(source, career / "tools" / source.name, created_files)

    for source in sorted((source_root / "templates").glob("*")):
        if source.is_file():
            copy_missing(source, career / "templates" / source.name, created_files)

    for name in ("profile.md", "skills.md", "voice.md", "resume.html"):
        copy_missing(career / "templates" / name, career / name, created_files)

    copy_missing(source_root / "config.example.json",
                 career / "templates" / "config.example.json", created_files)
    copy_missing(career / "templates" / "config.example.json",
                 career / "config.json", created_files)
    copy_missing(career / "templates" / "application-limits.json",
                 career / "application-limits.json", created_files)
    copy_missing(career / "templates" / "tracker.json",
                 career / "applications" / "tracker.json", created_files)

    boards = career / "tools" / "boards.json"
    if not boards.exists():
        boards.write_text(json.dumps({"companies": []}, indent=2) + "\n",
                          encoding="utf-8")
        if os.name != "nt":
            boards.chmod(0o600)
        created_files.append(boards)

    print(f"Career workspace: {career}")
    print(f"Created {len(created_files)} starter files; existing files were preserved.")
    print("No network requests were made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
