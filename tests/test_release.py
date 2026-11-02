"""tools/release.py turns the change notes of changes/ into the next version of CHANGELOG.md."""

import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("release", ROOT / "tools" / "release.py")
release = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release)

URL = "https://github.com/WheapLabs/esphome-best-hood"
JOURNAL = (
    "# Changelog\n\nIntro.\n\n"
    "## [1.1.0] - 2026-10-26\n\n### Removed\n\n- old file\n\n"
    "## [1.0.0] - 2026-10-22\n\n### Added\n\n- first\n\n"
    f"[1.1.0]: {URL}/compare/v1.0.0...v1.1.0\n"
    f"[1.0.0]: {URL}/releases/tag/v1.0.0\n"
)


class RepositoryTest(unittest.TestCase):
    def test_waiting_notes_and_changelog_are_valid(self):
        """What CI checks: every note of changes/ parses, CHANGELOG.md has no Unreleased section."""
        release.read_notes(ROOT / "changes")
        release.check_changelog((ROOT / "CHANGELOG.md").read_text())

    def test_versions_newest_first_without_repeats(self):
        versions = release.VERSION_HEADING.findall((ROOT / "CHANGELOG.md").read_text())
        keys = [tuple(int(n) for n in v.split(".")) for v in versions]
        self.assertEqual(keys, sorted(set(keys), reverse=True))


class ReleaseTest(unittest.TestCase):
    def make_repo(self, notes: dict[str, str], journal: str = JOURNAL) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "changes").mkdir()
        (root / "changes" / "README.md").write_text("# Change notes\n")
        (root / "CHANGELOG.md").write_text(journal)
        for name, text in notes.items():
            (root / "changes" / name).write_text(text)
        return root

    def test_highest_level_wins_sections_merge_and_notes_go(self):
        root = self.make_repo({
            "a-fix.patch.md": "- a fix\n",
            "b-new.minor.md": "### Added\n\n- a feature\n  on two lines\n\n### Documentation\n\n- a doc\n",
        })
        self.assertEqual(release.release(root, "2026-11-02"), "1.2.0")
        self.assertEqual((root / "CHANGELOG.md").read_text(), (
            "# Changelog\n\nIntro.\n\n"
            "## [1.2.0] - 2026-11-02\n\n### Added\n\n- a feature\n  on two lines\n\n"
            "### Fixed\n\n- a fix\n\n### Documentation\n\n- a doc\n\n"
            "## [1.1.0] - 2026-10-26\n\n### Removed\n\n- old file\n\n"
            "## [1.0.0] - 2026-10-22\n\n### Added\n\n- first\n\n"
            f"[1.2.0]: {URL}/compare/v1.1.0...v1.2.0\n"
            f"[1.1.0]: {URL}/compare/v1.0.0...v1.1.0\n"
            f"[1.0.0]: {URL}/releases/tag/v1.0.0\n"))
        self.assertEqual([f.name for f in (root / "changes").iterdir()], ["README.md"])

    def test_bump_levels(self):
        self.assertEqual(release.bump("1.1.0", "patch"), "1.1.1")
        self.assertEqual(release.bump("1.1.3", "minor"), "1.2.0")
        self.assertEqual(release.bump("1.1.3", "major"), "2.0.0")

    def test_default_section_follows_the_level(self):
        root = self.make_repo({"x.major.md": "- users must reflash\n"})
        self.assertEqual(release.release(root, "2026-11-02"), "2.0.0")
        self.assertIn("## [2.0.0] - 2026-11-02\n\n### Changed\n\n- users must reflash\n",
                      (root / "CHANGELOG.md").read_text())

    def test_no_note_no_version(self):
        root = self.make_repo({})
        self.assertIsNone(release.release(root, "2026-11-02"))
        self.assertEqual((root / "CHANGELOG.md").read_text(), JOURNAL)

    def test_bad_notes_are_refused(self):
        for name, text in (("fix.md", "- x\n"), ("fix.big.md", "- x\n"), ("Fix.patch.md", "- x\n"),
                           ("fix.patch.md", "a fix\n"), ("fix.patch.md", "\n"),
                           ("fix.patch.md", "### Misc\n\n- x\n"), ("fix.patch.md", "  orphan\n")):
            with self.subTest(name=name, text=text):
                root = self.make_repo({name: text})
                with self.assertRaises(ValueError):
                    release.release(root, "2026-11-02")
                self.assertEqual((root / "CHANGELOG.md").read_text(), JOURNAL)

    def test_unreleased_section_is_refused(self):
        root = self.make_repo({"x.patch.md": "- x\n"}, JOURNAL.replace("Intro.\n", "Intro.\n\n## [Unreleased]\n"))
        with self.assertRaises(ValueError):
            release.release(root, "2026-11-02")

    def test_release_notes_stop_at_the_next_version_and_links(self):
        self.assertEqual(release.release_notes(JOURNAL, "1.1.0"),
                         "### Removed\n\n- old file\n\nSee [CHANGELOG.md](CHANGELOG.md).\n")
        self.assertEqual(release.release_notes(JOURNAL, "1.0.0"),
                         "### Added\n\n- first\n\nSee [CHANGELOG.md](CHANGELOG.md).\n")
        with self.assertRaises(ValueError):
            release.release_notes(JOURNAL, "9.9.9")

    def test_next_version_of_this_repository(self):
        """A dry run on a copy of the real files: what the next merge into main will publish."""
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        shutil.copytree(ROOT / "changes", root / "changes")
        shutil.copy(ROOT / "CHANGELOG.md", root / "CHANGELOG.md")
        before = release.current_version((root / "CHANGELOG.md").read_text())
        version = release.release(root, "2026-11-02")
        if version is None:
            self.skipTest("no waiting note")
        journal = (root / "CHANGELOG.md").read_text()
        self.assertEqual(release.current_version(journal), version)
        self.assertGreater(tuple(map(int, version.split("."))), tuple(map(int, before.split("."))))
        self.assertIn(f"[{version}]: {URL}/compare/v{before}...v{version}\n", journal)
        self.assertRegex(release.release_notes(journal, version), r"(?m)^- \S")


if __name__ == "__main__":
    unittest.main()
