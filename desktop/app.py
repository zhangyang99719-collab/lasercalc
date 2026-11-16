"""LIMA 激光工具箱 - 桌面版（宽短三列布局）

完全自包含的 HTML 应用：所有计算逻辑、canvas 绘图、交互都内嵌在 web/index.html 中，
本启动器只负责用 pywebview 加载它，不依赖任何外部 Python 计算库或网络。
"""
import os
import sys

import webview


def resource_path(relative):
    """兼容开发环境与 PyInstaller 打包后的资源路径。"""
    base = getattr(sys, "_MEIPASS", None)
    if base is None:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative)


def main():
    html = resource_path(os.path.join("web", "index.html"))
    webview.create_window(
        title="LIMA 激光工具箱",
        url=html,
        width=1340,
        height=780,
        min_size=(980, 600),
        background_color="#0b1020",
        text_select=True,
    )
    webview.start()


if __name__ == "__main__":
    main()
