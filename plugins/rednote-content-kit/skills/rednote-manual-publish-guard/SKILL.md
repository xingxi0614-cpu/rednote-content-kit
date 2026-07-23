---
name: rednote-manual-publish-guard
description: "默认用中文把小红书/RedNote 的上传、草稿、定时、发布、评论或私信请求转换为本地人工交付清单，同时支持英文；绝不访问平台或凭证。Use as a safety guard for platform state-change requests."
---

# Rednote Manual Publish Guard

## Language / 语言

Use Simplified Chinese by default for the refusal, handoff checklist, copy blocks, and status report. Switch to English only when the user explicitly requests English. Apply the same hard boundary in both languages.

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
