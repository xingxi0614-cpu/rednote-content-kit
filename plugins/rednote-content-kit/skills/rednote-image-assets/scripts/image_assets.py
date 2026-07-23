#!/usr/bin/env python3
"""Plan and bind local image assets for RedNote calendar and album specs."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import struct
import sys
from pathlib import Path


IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")
MIN_WIDTH = 768
MIN_HEIGHT = 512
MIN_RATIO = 1.20
MAX_RATIO = 1.80


class ImageAssetsError(RuntimeError):
    pass


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ImageAssetsError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ImageAssetsError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ImageAssetsError(f"JSON root must be an object: {path}")
    return value


def nonempty(value: object, label: str) -> str:
    result = str(value or "").strip()
    if not result:
        raise ImageAssetsError(f"{label} is required")
    return result


def expected_assets(spec: dict) -> list[dict]:
    if spec.get("schema_version") != 1:
        raise ImageAssetsError("schema_version must be 1")
    package_type = spec.get("package_type")
    slug = nonempty(spec.get("slug"), "slug")
    if package_type == "dated-rednote-calendar":
        return [
            {
                "slot": "calendar",
                "filename": "calendar.png",
                "prompt": nonempty(spec.get("photo_prompt"), "photo_prompt"),
                "target": ("calendar", None),
                "slug": slug,
            }
        ]
    if package_type == "heartfelt-xhs-album":
        cover = spec.get("cover")
        slides = spec.get("slides")
        if not isinstance(cover, dict):
            raise ImageAssetsError("cover must be an object")
        if not isinstance(slides, list) or len(slides) != 6:
            raise ImageAssetsError("slides must contain exactly six objects")
        items = [
            {
                "slot": "cover",
                "filename": "00-cover.png",
                "prompt": nonempty(cover.get("photo_prompt"), "cover.photo_prompt"),
                "target": ("cover", None),
                "slug": slug,
            }
        ]
        for index, slide in enumerate(slides, start=1):
            if not isinstance(slide, dict):
                raise ImageAssetsError(f"slide {index} must be an object")
            items.append(
                {
                    "slot": f"slide-{index:02d}",
                    "filename": f"{index:02d}.png",
                    "prompt": nonempty(
                        slide.get("photo_prompt"), f"slide {index}.photo_prompt"
                    ),
                    "target": ("slide", index - 1),
                    "slug": slug,
                }
            )
        return items
    raise ImageAssetsError(
        "package_type must be dated-rednote-calendar or heartfelt-xhs-album"
    )


def build_plan(spec_path: Path) -> dict:
    spec = read_json(spec_path)
    items = expected_assets(spec)
    return {
        "schema_version": 1,
        "package_type": "rednote-image-plan",
        "source_package_type": spec["package_type"],
        "slug": items[0]["slug"],
        "preferred_generator": "host-imagegen-or-imagen",
        "requirements": {
            "orientation": "landscape",
            "preferred_aspect_ratio": "4:3",
            "minimum_dimensions": f"{MIN_WIDTH}x{MIN_HEIGHT}",
            "embedded_text": False,
            "watermark": False,
            "logo": False,
            "unique_images_required": len(items) > 1,
        },
        "assets": [
            {
                "slot": item["slot"],
                "filename": item["filename"],
                "prompt": item["prompt"],
            }
            for item in items
        ],
    }


def write_new_json(path: Path, value: dict) -> None:
    if path.exists():
        raise ImageAssetsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if (
        len(header) < 24
        or header[:8] != b"\x89PNG\r\n\x1a\n"
        or header[12:16] != b"IHDR"
    ):
        raise ImageAssetsError(f"invalid PNG: {path.name}")
    return struct.unpack(">II", header[16:24])


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ImageAssetsError(f"invalid JPEG: {path.name}")
    offset = 2
    while offset + 9 <= len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in {0xD8, 0xD9}:
            continue
        if marker == 0xDA:
            break
        if offset + 2 > len(data):
            break
        length = int.from_bytes(data[offset : offset + 2], "big")
        if length < 2 or offset + length > len(data):
            break
        if marker in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            return width, height
        offset += length
    raise ImageAssetsError(f"JPEG dimensions could not be read: {path.name}")


def image_dimensions(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return png_dimensions(path)
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_dimensions(path)
    raise ImageAssetsError(f"unsupported generated image format: {path.name}")


def find_asset(assets_dir: Path, expected_name: str) -> Path:
    stem = Path(expected_name).stem
    matches = [
        assets_dir / f"{stem}{suffix}"
        for suffix in IMAGE_SUFFIXES
        if (assets_dir / f"{stem}{suffix}").is_file()
    ]
    if not matches:
        raise ImageAssetsError(
            f"missing image asset for {stem}; expected one of: "
            + ", ".join(f"{stem}{suffix}" for suffix in IMAGE_SUFFIXES)
        )
    if len(matches) > 1:
        raise ImageAssetsError(
            f"ambiguous image asset for {stem}: "
            + ", ".join(path.name for path in matches)
        )
    path = matches[0]
    if path.is_symlink():
        raise ImageAssetsError(f"symbolic links are not allowed: {path.name}")
    return path.resolve()


def validate_asset(path: Path) -> dict:
    width, height = image_dimensions(path)
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        raise ImageAssetsError(
            f"image is too small ({width}x{height}): {path.name}; "
            f"minimum is {MIN_WIDTH}x{MIN_HEIGHT}"
        )
    ratio = width / height
    if width <= height or not MIN_RATIO <= ratio <= MAX_RATIO:
        raise ImageAssetsError(
            f"image must be landscape and close to 4:3 ({width}x{height}): {path.name}"
        )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "filename": path.name,
        "width": width,
        "height": height,
        "sha256": digest,
    }


def bind_images(spec_path: Path, assets_dir: Path, output_spec: Path) -> dict:
    spec = read_json(spec_path)
    items = expected_assets(spec)
    assets_dir = assets_dir.expanduser().resolve()
    if not assets_dir.is_dir():
        raise ImageAssetsError(f"assets directory not found: {assets_dir}")
    if output_spec.exists():
        raise ImageAssetsError(f"refusing to overwrite existing file: {output_spec}")

    bound = copy.deepcopy(spec)
    report_assets: list[dict] = []
    seen_hashes: set[str] = set()
    for item in items:
        path = find_asset(assets_dir, item["filename"])
        report = validate_asset(path)
        if report["sha256"] in seen_hashes:
            raise ImageAssetsError(
                f"duplicate image content detected for slot {item['slot']}: {path.name}"
            )
        seen_hashes.add(report["sha256"])
        target, index = item["target"]
        if target == "calendar":
            bound["photo_path"] = str(path)
        elif target == "cover":
            bound["cover"]["photo_path"] = str(path)
        else:
            bound["slides"][index]["photo_path"] = str(path)
        report_assets.append({"slot": item["slot"], **report})

    output_spec.parent.mkdir(parents=True, exist_ok=True)
    output_spec.write_text(
        json.dumps(bound, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "ok": True,
        "source_package_type": spec["package_type"],
        "asset_count": len(report_assets),
        "unique_assets": len(seen_hashes) == len(report_assets),
        "output_spec": str(output_spec.resolve()),
        "assets": report_assets,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="write an image-generation plan")
    plan_parser.add_argument("--spec", required=True, type=Path)
    plan_parser.add_argument("--output", required=True, type=Path)

    bind_parser = subparsers.add_parser(
        "bind", help="validate deterministic image files and bind them to a spec"
    )
    bind_parser.add_argument("--spec", required=True, type=Path)
    bind_parser.add_argument("--assets-dir", required=True, type=Path)
    bind_parser.add_argument("--output-spec", required=True, type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "plan":
            plan = build_plan(args.spec.expanduser().resolve())
            write_new_json(args.output.expanduser().resolve(), plan)
            result = {
                "ok": True,
                "asset_count": len(plan["assets"]),
                "output": str(args.output.expanduser().resolve()),
            }
        else:
            result = bind_images(
                args.spec.expanduser().resolve(),
                args.assets_dir,
                args.output_spec.expanduser().resolve(),
            )
    except ImageAssetsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
