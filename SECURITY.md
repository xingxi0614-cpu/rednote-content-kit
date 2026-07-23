# Security Policy

## Supported versions

The latest tagged release and the current `main` branch receive security fixes. Before `1.0.0`, interfaces may change between minor releases.

## Reporting a vulnerability

Do not open a public issue for suspected credential exposure, personal-data leakage, unsafe file handling, or platform automation. Use GitHub Security Advisories / private vulnerability reporting when available and include only the minimum synthetic reproduction details. Never attach real credentials, cookies, tokens, account exports, private analytics, or user images.

## Security boundaries

- No platform login, upload, draft, schedule, publish, comment, or message automation.
- No network requests in bundled runtime scripts.
- No execution of untrusted shell commands.
- No following image symlinks outside the declared package root.
- No absolute source paths in generated manifests.
- No secrets in configuration files or examples.
