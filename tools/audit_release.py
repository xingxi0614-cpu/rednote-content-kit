#!/usr/bin/env python3
"""Audit a release tree for secrets, personal paths, unsafe files, and platform automation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".mjs", ".css", ".toml"}
REVIEWED_EXAMPLE_IMAGES = {
    "docs/assets/examples/freedom-album-cover.png": (1242, 1656),
    "docs/assets/examples/freedom-album-overview.png": (1440, 980),
    "docs/assets/examples/freedom-album-slide-01.png": (1242, 1656),
    "docs/assets/examples/freedom-album-slide-06.png": (1242, 1656),
}
BLOCKED_NAMES = {".DS_Store", ".env", "id_rsa", "id_ed25519"}
BLOCKED_SUFFIXES = {".pyc", ".pyo", ".pem", ".key", ".p12", ".pfx", ".zip", ".tar", ".gz"}
BLOCKED_PARTS = {"__pycache__", ".git", "output", "private", "secrets"}

PATTERNS = {
    "macOS home path": re.compile(r"/Users/[^/$\s`]+/"),
    "Windows home path": re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s`]+\\\\"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "platform creator URL": re.compile(r"creator\.xiaohongshu\.com", re.IGNORECASE),
    "removed upload adapter": re.compile(r"xhs_creator_draft_adapter|stageDraftBatch|stageNewDraft"),
    "browser automation dependency": re.compile(r"playwright|selenium|puppeteer|chrome:control-chrome", re.IGNORECASE),
}


def audit(root: Path, release: bool) -> list[str]:
    findings: list[str] = []
    root = root.resolve()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in BLOCKED_PARTS for part in relative.parts):
            if path.is_file() and ".git" not in relative.parts:
                findings.append(f"blocked directory content: {relative}")
            continue
        if not path.is_file():
            continue
        if path.name in BLOCKED_NAMES or path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(f"blocked file: {relative}")
            continue
        relative_posix = relative.as_posix()
        if relative_posix in REVIEWED_EXAMPLE_IMAGES:
            data = path.read_bytes()
            if len(data) > 10 * 1024 * 1024:
                findings.append(f"example image exceeds 10MB: {relative}")
                continue
            if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
                findings.append(f"invalid reviewed PNG: {relative}")
                continue
            width = int.from_bytes(data[16:20], "big")
            height = int.from_bytes(data[20:24], "big")
            if (width, height) != REVIEWED_EXAMPLE_IMAGES[relative_posix]:
                findings.append(f"reviewed PNG dimensions changed: {relative}")
            for marker in (b"/Users/", b"\\Users\\", b"password", b"token", b"cookie"):
                if marker.lower() in data.lower():
                    findings.append(f"sensitive metadata marker in reviewed PNG: {relative}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", ".gitignore"}:
            findings.append(f"unreviewed binary or file type: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non-UTF-8 file: {relative}")
            continue
        if relative.as_posix() == "tools/audit_release.py":
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {relative}")

    plugin_manifest = root / "plugins/rednote-content-kit/.codex-plugin/plugin.json"
    marketplace = root / ".agents/plugins/marketplace.json"
    try:
        plugin = json.loads(plugin_manifest.read_text(encoding="utf-8"))
        catalog = json.loads(marketplace.read_text(encoding="utf-8"))
        if plugin.get("name") != "rednote-content-kit":
            findings.append("plugin name mismatch")
        if plugin.get("skills") != "./skills/":
            findings.append("plugin skills path mismatch")
        entries = catalog.get("plugins", [])
        if len(entries) != 1 or entries[0].get("name") != plugin.get("name"):
            findings.append("marketplace entry mismatch")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        findings.append(f"manifest error: {exc}")

    if release:
        if (root / "RELEASE-HOLD.md").exists():
            findings.append("release hold is still active")
        license_text = (root / "LICENSE").read_text(encoding="utf-8") if (root / "LICENSE").exists() else ""
        if not license_text.startswith("MIT License\n"):
            findings.append("LICENSE is not the selected MIT license")
        try:
            plugin = json.loads(plugin_manifest.read_text(encoding="utf-8"))
            if plugin.get("license") != "MIT":
                findings.append("plugin manifest SPDX license is not MIT")
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        release_status_path = root / "release-status.json"
        try:
            status = json.loads(release_status_path.read_text(encoding="utf-8"))
            if status.get("public_release_allowed") is not True:
                findings.append("release status does not authorize public release")
            if status.get("license") != "MIT":
                findings.append("release status license is not MIT")
            if status.get("patent_review") not in {"application_filed", "cleared_no_filing"}:
                findings.append("patent review has not cleared public disclosure")
            if status.get("asset_rights_review") != "approved":
                findings.append("asset rights review is not approved")
            if status.get("publisher_identity") != "approved":
                findings.append("publisher identity is not approved")
            if status.get("repository") != "approved":
                findings.append("repository destination is not approved")
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            findings.append(f"release status error: {exc}")
        readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
        if "OWNER/REPOSITORY" in readme:
            findings.append("installation repository placeholder remains")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--release", action="store_true", help="enforce final public-release requirements")
    args = parser.parse_args()
    findings = audit(args.root, args.release)
    if findings:
        print("Audit failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Audit passed: no blocked files, secret patterns, personal paths, or platform automation found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
