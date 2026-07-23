# Installation

[简体中文（默认）](INSTALL.md) | [English](INSTALL.en.md)

## Plugin installation after public release

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

Restart the ChatGPT desktop app, open Plugins, select the repository marketplace, and install Rednote Content Kit.

## Manual skill installation

Copy either skill directory from `plugins/rednote-content-kit/skills/` into `$HOME/.agents/skills/`, then restart Codex if it does not detect the change automatically.

## Requirements

- Python 3.10 or newer for the handoff builder and tests.
- An image-generation capability is optional. Users may supply their own images.
- No Xiaohongshu/RedNote login, browser extension, API key, or platform credential is required or supported.
