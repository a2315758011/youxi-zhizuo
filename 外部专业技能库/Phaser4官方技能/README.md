# Phaser 4 官方 AI 技能（版本隔离归档）

来源：[phaserjs/phaser](https://github.com/phaserjs/phaser)

- 上游分支：`master`
- 固定提交：`02d8931b626d9764c133cbb3fbf99966c03c757c`
- 上游 `package.json` 版本：**Phaser 4.2.1**
- 许可证：MIT；原始 `LICENSE.md` 已完整保留。
- 上游仓库最后推送时间元数据：2026-08-21；仓库页面的更新时间不代表代码有新提交。
- 归档：27 项官方 `SKILL.md`，按上游 `skills/<name>/SKILL.md` 目录结构保存，正文未翻译、未改写。

## 最高优先级：引擎版本门禁

**本目录所有技能只适用于 Phaser 4。禁止直接用于 Phaser 3 项目。**

使用前必须检查目标项目的 `package.json` 和 lockfile 中实际安装的 `phaser` 版本：

- Phaser 4.2.x：可以按任务加载本目录对应技能。
- Phaser 3.90.x：使用本仓库自编写的 [Phaser 3.90 运行时资产集成技能](../Phaser3.90运行时资产集成/SKILL.md) 与现有移动端 Phaser 工作流；`awesome-gamedev-agent-skills` 中的 `phaser-core`、`phaser-arcade-physics` 当前正文以 Phaser 4.2 为目标，不得误当作 Phaser 3.90 技能。
- Phaser 3 → Phaser 4：只有用户明确要求升级时，才加载 `v3-to-v4-migration`，逐项核对官方迁移文档、锁文件和回归测试；不得因有新技能就主动升级。

当前 `PVZ-Complete-Game` 的 `package.json` 声明 `phaser: ^3.90.0`。因此，本目录**不适用于当前 PVZ 工程**，也不计入该工程的已验证能力。

## 归档技能（27 项）

| 技能 | 用途 |
|---|---|
| `actions-and-utilities` | 动作工具与通用辅助 |
| `animations` | 精灵动画、播放状态与动画事件 |
| `audio-and-sound` | 音频加载、播放与声音管理 |
| `cameras` | 相机、跟随、边界、震动和淡入淡出 |
| `curves-and-paths` | 曲线、路径与轨迹 |
| `data-manager` | 游戏对象数据管理 |
| `events-system` | 事件系统与监听生命周期 |
| `filters-and-postfx` | 滤镜与后期效果 |
| `game-object-components` | 游戏对象组件与混入能力 |
| `game-setup-and-config` | 游戏实例与配置 |
| `geometry-and-math` | 几何与数学工具 |
| `graphics-and-shapes` | 图形绘制与形状 |
| `groups-and-containers` | 对象组与容器 |
| `loading-assets` | 资源加载器与加载生命周期 |
| `particles` | 粒子发射器、区域、重力井和生命周期 |
| `physics-arcade` | Arcade 物理 |
| `physics-matter` | Matter.js 物理 |
| `render-textures` | RenderTexture / DynamicTexture |
| `scale-and-responsive` | 分辨率、缩放和响应式视口 |
| `scenes` | 场景生命周期与场景切换 |
| `sprites-and-images` | Sprite / Image 对象与显示属性 |
| `text-and-bitmaptext` | 普通文本与位图字体 |
| `tilemaps` | 瓦片地图与图层 |
| `time-and-timers` | 时间事件与计时器 |
| `tweens` | 缓动、链式动画和属性插值 |
| `v3-to-v4-migration` | Phaser 3 到 4 的迁移 |
| `v4-new-features` | Phaser 4 新增能力 |

### 未导入的第 28 项

上游 `input-keyboard-mouse-touch` 共 501 行，超过本仓库技能质量门禁采用的单文件 500 行上限；且本仓库已有移动端输入技能。为避免未经拆分就破坏原文或重复引入，暂不作为独立 Skill 导入。需要 Phaser 4 输入细节时可从上游固定版本在线读取，不得用 Phaser 3 输入 API 替代。

## 中文调度建议

- 动画/精灵：`animations` + `sprites-and-images`，必要时加 `loading-assets`。
- 粒子/特效：`particles` + `sprites-and-images`；游戏反馈设计另按需加载现有 `game-feel` / `juice-vfx`。
- UI/响应式：`scale-and-responsive`，并结合本仓库已有 `game-ui-ux`；具体输入需匹配 Phaser 版本。
- 场景和资源：`scenes` + `loading-assets`。
- 性能/渲染问题：先采集实际数据，再按问题选择 `render-textures`、`filters-and-postfx` 或物理技能。
- 不要一次性加载 27 项；每阶段最多 3 个专业技能 + 1 个必要引擎技能。

## 质量与验证边界

- 已核对上游仓库、固定 commit、Phaser 4.2.1 版本和 MIT 许可证。
- 27 份正文均来自固定提交；本地保留上游目录层级。
- 上游技能是 Phaser 4 文档，不是 Phaser 3.90 兼容性证明。
- 本轮只做仓库归档和静态结构验收；没有在 Phaser 4.2.1 项目运行这些技能，也没有做 A/B 实验。
- 当前评级：**B（来源和版本已核验，真实项目效果待验证）**。
