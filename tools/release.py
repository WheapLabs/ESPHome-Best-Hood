#!/usr/bin/env python3
"""Turn the change notes in changes/ into a version: a new section at the top of CHANGELOG.md.

Each pull request adds one note, changes/<name>.<level>.md, where <level> is patch, minor
or major. A note holds Keep a Changelog sections (### Added, ### Fixed...) with "- " lines;
without a section, its lines go to Fixed (patch), Added (minor) or Changed (major).
No pull request edits CHANGELOG.md, so two pull requests never conflict on it.
After a merge, .github/workflows/release.yml runs this script on main, commits, tags and
publishes the GitHub release.

  tools/release.py --check           only check the notes (exit 1 with the reason)
  tools/release.py                   write CHANGELOG.md, delete the notes, print the new version
  tools/release.py --current         print the newest version of CHANGELOG.md
  tools/release.py --notes <version> print the release text of that version
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/WheapLabs/esphome-best-hood"
LEVELS = ("patch", "minor", "major")
DEFAULT_SECTION = {"patch": "Fixed", "minor": "Added", "major": "Changed"}
SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security", "Documentation")
NOTE_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*\.(patch|minor|major)\.md$")
VERSION_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}$", re.M)
LINK = re.compile(r"^\[\d+\.\d+\.\d+\]: ", re.M)


def parse_note(name: str, text: str, level: str) -> dict[str, list[str]]:
    """{section: [entries]}; an entry is a "- " line plus its indented continuation lines."""
    sections: dict[str, list[str]] = {}
    section = DEFAULT_SECTION[level]
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("### "):
            section = line[4:].strip()
            if section not in SECTIONS:
                raise ValueError(f"{name}: unknown section « {section} » (use {', '.join(SECTIONS)})")
        elif line.startswith("- ") and line[2:].strip():
            sections.setdefault(section, []).append(line.rstrip())
        elif line.startswith("  ") and sections.get(section):
            sections[section][-1] += "\n" + line.rstrip()
        else:
            raise ValueError(f"{name}: each entry must start with « - » (continuation lines indented by 2 spaces)")
    if not sections:
        raise ValueError(f"{name}: no « - » entry")
    return sections


def read_notes(changes: Path) -> list[tuple[str, str, dict[str, list[str]]]]:
    """[(file name, level, sections)], sorted by name. Raises ValueError on a bad note."""
    notes = []
    for f in sorted(changes.glob("*.md")):
        if f.name == "README.md":
            continue
        m = NOTE_NAME.match(f.name)
        if not m:
            raise ValueError(f"{f.name}: name must be <name>.patch.md, <name>.minor.md or <name>.major.md")
        notes.append((f.name, m.group(1), parse_note(f.name, f.read_text(), m.group(1))))
    return notes


def check_changelog(journal: str) -> None:
    if re.search(r"^## \[Unreleased\]", journal, re.M):
        raise ValueError("CHANGELOG.md: remove « ## [Unreleased] », pending changes live in changes/")
    if not VERSION_HEADING.search(journal):
        raise ValueError("CHANGELOG.md: no « ## [x.y.z] - YYYY-MM-DD » heading")


def current_version(journal: str) -> str:
    return VERSION_HEADING.search(journal).group(1)


def bump(version: str, level: str) -> str:
    major, minor, patch = (int(n) for n in version.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def release(root: Path, today: str) -> str | None:
    """Apply the notes; returns the new version, or None when there is no note."""
    notes = read_notes(root / "changes")
    if not notes:
        return None
    journal = (root / "CHANGELOG.md").read_text()
    check_changelog(journal)
    previous = current_version(journal)
    version = bump(previous, max((n[1] for n in notes), key=LEVELS.index))
    merged: dict[str, list[str]] = {}
    for _name, _level, sections in notes:
        for section, entries in sections.items():
            merged.setdefault(section, []).extend(entries)
    body = "".join(f"### {s}\n\n" + "\n".join(merged[s]) + "\n\n" for s in SECTIONS if s in merged)
    first = VERSION_HEADING.search(journal)
    journal = journal[:first.start()] + f"## [{version}] - {today}\n\n" + body + journal[first.start():]
    link = f"[{version}]: {REPO_URL}/compare/v{previous}...v{version}\n"
    first_link = LINK.search(journal)
    if first_link:
        journal = journal[:first_link.start()] + link + journal[first_link.start():]
    else:
        journal = journal.rstrip("\n") + "\n\n" + link
    (root / "CHANGELOG.md").write_text(journal)
    for name, _level, _sections in notes:
        (root / "changes" / name).unlink()
    return version


def release_notes(journal: str, version: str) -> str:
    """The section of that version, for the GitHub release page."""
    m = re.search(rf"^## \[{re.escape(version)}\] - .*$", journal, re.M)
    if not m:
        raise ValueError(f"CHANGELOG.md: no section for {version}")
    rest = journal[m.end():]
    end = re.search(r"^## |^\[[^\]]+\]: ", rest, re.M)
    section = (rest[:end.start()] if end else rest).strip()
    return section + "\n\nSee [CHANGELOG.md](CHANGELOG.md).\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="only check the notes and CHANGELOG.md")
    group.add_argument("--current", action="store_true", help="print the newest version")
    group.add_argument("--notes", metavar="VERSION", help="print the release text of VERSION")
    args = parser.parse_args()
    try:
        journal = (ROOT / "CHANGELOG.md").read_text()
        if args.check:
            check_changelog(journal)
            print(f"{len(read_notes(ROOT / 'changes'))} note(s), all valid")
        elif args.current:
            check_changelog(journal)
            print(current_version(journal))
        elif args.notes:
            print(release_notes(journal, args.notes), end="")
        else:
            today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            version = release(ROOT, today)
            if version:
                print(version)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
