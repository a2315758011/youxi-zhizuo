# Phaser 3.90 专项运行时资产集成

- 类型：本仓库自编写的版本适配技能，不是第三方原文镜像。
- 引擎：Phaser 3.90.0。
- 官方依据：Phaser 3.90 API 文档、AnimationState、ParticleEmitter、Container。
- 适用：分层角色、帧动画、动画状态映射、事件、粒子、锚点、碰撞代理和 UI 接入。
- 与 Phaser4 官方技能完全隔离；不要把 Phaser4 API 复制到 Phaser3.90 工程。
- 当前 PVZ 项目依赖声明为 phaser ^3.90.0；执行前仍须从 lockfile 核对实际解析版本。
- 评级：B。技能正文已按官方 API 审阅；尚未在 PVZ 工程完成独立 A/B 对照与运行验收。

## 官方文档
- https://docs.phaser.io/api-documentation/3.90.0/api-documentation
- https://docs.phaser.io/api-documentation/3.90.0/class/animations-animationstate
- https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-particles-particleemitter
- https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-container