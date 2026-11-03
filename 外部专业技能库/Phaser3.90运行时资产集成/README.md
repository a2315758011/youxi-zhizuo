# Phaser 3.90 专项运行时资产集成

- 类型：本仓库自编写的版本适配技能，不是第三方原文镜像。
- 引擎：Phaser 3.90.0。
- 官方依据：Phaser 3.90 API 文档、AnimationState、ParticleEmitter、Container。
- 适用：分层角色、帧动画、动画状态映射、事件、粒子、锚点、碰撞代理和 UI 接入。
- 与 Phaser4 官方技能完全隔离；不要把 Phaser4 API 复制到 Phaser3.90 工程。
- 当前 PVZ 项目依赖声明为 phaser ^3.90.0；执行前仍须从 lockfile 核对实际解析版本。
- 2026-11-03：在真实 PVZ Phaser 3.90.0 工程达到 E3 定向集成验证；npm test 14/14、生产构建、Edge 桌面/触摸模拟 E2E、PWA 离线 250/250 通过。发现并修复三种特殊僵尸 hurt → 原始 walk clip 的清单映射误报，未修改玩法运行时代码。
- 评级暂保持 B：E3 证明技能适用于该工程，但严格 A/B 对照（同一基线、A/B 各三轮）尚未执行；Android 真机也未验证。

## 官方文档
- https://docs.phaser.io/api-documentation/3.90.0/api-documentation
- https://docs.phaser.io/api-documentation/3.90.0/class/animations-animationstate
- https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-particles-particleemitter
- https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-container
## 2026-11-03 ParticleEmitter API 冒烟补充

- 真实 Phaser 3.90.0 GameScene 临时使用现有 `projectile.pea` 纹理创建 ParticleEmitter。
- 12 粒子一次性爆发，260ms 生命周期；实测 12 → 0 存活、12 死亡，显式 destroy 后 emitter 从 Scene display list 移除，浏览器错误 0。
- 这是 E3 级 ParticleEmitter API/生命周期 smoke test，不是生产 VFX 接入；没有新增正式粒子资产，也没有把粒子连接到伤害/碰撞逻辑。
- 完整证据在本地工程 `evidence/PARTICLE-EMITTER-RUNTIME-SMOKE-20261103.md`。