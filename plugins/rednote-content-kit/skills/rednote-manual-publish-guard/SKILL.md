---
name: rednote-manual-publish-guard
description: "Convert requests to upload, save drafts, schedule, publish, comment, message, or otherwise operate Xiaohongshu/RedNote into a local manual handoff checklist. Use as a safety guard whenever platform state changes are requested; never access the platform or credentials."
---

# Rednote Manual Publish Guard

## Hard boundary

Never open or log into Xiaohongshu/RedNote, upload files, paste through a browser, save or edit drafts, create or select collections, schedule or publish, reply to comments, send messages, inspect credentials, or change account state.

Do not provide automation intended to imitate human activity, bypass detection, evade rate limits, reuse sessions, or conceal AI involvement.

## Safe conversion

When a platform action is requested:

1. State that the workflow stops at a local handoff.
2. Prepare ordered local image paths and image count.
3. Provide the recommended title, exact caption, up to ten topic candidates, comment starter, and optional collection suggestion.
4. Provide a numbered manual checklist for the user.
5. Validate only local files and wording.

Report `local-package-ready` or a concrete local blocker. Never claim platform success.
