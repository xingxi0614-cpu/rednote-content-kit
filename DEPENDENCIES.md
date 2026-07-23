# Dependencies

## Runtime

- Python 3.10 or newer.
- Python standard library only for bundled scripts.

## Optional capabilities

An image-generation or image-editing capability may be used independently, but it is not bundled and may have separate privacy, license, and cost terms.

## Development and CI

GitHub Actions pins `actions/checkout` and `actions/setup-python` to reviewed commit SHAs, with their major versions documented in comments. Review and update those pins before each release. The plugin runtime itself performs no package installation and no network requests.
