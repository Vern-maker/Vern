# Vern 专属 Codex / Plugin 工作区

首版 0.1.0：把 Vern 的 SOP、研究、项目、网站、会议、Excel 和产品开发方法整理成七个可复用 Skills。既可在本仓库中由 Codex 读取，也可通过仓库 marketplace 安装完整插件。**仓库创建不等于本机已经安装或外部工具已接通。**

## 已包含的能力

| Skill | 主要用途 |
|---|---|
| [vern-sop](plugins/vern-workspace/skills/vern-sop/SKILL.md) | SOP 与企业流程 |
| [vern-market-insight](plugins/vern-workspace/skills/vern-market-insight/SKILL.md) | 市场洞察与机会验证 |
| [vern-project-coordination](plugins/vern-workspace/skills/vern-project-coordination/SKILL.md) | 项目统筹与进度管理 |
| [vern-website-seo](plugins/vern-workspace/skills/vern-website-seo/SKILL.md) | 网站内容与 SEO |
| [vern-meeting-minutes](plugins/vern-workspace/skills/vern-meeting-minutes/SKILL.md) | 会议纪要与行动闭环 |
| [vern-excel-dashboard](plugins/vern-workspace/skills/vern-excel-dashboard/SKILL.md) | Excel 与经营看板 |
| [vern-product-development](plugins/vern-workspace/skills/vern-product-development/SKILL.md) | 产品开发与阶段门 |

每项包含触发条件、输入、执行方法、交付检查、可调整的交付结构和 UI 元数据。默认允许按任务自动匹配；只加载相关 Skill。

## 目录

```text
Vern/
├── .agents/plugins/marketplace.json
├── AGENTS.md
├── README.md
├── tests/test_workspace.py
└── plugins/vern-workspace/
    ├── plugin.json
    ├── .codex-plugin/plugin.json
    ├── README.md
    ├── skills/<skill-name>/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/deliverable.md
    ├── references/
    │   ├── working-principles.md
    │   ├── evidence-standard.md
    │   ├── task-data-contract.md
    │   ├── official-sources.md
    │   ├── acceptance-cases.md
    │   └── integrations/{README.md,registry.json}
    ├── assets/templates/{brief.md,tasks.csv,evidence.csv}
    └── scripts/{validate_workspace.py,new_case.py}
```

## 使用

### 在当前仓库使用
把仓库克隆/下载到可访问目录，在 Codex 中打开它。未安装插件时可直接要求：“读取 `plugins/vern-workspace/skills/vern-sop/SKILL.md`，按其方法整理我提供的流程。”根 AGENTS.md 包含入口约定。

### 安装完整插件
在支持 Plugin marketplace 的 Codex CLI 中添加这个仓库来源：

```shell
codex plugin marketplace add Vern-maker/Vern --ref main
codex plugin marketplace list
```

然后在应用的 Plugins Directory 中选择该来源，安装 `vern-workspace`，并开新聊天试用。若列表未更新，刷新/重启应用。当前由官方 scaffold 生成的 marketplace 标识为 `personal`、显示名为 `Personal`；用 `marketplace list` 核对其来源是本仓库，避免与其他同名来源混淆。若已有同名 marketplace，先由维护者按官方流程调整仓库 catalog 标识后再添加，不覆盖个人配置。

安装后可按界面使用 `@` 或 `$` 选择相应 Skill，例如：

```text
用 $vern-meeting-minutes 整理这份转写，区分已决定、建议和待确认。
用 $vern-project-coordination 把这些项目整理成同一份任务台账与周报。
用 $vern-excel-dashboard 基于台账制作可编辑看板，说明公式和更新方法。
```

各版本的安装界面/命令可变化，见 [官方规范与来源](plugins/vern-workspace/references/official-sources.md)。不要将七个 Skill 单独复制到全局目录后又安装本插件，避免重复入口和共享引用断开。

## 本地工具

Python 3.10+，仅标准库；从仓库根目录运行：

```shell
python plugins/vern-workspace/scripts/validate_workspace.py
python -m unittest discover -s tests
python plugins/vern-workspace/scripts/new_case.py sample-project --root cases
```

最后一条在明确的 cases 目录创建简报、任务/证据空表以及 inputs/work/outputs 子目录；存在同名目录会停止，不覆盖资料。未自动生成业务事实。

校验涵盖本仓库采用的 manifest 字段、身份一致性、七项 Skill、引用路径、UI 信息和扩展位；不是官方完整 schema 校验或业务能力认证。业务验收见 [试用用例](plugins/vern-workspace/references/acceptance-cases.md)。

## 后续接入

Mermaid、MarkItDown、n8n、Firecrawl、Plane 均已留 [规划入口](plugins/vern-workspace/references/integrations/README.md)，当前全部 `planned` / `enabled: false`。没有配置自动抓取、定时提醒、账号、收费服务或外部任务同步。

建议先用一份真实流程、一份会议记录和一份任务台账试用；修正输出规则后，再按实际需要接入工具。业务资料放私有工作区，公开仓库保留方法和脱敏模板。

## 维护

- 修改 Skill 时同步相关模板和描述，按影响范围验收，不堆积互相冲突的规则。
- 发布新版本时同步两份 plugin manifest 的版本，运行校验，重新安装/刷新后在新聊天验证；不要只改源文件便宣称已更新安装缓存。
- 公司模板、术语和品牌证据以后按需补入；未经核验的内容不得写成公司事实。
- 暂未指定开源许可证；后续公开授权复用由仓库所有者决定。
