# AI 编程代理通用工程技能（精选原文）

- 上游：https://github.com/khasky/awesome-agent-skills
- 固定提交：58ea4e8915de64907d04cc909a1b8c6e5cf0fcb7
- 许可证：MIT，原文见本目录 LICENSE。
- 上游定位：跨语言 AI 编程代理工程技能，覆盖代码规范、架构审计、缺陷修复、重构、代码审查、测试、安全、性能、依赖和工程决策。
- 本次精选保存 17 份独立 SKILL.md 原文；保留原始英文内容和上游署名，不把它们伪装成已验证的中文原创技能。

## 已保存技能

| 中文目录 | 上游技能 | 能力 |
|---|---|---|
| 代码工程规范 | awesome-code-standards | 命名、结构、类型、错误处理、分层 |
| 架构审计 | awesome-architecture-audit | 模块边界、依赖方向、文档与代码一致性 |
| 系统化缺陷修复 | awesome-bug-fix | 复现、定位根因、最小修复、回归 |
| AI代码清理与重构 | awesome-code-cleanup | 清理 AI 生成噪声、死代码、过度抽象 |
| 代码审查 | awesome-code-review | 差异审查、严重度排序、安全与正确性 |
| 多模型代码复核 | awesome-code-review-jury | 盲审、交叉质询、独立裁决；依赖可用的独立模型 |
| 高价值测试设计 | awesome-test-writing | 单元/集成/E2E、行为断言、属性测试 |
| 测试缺口审计 | awesome-test-gap-audit | 测试缺失、弱测试、错层测试 |
| 安全审计 | awesome-security-audit | 输入边界、权限、依赖、构建供应链 |
| 性能与可靠性审计 | awesome-performance-audit | CPU、内存、延迟、背压、资源预算 |
| 全链路回归扫描 | awesome-regression-sweep | 基线、契约、构建、部署漂移 |
| 依赖升级治理 | awesome-dependency-upgrade | 风险分批、变更日志、可回退升级 |
| 系统根因分析 | awesome-root-cause | 反复故障、流程根因、纠正措施 |
| 方案反过度设计 | awesome-plan-simplify | 删除无价值复杂度，保留必要安全 |
| 技术方案与架构决策 | awesome-design-doc | 备选方案、权衡、决策记录、预演失败 |
| 错误处理规范 | awesome-error-standards | 错误分类、传播边界、用户反馈 |
| 日志与隐私规范 | awesome-logging-standards | 结构化日志、等级、隐私脱敏 |

## 采用纪律

- 这些是通用软件工程技能，不会自动替代游戏引擎的专用 API 规范。
- 使用时先读目标项目现有约定、AGENTS.md 和架构；项目规则优先于通用示例。
- 只加载本次任务需要的技能，不一次性把 17 份全文塞进上下文。
- 原文可能包含需要在当前工具环境适配的命令或 Agent 调用方式；执行前检查工具是否存在。
- 多模型复核只有在确有独立模型/审查者时启用，单模型自我复述不能冒充独立复核。
- 原始资料等级：已导入、来源和许可已记录；尚未在具体游戏工程完成对照测试。
- 中文执行入口：../../程序开发/AI游戏代码工程总规范/SKILL.md。
