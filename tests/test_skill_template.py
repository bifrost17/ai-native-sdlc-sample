"""L2 202: "Ask Claude to write the result as intent.md using the organization's
template, which can be encoded as a skill set up by a technical team member and
signed off by a lead."  The template lives in the capture-intent skill; templates/intent.md
is its copy. This is the one check that the two have not drifted apart."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "capture-intent" / "SKILL.md"
TEMPLATE = ROOT / "templates" / "intent.md"


def fenced_template(text):
    m = re.search(r"```markdown\n(.*?)```", text, re.S)
    return m.group(1) if m else None


class SkillTemplateMatchesCopy(unittest.TestCase):
    def test_skill_embeds_template_verbatim(self):
        embedded = fenced_template(SKILL.read_text(encoding="utf-8"))
        self.assertIsNotNone(embedded, "capture-intent SKILL.md has no ```markdown fence")
        self.assertEqual(embedded, TEMPLATE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
