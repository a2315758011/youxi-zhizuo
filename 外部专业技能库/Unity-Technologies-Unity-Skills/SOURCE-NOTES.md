# Unity 官方 AI 技能来源说明

- 上游：[Unity-Technologies/skills](https://github.com/Unity-Technologies/skills)
- 固定上游 Git tree：`089bedebab64e9e75943b19a364c7aec2162a7e7`（main，2026-11-02 检索）
- 上游最近更新：2026-11-01；官方仓库约 35 项 Unity 工作流技能。
- 上游许可证：Unity Companion License，完整 `LICENSE.md` 已保留。
- 本次精选导入 2 项完整技能及引用/示例：
  1. `unity-cli/`：通过 Unity CLI 发现命令、驱动已连接 Editor、执行 C#、构建、测试、读取日志，并用运行时证据确认游戏确实推进。
  2. `sprite-editor/`：通过 Unity Sprite Editor 数据提供器修改 Sprite rect、pivot、border、outline 与切片；附带完整参考与 C# 示例。
- 选择理由：Sprite 元数据保存在 Unity importer 中，不应手工编辑 .meta；需要在真实 Editor 中验证切片和 pivot。该流程与恢复 PVZ 原始 Sprite 层级/帧资源的工作直接相关。
- 重要限制：`sprite-editor` 依赖 `unity-cli`、已连接的 Unity Editor，以及实际存在的 `script eval` Pipeline 命令。若 Editor 或命令不可用，必须停止相关修改，不得改为手工篡改 .meta。
- 版本注意：Unity CLI 文档标记其为 experimental（实验性），命令和文档可能变化；每次使用先读取本地 Unity 版本、CLI 版本、Pipeline 包版本及命令目录。
- 许可证限制：Unity Companion License 仅允许在有效 Unity Engine License 关联的 Unity 内容创作/发行场景中使用。此目录仅供 Unity 工程；不得将 Unity 技能内容拆出后当作通用 MIT/Apache 技能重新分发。
- 未做事项：本轮仅归档，不在工作站安装 Unity CLI、不修改 Unity 项目、不执行 Sprite Importer 写入。
- 评级：B（Unity 第一方来源、许可证与依赖已核对；未在用户工程中实测）。
