# DeepSeek Harness 插件开发技能来源说明

- 上游：[green-dalii/dsh-plugin-dev-skill](https://github.com/green-dalii/dsh-plugin-dev-skill)
- 固定上游提交：`0d25669522eca63698f13c2ef987fedbed08f61c`（2026-11-01）
- 技能版本：0.7.0
- 上游 SDK 基线：`@deepseek-ai/* 0.2.2-alpha.2`、Cordis `4.0.6-alpha.1`
- 上游许可证：MIT，已保留 `LICENSE`。
- 已收录：完整 `SKILL.md`、`VERSION`、中文 README、CHANGELOG、11 篇 References、`scripts/verify.sh`。
- 主要能力：DeepSeek Harness（DSH）插件架构、Cordis 生命周期、工具定义、LLM 适配器、服务依赖、事件、配置、插件打包、权限门禁与 UI/协议桥扩展。
- 定位：这是 **Harness/插件工程技能**，不是直接制作游戏玩法的技能。它适用于为 DSH 做游戏开发工具插件、资源浏览器、构建/测试工具、MCP/协议桥等扩展。
- 兼容性：技能作者说明可供任何读取 Agent Skills 的 Agent 使用；本轮只做源码审阅和归档，尚未在 DeepSeek Harness 实际安装或开发插件验证。
- 版本注意：上游最新技能提交是 0.7.0，针对 DSH 0.2.2-alpha.2。官方 Releases 列表同时出现 0.2.1-rc.5（2026-10-30）与 0.2.2-alpha.2（2026-10-28），不能仅按发布日期判断兼容版本；实际项目必须读取已安装 SDK / lockfile，并对照对应官方升级指南。
- 安全注意：上游 SKILL.md 的普通拷贝更新示例包含 `rsync -a --delete`。归档不代表授权自动执行。任何更新必须先下载到独立临时目录、比较差异、备份目标文件；禁止未经核对对用户目录或工程目录运行 `--delete`。
- 评级：B（内容结构与版本信息已审阅、MIT 许可证保留；未做 DSH 环境端到端验证）。

- 原始英文上游 README 保存在 `UPSTREAM-README.md`；中文 README 已将链接改为该文件。上游 `AGENTS.md` 未作为活动指令文件导入，以免误用上游仓库规则。
