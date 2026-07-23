import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rednote-content-kit/skills"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


calendar = load_module(
    "render_calendar",
    SKILLS / "rednote-dated-calendar/scripts/render_calendar.py",
)
album = load_module(
    "render_album",
    SKILLS / "rednote-heartfelt-album/scripts/render_album.py",
)


class CreationSkillTests(unittest.TestCase):
    def test_calendar_template_validates_and_renders_html(self):
        template = SKILLS / "rednote-dated-calendar/assets/calendar-spec-template.json"
        with tempfile.TemporaryDirectory() as folder:
            result = calendar.render(template, Path(folder), None, True)
            self.assertTrue(result["ok"])
            self.assertTrue(result["weekday_verified"])
            self.assertTrue(Path(result["html_path"]).is_file())
            self.assertFalse(result["png_rendered"])

    def test_calendar_rejects_wrong_weekday(self):
        template = SKILLS / "rednote-dated-calendar/assets/calendar-spec-template.json"
        payload = json.loads(template.read_text(encoding="utf-8"))
        payload["weekday"] = "星期四"
        with tempfile.TemporaryDirectory() as folder:
            spec_path = Path(folder) / "calendar.json"
            spec_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(calendar.CalendarError):
                calendar.load_spec(spec_path)

    def test_album_template_validates_and_renders_seven_html_cards(self):
        template = SKILLS / "rednote-heartfelt-album/assets/album-spec-template.json"
        with tempfile.TemporaryDirectory() as folder:
            result = album.render(template, Path(folder), None, True)
            self.assertTrue(result["ok"])
            self.assertEqual(result["card_count"], 7)
            self.assertEqual(len(result["html_paths"]), 7)
            self.assertTrue(all(Path(path).is_file() for path in result["html_paths"]))

    def test_creation_skills_are_local_only(self):
        for skill in ("rednote-dated-calendar", "rednote-heartfelt-album"):
            text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("do not log in", text)
            self.assertIn("do not", text)
            self.assertNotIn("platform creator url", text)


if __name__ == "__main__":
    unittest.main()
