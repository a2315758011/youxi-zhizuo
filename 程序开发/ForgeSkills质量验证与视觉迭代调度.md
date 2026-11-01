# ForgeSkills 中文调度与适用边界

## 来源与固定版本

- 上游：[sekaikx/ForgeSkills](https://github.com/sekaikx/ForgeSkills)
- 导入时上游提交：`cefbba0720b58b110a2e8ab36e71e46246ea1e29`
- 许可证：Apache-2.0，原始 LICENSE 已保留。
- 导入内容：10 项技能、4 个图像评估脚本、5 个 Blender 脚本、上游测试结果、A/B 测试记录、限制说明。
- 当前评级：B（已保存、完成静态审阅；尚未在用户游戏项目执行）。
- 不把上游作者的测试报告当成用户项目的测试证据。

## 四项技能的中文用途

| 原始技能 | 中文职责 | 何时调用 |
|---|---|---|
| `gamedev-gameplay-systems` | 玩法系统设计与实现 | 战斗、敌人、背包、波次、成长、资源等系统规则不清或互相冲突时 |
| `gamedev-game-testing` | 游戏自动化测试 | 玩法规则、状态转换、回归、资产管线需要可重复测试时 |
| `gamedev-verification` | 完成前独立验收 | 即将报告完成、修复、构建成功或交付时 |
| `gamedev-visual-iteration` | 量化视觉迭代 | 场景/角色/道具与参考图不一致，反复修改却没有收敛时 |

一次只按任务选择必要技能，不要四项全部加载。

## 已导入的核心技能与常用依赖

导入 4 项核心技能，并额外保存 6 项常用依赖：
- `gamedev-debugging`：缺陷复现、隔离和定位。
- `gamedev-vfx-impact`：打击反馈与视觉/音频反馈。
- `gamedev-locomotion`：移动控制与运动手感。
- `gamedev-orchestrator`：研发阶段编排和门禁。
- `gamedev-reference-reconstruction`：按参考图重建资产。
- `gamedev-lighting`：光照与视觉层次。

这六项作为依赖按需调用，不要求每个游戏都加载。

### 尚未导入的可选上游技能

部分原始技能还引用其他专项能力。为避免无必要地复制全部 28 项技能，以下内容保留为上游按需获取项：
- 动画、镜头、性能：`gamedev-animation`、`gamedev-camera`、`gamedev-performance`。
- 美术与材质：`gamedev-texture-authoring`、`gamedev-art-direction`、`gamedev-foliage`。
- 概念与建模：`gamedev-concept-judge`、`gamedev-concept-lab`、`gamedev-blender-headless`、`gamedev-procedural-modeling`、`gamedev-modular-kit`、`gamedev-visual-artifacts`、`gamedev-world-from-data`。
- 引擎专用：`gamedev-godot-pipeline`、`gamedev-godot-visual-polish`、`gamedev-unity-pipeline`。
- 内容专项：`gamedev-boss-encounter`、`gamedev-audio-wire`。

需要时从固定上游版本按完整目录获取：[ForgeSkills 技能目录](https://github.com/sekaikx/ForgeSkills/tree/cefbba0720b58b110a2e8ab36e71e46246ea1e29/skills)。不要把未导入的名称误认为本仓库已有文件。

## 图像评估工具

位置：`外部专业技能库/ForgeSkills/tools/refmatch/`

- `compare.py`：轮廓 IoU、分段宽度轮廓、包围盒、主色差、亮度直方图；SSIM/RMSE 仅作辅助指标。
- `overlay.py`：生成参考图、渲染图和轮廓叠加的三联诊断图。
- `measure_sheet.py`：从概念资产板中裁出单个角色视图并采样色板。
- `palette_report.py`：提取色板并比较渲染色彩。

依赖：Python、Pillow、NumPy。当前只保存了源脚本，没有在用户仓库运行环境中安装依赖或执行工具；因此工具当前状态为“已导入、未运行验证”。不得宣称已经可以直接运行。

Blender 脚本位于 `外部专业技能库/ForgeSkills/tools/blender/`，依赖 Blender 自带的 `bpy` / `mathutils`。其中 `character_blockout.py` 与 `explorer_build.py` 会清理或移除活动场景中的对象/集合；在真实项目中运行前必须复制到隔离测试场景或独立 `.blend` 文件，禁止直接在用户主场景执行。其余脚本也必须先确认输入、输出和场景上下文。当前只做静态审阅，没有执行。

### 使用约束

1. 参考图与目标渲染必须使用同一视角、同一构图、同一裁切规则；视角/姿态不同，轮廓 IoU 不可直接作合格判定。
2. 先检查主体分割是否正确，再信任数值。背景漏入、阴影、透明边缘或裁切错误会污染指标。
3. IoU 只比较外轮廓，不代表内部结构、材质、动作和可读性都正确。
4. 色差只能检查颜色接近程度，不能证明角色身份或美术质量。
5. 指标与肉眼冲突时，先检查测量方法，不允许为了过线而篡改阈值。
6. 每轮只改一个主要原因，固定镜头重渲染；结果变差则回退。
7. 用户指定 GPT 原生图像生成功能时，不得静默改用第三方生图服务。这里的脚本只用于对比与测量，不负责生成图像。

## 玩法测试的最小闭环

按需采用四层测试：
1. 纯逻辑：伤害、资源、背包、经济和数值边界。
2. 状态机：转换条件、事件发射、重复触发和非法状态。
3. 无头集成：场景启动、系统接线、循环执行。
4. 视觉回归：固定状态截图与视觉检查。

玩法进入可玩阶段后，至少增加一个不使用设计者预设路线的独立测试代理/脚本，使用同一场景运行三次，验证目标是否可达、伤害是否实际产生、资源是否真实变化。若三个回合都未触达目标，说明内容可能只是装饰，必须调查原因。

测试必须证明测试本身有效：至少人为破坏一条规则，确认测试会失败。只会 PASS 的测试不构成可靠门禁。

## 上游测试报告：可以证明什么，不能证明什么

上游 `docs/TEST_RESULTS.md` 记录了：
- 技能库结构验证 28 项技能、81 项技术点，错误 0、警告 0；
- 图像裁切/轮廓/色彩测量脚本曾运行，并修复多个真实缺陷；
- Blender 场景验证曾发现模型漂移和缓存边界框问题；
- 参考角色重建最终未达标：轮廓 IoU 0.4628，要求 0.85，结论 FAIL。

上游 A/B 文档明确只有各一轮运行，是案例而非统计基准；上游也明确 Godot/Unity 技能没有在对应引擎中执行。故本仓库只采纳方法，不采纳未经验证的成功宣传。

## 工具安全审阅结论

已检查导入的四个 `refmatch` 脚本入口与依赖声明：它们用于读取图像、计算指标和输出诊断图；依赖 Pillow/NumPy。当前未执行第三方脚本，也未安装依赖。第一次在本机运行前，仍需检查实际 Python 环境、输入文件路径和输出目录，禁止把未知文件路径作为批量写入目标。

## 相关资料

- [原始技能与脚本](../../外部专业技能库/ForgeSkills/)
- [上游真实测试记录](../../外部专业技能库/ForgeSkills/docs/TEST_RESULTS.md)
- [上游 A/B 测试记录](../../外部专业技能库/ForgeSkills/docs/AB_TEST.md)
- [上游限制说明](../../外部专业技能库/ForgeSkills/docs/LIMITATIONS.md)
- [游戏技能效果评估与对照测试规范](../游戏技能效果评估与对照测试规范.md)
- [2D 美术资产与运行时交付规范](../2D美术资产与运行时交付规范.md)
