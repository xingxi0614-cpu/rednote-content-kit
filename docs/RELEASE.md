# Public Release Procedure

This file records the release controls for `xingxi0614-cpu/rednote-content-kit`. It contains no credentials or private identity data.

## Recorded decisions

- License: MIT.
- Patent: on 2026-07-22, the owner decided not to seek patent protection for the currently published project content and accepted the effect of public disclosure.
- Rights: the owner confirmed the right to publish the tracked code, documentation, original copy, and four example images.
- Publisher and destination: `xingxi0614-cpu/rednote-content-kit` approved for public visibility.
- Commit identity: GitHub-provided `noreply` email.

## Pre-visibility checks

- [x] MIT text and SPDX metadata agree.
- [x] Personal paths, names, common secret patterns, private keys, symlinks, caches, archives, and platform automation are absent from the release tree.
- [x] Four example images have reviewed dimensions, provenance notes, and SHA-256 values.
- [x] Full Git history uses the approved GitHub `noreply` identity and passes the history pattern scan.
- [x] Unit tests and `python3 tools/audit_release.py . --release` pass.
- [x] The public README is complete in Chinese and English.
- [x] The owner explicitly approved public visibility.

## Post-visibility checks

- [ ] Confirm anonymous repository, README, image, clone, and ZIP access.
- [ ] Enable GitHub secret scanning and push protection when available.
- [ ] Enable private vulnerability reporting when available.
- [ ] Confirm Dependabot vulnerability alerts and automated security fixes.
- [ ] Confirm GitHub Actions succeeds on the public release commit.
- [ ] Create and verify the `v0.1.0` tag from the approved commit.

Never bypass a GitHub security alert to finish a release. If a secret is ever exposed, revoke or rotate it first, then remediate the Git history and verify the result.
