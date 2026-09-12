"""template-variants completion criteria: adopt each product without maker files.

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
EDITIONS = ("tdd-first", "tdd-optional")


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
        for edition in EDITIONS:
            with self.subTest(edition=edition), tempfile.TemporaryDirectory() as td:
                project = pathlib.Path(td).resolve() / "product"
                shutil.copytree(ROOT / edition / "project", project)
                broken = []
                for page in project.rglob("*.md"):
                    for link in local_links(page):
                        target = (page.parent / link).resolve()
                        if not target.is_relative_to(project) or not target.exists():
                            broken.append(f"{page.relative_to(project)} -> {link}")
                self.assertEqual([], broken, "Adopted product depends on missing/external files")
                for path in ("CLAUDE.md", "PROJECT-POLICY.md", "REVIEW.md", "templates/plan.md"):
                    self.assertTrue((project / path).is_file(), path)
                for path in (".claude", ".opencode", "org-skills", "docs/research"):
                    self.assertFalse((project / path).exists(), "Maker tools must not be auto-installed")
                self.assertFalse(any(p.is_symlink() for p in project.rglob("*")))

    def test_marketplaces_resolve_the_matching_complete_plugin(self):
        manifests = []
        for edition in EDITIONS:
            with self.subTest(edition=edition):
                folder = ROOT / edition
                manifest = json.loads((folder / "org-skills/.claude-plugin/plugin.json").read_text())
                manifests.append(manifest["name"])
                catalog = json.loads((folder / ".claude-plugin/marketplace.json").read_text())
                self.assertEqual(1, len(catalog["plugins"]))
                plugin = catalog["plugins"][0]
                self.assertEqual(manifest["name"], plugin["name"])
                self.assertEqual((folder / plugin["source"]).resolve(), (folder / "org-skills").resolve())
                self.assertTrue((folder / "org-skills/agents/sdlc-verifier.md").is_file())
                self.assertTrue((folder / "org-skills/opencode/agents/sdlc-verifier.md").is_file())
        self.assertEqual(len(manifests), len(set(manifests)), "Edition plugin identities collide")

    def test_non_strategy_forms_keep_the_same_contract(self):
        for name in ("intent.md", "spec.md"):
            with self.subTest(form=name):
                self.assertEqual((ROOT / EDITIONS[0] / "project/templates" / name).read_bytes(),
                                 (ROOT / EDITIONS[1] / "project/templates" / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
