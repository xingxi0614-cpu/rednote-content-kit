import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BilingualContractTests(unittest.TestCase):
    def test_chinese_is_default_readme(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("# 小红书本地内容工具包\n"))
        self.assertIn("[English](README.en.md)", readme)
        self.assertTrue((ROOT / "README.en.md").is_file())

    def test_core_guides_have_english_alternatives(self):
        for chinese_path, english_path in (
            ("docs/INSTALL.md", "docs/INSTALL.en.md"),
            ("docs/EXAMPLES.md", "docs/EXAMPLES.en.md"),
        ):
            self.assertTrue((ROOT / chinese_path).is_file())
            self.assertTrue((ROOT / english_path).is_file())

    def test_plugin_defaults_to_chinese(self):
        manifest = json.loads(
            (ROOT / "plugins/rednote-content-kit/.codex-plugin/plugin.json").read_text(
                encoding="utf-8"
            )
        )
        interface = manifest["interface"]
        self.assertEqual(interface["displayName"], "小红书本地内容工具包")
        self.assertTrue(all("中文" in prompt for prompt in interface["defaultPrompt"]))

    def test_skills_share_the_language_contract(self):
        for skill in ("rednote-content-pack", "rednote-manual-publish-guard"):
            text = (
                ROOT / f"plugins/rednote-content-kit/skills/{skill}/SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Use Simplified Chinese by default", text)
            self.assertIn("Switch to English only", text)


if __name__ == "__main__":
    unittest.main()
