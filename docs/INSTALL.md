# 安装说明

[简体中文（默认）](INSTALL.md) | [English](INSTALL.en.md)

## 公开发布后的 Plugin 安装

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

重启 ChatGPT 桌面应用，打开 Plugins，选择该仓库的 Marketplace，然后安装“小红书本地内容工具包”。

## 手动安装 Skill

从 `plugins/rednote-content-kit/skills/` 复制任意一个 Skill 目录到 `$HOME/.agents/skills/`。如果 Codex 没有自动识别，重启 Codex。

## 环境要求

- 交付构建器和测试需要 Python 3.10 或更高版本。
- 图片生成能力是可选项，用户也可以提供自己的图片。
- 不需要、也不支持小红书 / RedNote 登录、浏览器扩展、API Key 或平台凭证。
