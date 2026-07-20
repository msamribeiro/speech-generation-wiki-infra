from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.resolve_wiki_dir import resolve_wiki_dir


class ResolveWikiDirTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.infra = self.root / "speech-generation-wiki-infra"
        self.wiki = self.root / "speech-generation-wiki-content"
        self.infra.mkdir()
        self.wiki.mkdir()
        (self.infra / ".gitmodules").write_text(
            '[submodule "wiki"]\n'
            "\tpath = wiki\n"
            "\turl = git@github.com:example/speech-generation-wiki.git\n"
        )
        subprocess.run(["git", "init", "-q", str(self.wiki)], check=True)
        subprocess.run(
            ["git", "-C", str(self.wiki), "remote", "add", "origin", "https://github.com/example/speech-generation-wiki.git"],
            check=True,
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_default_sibling(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(resolve_wiki_dir(self.infra), self.wiki.resolve())

    def test_environment_override(self) -> None:
        alternate = self.root / "alternate"
        self.wiki.rename(alternate)
        with mock.patch.dict(os.environ, {"SPEECH_WIKI_CONTENT_DIR": str(alternate)}):
            self.assertEqual(resolve_wiki_dir(self.infra), alternate.resolve())

    def test_missing_repository(self) -> None:
        self.wiki.rename(self.root / "moved")
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "not found"):
                resolve_wiki_dir(self.infra)

    def test_wrong_remote(self) -> None:
        subprocess.run(
            ["git", "-C", str(self.wiki), "remote", "set-url", "origin", "https://github.com/example/wrong.git"],
            check=True,
        )
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "origin mismatch"):
                resolve_wiki_dir(self.infra)

    def test_non_writable_repository(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch("os.access", return_value=False):
            with self.assertRaisesRegex(ValueError, "not writable"):
                resolve_wiki_dir(self.infra)


if __name__ == "__main__":
    unittest.main()
