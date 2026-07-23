---
name: rednote-image-assets
description: "Generate or bind clean local image assets for RedNote dated-calendar and seven-page album specs, using a host-provided imagegen/Imagen capability when available, deterministic filenames, visual inspection, duplicate checks, and strict local-only handoff. Use when finished photographic cards, generated backgrounds, image prompts, missing photo_path fields, or placeholder replacement are requested."
---

# RedNote Image Assets

Use Simplified Chinese by default. Switch to English only when the user explicitly requests English.

## Goal

Complete the visual layer that the calendar and album Skills need. Use the host's built-in image-generation capability when it is available, bind the resulting local files to the JSON spec, and never misreport a placeholder as a finished photographic visual.

The image model itself is provided by the host application and is not stored in this repository. This Skill packages the workflow, prompts, deterministic asset contract, validation, and binding tools. It never asks for or stores an image-provider API key.

## Workflow

1. Read the dated-calendar or heartfelt-album JSON spec.
2. Create a deterministic image plan:

```bash
python3 scripts/image_assets.py plan \
  --spec /absolute/path/to/spec.json \
  --output /absolute/path/to/image-plan.json
```

3. Inspect the tools available in the current host:
   - If a built-in `imagegen` or Imagen-compatible image-generation tool is available, use it.
   - If no image-generation tool is available, use user-supplied images or stop at the image plan. Do not silently substitute gradients or claim photographic completion.
   - Do not request an API key, call an unapproved external image service, or add a runtime network dependency.
4. Generate exactly one clean landscape source image for every plan slot:
   - calendar: `calendar.png`
   - album: `00-cover.png`, then `01.png` through `06.png`
5. Keep generated images free of text, watermarks, logos, brand marks, application interfaces, and fake screenshots. Prefer a 4:3 landscape composition with enough negative space for the later crop.
6. For albums, every source image must be visually distinct. Do not reuse the same generated file with a different crop or filename.
7. Inspect every generated image. Retry once when an image contains unwanted text, a watermark, a broken subject, or a composition that cannot survive the intended crop.
8. Bind and validate the local files:

```bash
python3 scripts/image_assets.py bind \
  --spec /absolute/path/to/spec.json \
  --assets-dir /absolute/path/to/generated-images \
  --output-spec /absolute/path/to/spec.with-images.json
```

9. Render the bound spec with the originating Skill and enable strict completion:

```bash
# dated calendar
python3 ../rednote-dated-calendar/scripts/render_calendar.py \
  --spec /absolute/path/to/calendar.with-images.json \
  --output-dir /absolute/path/to/output \
  --require-complete-visuals \
  --require-png

# seven-page album
python3 ../rednote-heartfelt-album/scripts/render_album.py \
  --spec /absolute/path/to/album.with-images.json \
  --output-dir /absolute/path/to/output \
  --require-complete-visuals \
  --require-png
```

10. Inspect the final PNG files, not only the source images. Confirm crop, text legibility, page order, dimensions, and visual-copy consistency.

## Completion Rules

A finished photographic package requires all of the following:

- every required slot has a unique, validated local image
- the bound spec contains every `photo_path`
- strict rendering succeeds
- final PNG dimensions are correct
- a human-readable preview has been inspected

If any requirement fails, report the package as partial and state the exact missing capability or file.

## Boundaries

- Do not log in to, upload to, save drafts in, schedule, publish to, or otherwise operate Xiaohongshu/RedNote.
- Do not collect image-provider credentials.
- Do not hide image-generation costs, rights terms, or host limitations.
- Do not present abstract placeholders as generated photographs.
- Do not commit bound specs containing source-machine absolute paths.

## Final Response

Report the generator actually used, asset count, binding status, strict-render status, output folder, and whether any placeholder remains. State clearly that nothing was uploaded or published.
