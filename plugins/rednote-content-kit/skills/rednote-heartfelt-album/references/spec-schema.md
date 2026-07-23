# Album JSON Schema

Use UTF-8 JSON. Required top-level fields:

```json
{
  "schema_version": 1,
  "package_type": "heartfelt-xhs-album",
  "slug": "lowercase-hyphenated-slug",
  "series": "一句话走心图集",
  "theme": "theme shown in preview",
  "volume": "VOL. 01",
  "palette": "clay",
  "cover": {},
  "slides": []
}
```

`palette` may be `clay`, `forest`, `night`, or `ocean`.

The cover requires:

```json
{
  "headline": "one or two short lines",
  "subtitle": "one restrained supporting sentence",
  "photo_path": "/absolute/path/to/photo.png",
  "photo_prompt": "4:3 clean photograph prompt"
}
```

`photo_path` is optional only for copy-only drafts and explicit wireframes. A finished album must contain seven unique paths and render with `--require-complete-visuals`. `photo_prompt` is always required so the sibling `rednote-image-assets` Skill can use the host image-generation capability or bind user-supplied photographs.

`slides` must contain exactly six objects:

```json
{
  "headline": "original editorial headline",
  "support_line": "separate resonance, explanation, or action",
  "source_type": "original",
  "source_label": "原创",
  "photo_path": "/absolute/path/to/photo.png",
  "photo_prompt": "4:3 clean photograph prompt"
}
```

For a verified quotation, set `source_type` to `sourced`, put the exact short quotation in `support_line`, and use a traceable `source_label` such as `张三《书名》`. Create a separate source-audit file containing the verification evidence.

All paths must be absolute. Supported photo formats are PNG, JPEG, and WebP.

The image-assets binder expects deterministic generated filenames: `00-cover.png`, then `01.png` through `06.png`. It checks image dimensions and exact duplicate content before writing a bound spec. `--require-png` makes the renderer fail when the final PNG set and contact sheet cannot be created.
