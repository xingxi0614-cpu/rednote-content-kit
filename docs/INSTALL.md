# 安装说明

[简体中文（默认）](INSTALL.md) | [English](INSTALL.en.md)

## Plugin 安装

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

重启 ChatGPT 桌面应用，打开 Plugins，选择该仓库的 Marketplace，然后安装“小红书本地内容工具包”。

## 手动安装 Skill

从 `plugins/rednote-content-kit/skills/` 复制需要的 Skill 目录到 `$HOME/.agents/skills/`。如需完整摄影成品，除日签或图集 Skill 外，还要同时复制 `rednote-image-assets`。如果 Codex 没有自动识别，重启 Codex。

## 环境要求

- 交付构建器和测试需要 Python 3.10 或更高版本。
- 如果要自动获得摄影背景，宿主 Codex/ChatGPT 必须提供内置的 imagegen/Imagen 能力；模型本身不包含在 GitHub 仓库里。
- 没有宿主图片生成能力时，可以提供自己的 PNG/JPEG 图片；两者都没有时只能生成图片计划，不能完成摄影成品。
- 导出最终 PNG 需要本机 Chrome/Chromium。受限沙箱可能要求用户批准启动本地浏览器渲染进程；插件不会使用 `--no-sandbox` 绕过安全限制。
- 不需要、也不支持小红书 / RedNote 登录、浏览器扩展、API Key 或平台凭证。

## 完整视觉能力自检

安装后在新 Codex 任务中要求：

```text
读取 rednote-image-assets，确认当前是否有宿主 imagegen/Imagen，
为模板生成图片计划；不要登录或操作小红书。
```

如果宿主没有图片生成工具，Skill 会明确返回缺失能力。不要把这种结果描述为插件安装失败：文案和图片计划仍可用，但摄影视觉尚未完成。
