# AI Agents for Unity：精选技能归档

来源：[ilezhnin/gamedev-ai-agents](https://github.com/ilezhnin/gamedev-ai-agents)

- 上游固定提交：`491d0c5e96306c3abc7a414b04603c441c3118fd`
- 上游技能包版本：0.4.20（README/CHANGELOG）
- 许可证：MIT；原始 LICENSE 已完整保留。
- 上游 CI：GitHub Actions run [29075510101](https://github.com/ilezhnin/gamedev-ai-agents/actions/runs/29075510101)，`validate-kit` 成功。
- 上游目录声明 28 项技能。本仓库仅精选 5 项，不复制整套安装器、角色、命令、钩子或 MCP 配置。

## 已归档技能

| 技能 | 主要用途 | 关键增量 |
|---|---|---|
| [unity-mcp](./unity-mcp/SKILL.md) | 通过 Unity MCP 读取编辑器、场景、对象、资源、测试和截图 | 先读状态与控制台，明确实例，刷新 AssetDatabase，PlayMode 与持久修改分离 |
| [unity-orient](./unity-orient/SKILL.md) | 修改前快速侦察 Unity 工程 | 识别 Unity 版本、包、asmdef、资源边界与最便宜验证路径 |
| [unity-tests](./unity-tests/SKILL.md) | Unity EditMode/PlayMode 测试策略 | 先匹配现有测试结构；回归测试先失败后通过；保护序列化字段与场景数据 |
| [unity-validate](./unity-validate/SKILL.md) | Unity 隔离候选版本验证 | 要求候选工作树、树 SHA、任务文件指纹、前后资源清单和不可覆盖的证据目录 |
| [unity-profile](./unity-profile/SKILL.md) | Unity 性能测量与优化 | 同一场景先测基线，只修最高成本项，再用相同指标复测并设置预算 |

## 参考资料依赖

- `unity-orient/references/discovery-checklist.md`
- `unity-tests/references/test-setup.md`
- `unity-validate/references/validation-commands.md`
- `unity-profile/references/performance-budgets.md`

上述 references 与入口技能一起归档，避免只复制 SKILL.md 后引用断链。

## 调度规则

1. 只有真实 Unity 工程任务才加载本组技能。Phaser、Cocos、Godot 工程不得套用 Unity API 或测试命令。
2. Unity 工程起步/陌生工程：先用 `unity-orient`；若涉及编辑器状态或场景资源操作，再用 `unity-mcp`。
3. 代码修改后的测试：按需用 `unity-tests`；交付级验证再用 `unity-validate`，不能在共享脏工作树上冒充隔离候选验证。
4. 性能问题先用 `unity-profile` 采集同场景基线；没有 Profiler/目标设备数据时不得声称已优化。
5. 不要求每个任务加载全部 5 项；按阶段最多选取必要技能，避免叠加多个编排器。

## 许可证、维护与限制

- 本地只保留 5 项精选技能及必要 references，未导入上游 UPM 安装器、权限配置、Hooks、Agent 角色、MCP server 配置和其他 23 项技能。
- 上游 README 标注 Unity 2020.3+，但这不保证每条流程适用于所有版本；实际执行前核对项目的 `ProjectVersion.txt`、Packages 与工具能力。
- `unity-validate` 的 PowerShell 参考是操作模板，包含隔离候选、证据目录和文件清单逻辑；本轮只归档，未执行，不得直接对用户工程运行。
- 上游主分支快照的 Changelog 最新列出 0.4.20（2026-07-10），仓库最近推送元数据为 2026-07-26；GitHub 页面更新时间不是代码提交时间。故将其作为有用的 Unity 工作流参考，不认定为近期持续维护或官方 Unity 技能。
- 当前评级：**B**。已审阅来源、固定提交、MIT 许可证、5 项入口及必要参考文件；上游 CI 成功。尚未在用户真实 Unity 项目执行 A/B 实测，本地 Unity MCP 也未做本轮连接验证。

