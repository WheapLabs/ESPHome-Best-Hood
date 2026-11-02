# Change notes

Each pull request adds **one file here** instead of editing `CHANGELOG.md`:

```
changes/<short-name>.<level>.md      level = patch (a fix) · minor (a new feature) · major (users must redo something)
```

Content: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) sections with `- ` entries
(continuation lines indented by two spaces):

```markdown
### Fixed

- The light level is read again after a reconnection
  ([#42](https://github.com/WheapLabs/esphome-best-hood/pull/42)).
```

Sections: Added, Changed, Deprecated, Removed, Fixed, Security, Documentation. Without a section,
the entries go to Fixed (patch), Added (minor) or Changed (major).

After the merge, GitHub (`.github/workflows/release.yml`) runs `tools/release.py` on `main`: the
highest level of the waiting notes raises the version, their entries become the new section at the
top of `CHANGELOG.md`, the notes are deleted, then the `v<number>` tag and the GitHub release are
created. Check a note with `python3 tools/release.py --check`.
