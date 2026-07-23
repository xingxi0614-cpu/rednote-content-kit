# Rednote Content Kit

> Pre-release security candidate. **Do not publish this repository until `RELEASE-HOLD.md` is cleared.** The project license has been selected, but patent, ownership, privacy, and publisher checks remain mandatory.

Rednote Content Kit is a privacy-first Codex plugin for preparing Xiaohongshu/RedNote image-and-copy packages locally. It deliberately excludes browser automation, account login, upload, draft saving, scheduling, publishing, comment replies, direct messages, and credential handling.

## Example output

The following original sample demonstrates a local `1 cover + 6 inner cards` workflow. It contains generated scenery and original editorial copy. It is included only to show the visual result; it was not uploaded to or published on any platform.

![Freedom album overview](docs/assets/examples/freedom-album-overview.png)

<p align="center">
  <img src="docs/assets/examples/freedom-album-cover.png" alt="Freedom album cover" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-01.png" alt="Freedom album first inner card" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-06.png" alt="Freedom album final inner card" width="31%">
</p>

See `docs/EXAMPLES.md` for provenance, safety review, dimensions, and checksums.

## What it includes

- `rednote-content-pack`: creates content briefs, image plans, copy, topics, and a deterministic manual handoff package.
- `rednote-manual-publish-guard`: converts requests to upload or publish into a manual checklist without accessing the platform.
- A local handoff builder that copies only explicitly listed images and emits relative paths.
- Privacy, security, contribution, commercialization, patent, release, and incident-response documentation.
- A platform-compliance checklist that keeps all account actions manual and requires current rule review.
- CI checks for tests, credentials, personal paths, prohibited platform automation, caches, and unsafe release state.

## Safety properties

- No Xiaohongshu/RedNote API, browser driver, cookie, token, password, or login support.
- No telemetry or outbound network calls.
- No bundled user images, analytics, account names, conversation history, or machine-specific paths.
- Generated handoff manifests contain relative copied paths, not the source machine's absolute paths.
- The source is prepared under the MIT License; public release remains blocked until the patent and remaining release decisions are recorded.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/rednote-content-kit/
  .codex-plugin/plugin.json
  skills/rednote-content-pack/
  skills/rednote-manual-publish-guard/
docs/
  assets/examples/
examples/
tests/
tools/
```

## Local validation

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
```

The final release gate is intentionally expected to fail while the hold is active:

```bash
python3 tools/audit_release.py . --release
```

## Installation after release approval

Once this repository is public and the release hold has been removed:

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

Then restart the ChatGPT desktop app, open Plugins, choose the Rednote Content Kit marketplace, and install the plugin. See `docs/INSTALL.md` for manual installation.

## Legal and brand notice

This is an independent community project. It is not affiliated with, endorsed by, or sponsored by Xiaohongshu/RedNote. Platform names are used only to describe compatibility. Do not add platform logos, copied interface assets, private account data, or third-party content without permission.

## License

The project is prepared under the MIT License. It permits use, modification, distribution, and commercial use when the copyright and license notices are preserved. See `LICENSE`.

Selecting MIT does not clear the public-release hold. See `PATENT-AND-LICENSING.md` before making any public disclosure. This repository is not legal advice.
