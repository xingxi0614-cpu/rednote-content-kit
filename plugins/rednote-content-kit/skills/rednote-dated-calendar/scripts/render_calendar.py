#!/usr/bin/env python3
"""Validate and render one local-only dated RedNote calendar card."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import struct
import subprocess
import sys
from datetime import date
from pathlib import Path

WIDTH, HEIGHT = 1242, 1656
WEEKDAYS = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
SKILL_DIR = Path(__file__).resolve().parents[1]
CSS_PATH = SKILL_DIR / "assets" / "calendar.css"


class CalendarError(RuntimeError):
    pass


def text_value(spec: dict, key: str) -> str:
    value = str(spec.get(key) or "").strip()
    if not value:
        raise CalendarError(f"{key} is required")
    return value


def photo_path(spec: dict) -> Path | None:
    raw = str(spec.get("photo_path") or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise CalendarError("photo_path must be absolute")
    if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
        raise CalendarError(f"photo_path is missing or unsupported: {path}")
    return path.resolve()


def load_spec(path: Path) -> dict:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CalendarError(f"spec not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CalendarError(f"invalid JSON: {exc}") from exc
    if spec.get("schema_version") != 1:
        raise CalendarError("schema_version must be 1")
    if spec.get("package_type") != "dated-rednote-calendar":
        raise CalendarError("package_type must be dated-rednote-calendar")
    slug = text_value(spec, "slug")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise CalendarError("slug must contain lowercase letters, digits, and hyphens only")
    try:
        target = date.fromisoformat(text_value(spec, "date"))
    except ValueError as exc:
        raise CalendarError("date must use YYYY-MM-DD") from exc
    weekday = text_value(spec, "weekday")
    expected = WEEKDAYS[target.weekday()]
    if weekday != expected:
        raise CalendarError(f"weekday mismatch: expected {expected}")
    for key in ("lunar", "headline", "support_line", "source_type", "source_label", "photo_prompt"):
        text_value(spec, key)
    if spec["source_type"] not in {"original", "sourced"}:
        raise CalendarError("source_type must be original or sourced")
    if spec["source_type"] == "original" and spec["source_label"] != "原创":
        raise CalendarError("original text must use source_label 原创")
    if spec["source_type"] == "sourced" and spec["source_label"] == "原创":
        raise CalendarError("sourced text needs a traceable source_label")
    if spec["headline"].replace("\n", "") == spec["support_line"].replace("\n", ""):
        raise CalendarError("headline must not repeat support_line")
    photo_path(spec)
    return spec


def br(value: object) -> str:
    return "<br>".join(html.escape(part.strip()) for part in str(value).splitlines())


def make_html(spec: dict, css: str) -> str:
    target = date.fromisoformat(spec["date"])
    photo = photo_path(spec)
    style = ""
    if photo:
        position = html.escape(str(spec.get("photo_position") or "center"), quote=True)
        style = f' style="background-image:url(\'{html.escape(photo.as_uri(), quote=True)}\');background-position:{position}"'
    term = str(spec.get("term") or "").strip()
    term_html = f'<div class="term">{html.escape(term)}</div>' if term else ""
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(spec["date"])} 日历日签</title><style>{css}</style></head>
<body><main class="stage"><article class="card">
<section class="photo"{style}></section>
<section class="paper"><div class="copy">
<div class="headline">{br(spec["headline"])}</div>
<div class="support">{br(spec["support_line"])}<span class="source">—— {html.escape(spec["source_label"])}</span></div>
</div><aside class="date">
<div class="day">{target.day:02d}</div><div class="weekday">{html.escape(spec["weekday"])}</div>
<div class="ym">{target.year} . {target.month:02d}</div><div class="lunar">{html.escape(spec["lunar"])}</div>{term_html}
</aside></section></article></main></body></html>"""


def find_chrome(explicit: Path | None) -> Path | None:
    if explicit:
        path = explicit.expanduser().resolve()
        if not path.is_file():
            raise CalendarError(f"Chrome not found: {path}")
        return path
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    for name in ("google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return Path(found).resolve()
    return None


def inspect_png(path: Path) -> None:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise CalendarError(f"invalid PNG: {path}")
    if struct.unpack(">II", header[16:24]) != (WIDTH, HEIGHT):
        raise CalendarError(f"unexpected PNG dimensions: {path}")


def render(spec_path: Path, output_dir: Path, chrome_arg: Path | None, html_only: bool) -> dict:
    spec = load_spec(spec_path)
    if not CSS_PATH.is_file():
        raise CalendarError(f"CSS missing: {CSS_PATH}")
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f'rednote-{spec["date"]}-{spec["slug"]}'
    html_path = output_dir / f"{stem}.html"
    html_path.write_text(make_html(spec, CSS_PATH.read_text(encoding="utf-8")), encoding="utf-8")
    png_path = output_dir / f"{stem}.png"
    chrome = None if html_only else find_chrome(chrome_arg)
    warning = None
    if chrome:
        command = [str(chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                   "--allow-file-access-from-files", "--force-device-scale-factor=1",
                   f"--window-size={WIDTH},{HEIGHT}", "--virtual-time-budget=1500",
                   f"--screenshot={png_path}", html_path.resolve().as_uri()]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0 or not png_path.is_file():
            raise CalendarError((result.stderr or result.stdout).strip() or "Chrome render failed")
        inspect_png(png_path)
    elif not html_only:
        warning = "Chrome was not found; HTML was created but PNG rendering was skipped."
    return {"ok": True, "date": spec["date"], "weekday_verified": True,
            "html_path": str(html_path.resolve()), "png_rendered": png_path.is_file(),
            "png_path": str(png_path.resolve()) if png_path.is_file() else None,
            "warning": warning}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--chrome", type=Path)
    parser.add_argument("--html-only", action="store_true")
    args = parser.parse_args()
    try:
        result = render(args.spec.resolve(), args.output_dir.resolve(), args.chrome, args.html_only)
    except CalendarError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
