import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "plugins/rednote-content-kit/skills/rednote-content-pack/scripts/build_handoff.py"
SPEC = importlib.util.spec_from_file_location("build_handoff", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class BuildHandoffTests(unittest.TestCase):
    def write_spec(self, root: Path, image_path: str = "images/cover.png") -> Path:
        (root / "images").mkdir()
        (root / "images/cover.png").write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-test-data")
        payload = {
            "schema_version": 1,
            "language": "zh-CN",
            "package_id": "test-package",
            "title_options": ["测试标题", "备选标题"],
            "recommended_title": "测试标题",
            "caption": "这是一段只使用合成数据的测试正文。",
            "topics": ["测试", "本地交付"],
            "comment_starter": "测试问题？",
            "collection_suggestion": "测试合集",
            "images": [{"path": image_path, "alt": "合成测试图片"}],
        }
        path = root / "spec.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_build_uses_relative_output_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = self.write_spec(root)
            output = root / "dist/package"
            result = MODULE.build(spec, output)
            manifest_text = Path(result["manifest"]).read_text(encoding="utf-8")
            handoff_text = Path(result["handoff"]).read_text(encoding="utf-8")
            self.assertNotIn(str(root), manifest_text)
            self.assertNotIn(str(root), handoff_text)
            manifest = json.loads(manifest_text)
            self.assertEqual(manifest["language"], "zh-CN")
            self.assertEqual(manifest["images"][0]["path"], "images/01.png")
            self.assertIn("## 推荐标题", handoff_text)
            self.assertEqual(result["images"], 1)

    def test_build_supports_english_handoff(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = self.write_spec(root)
            payload = json.loads(spec_path.read_text(encoding="utf-8"))
            payload["language"] = "en"
            payload["title_options"] = ["Test title", "Alternative title"]
            payload["recommended_title"] = "Test title"
            payload["caption"] = "Synthetic test caption."
            payload["topics"] = ["test", "local handoff"]
            payload["comment_starter"] = "Test question?"
            payload["collection_suggestion"] = "Test collection"
            spec_path.write_text(json.dumps(payload), encoding="utf-8")

            result = MODULE.build(spec_path, root / "dist/package")
            manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
            handoff = Path(result["handoff"]).read_text(encoding="utf-8")
            self.assertEqual(manifest["language"], "en")
            self.assertIn("## Recommended Title", handoff)
            self.assertIn("## Manual Checklist", handoff)
            self.assertNotIn("## 推荐标题", handoff)

    def test_rejects_unsupported_language(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = self.write_spec(root)
            payload = json.loads(spec_path.read_text(encoding="utf-8"))
            payload["language"] = "fr"
            spec_path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(MODULE.HandoffError):
                MODULE.build(spec_path, root / "dist/package")

    def test_rejects_absolute_image_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = self.write_spec(root, str((root / "images/cover.png").resolve()))
            with self.assertRaises(MODULE.HandoffError):
                MODULE.build(spec, root / "dist/package")

    def test_rejects_too_many_topics(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = self.write_spec(root)
            payload = json.loads(spec_path.read_text(encoding="utf-8"))
            payload["topics"] = [f"topic-{index}" for index in range(11)]
            spec_path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(MODULE.HandoffError):
                MODULE.build(spec_path, root / "dist/package")

    def test_rejects_disguised_non_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = self.write_spec(root)
            (root / "images/cover.png").write_bytes(b"not-an-image")
            with self.assertRaises(MODULE.HandoffError):
                MODULE.build(spec_path, root / "dist/package")

    def test_refuses_nonempty_output_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = self.write_spec(root)
            output = root / "dist/package"
            output.mkdir(parents=True)
            (output / "keep.txt").write_text("do not overwrite", encoding="utf-8")
            with self.assertRaises(MODULE.HandoffError):
                MODULE.build(spec_path, output)


if __name__ == "__main__":
    unittest.main()
