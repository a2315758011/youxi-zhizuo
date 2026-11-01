# 通用 AI 编程工程规范（精选原文）

- 上游：https://github.com/Yogndrr/engineering-standards
- 固定提交：764082534dcb035f08ca85d1f4c9fe4558843db3
- 许可证：MIT，原文见本目录 LICENSE。
- 本次精选保存 7 份核心层 SKILL.md，未导入 Angular/NestJS 等与游戏仓库当前任务无关的框架专用规范。

## 已保存技能

| 中文目录 | 上游技能 | 能力 |
|---|---|---|
| 代码变更完整性 | core/code-hygiene | 需求验收追踪、枚举穷尽、死代码、重复与调试残留 |
| 代码职责与分层 | core/code-structure | 区分流程编排与共享机制，避免逻辑散落 |
| 通用代码审查 | core/code-review | 统一入口，按严重度报告发现 |
| 历史行为回归检查 | core/historical-regression-check | 与改动前行为比较，发现重构丢失的校验与业务规则 |
| 安全重构与死代码核查 | core/refactor-checker | 沿引用追踪，评估删除/合并的证据和风险 |
| 需求到代码差距分析 | core/prd-implementation-planner | 逐条核对需求与真实实现 |
| 跨会话实施跟踪 | core/plan-tracker-flow | 长任务计划、检查点和进度追踪 |

## 采用纪律

- 只采用通用 core 层；框架专用技能不自动套用到 Godot、Unity、Unreal 或 Web 游戏。
- 与本仓库现有 AGENTS.md、小游戏开发工作室技能、ForgeSkills 和通用工程技能互补；重复规则以统一中文入口为准。
- 上游原文保留，不宣称已经在用户游戏项目验证。
- 中文执行入口：../../程序开发/AI游戏代码工程总规范/SKILL.md。
