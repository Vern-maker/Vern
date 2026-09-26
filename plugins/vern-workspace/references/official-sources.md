# 规范核验与来源

核验日期：2026-09-26。网页和主分支会变化，修改打包方式前应再次核验。

| 来源 | 本次采用的规则/用途 |
|---|---|
| [OpenAI Package your plugin](https://developers.openai.com/plugins/build/plugins) | 新包使用根 plugin.json 的 Agent Plugins schema；保留 Codex 兼容层；仓库 marketplace 指向 plugins 目录 |
| [OpenAI Build skills](https://developers.openai.com/plugins/build/skills) | 一项明确工作流一个 Skill；SKILL.md 的 name/description；按需引用资源 |
| [Codex / Build skills](https://learn.chatgpt.com/docs/build-skills) | 显式/隐式调用、agents/openai.yaml、本地发现与插件分发区别 |
| [openai/plugins README](https://github.com/openai/plugins/blob/main/README.md) | 官方示例仓库结构 |
| [openai/skills README](https://github.com/openai/skills/blob/main/README.md) | 已标 deprecated，并指向 openai/plugins；不是说 Skills 格式本身失效 |

本包以根 `plugin.json` 保存通用身份，`.codex-plugin/plugin.json` 保存兼容身份和界面元数据。没有内嵌 `extensions.com.openai`，因此使用兼容层提供 OpenAI 界面设置。两份身份/版本由本地校验保持一致。未接入的工具不声明为 apps/mcpServers 依赖。

## 既有工作方法的来源
业务内容根据用户当前提供的 Vern 全局工作偏好，以及本机可访问的 enterprise-sop、market-insight、company-project-dashboard、website-copywriting、meeting-minutes、excel-automation、product-development-loop 七项方法整理与扩充。未搬入私人业务文档、品牌事实或不可访问的聊天内容。

未复制 Marketing Skills 或其他第三方技能库的实现，未为本仓库擅自指定开源许可证。需要对外授权复用时，由仓库所有者选择许可证后再加入 LICENSE。
