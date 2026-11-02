# Game Dev Skills 来源说明

- 上游：[ThiagoFdaSLopes/game-dev-skills](https://github.com/ThiagoFdaSLopes/game-dev-skills)
- 固定上游提交：`0b57f930cee5fcb5fb4b3f90cf6e41b180e43445`
- 最近推送：2026-10-19
- 许可证：MIT，完整原文保存在本目录 `LICENSE`。
- 本次精选导入：`game-test` 与 `game-implement` 两项技能及其完整 references；另保存项目配置模板。
- 核心特点：跨引擎（Godot/Unity/Unreal/自定义引擎）、按项目现状选最便宜有效的测试、垂直切片 test-first（先测试后实现）、真实首次使用路径、性能前后同条件测量、明确区分 verified/inferred/assumed。
- 适用边界：来源针对 Claude Code 测试；README 称 Codex 支持已内置但确认仍待完成。其他 Agent 只声明兼容 Agent Skills 格式，需逐一实测。不能把作者声明的兼容性当作已验证。
- 去重：本仓库已有通用测试、代码工程和游戏玩法技能；本次仅选择其“首次使用检查 + 证据分级”测试流程和“垂直切片、按项目既有检查执行、禁止无谓重构”的实现流程，不导入重复的计划、调试、优化、审查技能。
- 等级：B（源代码与许可证审阅、导入和仓库 CI 通过；尚未在用户具体游戏项目中进行技能 A/B 对照）。
- 使用提示：项目 profile 模板是可选配置示例，不得直接覆盖用户 AGENTS.md 或项目规则。项目现有协议优先。
