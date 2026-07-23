# Security and Privacy Review

## Executive summary

No critical or high-severity issue was found in the public release tree. Eleven unit tests, the generic and final release audits, JSON/frontmatter checks, documentation-link checks, current-tree scans, and full-history pattern scans passed before the visibility change.

The runtime uses the Python standard library, makes no network request, and has no platform login, upload, draft, scheduling, publishing, comment, message, or credential feature.

## Critical

None found.

## High

None found.

## Medium

None open.

## Resolved release decisions

### SEC-002 — Patent disclosure decision

The owner explicitly decided not to seek patent protection for the currently published content and accepted the effect of public disclosure.

Status: resolved on 2026-07-22.

### SEC-003 — Publisher, repository, and asset rights

The owner approved `xingxi0614-cpu/rednote-content-kit` for public visibility and confirmed the right to publish the code, documentation, original copy, and four reviewed example images. Commit metadata uses the GitHub-provided `noreply` identity.

Status: resolved on 2026-07-22.

### SEC-004 — GitHub public security controls

Anonymous repository, README, example-image, Git clone, and source-ZIP access were verified after the visibility change. GitHub secret scanning, push protection, private vulnerability reporting, Dependabot vulnerability alerts, and automated security fixes are enabled.

Status: resolved on 2026-07-22.

## Verified controls

- Input paths must be relative, cannot traverse parents, must stay inside the specification root, and cannot be symlinks.
- Input files must use supported image suffixes, valid image signatures, and a maximum size of 32MB.
- Output directories must be new or empty and cannot be symlinks, preventing accidental overwrite.
- Generated manifests contain copied relative image paths and SHA-256 hashes rather than source-machine paths.
- Chinese is the default handoff language; English is an explicit supported option, and unsupported language values are rejected.
- Release auditing rejects caches, key material, archives, personal home paths, common credential formats, platform creator URLs, removed upload adapters, and browser automation dependencies.
- Reviewed example PNGs use fixed names and dimensions and are checked for sensitive metadata markers.
- CI has read-only repository permissions and pins third-party Actions to reviewed commit SHAs.
- No telemetry, runtime network request, platform credential, login, upload, draft, scheduling, publishing, comment, or message feature is included.

## Verification commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
python3 tools/audit_release.py . --release
```

All three commands must pass for a public release.
