#!/usr/bin/env python3
"""
矩形绘图工具启动器
"""

try:
    import tkinter as tk
    print("[OK] tkinter已安装")
except ImportError:
    print("[ERROR] tkinter未安装，GUI功能不可用")
    exit(1)

try:
    import matplotlib.pyplot as plt
    print("[OK] matplotlib已安装")
except ImportError:
    print("[INFO] matplotlib未安装，正在尝试安装...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    print("[OK] matplotlib安装完成")

try:
    import numpy as np
    print("[OK] numpy已安装")
except ImportError:
    print("[INFO] numpy未安装，正在尝试安装...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    print("[OK] numpy安装完成")

print("\n正在启动矩形绘图工具GUI...")
print("-" * 40)

# 导入并启动GUI
from rectangle_gui import RectanglePlotterGUI
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    root = tk.Tk()
    app = RectanglePlotterGUI(root)

    # 设置窗口关闭时的确认
    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to exit the Rectangle Plotter?"):
            root.destroy()
            # 确保程序完全退出
            root.quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[INFO] 程序被用户中断")
    finally:
        print("[INFO] 矩形绘图工具已退出")
