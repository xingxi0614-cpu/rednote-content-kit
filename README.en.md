# Rednote Content Kit

[简体中文（默认）](README.md) | [English](README.en.md)

[![CI](https://github.com/xingxi0614-cpu/rednote-content-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/xingxi0614-cpu/rednote-content-kit/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

An open-source Codex workflow for preparing Xiaohongshu/RedNote image posts locally: planning, copy, image ordering, privacy checks, and a manual publishing handoff.

**It prepares the content, but it never logs in, uploads, or publishes for you.**

## Why this project exists

Image-post creation involves more than writing a caption. Common failures include incorrect image order, copy that does not match the visuals, excessive topics, unreliable attribution, leaked local paths, or handing account credentials to automation.

This project turns those steps into a reusable, verifiable, local-only workflow. The output is a set of images, copy-ready text, a JSON manifest, and a manual checklist, while the user keeps control of the account.

## Example output

This original sample shows a local `1 cover + 6 inner cards` workflow. The scenery was generated and all editorial copy is original.

![Freedom album overview](docs/assets/examples/freedom-album-overview.png)

<p align="center">
  <img src="docs/assets/examples/freedom-album-cover.png" alt="Freedom album cover" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-01.png" alt="Freedom album first inner card" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-06.png" alt="Freedom album final inner card" width="31%">
</p>

See [example provenance and checks](docs/EXAMPLES.en.md) for dimensions, safety review, and SHA-256 values.

## Features

- Build a content brief covering audience, scene, objective, evidence, and intended next action.
- Plan dated cards, single-image notes, or no-date albums.
- Prepare recommended and alternative titles, captions, topics, and a comment starter.
- Validate image type and order, topic limits, attribution, and copy-image consistency.
- Copy only selected images into a clean handoff directory with relative paths and SHA-256 hashes.
- Generate `handoff.md` and `manifest.json` for manual copy and upload.
- Use Simplified Chinese by default or switch to English when requested.

## Included Skills

### `rednote-content-pack`

Creates the complete local content and handoff package: brief, image plan, titles, caption, topics, image order, validation, and packaged output.

### `rednote-manual-publish-guard`

Converts requests to upload, save drafts, schedule, or publish into a safe manual checklist without accessing the platform or account credentials.

## Installation

### Install as a Codex Plugin

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

Restart the ChatGPT desktop app, open Plugins, select Rednote Content Kit, and install it.

### Install a Skill manually

Copy the required Skill directory from `plugins/rednote-content-kit/skills/` into:

```text
$HOME/.agents/skills/
```

See [Installation](docs/INSTALL.en.md) for details.

## Example prompts

```text
Create a seven-card Xiaohongshu album about slowing down.
Prepare the titles, caption, topics, and manual image order in English.
```

```text
Package these images locally. Do not log in to or operate Xiaohongshu.
```

## Deterministic handoff builder

Create a UTF-8 JSON spec and run:

```bash
python3 plugins/rednote-content-kit/skills/rednote-content-pack/scripts/build_handoff.py \
  --spec /path/to/package-spec.json \
  --output /path/to/dist/package-id
```

The builder emits `handoff.md`, `manifest.json`, and an ordered `images/` directory. Omit `language` for the default `zh-CN`, or set it to `en` for English. See the [English schema](plugins/rednote-content-kit/skills/rednote-content-pack/references/package-schema.en.md).

## Privacy and security boundary

- No Xiaohongshu/RedNote login.
- No cookies, tokens, passwords, verification codes, or browser sessions.
- No upload, draft saving, scheduling, publishing, comments, or messages.
- No telemetry or runtime network requests.
- No source-machine absolute paths in the handoff.
- Rejects symlinks, path traversal, disguised images, oversized files, and non-empty output directories.
- Users remain responsible for rights to images, fonts, quotations, and other materials.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
```

## Contributing

Issues and pull requests are welcome. Use synthetic reproduction data and never attach real account data, credentials, unpublished images, private analytics, or conversations. See `CONTRIBUTING.md` and `SECURITY.md`.

## Commercial use and support

The MIT License permits commercial use. Installation, custom templates, team training, private extensions, and ongoing support may be offered as separate paid services without changing the repository license.

## Independent project notice

This is an independent community project and is not affiliated with, endorsed by, or sponsored by Xiaohongshu/RedNote. Platform names are used only to describe the intended workflow. Users are responsible for applicable law, platform rules, and content rights.

## License

[MIT License](LICENSE) © 2026 Rednote Content Kit Contributors
