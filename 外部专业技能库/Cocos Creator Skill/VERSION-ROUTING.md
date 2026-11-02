# Cocos Creator / COCOS 版本路由补充

## 目的

将“引擎版本”与“COCOS 4 平台/发布体系”分开识别，避免因名称相似而套错 API。

## 当前证据与谨慎结论

- 本仓库归档的社区 Skill hsiaozzz/cocos-creator-skill 固定版本 2.0.0，明确覆盖 Cocos Creator 3.8.x 与 COCOS 4；它属于社区维护资料，官方 API 不一致时以目标编辑器对应的官方文档为准。
- Cocos 官方 2026 年 10 月全版本更新公告说明，升级新增全平台发布能力，但不会更改当前 Creator 版本号。COCOS 4 的发布/应用/场景体系不能直接当成“Cocos Creator 引擎 4.x API”。
- 官方文档站当前存在 /creator/4.0/ 路径和“Cocos Creator 4.0”页面标题，但同一页面的产品线说明仍称 Creator 3.x 为最新 Creator 版本，并明确提示 2.x 与 3.x API 不完全兼容。该页面命名与产品线文字存在歧义，不能只凭 URL 认定项目实际引擎版本。
- 官方入口：https://docs.cocos.com/creator/4.0/manual/zh/；3.8 LTS：https://docs.cocos.com/creator/3.8/manual/zh/。

## 强制版本探针

每个项目开始前读取并交叉核对：
1. 项目 project.json 的 engine / version 字段（如存在）。
2. 编辑器实际启动版本与安装目录。
3. settings/v2/packages、package.json、项目配置或构建日志中记录的版本（按项目结构适用）。
4. 官方 API Reference 的对应版本入口。

如果上述信息不一致，标记 VERSION_MISMATCH 并停止写入；不得自动升级、迁移或用 COCOS 4 平台名称替代 Creator 版本。

## 路由规则

- Creator 3.8.x：使用现有 Cocos Creator Skill 的 3.8.x API 路由，并按精确补丁版本核验。
- COCOS 4 发布/应用/场景功能：作为平台集成层单独处理；先核验当前 Creator 编辑器版本及平台能力，不推断 API 主版本。
- 未能确认真实 Creator 4.x 编辑器与 API 基线：不建立“Creator 4 引擎 API”假技能；标记待官方版本证据确认。
- Creator 2.x、3.x、其他分支不能混用脚本、序列化资源或 .meta UUID 规则。

## 动画、美术和运行时验收

官方 Creator 手册目录列出 Spine、DragonBones、关键帧动画、Marionette Animation Graph、2D 粒子、UI 组件、资源管理和跨平台构建章节。实际导入时仍要确认目标版本对 Spine/DragonBones runtime、资源格式和导出器版本的支持矩阵。不要只凭文档目录就宣称已运行兼容。

## 结论

当前技能库已有 Cocos Creator 3.8.x / COCOS 4 的社区技能；本补充负责版本命名纠偏和 API 路由，不宣称 COCOS 4 等于 Creator 4.x，也不替代真实工程测试。

## 官方来源
- COCOS 全版本升级指南（2026-10-01）：https://www.cocos.com/post/LZ9OEy7zzL9ZUhrOMx6gJEcrUdD4LU1D — 明确说明本次更新不更改 Creator 版本号，只新增全平台发布平台。
- COCOS 全版本更新（第二批，2026-10-19）：https://www.cocos.com/post/sEVobOeOg1RNyzgSfHDS1suE3HUzkshJ — 说明各 Creator 版本新增全平台发布能力。
- Cocos Creator 4.0 文档页：https://docs.cocos.com/creator/4.0/manual/en/ — 页面目录涵盖 Spine、DragonBones、动画、粒子与 UI；同页产品线说明仍称 Creator 3.x 为最新版本，因此须按实际编辑器版本确认 API。
