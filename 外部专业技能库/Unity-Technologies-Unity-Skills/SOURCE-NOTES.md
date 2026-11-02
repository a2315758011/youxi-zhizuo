# Unity 官方技能来源说明

- 上游：[Unity-Technologies/skills](https://github.com/Unity-Technologies/skills)
- 固定 Git tree：`089bedebab64e9e75943b19a364c7aec2162a7e7`（2026-11-02 检索）
- 上游许可证：Unity Companion License，根目录 `LICENSE.md` 已保留；仅用于有效 Unity Engine License 关联的 Unity 内容创作/发行场景，不按 MIT/Apache 重新分发。
- 本仓库精选 5 项官方技能：
  1. `unity-cli`：控制已连接 Unity Editor、构建、测试和运行时检查；官方仍标记为 experimental，使用前核对版本。
  2. `sprite-editor`：通过 Sprite Editor Data Provider 管理切片、rect、pivot、border、outline；不手工修改 .meta。
  3. `manage-sprite-atlas`：SpriteAtlas V2、编辑器/运行时分离、预构建、变体、Addressables、缓存和加载；主技能、references 与 38 个资源示例已导入。
  4. `2d-pixel-perfect`：区分 URP 与 Built-in 两套不兼容实现，先识别渲染管线；只适用于像素风/低分辨率素材，不用于高清 2D。
  5. `create-tile-palette-or-rule-tiles`：创建 Tile Palette/RuleTile，适合网格地形、自动连接边缘和关卡网格。
- SpriteAtlas V2 强制区分 Editor-only 的 SpriteAtlasAsset 与 Runtime-only 的 SpriteAtlas；通过 SpriteAtlasImporter 配置；修改后 SaveAndReimport；禁止在运行时代码执行编辑器打包逻辑。
- Tile Palette 上游示例创建资源前需检查目标路径，防止覆盖同名资产；依赖 `com.unity.2d.tilemap`。
- Pixel Perfect：URP/Built-in 的组件、包和 API 不兼容；HDRP 不支持；高清美术不应强行启用 Point filtering。
- 未做事项：未安装 Unity CLI，未在用户 Unity 工程创建/修改 SpriteAtlas、Tile Palette 或相机设置。
- 评级：B（官方来源、依赖文档与示例已归档；真实项目运行验收待执行）。
