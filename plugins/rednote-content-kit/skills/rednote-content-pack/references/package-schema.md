# 交付包数据结构

[简体中文（默认）](package-schema.md) | [English](package-schema.en.md)

创建一个 UTF-8 JSON 对象，字段如下：

- `schema_version`：整数 `1`。
- `language`：可选，`zh-CN` 或 `en`；省略时默认 `zh-CN`。
- `package_id`：仅使用小写字母、数字和连字符。
- `title_options`：1 至 5 个非空标题。
- `recommended_title`：必须与一个备选标题完全一致。
- `caption`：非空、可直接复制的正文。
- `topics`：1 至 10 个不带 `#` 前缀且不重复的话题。
- `comment_starter`：可选评论引导。
- `collection_suggestion`：可选合集建议。
- `images`：1 至 18 个对象，每项包含相对路径 `path` 和可选的 `alt`。

图片路径必须位于 spec 文件目录内部，不得使用父目录穿越，不得为软链接。支持 `.png`、`.jpg`、`.jpeg` 和 `.webp`。

构建器会把图片复制进输出包，并且只输出相对路径。`handoff.md` 默认使用简体中文；设置 `"language": "en"` 后输出英文。
