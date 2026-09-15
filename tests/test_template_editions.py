"""0027 FR01/AC01: adopt the sole product without maker files.

These checks cover package paths and isolation, not the agent's choice of TDD.
"""
import json
import pathlib
import re
import shutil
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
EDITION = "tdd-optional"


def local_links(path):
    # Fenced examples can contain illustrative links; do not treat them as dependencies.
    body = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
        target = target.strip().strip("<>")
        if urlsplit(target).scheme or target.startswith("#") or "‹" in target:
            continue
        yield unquote(target.split("#", 1)[0])


class TemplateEditions(unittest.TestCase):
    def test_product_copies_have_closed_document_links(self):
        with tempfile.TemporaryDirectory() as td:
            project = pathlib.Path(td).resolve() / "product"
            shutil.copytree(ROOT / EDITION / "project", project)
            broken = []
            for page in project.rglob("*.md"):
                for link in local_links(page):
                    target = (page.parent / link).resolve()
                    if not target.is_relative_to(project) or not target.exists():
                        broken.append(f"{page.relative_to(project)} -> {link}")
            self.assertEqual([], broken, "Adopted product depends on missing/external files")
            for path in ("CLAUDE.md", "PROJECT-POLICY.md", "REVIEW.md", "templates/plan.md"):
                self.assertTrue((project / path).is_file(), path)
            for path in (".claude", ".agents", ".codex", ".opencode",
                         "org-skills", "docs/research"):
                self.assertFalse((project / path).exists(), "Maker tools must not be auto-installed")
            self.assertFalse(any(p.is_symlink() for p in project.rglob("*")))

    def test_marketplaces_resolve_the_matching_complete_plugin(self):
        folder = ROOT / EDITION
        manifest = json.loads((folder / "org-skills/.claude-plugin/plugin.json").read_text())
        catalog = json.loads((folder / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(1, len(catalog["plugins"]))
        plugin = catalog["plugins"][0]
        self.assertEqual(manifest["name"], plugin["name"])
        self.assertEqual(manifest["version"], plugin["version"])
        self.assertEqual((folder / plugin["source"]).resolve(), (folder / "org-skills").resolve())
        self.assertTrue((folder / "org-skills/agents/sdlc-verifier.md").is_file())
        self.assertTrue((folder / "org-skills/opencode/agents/sdlc-verifier.md").is_file())

    def test_root_marketplace_exports_only_the_surviving_package(self):
        folder = ROOT / EDITION
        manifest = json.loads((folder / "org-skills/.claude-plugin/plugin.json").read_text())
        local_plugin = json.loads((folder / ".claude-plugin/marketplace.json").read_text())["plugins"][0]
        root_catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(1, len(root_catalog["plugins"]))
        root_plugin = root_catalog["plugins"][0]
        self.assertEqual("intent-sdlc-skills-optional", root_plugin["name"])
        self.assertEqual(manifest["name"], root_plugin["name"])
        self.assertEqual(manifest["version"], root_plugin["version"])
        self.assertEqual(local_plugin["version"], root_plugin["version"])
        self.assertEqual((ROOT / root_plugin["source"]).resolve(),
                         (folder / "org-skills").resolve())
        self.assertFalse((ROOT / "tdd-first").exists())


if __name__ == "__main__":
    unittest.main()
