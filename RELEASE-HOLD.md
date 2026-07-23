# Release Hold

Public release is blocked.

Do not create a public repository, push this directory to a public remote, publish a release, upload a ZIP, or share a public download link until every item below is complete:

- [ ] A qualified patent professional confirms whether any patent filing should occur before disclosure.
- [x] The copyright holder selected the MIT License and installed its complete text in `LICENSE`.
- [x] `MIT` is recorded in `plugin.json` as the SPDX license identifier.
- [ ] Ownership and permissions are confirmed for all code, text, CSS, examples, images, fonts, and other assets.
- [ ] No confidential account data, user content, analytics, personal names, credentials, or machine-specific paths are present.
- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 tools/audit_release.py . --release` passes.
- [ ] The complete public diff and repository visibility are shown to the owner for current approval.

Removing this file is not sufficient by itself. All checks must be documented in `docs/RELEASE.md`.
