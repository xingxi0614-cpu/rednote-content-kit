# Installation

[简体中文（默认）](INSTALL.md) | [English](INSTALL.en.md)

## Plugin installation

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

Restart the ChatGPT desktop app, open Plugins, select the repository marketplace, and install Rednote Content Kit.

## Manual skill installation

Copy the required Skill directories from `plugins/rednote-content-kit/skills/` into `$HOME/.agents/skills/`. For complete photographic output, install `rednote-image-assets` alongside the calendar or album Skill. Restart Codex if it does not detect the change automatically.

## Requirements

- Python 3.10 or newer for the handoff builder and tests.
- Automatic photographic backgrounds require a built-in imagegen/Imagen capability from the Codex/ChatGPT host. The model itself is not stored in this GitHub repository.
- Users may supply their own PNG/JPEG images when host image generation is unavailable. Without either source, the workflow emits an image plan but cannot complete photographic output.
- Final PNG export requires local Chrome/Chromium. A restricted sandbox may ask the user to approve the local browser rendering process; the plugin never adds `--no-sandbox` to bypass host security.
- No Xiaohongshu/RedNote login, browser extension, API key, or platform credential is required or supported.

## Complete-visual capability check

After installation, start a new Codex task and ask:

```text
Read rednote-image-assets, confirm whether host imagegen/Imagen is available,
and create an image plan from the template. Do not operate Xiaohongshu.
```

When the host lacks image generation, the Skill reports the missing capability explicitly. Copy and planning remain usable, but photographic completion has not succeeded.
