# Package Schema

Create a UTF-8 JSON object with:

- `schema_version`: integer `1`.
- `package_id`: lowercase letters, digits, and hyphens.
- `title_options`: one to five non-empty strings.
- `recommended_title`: must exactly match one title option.
- `caption`: non-empty copy-ready text.
- `topics`: one to ten unique topic strings without a leading `#`.
- `comment_starter`: optional string.
- `collection_suggestion`: optional string.
- `images`: one to eighteen objects containing relative `path` and optional `alt`.

Image paths must remain inside the spec directory, must not use parent traversal, and must not be symlinks. Supported suffixes are `.png`, `.jpg`, `.jpeg`, and `.webp`.

The builder copies images into the output package and emits relative paths only.
