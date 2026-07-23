# Threat Model

## Protected assets

- User identity and account information.
- Passwords, cookies, tokens, and authentication state.
- Private images, analytics, drafts, comments, and conversations.
- Source-machine paths and usernames.
- Copyrighted or confidential source materials.

## Main threats and controls

| Threat | Control |
|---|---|
| Accidental credential commit | Ignore rules, release scanner, GitHub secret scanning, no credential features |
| Personal path leakage | Relative input paths, copied output assets, generic path scanner |
| Platform enforcement or account risk | No login, browser, upload, draft, scheduling, or publishing code |
| Hidden network exfiltration | Standard-library local scripts only; no network calls or telemetry |
| Untrusted file traversal | Reject absolute paths, parent traversal, and symlinks |
| Disguised or oversized image input | Verify image signatures and enforce a 32MB per-image limit |
| Accidental output overwrite | Require a new or empty non-symlink output directory |
| Copyright leakage | No bundled user assets; rights checklist and short-source discipline |
| Unsafe public disclosure | Patent/license release hold and explicit approval gate |

## Out of scope

The plugin cannot control the privacy, copyright, or platform behavior of third-party image generators, editors, browsers, or services a user chooses independently.
