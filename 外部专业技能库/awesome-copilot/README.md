# GitHub Awesome Copilot：AI 工程辅助技能精选

- 上游：https://github.com/github/awesome-copilot
- 固定提交：5269f7ea2d6c3a9bfda5ed878b6726cf509121fd
- 许可证：MIT，原文见本目录 LICENSE。
- 上游规模：数百份 Agent Skills、指令和 Agent 配置；本次只选 3 项与游戏代码工程直接相关的内容，不复制整个庞大集合。

## 已保存技能

| 中文目录 | 上游技能 | 能力 |
|---|---|---|
| 代码库认知与架构地图 | acquire-codebase-knowledge | 建立现有代码库地图、模块说明与上手资料 |
| AI代码输出评估 | agentic-eval | 为 AI 生成代码/代理结果建立评估维度和迭代评估 |
| AI工具与依赖供应链审计 | agent-supply-chain | 核验 Agent 插件、工具包、依赖完整性与来源 |

## 不导入的项目

- 仓库专用的 code-review skill 只服务于 awesome-copilot 自身 PR，不作为通用游戏代码审查规范。
- API Breaking Change Detector 主要面向 C# Web API 与 TypeScript/JavaScript 客户端，不适用于多数单机游戏。
- Agent OWASP Compliance 与 Agent Governance 面向 AI Agent 产品自身的治理与安全，不应误套到普通离线游戏。
- Architecture Blueprint Generator 可生成架构图，但有自动识别和模板化输出局限；本仓库优先采用证据驱动的架构审计，不将生成图当成事实。

## 采用纪律

- 代码库认知用于新接手项目或用户要求全库梳理，不在每次小修复时重复扫描。
- AI 输出评估用来评估技能/流程是否真的改善代码质量；必须采用同一任务、同一基线和可观察结果。
- 供应链审计只在引入第三方插件、Agent 工具、原生库或外部技能时触发。
- 资料已导入，尚未在用户具体游戏工程验证。中文入口：../../程序开发/AI游戏代码工程总规范/SKILL.md。
