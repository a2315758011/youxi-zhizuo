---
name: phaser-3.90-runtime-asset-integration
description: Phaser 3.90.0 专项运行时资产集成技能。用于把分层角色、序列帧、动画状态、事件、粒子特效、UI 和运行时碰撞代理可靠接入既有 Phaser 3.90 游戏。
license: MIT
compatibility: Phaser 3.90.0；TypeScript/JavaScript；以目标项目 package.json 与 lockfile 的实际解析版本为准。
metadata:
  author: a2315758011
  version: "1.0.0"
  engine: "Phaser 3.90.0"
  source: "Phaser 3.90.0 official API documentation"
---

# Phaser 3.90 运行时资产集成

## 适用范围与版本门禁

- 仅用于实际安装 Phaser 3.90.0 的工程。先检查 package.json、package-lock.json/pnpm-lock/yarn.lock 与 node_modules 实际版本。
- 不使用 Phaser 4 的 filters、renderer pipeline、API 重命名或新版本示例。Phaser 3.90 官方 API 文档：https://docs.phaser.io/api-documentation/3.90.0/api-documentation
- 不因新技能或上游教程升级项目；Phaser 3→4 迁移必须单独获得用户授权并建立迁移回归计划。
- 若项目不是 3.90.0，停止套用本技能，重新路由到准确版本。

## 目标生产链

原始资产 → 结构化部件/帧 → 资产清单 → 锚点与坐标 → 逻辑状态映射 → Phaser 运行时对象 → 动画事件与 VFX → 碰撞代理 → 真实场景测试。

任何阶段失败都应定位到具体资产、帧、状态或对象，不以静态预览替代引擎运行。

## 资产合同

每个动态角色或对象至少记录：
- 稳定 assetId、源文件路径、来源/许可、SHA-256、目标分辨率和缩放基准。
- 表现方式：原生序列帧、独立分层部件、Spine/DragonBones（如实际集成），或静态图；不得把单张 PNG 伪装成完整动画。
- 部件 ID、父子关系、局部位置、旋转、缩放、绘制顺序、Pivot/锚点、透明边界。
- 动画 clip、帧序、帧时长、循环标记、事件时间、完成后的目标状态。
- 物理/命中代理的尺寸、偏移、碰撞层；视觉轮廓与物理体分离管理。
- 替换资产时保持稳定 ID 和接口，不让玩法代码直接依赖临时文件名。

## Phaser 3.90 运行时规则

1. **动画由玩法状态驱动。** 逻辑层决定 idle/attack/hurt/death 等状态；渲染层只映射到已登记 animation key/clip，不得自行创造玩法转换。
2. **使用 Phaser 3.90 原生 AnimationState。** 通过 Sprite 的 anims 播放、排队和监听完成事件；对非循环动画明确处理 ANIMATION_COMPLETE，回到声明的 onComplete 状态或销毁。
3. **分层角色按需组织。** 可用 Container 处理纯视觉父子变换，但必须实测嵌套深度、排序和输入成本。不要把 Container 子对象的 Arcade Physics body 当成完整父变换后的世界碰撞体；将权威碰撞代理放在独立对象/场景层。
4. **事件驱动特效。** 伤害、命中、死亡、技能释放等权威游戏事件触发粒子；VFX 不计算伤害、不决定命中、不改变游戏状态。
5. **粒子生命周期受控。** 为高频命中、投射物、爆炸和浮字设置合理上限/复用策略；场景 shutdown/destroy 时停止 emitter、移除监听并回收对象。
6. **资源键统一管理。** 由 manifest 提供纹理、图集和动画 key；禁止在玩法逻辑中散落路径字符串。加载失败要给出具体 assetId 和路径。
7. **锚点与地面接触一致。** 角色底部脚点、投射物发射点、命中特效中心和阴影分别定义；禁止用视觉图像边界代替脚底碰撞点。
8. **UI 与游戏层分责。** HUD 的数值来自权威状态；文本、按钮、触控区域和安全区单独验收，UI 不反向篡改战斗规则。

## 状态机与事件合同

每个动态实体需要可检查的状态映射表：
| 字段 | 要求 |
|---|---|
| logicStates | 逻辑允许的状态集合 |
| transitions | 触发条件及来源状态 |
| animationKeys | 对应 Phaser 3.90 动画键 |
| onComplete | 非循环动画结束后的明确状态 |
| events | 命中、发射、释放、落地等事件及唯一触发时刻 |
| cleanup | 场景退出、对象销毁时的监听与资源清理 |

同一动作事件必须幂等：一次攻击/投掷不得因多次 update、动画重复回调或场景恢复而重复造成伤害/生成对象。

## 验收门禁

- 静态：manifest 引用、帧数/帧序、透明通道、锚点、父子节点、状态转换无缺项。
- 自动化：动画状态进入/退出、完成回调、重复事件防重、对象销毁后无残留监听。
- 引擎集成：在 Phaser 3.90.0 真实浏览器运行，验证动画实际播放、帧序、层级、碰撞代理和 VFX 触发。
- 回归：开始/暂停/恢复/重开/场景切换后不重复监听、不残留 emitter、不出现第二个 Game 实例。
- 移动端：代表性低/中端视口检查触控命中、帧时间、纹理内存和缩放。
- 证据绑定代码提交、资产版本、构建编号、浏览器版本和测试命令。

## 禁止做法

- 将 Phaser 4 技能示例直接复制到 Phaser 3.90。
- 用整图平移/缩放/闪烁冒充骨骼或逐帧动画。
- 把 VFX 回调作为伤害或碰撞的权威来源。
- 在 update 每帧创建新 emitter、timer、collider 或匿名全局监听。
- 仅凭 TypeScript 编译或静态测试声称角色已在场景内正确播放。
- 为使用技能而重写现有 renderer、动画系统或资源目录。

## 官方 API 参考

- Phaser 3.90 API：https://docs.phaser.io/api-documentation/3.90.0/api-documentation
- AnimationState：https://docs.phaser.io/api-documentation/3.90.0/class/animations-animationstate
- ParticleEmitter：https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-particles-particleemitter
- Container：https://docs.phaser.io/api-documentation/3.90.0/class/gameobjects-container

验证记录（2026-11-03）：在用户 PVZ Phaser 3.90.0 工程完成 E3 定向集成验证：14 项自动化测试、生产构建、Edge 桌面/触摸模拟 E2E、PWA 离线资源 250/250 通过。受击 fallback 清单问题已修复，未修改运行时代码。评级暂保持 B，等待同一基线 A/B 各三轮对照；移动视口模拟不等于 Android 真机。