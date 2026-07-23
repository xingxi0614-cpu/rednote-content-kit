#!/usr/bin/env python3
"""Validate and render a seven-page heartfelt Xiaohongshu carousel."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path


WIDTH = 1242
HEIGHT = 1656
PALETTES = {"clay", "forest", "night", "ocean"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
SKILL_DIR = Path(__file__).resolve().parents[1]
CSS_PATH = SKILL_DIR / "assets" / "album.css"


class AlbumError(RuntimeError):
    pass


def nonempty(value: object, label: str) -> str:
    result = str(value or "").strip()
    if not result:
        raise AlbumError(f"{label} is required")
    return result


def optional_photo(block: dict, label: str) -> Path | None:
    raw = str(block.get("photo_path") or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise AlbumError(f"{label}.photo_path must be absolute: {raw}")
    if not path.is_file():
        raise AlbumError(f"{label}.photo_path does not exist: {path}")
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        raise AlbumError(f"{label}.photo_path has unsupported format: {path}")
    return path.resolve()


def load_spec(path: Path) -> dict:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AlbumError(f"spec not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AlbumError(f"invalid JSON: {path}: {exc}") from exc

    if spec.get("schema_version") != 1:
        raise AlbumError("schema_version must be 1")
    if spec.get("package_type") != "heartfelt-xhs-album":
        raise AlbumError("package_type must be heartfelt-xhs-album")

    slug = nonempty(spec.get("slug"), "slug")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise AlbumError("slug must contain lowercase letters, digits, and hyphens only")
    nonempty(spec.get("series"), "series")
    nonempty(spec.get("theme"), "theme")
    if str(spec.get("palette", "clay")) not in PALETTES:
        raise AlbumError(f"palette must be one of: {', '.join(sorted(PALETTES))}")

    cover = spec.get("cover")
    if not isinstance(cover, dict):
        raise AlbumError("cover must be an object")
    nonempty(cover.get("headline"), "cover.headline")
    nonempty(cover.get("subtitle"), "cover.subtitle")
    nonempty(cover.get("photo_prompt"), "cover.photo_prompt")
    optional_photo(cover, "cover")

    slides = spec.get("slides")
    if not isinstance(slides, list) or len(slides) != 6:
        raise AlbumError("slides must contain exactly six objects")
    seen_headlines: set[str] = set()
    seen_support: set[str] = set()
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise AlbumError(f"slide {index} must be an object")
        headline = nonempty(slide.get("headline"), f"slide {index}.headline")
        support = nonempty(slide.get("support_line"), f"slide {index}.support_line")
        source_type = nonempty(slide.get("source_type"), f"slide {index}.source_type")
        source_label = nonempty(slide.get("source_label"), f"slide {index}.source_label")
        nonempty(slide.get("photo_prompt"), f"slide {index}.photo_prompt")
        optional_photo(slide, f"slide {index}")
        if source_type not in {"original", "sourced"}:
            raise AlbumError(f"slide {index}.source_type must be original or sourced")
        if source_type == "original" and source_label != "原创":
            raise AlbumError(f"slide {index} original text must use source_label 原创")
        if source_type == "sourced" and source_label == "原创":
            raise AlbumError(f"slide {index} sourced text requires a traceable source_label")
        if headline == support:
            raise AlbumError(f"slide {index} headline must not repeat support_line")
        if headline in seen_headlines:
            raise AlbumError(f"duplicate slide headline: {headline}")
        if support in seen_support:
            raise AlbumError(f"duplicate slide support_line: {support}")
        seen_headlines.add(headline)
        seen_support.add(support)
    return spec


def br(value: object) -> str:
    return "<br>".join(html.escape(part.strip()) for part in str(value).splitlines())


def visual(block: dict) -> str:
    path = optional_photo(block, "visual")
    if path:
        uri = html.escape(path.as_uri(), quote=True)
        return f'<section class="visual" style="background-image:url(\'{uri}\')"></section>'
    return '<section class="visual placeholder"></section>'


def document(title: str, palette: str, markup: str, css: str) -> str:
    palette_class = "" if palette == "clay" else f" palette-{palette}"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{css}</style>
</head>
<body class="{palette_class.strip()}">
  <main class="stage">{markup}</main>
</body>
</html>
"""


def cover_markup(spec: dict) -> str:
    cover = spec["cover"]
    volume = html.escape(str(spec.get("volume", "VOL. 01")))
    return f"""
<article class="card cover">
  {visual(cover)}
  <section class="paper">
    <div class="kicker">{html.escape(spec['series'])} · {volume}</div>
    <h1>{br(cover['headline'])}</h1>
    <div class="subtitle">{br(cover['subtitle'])}</div>
    <div class="rule"></div>
  </section>
</article>"""


def slide_markup(spec: dict, slide: dict, index: int) -> str:
    return f"""
<article class="card inner">
  {visual(slide)}
  <section class="paper">
    <div>
      <div class="kicker">{html.escape(spec['series'])}</div>
      <h1>{br(slide['headline'])}</h1>
      <div class="support">{br(slide['support_line'])}</div>
      <span class="source">—— {html.escape(slide['source_label'])}</span>
    </div>
    <aside class="page-mark">
      <div class="number">{index:02d}</div>
      <div class="total">OF 06</div>
      <div class="series">{html.escape(spec['series'])}<br>{html.escape(str(spec.get('volume', 'VOL. 01')))}</div>
    </aside>
  </section>
</article>"""


def find_chrome(explicit: Path | None) -> Path | None:
    if explicit:
        path = explicit.expanduser().resolve()
        if not path.is_file():
            raise AlbumError(f"Chrome executable not found: {path}")
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
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return Path(found).resolve()
    return None


def inspect_png(path: Path, width: int, height: int) -> None:
    with path.open("rb") as image_file:
        header = image_file.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise AlbumError(f"invalid PNG output: {path}")
    actual = struct.unpack(">II", header[16:24])
    if actual != (width, height):
        raise AlbumError(f"unexpected PNG dimensions {actual[0]}x{actual[1]}: {path}")


def screenshot(chrome: Path, html_path: Path, png_path: Path, width: int, height: int) -> None:
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        "--virtual-time-budget=1500",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not png_path.is_file():
        detail = (result.stderr or result.stdout).strip()
        raise AlbumError(f"Chrome render failed for {html_path.name}: {detail}")
    inspect_png(png_path, width, height)


def preview_document(spec: dict, images: list[Path]) -> str:
    figures = "\n".join(
        f'<figure><img src="{path.as_uri()}" alt="card {index}"><figcaption>{index:02d}</figcaption></figure>'
        for index, path in enumerate(images)
    )
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box}} html,body{{margin:0;width:1440px;height:980px;overflow:hidden;background:#e8e1d6}}
body{{padding:40px 50px;font-family:"PingFang SC",sans-serif;color:#25211d}} header{{height:76px;display:flex;justify-content:space-between;align-items:baseline}}
h1{{margin:0;font-family:"Songti SC",serif;font-size:36px}} p{{margin:0;color:#81776c;font-size:17px}}
main{{display:grid;grid-template-columns:repeat(4,1fr);gap:26px 24px}} figure{{margin:0;height:388px;position:relative;background:#f6f1e9;box-shadow:0 10px 24px rgba(44,38,28,.14)}}
img{{width:100%;height:100%;object-fit:contain;display:block}} figcaption{{position:absolute;right:9px;bottom:8px;background:rgba(246,241,233,.92);padding:4px 7px;color:#ad493d;font-size:12px}}
</style></head><body><header><h1>{html.escape(spec['theme'])}</h1><p>{html.escape(spec['series'])} · 1 封面 + 6 内页</p></header><main>{figures}</main></body></html>"""


def render(spec_path: Path, output_dir: Path, chrome_arg: Path | None, html_only: bool) -> dict:
    spec = load_spec(spec_path)
    if not CSS_PATH.is_file():
        raise AlbumError(f"CSS asset missing: {CSS_PATH}")
    css = CSS_PATH.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = spec["slug"]
    palette = str(spec.get("palette", "clay"))

    markup = [cover_markup(spec)] + [slide_markup(spec, slide, index) for index, slide in enumerate(spec["slides"], 1)]
    html_paths: list[Path] = []
    for index, card in enumerate(markup):
        suffix = "00-cover" if index == 0 else f"{index:02d}"
        path = output_dir / f"xhs-album-{slug}-{suffix}.html"
        path.write_text(document(spec["theme"], palette, card, css), encoding="utf-8")
        html_paths.append(path.resolve())

    chrome = None if html_only else find_chrome(chrome_arg)
    image_paths: list[Path] = []
    preview_path: Path | None = None
    warning = None
    if chrome:
        for html_path in html_paths:
            png_path = html_path.with_suffix(".png")
            screenshot(chrome, html_path, png_path, WIDTH, HEIGHT)
            image_paths.append(png_path.resolve())
        preview_html = output_dir / f"xhs-album-{slug}-preview.html"
        preview_html.write_text(preview_document(spec, image_paths), encoding="utf-8")
        preview_path = output_dir / f"xhs-album-{slug}-preview.png"
        screenshot(chrome, preview_html.resolve(), preview_path, 1440, 980)
        preview_path = preview_path.resolve()
    elif not html_only:
        warning = "Chrome was not found; HTML cards were created but PNG rendering was skipped."

    return {
        "ok": True,
        "slug": slug,
        "card_count": 7,
        "html_paths": [str(path) for path in html_paths],
        "png_rendered": bool(image_paths),
        "image_paths": [str(path) for path in image_paths],
        "preview_path": str(preview_path) if preview_path else None,
        "warning": warning,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--chrome", type=Path)
    parser.add_argument("--html-only", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output_dir = (args.output_dir or args.spec.parent).expanduser().resolve()
    try:
        result = render(args.spec.expanduser().resolve(), output_dir, args.chrome, args.html_only)
    except AlbumError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
