---
name: rednote-dated-calendar
description: "Create a local-only dated Xiaohongshu/RedNote photo-paper calendar card with verified Gregorian date, weekday, lunar label, optional exact-day solar term or festival, original-first copy, image prompt, caption, topics, HTML, and optional 1242x1656 PNG rendering. Use for 日签, 日期卡, 日历卡, 每日一句, 节气卡, or dated RedNote image posts."
---

# RedNote Dated Calendar

Use Simplified Chinese by default. Switch to English only when the user explicitly requests English.

## Goal

Turn one exact date into a polished 3:4 photo-paper calendar card and a copy-ready local handoff. Default to Chinese and never operate a platform account.

## Workflow

1. Resolve the exact ISO date. If the request says today or tomorrow, state the concrete date.
2. Verify weekday, lunar label, and any solar term or festival. Show a term tag only when the chosen date is exactly that day.
3. Write a compact brief: reader, scene, one objective, grounded promise, visual mood, and intended action.
4. Produce three title directions and recommend one.
5. Write an editorial headline and a separate supporting line. Default both to original writing.
6. If using a quotation, verify exact wording, author, work, and a reliable source. Otherwise remove the attribution and write original text.
7. Create a clean 4:3 photo prompt with no text, watermark, logo, brand mark, or app interface.
8. Save a JSON spec using `assets/calendar-spec-template.json`. Read `references/spec-schema.md`.
9. Render locally when Chrome is available:

```bash
python3 scripts/render_calendar.py --spec /absolute/path/calendar.json --output-dir /absolute/path/output
```

10. Inspect the PNG at full size: 1242x1656, correct date metadata, no text overflow, clean image crop, and copy-image consistency.
11. Prepare 80-220 Chinese characters of caption, one low-pressure question, and 5-8 unique topics.

## Output Contract

Deliver the content brief, JSON spec, HTML card, optional 1242x1656 PNG, copy package, source audit when quotations are used, and a manual upload order. Never include credentials, browser profiles, account names, private analytics, or source-machine paths in a public package.

## Boundaries

- Do not log in, upload, save drafts, schedule, publish, comment, or message.
- Do not calculate lunar dates or solar terms from memory. Verify them with a reliable calendar source.
- Do not copy a distinctive creator's post or imply generated experiences or performance data are real.
- Do not promise virality, followers, sales, or platform approval.

## Final Response

Report the exact date, validation status, output folder, whether a quotation was used and verified, and whether PNG rendering succeeded. State that nothing was uploaded or published.
