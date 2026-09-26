# 首版验证记录

验证日期：2026-09-26。版本：0.1.0。

## 已完成

- 使用当前 Codex 内置 Plugin Creator 的 `validate_plugin.py`：兼容 manifest 通过。
- 使用当前 Codex 内置 Skill Creator 的 `quick_validate.py`：七个 `SKILL.md` 全部通过。
- 仓库自带 `validate_workspace.py`：通用/兼容 manifest 身份一致、marketplace 路径、七项 Skill、UI 字段、本地文档引用、空白 CSV 模板和五个禁用扩展位通过。
- `python -m unittest discover -s tests -v`：4 项测试通过。覆盖完整工作区、空模板创建/已有资料不覆盖、路径越界/Windows 设备名拒绝、版本漂移/引用断裂检测。

验证环境：Windows，Python 3.12；官方校验所需 PyYAML 6.0.3 临时安装于构建工作目录，没有加入插件依赖。插件自带脚本只用标准库。

## 验证边界

- 通用 `plugin.json` 依据当日官方文档最小格式构建并做本地结构检查；内置官方脚本针对 `.codex-plugin/plugin.json`，不是 Agent Plugins 全量 JSON Schema 校验器。
- 未在应用中安装本插件，未验证新聊天中的自动触发和业务输出效果。当前环境的 CLI marketplace 列表检查因无法解析应用 home 目录而未完成，不据此判断用户主应用的安装状态。
- Mermaid、MarkItDown、n8n、Firecrawl、Plane 未连接，也未运行外部同步、抓取、提醒或计费任务。
- 业务试用场景及观察点见 [验收用例](plugins/vern-workspace/references/acceptance-cases.md)。

结构校验通过证明文件可解析、引用可达和受测脚本行为符合约定；实际方法仍需用真实或脱敏材料试用迭代。
