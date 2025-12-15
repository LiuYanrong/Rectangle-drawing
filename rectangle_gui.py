#!/usr/bin/env python3
"""
矩形绘图工具 - GUI版本
提供图形界面用于输入矩形坐标并绘图
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class RectanglePlotterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Plotter")
        self.root.geometry("1200x800")

        # 矩形数据存储
        self.rectangles = []
        self.rectangles_data = []

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # 输入区域
        input_frame = ttk.LabelFrame(control_frame, text="输入矩形坐标", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 10))

        # 坐标输入（一行）
        ttk.Label(input_frame, text="坐标 (Left Right Back Front):").grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=2)
        self.coords_var = tk.StringVar(value="0.0 5.0 0.0 5.0")
        coords_entry = ttk.Entry(input_frame, textvariable=self.coords_var, width=40)
        coords_entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2, padx=(0, 5))

        # 坐标输入提示
        ttk.Label(input_frame, text="格式: 用空格或逗号分隔", font=('Arial', 8), foreground='gray').grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # 颜色和标签（一行）
        color_label_frame = ttk.Frame(input_frame)
        color_label_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # 颜色选择
        ttk.Label(color_label_frame, text="颜色:").pack(side=tk.LEFT, padx=(0, 5))
        self.color_var = tk.StringVar(value="blue")
        color_combo = ttk.Combobox(color_label_frame, textvariable=self.color_var, width=10, state="readonly")
        color_combo['values'] = ('blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan', 'magenta', 'yellow')
        color_combo.pack(side=tk.LEFT, padx=(0, 20))

        # 标签输入
        ttk.Label(color_label_frame, text="标签:").pack(side=tk.LEFT, padx=(0, 5))
        self.label_var = tk.StringVar(value="")
        ttk.Entry(color_label_frame, textvariable=self.label_var, width=15).pack(side=tk.LEFT)

        # 按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="添加矩形", command=self.add_rectangle).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清除所有", command=self.clear_all).pack(side=tk.LEFT)

        # 矩形列表
        list_frame = ttk.LabelFrame(control_frame, text="矩形列表", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 创建Treeview
        columns = ('Left', 'Right', 'Back', 'Front', 'Color', 'Label')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)

        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 删除选中项按钮
        ttk.Button(list_frame, text="删除选中", command=self.delete_selected).pack(pady=(5, 0))

        # 绘图选项
        options_frame = ttk.LabelFrame(control_frame, text="绘图选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        self.show_centers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="显示中心点", variable=self.show_centers_var).pack(anchor=tk.W)

        self.show_grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="显示网格", variable=self.show_grid_var).pack(anchor=tk.W)

        self.equal_aspect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="等比例坐标", variable=self.equal_aspect_var).pack(anchor=tk.W)

        # 操作按钮
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill=tk.X)

        ttk.Button(action_frame, text="绘制图形", command=self.plot_rectangles, style="Accent.TButton").pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="保存图片", command=self.save_plot).pack(fill=tk.X)

        # 右侧绘图区域
        plot_frame = ttk.LabelFrame(main_frame, text="绘图区域", padding="10")
        plot_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建matplotlib图形
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 初始化空图
        self.setup_empty_plot()

    def setup_empty_plot(self):
        """设置空白的初始图形"""
        self.ax.clear()
        self.ax.set_xlabel('Left - Right Coordinates')
        self.ax.set_ylabel('Back - Front Coordinates')
        self.ax.set_title('Rectangle Plotter')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3, linewidth=0.5)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.canvas.draw()

    def add_rectangle(self):
        """添加矩形"""
        try:
            # 获取坐标输入
            coords_input = self.coords_var.get().strip()
            if not coords_input:
                messagebox.showerror("错误", "请输入坐标！")
                return

            # 解析坐标（支持空格或逗号分隔）
            # 先按逗号分割，再按空格分割
            parts = []
            for part in coords_input.replace(',', ' ').split():
                if part.strip():  # 忽略空字符串
                    parts.append(part.strip())

            if len(parts) != 4:
                messagebox.showerror("错误", f"需要4个坐标值，当前输入了{len(parts)}个值！")
                return

            left = float(parts[0])
            right = float(parts[1])
            back = float(parts[2])
            front = float(parts[3])
            color = self.color_var.get()
            label = self.label_var.get() or f"Box {len(self.rectangles) + 1}"

            # 添加到数据列表
            rect_data = {
                'left': left,
                'right': right,
                'back': back,
                'front': front,
                'color': color,
                'label': label
            }
            self.rectangles_data.append(rect_data)

            # 添加到树形列表
            self.tree.insert('', 'end', values=(
                f"{left:.2f}",
                f"{right:.2f}",
                f"{back:.2f}",
                f"{front:.2f}",
                color,
                label
            ))

            # 清空坐标输入框和标签（保留颜色）
            self.coords_var.set("0.0 5.0 0.0 5.0")
            self.label_var.set("")

            messagebox.showinfo("成功", f"矩形 '{label}' 已添加！")

        except ValueError as e:
            messagebox.showerror("错误", f"坐标格式错误，请输入有效的数字！\n详情：{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"添加矩形时发生错误：{str(e)}")

    def delete_selected(self):
        """删除选中的矩形"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的矩形！")
            return

        # 删除选中的项目
        for item in selected_items:
            # 获取选中项的索引
            index = self.tree.index(item)
            # 从数据列表中删除
            if 0 <= index < len(self.rectangles_data):
                del self.rectangles_data[index]
            # 从树形列表中删除
            self.tree.delete(item)

        messagebox.showinfo("成功", "选中的矩形已删除！")

    def clear_all(self):
        """清除所有矩形"""
        if not self.rectangles_data:
            messagebox.showinfo("提示", "没有矩形需要清除！")
            return

        if messagebox.askyesno("确认", "确定要清除所有矩形吗？"):
            self.rectangles_data.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.setup_empty_plot()
            messagebox.showinfo("成功", "所有矩形已清除！")

    def plot_rectangles(self):
        """绘制所有矩形"""
        if not self.rectangles_data:
            messagebox.showwarning("警告", "没有矩形可绘制！")
            return

        # 清除当前图形
        self.ax.clear()

        # 绘制每个矩形
        for i, rect_data in enumerate(self.rectangles_data):
            left = rect_data['left']
            right = rect_data['right']
            back = rect_data['back']
            front = rect_data['front']
            color = rect_data['color']
            label = rect_data['label']

            # 确保坐标顺序正确
            x_min, x_max = min(left, right), max(left, right)
            y_min, y_max = min(back, front), max(back, front)

            # 绘制矩形
            width = x_max - x_min
            height = y_max - y_min
            rect = patches.Rectangle((x_min, y_min), width, height,
                                   linewidth=2, edgecolor=color, facecolor='none',
                                   label=label)
            self.ax.add_patch(rect)

            # 添加中心点
            if self.show_centers_var.get():
                x_center = x_min + width / 2
                y_center = y_min + height / 2
                self.ax.plot(x_center, y_center, color=color, marker='+', markersize=10)

        # 设置坐标轴范围
        if self.rectangles_data:
            all_x = []
            all_y = []
            for rect_data in self.rectangles_data:
                all_x.extend([rect_data['left'], rect_data['right']])
                all_y.extend([rect_data['back'], rect_data['front']])

            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)

            # 添加边距
            x_pad = (x_max - x_min) * 0.1 if x_max != x_min else 1
            y_pad = (y_max - y_min) * 0.1 if y_max != y_min else 1

            self.ax.set_xlim(x_min - x_pad, x_max + x_pad)
            self.ax.set_ylim(y_min - y_pad, y_max + y_pad)

        # 设置图形属性
        self.ax.set_xlabel('Left - Right Coordinates')
        self.ax.set_ylabel('Back - Front Coordinates')
        self.ax.set_title('Rectangle Plotter')

        if self.show_grid_var.get():
            self.ax.grid(True, linestyle='--', alpha=0.6)

        if self.equal_aspect_var.get():
            self.ax.set_aspect('equal', adjustable='box')

        # 添加坐标轴
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3, linewidth=0.5)

        # 添加图例
        if self.rectangles_data:
            self.ax.legend()

        # 刷新画布
        self.canvas.draw()

    def save_plot(self):
        """保存图片"""
        if not self.rectangles_data:
            messagebox.showwarning("警告", "没有图形可保存！")
            return

        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            initialdir="out",  # 默认打开out目录
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # 确保目录存在
                import os
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"图片已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败: {str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    app = RectanglePlotterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()