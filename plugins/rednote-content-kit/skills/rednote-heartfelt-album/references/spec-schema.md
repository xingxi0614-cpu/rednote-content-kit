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

`photo_path` is optional. When absent, the renderer uses the selected palette as a placeholder visual. `photo_prompt` is always required so another image-capable agent can generate the intended photograph.

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
