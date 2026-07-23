# 小红书本地内容工具包

[简体中文（默认）](README.md) | [English](README.en.md)

[![CI](https://github.com/xingxi0614-cpu/rednote-content-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/xingxi0614-cpu/rednote-content-kit/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

一个面向 Codex 的开源内容工作流：在本地完成带日期的日历日签、无日期走心图集、文案整理、隐私校验和人工发布交付包。

**它帮助你把内容准备好，但不会代替你登录、上传或发布。**

## 为什么做这个项目

创作图文内容不只是写一句文案。真正容易出错的地方通常是：图片顺序混乱、标题和画面不一致、话题过多、引用来源不可靠、文件里残留个人路径，或者为了省事把账号凭证交给自动化工具。

本项目把这些步骤整理成一个可复用、可检查、纯本地的工作流。最终产物是图片文件、可复制文案、JSON 清单和人工操作步骤，账号始终由用户本人掌控。

## 效果展示

### 日期日历日签

同一套 Skill 同时支持普通日期和“日期恰好为节气当天”的日历卡。日期、星期、农历和节气标签需要在渲染前逐项核验。

<p align="center">
  <img src="docs/assets/examples/calendar-2026-07-22.png" alt="2026年7月22日日期日历日签" width="46%">
  <img src="docs/assets/examples/calendar-2026-07-23-solar-term.png" alt="2026年7月23日大暑日历日签" width="46%">
</p>

### 无日期走心图集

图集 Skill 默认生成 `1 张封面 + 6 张内页`，可使用相纸排版或全幅手写排版。下面均为本地示例。

<p align="center">
  <img src="docs/assets/examples/photo-paper-album-cover.png" alt="相纸排版图集封面" width="31%">
  <img src="docs/assets/examples/freedom-album-cover.png" alt="全幅手写图集封面" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-01.png" alt="全幅手写图集内页" width="31%">
</p>

![自由感图集总览](docs/assets/examples/freedom-album-overview.png)

图片来源、安全复核、尺寸和 SHA-256 见：[示例说明](docs/EXAMPLES.md)｜[English](docs/EXAMPLES.en.md)。

## 可以做什么

- 制定内容简报：受众、场景、目标、依据和下一步动作。
- 生成日签、单图笔记或无日期图集方案。
- 整理推荐标题、备选标题、正文、话题和评论引导。
- 校验图片格式、图片顺序、话题数量、引用和文案一致性。
- 把指定图片复制到独立交付目录，并生成相对路径和 SHA-256。
- 输出 `handoff.md` 和 `manifest.json`，方便用户人工复制与上传。
- 默认输出简体中文，明确要求时支持英文。

## 两个核心创作 Skill

### `rednote-dated-calendar`

把一个准确日期做成 3:4 相纸日历卡。流程会核对公历日期与星期，要求人工复核农历和节气，生成标题、文案、图片提示词、HTML，并可通过本机 Chrome 导出 `1242 × 1656` PNG。

### `rednote-heartfelt-album`

把一个具体情绪或生活场景做成完整七页图集：`1 张封面 + 6 张内页`、三个标题方向、正文、话题、逐页图片提示词、引用来源审计，以及可选的本地 HTML/PNG 渲染。

## 两个辅助安全 Skill

### `rednote-content-pack`

负责完整的本地内容生产与交付：内容简报、图片规划、标题正文、话题候选、图片排序、校验和交付包。

### `rednote-manual-publish-guard`

当请求涉及上传、存草稿、定时或发布时，将请求转换为安全的人工操作清单，不访问平台和账号凭证。

## 安装

### 作为 Codex Plugin 安装

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

重启 ChatGPT 桌面应用，在 Plugins 中选择“小红书本地内容工具包”并安装。

### 手动安装 Skill

将 `plugins/rednote-content-kit/skills/` 中需要的 Skill 目录复制到：

```text
$HOME/.agents/skills/
```

详细步骤见：[安装说明](docs/INSTALL.md)｜[English](docs/INSTALL.en.md)。

## 使用示例

安装后可以直接提出类似请求：

```text
帮我做一张 2026-07-23 的大暑日历日签，核对星期、农历和节气，
默认中文，生成本地图片和可复制文案，不操作小红书。
```

```text
帮我做一组“慢一点也没关系”的小红书图集，默认中文，
1 张封面加 6 张内页，整理好标题、正文、话题和人工上传顺序。
```

或者：

```text
把这些图片整理为纯本地交付包，不要登录或操作小红书。
```

## 确定性交付构建器

准备一个 UTF-8 JSON spec：

```json
{
  "schema_version": 1,
  "language": "zh-CN",
  "package_id": "quiet-weekend",
  "title_options": ["把周末还给自己", "今天不用赶路"],
  "recommended_title": "把周末还给自己",
  "caption": "给忙了一周的自己留一点空白。",
  "topics": ["周末生活", "松弛感"],
  "images": [
    {"path": "images/01-cover.png", "alt": "安静的周末封面"}
  ]
}
```

运行：

```bash
python3 plugins/rednote-content-kit/skills/rednote-content-pack/scripts/build_handoff.py \
  --spec /path/to/package-spec.json \
  --output /path/to/dist/quiet-weekend
```

输出：

```text
quiet-weekend/
  handoff.md
  manifest.json
  images/
```

省略 `language` 时默认使用 `zh-CN`；设置为 `en` 时生成英文交付文件。完整字段见：[数据结构](plugins/rednote-content-kit/skills/rednote-content-pack/references/package-schema.md)｜[English](plugins/rednote-content-kit/skills/rednote-content-pack/references/package-schema.en.md)。

## 隐私与安全边界

- 不登录小红书 / RedNote。
- 不处理 Cookie、Token、密码、验证码或浏览器会话。
- 不上传、不存草稿、不定时、不发布、不回复评论或私信。
- 不包含遥测和运行时网络请求。
- 不在交付清单中保留源电脑绝对路径。
- 拒绝软链接、目录穿越、伪装图片、超限文件和非空输出目录。
- 用户应当自行确认图片、字体、引用和其他素材的使用权。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
```

## 项目结构

```text
.agents/plugins/marketplace.json
plugins/rednote-content-kit/
  .codex-plugin/plugin.json
  skills/rednote-dated-calendar/
  skills/rednote-heartfelt-album/
  skills/rednote-content-pack/
  skills/rednote-manual-publish-guard/
docs/
examples/
tests/
tools/
```

## 参与贡献

欢迎提交 Issue 和 Pull Request。请使用合成数据复现问题，不要上传真实账号资料、凭证、未公开图片、私人分析数据或聊天记录。详见 `CONTRIBUTING.md` 和 `SECURITY.md`。

## 商业使用与支持

MIT License 允许商业使用。安装部署、定制模板、团队培训、私有扩展和持续支持可以作为独立付费服务提供，具体服务不改变本仓库的开源许可证。

## 独立项目声明

本项目是独立社区项目，与小红书 / RedNote 没有隶属、授权或赞助关系。平台名称仅用于描述适用场景。使用者应自行遵守所在地法律、平台规则和素材权利要求。

## 许可证

[MIT License](LICENSE) © 2026 Rednote Content Kit Contributors
