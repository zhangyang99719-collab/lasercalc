# LIMA 激光工具箱 · 桌面版

把微信小程序「LIMA-Tools」（原 `limacalc` v2.1.0）的界面完整还原成**宽短三列**的桌面 App。

## 特点

- **宽短布局**：参数在左、原理/云图在中、结果在右，一屏装下，贴合电脑桌面使用习惯（区别于小程序的竖长屏）
- **完全自包含**：计算逻辑、canvas 绘图、交互全部内嵌在 `web/index.html`，不依赖网络、不需要 Python 计算库
- **五大功能模块**：光路设计、激光参数（能量密度仿真）、脉冲特性、激光智造日报、设置
- **单文件 exe**：打包后拷贝即可运行，无需安装 Python

## 源码结构

```
limacalc-desktop/
├── app.py                 # pywebview 启动器（只负责加载 HTML）
├── build.spec             # PyInstaller 打包配置
├── app.ico                # 应用图标
├── web/
│   └── index.html         # 自包含应用（界面 + 算法 + canvas 全部在内）
└── dist/
    └── LIMA激光工具箱.exe  # 打包产物
```

## 构建

本目录是 lasercalc 仓库的桌面子项目。进入本目录后：

```powershell
cd desktop
pip install pywebview pyinstaller
python -m PyInstaller build.spec --noconfirm --clean
```

生成的 `dist/LIMA激光工具箱.exe` 可直接双击运行，也可拷贝到任意 Win10/11 机器（无需 Python 环境）。
前提：Windows 需装有 Edge WebView2 运行时（Win11 默认自带，Win10 多数已装）。

## 说明

- 界面与算法是从微信小程序 `.js` 完整移植而来，非重新实现
- 日报页在桌面版使用本地示例数据（原小程序走 CloudBase 远程拉取）
- 关联的 Python 计算库开源版见 [lasercalc](https://github.com/zhangyang99719-collab/lasercalc)

MIT © 2026 LIMA
