# Security Policy

## Supported versions

Only the latest tagged release is supported after public release. The current `0.1.0` candidate is not publicly released.

## Reporting a vulnerability

Do not open a public issue for suspected credential exposure, personal-data leakage, unsafe file handling, or platform automation. After a public GitHub repository exists, use GitHub's private vulnerability reporting feature.

Until then, keep the report private and include only the minimum reproduction details. Never attach real credentials, cookies, tokens, account exports, private analytics, or user images.

## Security boundaries

- No platform login, upload, draft, schedule, publish, comment, or message automation.
- No network requests in bundled runtime scripts.
- No execution of untrusted shell commands.
- No following image symlinks outside the declared package root.
- No absolute source paths in generated manifests.
- No secrets in configuration files or examples.
