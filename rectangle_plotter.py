#!/usr/bin/env python3
"""
矩形绘图工具
输入多个矩形的坐标 (x1, x2, y1, y2)，在坐标系中绘制并显示这些矩形
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np
import os
from datetime import datetime


class RectanglePlotter:
    def __init__(self):
        self.rectangles = []
        self.rectangles_data = []  # 存储原始数据用于标签
        self.colors = []

    def add_rectangle(self, x1, x2, y1, y2, color='blue', alpha=0.5, label=None, facecolor='none'):
        """
        添加一个矩形到绘图列表

        参数:
        x1, x2: x轴坐标 (l=left, r=right)
        y1, y2: y轴坐标 (b=back, f=front)
        color: 矩形边框颜色
        alpha: 透明度 (0-1)
        label: 矩形标签
        facecolor: 填充颜色，默认为透明
        """
        # 确保坐标顺序正确
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)

        self.rectangles.append((x_min, y_min, x_max - x_min, y_max - y_min))
        self.rectangles_data.append({
            'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2,
            'color': color, 'alpha': alpha, 'label': label, 'facecolor': facecolor
        })
        self.colors.append((color, alpha, facecolor))

    def add_rectangles_from_list(self, rect_list, colors=None, labels=None):
        """
        从列表批量添加矩形

        参数:
        rect_list: 矩形列表，每个元素为 (x1, x2, y1, y2)
        colors: 颜色列表，如果为None则使用默认颜色循环
        labels: 标签列表，如果为None则自动生成
        """
        default_colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

        for i, rect in enumerate(rect_list):
            if len(rect) != 4:
                print(f"警告: 跳过无效矩形坐标 {rect}，需要4个坐标值")
                continue

            if colors and i < len(colors):
                color = colors[i]
            else:
                color = default_colors[i % len(default_colors)]

            if labels and i < len(labels):
                label = labels[i]
            else:
                label = f'Box {i+1}'

            x1, x2, y1, y2 = rect
            self.add_rectangle(x1, x2, y1, y2, color=color, label=label)

    def plot(self, show_grid=True, show_axes=True, equal_aspect=True, title="矩形绘图",
            show_centers=True, save_path=None, xlabel='Left - Right Coordinates', ylabel='Back - Front Coordinates', auto_save=False):
        """
        绘制所有矩形

        参数:
        show_grid: 是否显示网格
        show_axes: 是否显示坐标轴
        equal_aspect: 是否使用等比例坐标轴
        title: 图表标题
        show_centers: 是否显示中心点标记
        save_path: 保存图片路径，如果为None则不保存
        xlabel: x轴标签
        ylabel: y轴标签
        auto_save: 是否自动保存到out目录
        """
        if not self.rectangles:
            print("没有矩形可绘制！")
            return

        fig, ax = plt.subplots(figsize=(10, 8))

        # 绘制矩形
        for i, (rect_coords, rect_data, (color, alpha, facecolor)) in enumerate(
            zip(self.rectangles, self.rectangles_data, self.colors)):

            rect = patches.Rectangle(rect_coords[:2], rect_coords[2], rect_coords[3],
                                    linewidth=2, edgecolor=color, facecolor=facecolor,
                                    label=rect_data['label'])
            ax.add_patch(rect)

            # 添加中心点标记
            if show_centers:
                x_center = rect_coords[0] + rect_coords[2] / 2
                y_center = rect_coords[1] + rect_coords[3] / 2
                ax.plot(x_center, y_center, color=color, marker='+', markersize=10)

        # 设置坐标轴范围
        all_x = []
        all_y = []
        for rect_data in self.rectangles_data:
            all_x.extend([rect_data['x1'], rect_data['x2']])
            all_y.extend([rect_data['y1'], rect_data['y2']])

        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)

        # 添加一些边距
        x_pad = (x_max - x_min) * 0.1 if x_max != x_min else 1
        y_pad = (y_max - y_min) * 0.1 if y_max != y_min else 1

        ax.set_xlim(x_min - x_pad, x_max + x_pad)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)

        # 设置图表属性
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        if show_grid:
            ax.grid(True, linestyle='--', alpha=0.6)

        if equal_aspect:
            ax.set_aspect('equal', adjustable='box')

        # 添加图例
        if self.rectangles_data:
            ax.legend()

        plt.tight_layout()

        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图片已保存到: {save_path}")
        elif auto_save:
            # 自动保存到out目录
            os.makedirs('out', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_save_path = f'out/rectangles_{timestamp}.png'
            plt.savefig(default_save_path, dpi=300, bbox_inches='tight')
            print(f"图片已自动保存到: {default_save_path}")

        plt.show()

    def clear(self):
        """清除所有矩形"""
        self.rectangles = []
        self.rectangles_data = []
        self.colors = []


def main():
    """
    主函数 - 交互式使用示例
    """
    plotter = RectanglePlotter()

    print("=== 矩形绘图工具 ===")
    print("输入格式: x1 x2 y1 y2 (用空格分隔)")
    print("输入 'done' 完成输入并开始绘图")
    print("输入 'quit' 退出程序")
    print("输入 'clear' 清除所有已输入的矩形")
    print()

    while True:
        user_input = input("请输入矩形坐标 (x1 x2 y1 y2): ").strip()

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'done':
            if plotter.rectangles:
                plotter.plot()
            else:
                print("没有输入任何矩形！")
            break
        elif user_input.lower() == 'clear':
            plotter.clear()
            print("已清除所有矩形")
            continue

        try:
            coords = list(map(float, user_input.split()))
            if len(coords) != 4:
                print("错误: 请输入4个坐标值 (x1 x2 y1 y2)")
                continue

            x1, x2, y1, y2 = coords
            plotter.add_rectangle(x1, x2, y1, y2)
            print(f"已添加矩形: ({x1}, {x2}, {y1}, {y2})")

        except ValueError:
            print("错误: 请输入有效的数字")


def example_usage():
    """
    使用示例 - 基于参考代码的示例
    """
    # 创建绘图器
    plotter = RectanglePlotter()

    # 示例1: 类似参考代码的两个box
    # Box 1: l=-0.70, r=4.30, b=-0.01, f=3.78
    # Box 2: l=-0.38, r=0.52, b=1.46, f=3.46
    plotter.add_rectangle(-0.70, 4.30, -0.01, 3.78, color='blue', label='Box 1 (Outer)')
    plotter.add_rectangle(-0.38, 0.52, 1.46, 3.46, color='red', label='Box 2 (Inner)')

    # 绘制并保存到out目录
    plotter.plot(title="Relative Position of Bounding Boxes", save_path='out/boxes_plot.png')

    # 清除后重新演示其他示例
    plotter.clear()

    # 示例2: 多个矩形的复杂情况
    rectangles = [
        (1, 5, 2, 6),    # 矩形1
        (3, 8, 1, 4),    # 矩形2
        (6, 9, 3, 7),    # 矩形3
        (0, 2, 0, 3),    # 矩形4
        (-3, -1, -2, 1),  # 矩形5
        (4, 7, -1, 2),    # 矩形6
        (-2, 1, 4, 6)     # 矩形7
    ]
    labels = ['Rectangle A', 'Rectangle B', 'Rectangle C', 'Rectangle D',
              'Rectangle E', 'Rectangle F', 'Rectangle G']
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']

    plotter.add_rectangles_from_list(rectangles, colors, labels)
    plotter.plot(title="Multiple Rectangles Example", save_path='out/multiple_rectangles.png')


def simple_example():
    """
    简单示例 - 与参考代码完全一致的使用方式
    """
    # 创建绘图器
    plotter = RectanglePlotter()

    # 数据 - 与参考代码完全一致
    # Box 1: l=-0.70, r=4.30, b=-0.01, f=3.78
    box1_coords = {'l': -0.70, 'r': 4.30, 'b': -0.01, 'f': 3.78}
    # Box 2: l=-0.38, r=0.52, b=1.46, f=3.46
    box2_coords = {'l': -0.38, 'r': 0.52, 'b': 1.46, 'f': 3.46}

    # 添加矩形
    plotter.add_rectangle(box1_coords['l'], box1_coords['r'],
                         box1_coords['b'], box1_coords['f'],
                         color='blue', label='Box 1 (Outer)')
    plotter.add_rectangle(box2_coords['l'], box2_coords['r'],
                         box2_coords['b'], box2_coords['f'],
                         color='red', label='Box 2 (Inner)')

    # 绘制 - 与参考代码完全一致的设置，保存到out目录
    plotter.plot(title="Relative Position of Bounding Boxes",
                save_path='out/boxes_plot.png')


if __name__ == "__main__":
    # 运行交互式程序
    # main()

    # 运行简单示例（与参考代码一致）
    simple_example()

    # 或者运行复杂示例
    # example_usage()