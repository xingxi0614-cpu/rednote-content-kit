# Dependencies

## Runtime

- Python 3.10 or newer.
- Python standard library only for bundled scripts.
- Chrome or Chromium for deterministic final PNG rendering.

## Host-provided capabilities

Finished generated photography requires a host-provided `imagegen`/Imagen-compatible capability, or equivalent user-supplied local images. The image model is not a Python dependency and is not included in this repository. It may have separate privacy, license, quota, and cost terms.

The bundled `rednote-image-assets` Skill contains only the local workflow, prompt plan, file validation, duplicate detection, and spec binding. It performs no network request and never reads an image-provider API key.

## Development and CI

GitHub Actions pins `actions/checkout` and `actions/setup-python` to reviewed commit SHAs, with their major versions documented in comments. Review and update those pins before each release. The plugin runtime itself performs no package installation and no network requests.
