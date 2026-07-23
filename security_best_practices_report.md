# Security and Privacy Review

## Executive summary

No critical or high-severity issue was found in the generated public candidate. Five unit tests, both Skill validators, the Plugin validator, the generic release audit, and an owner-specific personal-information scan passed. The runtime uses the Python standard library, performs no network request, and contains no platform login or automation code.

“Absolute safety” cannot be guaranteed by pattern matching alone. Public release therefore remains blocked until patent, publisher identity, repository URL, GitHub secret scanning, and a final human review are complete. The MIT license selection is complete.

## Critical

None found.

## High

None found.

## Medium

### SEC-001 — Final public release still requires independent GitHub scanning and human review

Local pattern checks cannot recognize every possible secret or personal fact. The release procedure therefore requires a private repository first, GitHub secret scanning and push protection, private vulnerability reporting, a complete diff review, and current approval before public visibility (`docs/RELEASE.md`, lines 16-22).

Status: open release requirement; correctly blocked by `RELEASE-HOLD.md`.

### SEC-002 — Patent review is intentionally unresolved

The project now uses the MIT License and records its SPDX identifier. Public disclosure can still affect patent novelty, so the independent patent gate remains active (`RELEASE-HOLD.md`; `tools/audit_release.py`, release checks).

Status: open patent decision; intentionally blocks public release.

## Low

### SEC-003 — Repository owner and URL placeholders remain

Installation instructions retain `OWNER/REPOSITORY` until a final public-safe publisher identity is selected. The release audit rejects this placeholder in release mode.

Status: expected pre-release state.

## Verified controls

- Input paths must be relative, cannot traverse parents, must stay inside the specification root, and cannot be symlinks (`build_handoff.py`, path validation section).
- Input files must use supported image suffixes, valid image signatures, and a maximum size of 32MB.
- Output directories must be new or empty and cannot be symlinks, preventing accidental overwrite.
- Generated manifests contain copied relative image paths and SHA-256 hashes rather than source-machine paths.
- Release auditing rejects caches, key material, archives, personal home paths, common credential formats, platform creator URLs, removed upload adapters, and browser automation dependencies.
- CI has read-only repository permissions and pins third-party Actions to reviewed commit SHAs.
- No telemetry, network calls, platform credentials, login, upload, draft, scheduling, publishing, comment, or message features are included.

## Verification commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
python3 tools/audit_release.py . --release
```

The first two commands must pass. The third must continue to fail until every release blocker is deliberately resolved.
