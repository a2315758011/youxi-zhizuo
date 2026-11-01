# 自动化测试框架参考与版本记录

本目录保存框架选择依据和许可证副本，不直接捆绑/安装测试插件。实际游戏项目确定引擎与精确版本后，才安装对应版本。

## Godot

### GUT
- 仓库：https://github.com/bitwes/Gut
- 当前核对版本：9.7.1，适配 Godot 4.7.x；9.6.1 适配 4.6.x；9.5.0 适配 4.5.x；9.4.0 适配 4.3–4.4。
- 特点：GDScript 单元测试、命令行执行、JUnit XML。
- 适用：GDScript 为主、需要轻量逻辑测试的项目。
- 许可证：MIT，见 GUT-LICENSE。

### GdUnit4
- 仓库：https://github.com/godot-gdunit-labs/gdUnit4
- 当前核对稳定版：v6.2.2（2026-10-07），标签提交：0127a55f4543dfc24746f6e5c7ba6f94105d51f2。
- 兼容：6.2.x 对应 Godot 4.5–4.7 系列；更旧引擎需选择历史兼容版本。
- 特点：GDScript/C#、场景集成测试、Scene Runner、输入模拟、信号等待、测试报告与 CI。
- 适用：C# 项目，或需要场景/触控交互测试的 Godot 项目。
- 许可证：MIT，见 GdUnit4-LICENSE。

### GodotTestDriver
- 仓库：https://github.com/chickensoft-games/GodotTestDriver
- 定位：C# 项目的节点交互驱动库，不是测试执行器；需搭配测试运行器。
- 默认不安装，只有项目确实需要其节点驱动抽象时再评估。

## Unity

- 官方 Unity Test Framework 文档：https://docs.unity.com/en-us/engine/7000.0/manual/programming-environment/test-framework-introduction
- Edit Mode 与 Play Mode 区别：https://docs.unity.cn/6000.3/Documentation/Manual/test-framework/edit-mode-vs-play-mode-tests.html
- 优先用官方框架，不额外引入第三方运行器。

## 其他参考

- Godot headless 测试注意事项研究：https://github.com/Mozurok/fhorja.dev/blob/main/wos/godot-testing-and-ci.md
- GdUnit4 Scene Runner：https://godot-gdunit-labs.github.io/gdUnit4/latest/advanced_testing/sceneRunner/
- Godot 用户数据路径：https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html
- Godot ConfigFile：https://docs.godotengine.org/en/stable/classes/class_configfile.html

## 选择纪律

- 先确认项目引擎和版本；不为一个测试任务同时安装 GUT 与 GdUnit4。
- 自动化测试通过不等于真实设备通过；headless 不验证渲染窗口和真实输入设备。
- 不把测试框架依赖加入游戏正式运行包，除非引擎/平台明确要求。
- 当前仅保存选择依据与许可证，不代表已安装、已运行或通过用户项目验收。
