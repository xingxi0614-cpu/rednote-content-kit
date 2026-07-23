# 小红书本地内容工具包

[简体中文（默认）](README.md) | [English](README.en.md)

> 当前为发布前安全候选版。**在 `RELEASE-HOLD.md` 的全部门禁解除前，请勿将仓库改为公开。** MIT 许可证已经确定，但专利、权属、隐私和公开身份仍需最终确认。

这是一个隐私优先、纯本地运行的 Codex Plugin，用来整理小红书 / RedNote 图片与文案交付包。它不会进行浏览器自动化，不会登录账号，也不会上传、存草稿、定时、发布、回复评论、发送私信或处理平台凭证。

## 默认语言

- 默认使用简体中文生成内容、说明和人工交付清单。
- 用户明确要求英文时，切换为英文输出。
- 中文与英文使用相同的隐私边界、校验规则和纯本地工作流。

## 效果展示

下面是原创的 `1 张封面 + 6 张内页` 本地示例。画面为生成式自然场景，文字为原创编辑文案，仅用于展示生成效果；这些内容没有上传或发布到任何平台。

![自由感图集总览](docs/assets/examples/freedom-album-overview.png)

<p align="center">
  <img src="docs/assets/examples/freedom-album-cover.png" alt="自由感图集封面" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-01.png" alt="自由感图集内页一" width="31%">
  <img src="docs/assets/examples/freedom-album-slide-06.png" alt="自由感图集末页" width="31%">
</p>

图片来源、安全复核、尺寸和校验值见：[示例说明](docs/EXAMPLES.md)｜[English](docs/EXAMPLES.en.md)。

## 包含内容

- `rednote-content-pack`：生成内容简报、图片规划、标题、正文、话题和确定性的人工交付包。
- `rednote-manual-publish-guard`：把上传或发布请求转换为安全的人工操作清单，不访问平台。
- 本地交付构建器：只复制清单中明确列出的图片，输出相对路径。
- 隐私、安全、贡献、商业化、专利、许可证、发布和事件响应说明。
- 平台合规清单：所有账号操作都由用户本人手工完成。
- CI：检查测试、凭证、个人路径、平台自动化、缓存和发布门禁。

## 安全特性

- 不包含小红书 / RedNote API、浏览器驱动、Cookie、Token、密码或登录能力。
- 不包含遥测和外部网络请求。
- 不打包用户图片、账号数据、分析数据、对话历史或本机绝对路径。
- 交付清单只记录复制后的相对路径，不暴露源电脑目录。
- 代码使用 MIT License；公开发布仍受独立安全门禁约束。

## 项目结构

```text
.agents/plugins/marketplace.json
plugins/rednote-content-kit/
  .codex-plugin/plugin.json
  skills/rednote-content-pack/
  skills/rednote-manual-publish-guard/
docs/
  assets/examples/
examples/
tests/
tools/
```

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_release.py .
```

发布门禁仍生效时，下面的最终检查应当失败：

```bash
python3 tools/audit_release.py . --release
```

## 公开发布后的安装方式

仓库公开且发布门禁解除后运行：

```bash
codex plugin marketplace add xingxi0614-cpu/rednote-content-kit
```

然后重启 ChatGPT 桌面应用，在 Plugins 中选择该 Marketplace 并安装本插件。详细步骤见：[安装说明](docs/INSTALL.md)｜[English](docs/INSTALL.en.md)。

## 法律与品牌声明

这是独立的社区项目，与小红书 / RedNote 没有隶属、授权或赞助关系。平台名称仅用于描述兼容场景。未经许可，请勿加入平台 Logo、界面素材、私人账号数据或第三方内容。

## 许可证

项目采用 MIT License。保留版权和许可证声明的前提下，可以使用、修改、分发和商业使用。详见 `LICENSE`。

选择 MIT 不代表公开发布门禁已经解除。公开披露前请阅读 `PATENT-AND-LICENSING.md`。本项目文档不构成法律意见。
