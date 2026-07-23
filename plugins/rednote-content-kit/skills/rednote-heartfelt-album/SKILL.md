---
name: rednote-heartfelt-album
description: "Turn one emotion, audience, or everyday life scene into a complete seven-page Xiaohongshu/RedNote heartfelt carousel: one cover, six inner cards, three title directions, caption, topics, image prompts, source checks, and optional local HTML/PNG rendering. Use when the user asks for 一句话生成图集, 走心图集, 情绪图文, 治愈系图文, 小红书合集, 七页轮播, carousel copy, or a publish-ready no-date Xiaohongshu image post."
---

# RedNote Heartfelt Album

Use Simplified Chinese by default. Switch to English only when the user explicitly requests English.

## Goal

Turn one specific feeling or life scene into a coherent seven-page carousel. Produce useful finished assets, not a loose list of quotes. Keep the package no-date, original-first, visually consistent, and ready for the user to review.

## Workflow

1. Extract or infer four inputs: target reader, concrete scene, emotional tension, and desired after-feeling. Ask only when a missing answer would materially change the theme.
2. Choose one primary objective: `save`, `share`, or `comment`. Do not promise virality, followers, or sales.
3. Write a compact content brief before the cards:
   - target reader and scene
   - emotional tension
   - grounded promise
   - primary objective
   - visual atmosphere
   - one intended next action
4. Create three genuinely different cover-title directions: immediate feeling, reader voice, and gentle insight. Recommend one against the brief.
5. Build exactly seven cards: one cover plus six inner cards. Read `references/content-contract.md` for the writing and safety contract.
6. Default to original writing. If using a quotation, verify the exact wording, author, and work from a reliable source; otherwise rewrite it as original copy without attribution. Never invent a source.
7. Create one distinct 4:3 photo prompt per card. Keep text out of generated photos. Use a shared light, grain, and color family while varying the scene.
8. Write the companion post:
   - recommended title
   - 80-220 Chinese-character caption
   - one low-pressure question
   - 5-8 unique topics, never more than 10
9. Save a strict JSON spec using `assets/album-spec-template.json`. Read `references/spec-schema.md` when creating or debugging the spec.
10. When the user requests finished cards, read and follow the sibling `rednote-image-assets` Skill:
   - use the host-provided `imagegen`/Imagen capability when available
   - generate seven distinct source photographs named `00-cover.png`, then `01.png` through `06.png`
   - inspect every image and retry once when text, watermark, broken anatomy, or an unusable crop appears
   - bind the seven images to a new spec with `rednote-image-assets/scripts/image_assets.py`
   - if image generation is unavailable, accept seven user-supplied images or stop at the image plan; never call gradient placeholders a finished photographic album
11. Render the bound spec with strict completion:

```bash
python3 scripts/render_album.py \
  --spec /absolute/path/album.with-images.json \
  --output-dir /absolute/path/output \
  --require-complete-visuals \
  --require-png
```

12. If Chrome is blocked by the local sandbox, request approval to run the local rendering process. Do not add `--no-sandbox`, bypass host security, or silently replace the photographs.
13. Inspect the contact-sheet preview and all full-size cards. Check text overflow, image crop, repeated ideas, duplicate source images, source labels, and alignment between cover promise, inner cards, caption, and topics.

## Output Contract

Deliver:

- `album-brief.md`
- `album.json`
- `album-image-plan.json`
- `album.with-images.json`
- seven ordered HTML cards
- seven ordered 1242x1656 PNG cards for finished-card requests
- `album-preview.png`
- `album-copy.md` containing title options, recommended title, caption, question, topics, and the seven image prompts
- `album-source-audit.md` only when sourced quotations are used

Keep filenames portable and use a lowercase hyphenated slug. Never write account names, local credentials, cookies, browser profiles, or private analytics into the public package.

## Boundaries

- Do not log in, upload, save drafts, schedule, publish, comment, or message anyone. This skill produces local assets only.
- Do not copy a distinctive existing Xiaohongshu post or imitate a living creator's wording closely.
- Do not use medical, legal, financial, or mental-health claims as emotional reassurance.
- Do not present generated personal experiences, testimonials, or performance data as real.
- Treat platform trends as current only after live verification.

## Final Response

Show the preview when available. Report the recommended title, card count, objective, image generator actually used, unique source-image count, output folder, whether quotations were used and verified, and whether strict PNG rendering succeeded. State clearly that nothing was uploaded or published.
