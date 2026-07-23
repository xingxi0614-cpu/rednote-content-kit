# Calendar JSON Schema

Use UTF-8 JSON. Required fields:

- `schema_version`: must be `1`.
- `package_type`: must be `dated-rednote-calendar`.
- `slug`: lowercase letters, digits, and hyphens.
- `date`: ISO `YYYY-MM-DD`.
- `weekday`: Chinese weekday matching the ISO date.
- `lunar`: a human-verified lunar label.
- `term`: optional. Leave empty unless the date is exactly the verified solar term or festival.
- `headline`: original editorial headline.
- `support_line`: separate supporting line or exact verified short quotation.
- `source_type`: `original` or `sourced`.
- `source_label`: use `原创` for original text; otherwise use a traceable author and work.
- `photo_prompt`: clean 4:3 photograph prompt without embedded text.
- `photo_path`: optional absolute PNG/JPEG/WebP path. When omitted, the renderer uses a neutral placeholder.
- `photo_position`: optional CSS background position, default `center`.

The renderer verifies the Gregorian date and Chinese weekday. Lunar dates and exact-day term labels still require human verification because calendar conventions and data sources can differ.
