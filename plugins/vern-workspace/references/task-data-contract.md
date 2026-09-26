# 统一任务字段与指标口径

跨会议纪要、项目看板、Excel 和未来 Plane/n8n 接入复用 [tasks.csv](../assets/templates/tasks.csv)。这是默认模板；已有业务字段优先，经映射后再使用。

| 字段 | 口径 |
|---|---|
| task_id | 非空、唯一、稳定；同步后不得因排序改变 |
| project_id | 所属项目 ID；未知留空，不编造项目 |
| title | 动词加可验收成果 |
| owner | 一个主责；原材料未指定时留空，在 notes 标待确认 |
| department | 部门；不从姓名猜测 |
| status | not_started / in_progress / blocked / done / cancelled；未知留空并列为数据缺口 |
| priority | high / medium / low；未确定留空 |
| start_date / due_date / completed_date | ISO 日期 YYYY-MM-DD；未知为空，completed_date 仅用已确认完成日 |
| progress_pct | 0–100，只记录有依据的进度；未知为空，不按状态自动填 50 等数字 |
| depends_on | 前置 task_id，多个用分号分隔；检查缺失引用与循环 |
| next_action | 下一步动作，不重复状态 |
| blocker | 阻塞原因、解除条件及需谁处理 |
| acceptance | 完成的验收标准/证据 |
| source_ref | 原文件段落、会议时间戳或系统记录 |
| updated_at | 带时区的 ISO 时间；未知为空 |
| notes | 假设、建议、变更和待确认 |

## 默认指标
- 有效任务：task_id 非空、唯一且 status 不为 cancelled。未知状态仍在分母中，并另外列示数据缺口。
- 按任务数完成率：done 数 / 有效任务数；分母为 0 时显示空白或“不适用”。不能称为工时完成率或产值完成率。
- 逾期：有有效 due_date，due_date 早于明确基准日，且 status 不是 done/cancelled；当天到期不算逾期。缺日期任务单列。
- 临期：基准日至基准日加 N 天（含边界），未完成且未取消；N 是可调整参数，须展示。
- 项目进度如需权重，先确认权重依据；不得对主观 progress_pct 简单平均后冒充已验证项目完成率。

报表展示基准日期与时区。状态为 done 的任务缺验收依据时列为异常，不静默改写历史。
