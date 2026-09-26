# 外部工具扩展位

首版没有安装这些软件，没有配置 MCP、账户、定时任务或远端写入。登记在 [registry.json](registry.json)；它是规划数据，不是可执行的 MCP 配置。工具链接用于后续接入时查阅，首版未逐项验证其最新 API、价格或许可。

所有接入先明确本次业务目标、部署位置、输入/输出、账户和数据范围；检查当前官方文档后做一个小样本。凭据留在目标工具或环境的凭据管理中。通过验收后才新增实际适配器、必要的 mcp.json，并更新状态和 README。

## mermaid — 流程图与甘特图

官方仓库：[mermaid](https://github.com/mermaid-js/mermaid)

输入输出：本地源码 .mmd → SVG/PDF 或支持 Mermaid 的 Markdown。

实施约束：优先保留可编辑源码；渲染版本及字体在实施时固定。

验收：正常/异常节点一致，中文字体无缺字，导出图可读。

## markitdown — 文档输入转换

官方仓库：[markitdown](https://github.com/microsoft/markitdown)

输入输出：授权文件 → Markdown 与来源页码/工作表信息。

实施约束：保留原件；转换不是 OCR 或复杂表格完全保真的承诺。

验收：用带表格、日期、金额的样本核对原文；丢失内容进入人工复核。

## n8n — 周期汇总与提醒

官方仓库：[n8n](https://github.com/n8n-io/n8n)

输入输出：任务/证据事件 → 工作流执行记录与结果。

实施约束：凭据放工作流平台凭据库；明确时区、去重键、重试次数与失败队列。

验收：同一事件重放不重复创建任务/消息，失败可追踪且能停用。

## firecrawl — 授权网站内容采集

官方仓库：[firecrawl](https://github.com/firecrawl/firecrawl)

输入输出：URL 范围 → 页面 Markdown、来源 URL、采集时间。

实施约束：实施时确认账户、费用、页面权限与范围；不在占位配置中填写 API Key。

验收：指定页样本核对来源和正文，限速/失败清楚，预算可控制。

## plane — 项目与任务系统

官方仓库：[plane](https://github.com/makeplane/plane)

输入输出：tasks.csv → 指定工作区/项目的任务映射。

实施约束：保留 task_id 与外部 ID 的映射，先核对字段/状态和写入授权。

验收：创建/更新/重复请求分别验证；保留映射和冲突处理记录。

## 推荐实施顺序
先用真实任务验证 Skills；需要批量读文档时接 MarkItDown，需要稳定导图时接 Mermaid。采集量增长后再评估 Firecrawl；任务字段稳定后接 Plane；最后用 n8n 串接已经验证的步骤。现有可用工具能完成时无需重复部署。

## 适配器约定
未来脚本放 `scripts/integrations/<tool>/`。使用稳定业务 ID 与来源信息；记录成功/失败，不把凭据或完整客户内容写入日志。外部写入提供预览或 dry-run；重试需有上限和幂等键，失败保留人工接管信息。当前目录无需放无功能的空脚本。
