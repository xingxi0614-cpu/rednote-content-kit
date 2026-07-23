---
name: rednote-content-pack
description: "Create privacy-safe, local-only Xiaohongshu/RedNote image-and-copy handoff packages. Use for content briefs, dated cards, no-date albums, titles, captions, topic candidates, comment starters, image ordering, local validation, and manual upload checklists. Never access or operate the platform."
---

# Rednote Content Pack

## Boundary

Work locally only. Never open or log into the platform, upload files, paste through a browser, save or edit drafts, create or select collections, schedule or publish posts, reply to comments, send messages, inspect credentials, or change account state.

Do not include private account names, analytics, conversations, personal identifiers, passwords, cookies, tokens, absolute home paths, or content without redistribution rights in reusable outputs.

## Workflow

1. Identify the content mode, target audience, concrete scene, primary objective, and evidence supplied by the user.
2. Choose either one dated card or one no-date album. Default albums to one cover plus five or six inner cards.
3. Create fresh images with an available image-generation capability or use images explicitly supplied by the user. Require no embedded text, watermark, logo, or sensitive interface by default.
4. Write three title candidates, one recommended title, a concise caption, five to ten relevant topic candidates, and one comment starter.
5. Verify that quotes, claims, dates, and sources are accurate. Avoid long copyrighted passages and never invent attribution.
6. Store selected images under one local project root. Create a JSON spec based on `references/package-schema.md` using relative image paths only.
7. Run `scripts/build_handoff.py` from this skill directory or by its resolved absolute location:

   ```bash
   python3 scripts/build_handoff.py --spec /path/to/package-spec.json --output /path/to/dist/package-id
   ```

8. Inspect `handoff.md` and `manifest.json`. Confirm that only intended images were copied and that no source-machine absolute path appears.
9. Give the user the ordered local files and copy blocks. State that the user performs all platform actions manually.

Read `references/content-contract.md` for copy and visual rules, `references/package-schema.md` when creating a spec, and `references/privacy-safety.md` before packaging or sharing.

## Output

Report `local-package-ready` only after local validation succeeds. Never report uploaded, saved, scheduled, published, or platform-verified status.
