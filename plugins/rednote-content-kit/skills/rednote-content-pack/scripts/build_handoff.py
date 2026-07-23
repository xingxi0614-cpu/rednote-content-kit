#!/usr/bin/env python3
"""Build a privacy-safe local handoff package from a strict JSON spec."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}
MAX_IMAGE_BYTES = 32 * 1024 * 1024
PACKAGE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class HandoffError(RuntimeError):
    pass


def clean_line(value: object, field: str, *, required: bool = True) -> str:
    text = str(value or "").strip()
    if required and not text:
        raise HandoffError(f"{field} is required")
    if "\n" in text or "\r" in text:
        raise HandoffError(f"{field} must be a single line")
    return text


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_image_file(path: Path) -> None:
    size = path.stat().st_size
    if size <= 0 or size > MAX_IMAGE_BYTES:
        raise HandoffError(f"image size must be between 1 byte and {MAX_IMAGE_BYTES} bytes: {path.name}")
    with path.open("rb") as source:
        header = source.read(12)
    suffix = path.suffix.lower()
    valid = (
        (suffix == ".png" and header.startswith(b"\x89PNG\r\n\x1a\n"))
        or (suffix in {".jpg", ".jpeg"} and header.startswith(b"\xff\xd8\xff"))
        or (suffix == ".webp" and header[:4] == b"RIFF" and header[8:12] == b"WEBP")
    )
    if not valid:
        raise HandoffError(f"image content does not match its supported suffix: {path.name}")


def load_spec(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HandoffError(f"spec not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HandoffError(f"invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise HandoffError("spec root must be an object")
    if payload.get("schema_version") != 1:
        raise HandoffError("schema_version must be 1")
    return payload


def validate_spec(spec: dict, spec_dir: Path) -> dict:
    package_id = clean_line(spec.get("package_id"), "package_id")
    if not PACKAGE_ID.fullmatch(package_id):
        raise HandoffError("package_id must use lowercase letters, digits, and hyphens")

    raw_titles = spec.get("title_options")
    if not isinstance(raw_titles, list) or not 1 <= len(raw_titles) <= 5:
        raise HandoffError("title_options must contain 1-5 items")
    titles = [clean_line(value, "title option") for value in raw_titles]
    if len(set(titles)) != len(titles):
        raise HandoffError("title_options must be unique")
    recommended = clean_line(spec.get("recommended_title"), "recommended_title")
    if recommended not in titles:
        raise HandoffError("recommended_title must match one title option")

    caption = str(spec.get("caption") or "").strip()
    if not caption:
        raise HandoffError("caption is required")

    raw_topics = spec.get("topics")
    if not isinstance(raw_topics, list) or not 1 <= len(raw_topics) <= 10:
        raise HandoffError("topics must contain 1-10 items")
    topics = [clean_line(value, "topic").lstrip("#").strip() for value in raw_topics]
    if any(not topic for topic in topics) or len(set(topics)) != len(topics):
        raise HandoffError("topics must be non-empty and unique")

    raw_images = spec.get("images")
    if not isinstance(raw_images, list) or not 1 <= len(raw_images) <= 18:
        raise HandoffError("images must contain 1-18 items")

    images: list[dict] = []
    root = spec_dir.resolve()
    for index, item in enumerate(raw_images, start=1):
        if not isinstance(item, dict):
            raise HandoffError(f"image {index} must be an object")
        raw_path = clean_line(item.get("path"), f"image {index} path")
        relative = Path(raw_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise HandoffError(f"image {index} path must be relative and cannot traverse parents")
        source = (root / relative).resolve()
        if not is_within(source, root):
            raise HandoffError(f"image {index} escapes the spec directory")
        if source.is_symlink() or not source.is_file():
            raise HandoffError(f"image {index} must be a regular non-symlink file")
        if source.suffix.lower() not in SUPPORTED_IMAGES:
            raise HandoffError(f"image {index} has an unsupported suffix")
        validate_image_file(source)
        images.append({
            "source": source,
            "alt": clean_line(item.get("alt"), f"image {index} alt", required=False),
        })

    return {
        "schema_version": 1,
        "package_id": package_id,
        "title_options": titles,
        "recommended_title": recommended,
        "caption": caption,
        "topics": topics,
        "comment_starter": clean_line(spec.get("comment_starter"), "comment_starter", required=False),
        "collection_suggestion": clean_line(spec.get("collection_suggestion"), "collection_suggestion", required=False),
        "images": images,
    }


def build(spec_path: Path, output_dir: Path) -> dict:
    spec_path = spec_path.resolve()
    output_dir = output_dir.resolve()
    spec = validate_spec(load_spec(spec_path), spec_path.parent)
    if output_dir == Path(output_dir.anchor):
        raise HandoffError("refusing to use a filesystem root as output")
    if output_dir.is_symlink():
        raise HandoffError("output directory cannot be a symlink")
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise HandoffError("output directory must not exist or must be empty")

    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    manifest_images = []
    for index, image in enumerate(spec["images"], start=1):
        source: Path = image["source"]
        destination = images_dir / f"{index:02d}{source.suffix.lower()}"
        shutil.copy2(source, destination)
        manifest_images.append({
            "order": index,
            "path": destination.relative_to(output_dir).as_posix(),
            "alt": image["alt"],
            "sha256": sha256(destination),
        })

    manifest = {key: value for key, value in spec.items() if key != "images"}
    manifest["images"] = manifest_images
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {spec['package_id']} 手工发布交付包",
        "",
        "## 图片顺序",
        "",
    ]
    for image in manifest_images:
        suffix = f" — {image['alt']}" if image["alt"] else ""
        lines.append(f"{image['order']}. `{image['path']}`{suffix}")
    lines.extend([
        "",
        "## 推荐标题",
        "",
        spec["recommended_title"],
        "",
        "## 备选标题",
        "",
        *[f"- {title}" for title in spec["title_options"] if title != spec["recommended_title"]],
        "",
        "## 正文",
        "",
        spec["caption"],
        "",
        "## 话题候选",
        "",
        " ".join(f"#{topic}" for topic in spec["topics"]),
    ])
    if spec["comment_starter"]:
        lines.extend(["", "## 评论引导", "", spec["comment_starter"]])
    if spec["collection_suggestion"]:
        lines.extend(["", "## 合集建议", "", spec["collection_suggestion"]])
    lines.extend([
        "",
        "## 手工操作清单",
        "",
        "1. 按图片顺序由用户本人选择本地文件。",
        "2. 复制推荐标题。",
        "3. 复制正文。",
        "4. 由用户本人核对并选择相关话题、合集、可见范围和发布时间。",
        "5. 发布前再次检查图片、文字、版权、隐私和平台规则。",
        "",
        "> 本工具未登录、上传、存草稿、定时或发布任何内容。",
        "",
    ])
    handoff_path = output_dir / "handoff.md"
    handoff_path.write_text("\n".join(lines), encoding="utf-8")
    return {"manifest": str(manifest_path), "handoff": str(handoff_path), "images": len(manifest_images)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.spec, args.output)
    except HandoffError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
