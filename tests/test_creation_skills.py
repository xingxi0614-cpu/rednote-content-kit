import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
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
image_assets = load_module(
    "image_assets",
    SKILLS / "rednote-image-assets/scripts/image_assets.py",
)


def write_png(path: Path, width: int, height: int, color: tuple[int, int, int]):
    def chunk(name: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + name
            + data
            + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)
        )

    row = b"\x00" + bytes(color) * width
    raw = row * height
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


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
        for skill in (
            "rednote-dated-calendar",
            "rednote-heartfelt-album",
            "rednote-image-assets",
        ):
            text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("do not log in", text)
            self.assertIn("do not", text)
            self.assertNotIn("platform creator url", text)

    def test_image_plan_lists_calendar_and_album_slots(self):
        calendar_template = (
            SKILLS / "rednote-dated-calendar/assets/calendar-spec-template.json"
        )
        album_template = (
            SKILLS / "rednote-heartfelt-album/assets/album-spec-template.json"
        )
        calendar_plan = image_assets.build_plan(calendar_template)
        album_plan = image_assets.build_plan(album_template)
        self.assertEqual(
            [asset["slot"] for asset in calendar_plan["assets"]], ["calendar"]
        )
        self.assertEqual(len(album_plan["assets"]), 7)
        self.assertEqual(album_plan["assets"][0]["filename"], "00-cover.png")
        self.assertEqual(album_plan["assets"][-1]["filename"], "06.png")
        self.assertTrue(album_plan["requirements"]["unique_images_required"])

    def test_album_images_bind_and_pass_strict_html_render(self):
        template = SKILLS / "rednote-heartfelt-album/assets/album-spec-template.json"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            assets_dir = root / "generated-images"
            assets_dir.mkdir()
            names = ["00-cover.png"] + [f"{index:02d}.png" for index in range(1, 7)]
            for index, name in enumerate(names):
                write_png(
                    assets_dir / name,
                    1024,
                    768,
                    (40 + index * 20, 90 + index * 10, 120 + index * 8),
                )
            bound_spec = root / "album.with-images.json"
            result = image_assets.bind_images(template, assets_dir, bound_spec)
            self.assertTrue(result["ok"])
            self.assertEqual(result["asset_count"], 7)
            self.assertTrue(result["unique_assets"])

            bound = json.loads(bound_spec.read_text(encoding="utf-8"))
            self.assertTrue(Path(bound["cover"]["photo_path"]).is_absolute())
            self.assertEqual(
                len({slide["photo_path"] for slide in bound["slides"]}), 6
            )
            render_result = album.render(
                bound_spec,
                root / "html",
                None,
                True,
                require_complete_visuals=True,
            )
            self.assertEqual(render_result["photo_count"], 7)
            self.assertEqual(render_result["visual_mode"], "photographs")
            self.assertTrue(render_result["strict_visuals"])

    def test_strict_render_rejects_placeholders(self):
        calendar_template = (
            SKILLS / "rednote-dated-calendar/assets/calendar-spec-template.json"
        )
        album_template = (
            SKILLS / "rednote-heartfelt-album/assets/album-spec-template.json"
        )
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            with self.assertRaises(calendar.CalendarError):
                calendar.render(
                    calendar_template,
                    output / "calendar",
                    None,
                    True,
                    require_complete_visuals=True,
                )
            with self.assertRaises(album.AlbumError):
                album.render(
                    album_template,
                    output / "album",
                    None,
                    True,
                    require_complete_visuals=True,
                )

    def test_binding_rejects_duplicate_album_images(self):
        template = SKILLS / "rednote-heartfelt-album/assets/album-spec-template.json"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            assets_dir = root / "generated-images"
            assets_dir.mkdir()
            names = ["00-cover.png"] + [f"{index:02d}.png" for index in range(1, 7)]
            for name in names:
                write_png(assets_dir / name, 1024, 768, (80, 120, 160))
            with self.assertRaises(image_assets.ImageAssetsError):
                image_assets.bind_images(
                    template, assets_dir, root / "album.with-images.json"
                )


if __name__ == "__main__":
    unittest.main()
