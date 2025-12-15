# 矩形绘图工具

一个使用Python编写的矩形绘图工具，提供GUI界面和核心绘图功能，可以根据坐标输入绘制多个矩形并在坐标系中显示。

## 📁 文件说明

- **[rectangle_plotter.py](d:\code\ZhuoBiao\rectangle_plotter.py)** - 核心绘图类库
- **[rectangle_gui.py](d:\code\ZhuoBiao\rectangle_gui.py)** - GUI图形界面版本
- **[startGUI.py](d:\code\ZhuoBiao\startGUI.py)** - GUI启动器（自动安装依赖）

## 🚀 使用方法

### 准备工作
1. 激活Python环境：
   ```bash
   activate radar
   ```

2. 安装依赖（如果尚未安装）：
   ```bash
   pip install -r requirements.txt
   ```

### 方法1: 启动GUI版本（推荐）
```bash
python startGUI.py
```
这将自动检查依赖并启动图形界面。

### 方法2: 直接运行GUI
```bash
python rectangle_gui.py
```

### 方法3: 使用核心库编程
```python
from rectangle_plotter import RectanglePlotter

# 创建绘图器
plotter = RectanglePlotter()

# 添加矩形
plotter.add_rectangle(-0.70, 4.30, -0.01, 3.78, color='blue', label='Box 1')
plotter.add_rectangle(-0.38, 0.52, 1.46, 3.46, color='red', label='Box 2')

# 绘制并显示
plotter.plot(title="My Rectangles")
```

## 🖥️ GUI界面功能

### 左侧控制面板
- **坐标输入**: 一行输入框，格式为 "Left Right Back Front"，支持空格或逗号分隔
- **颜色和标签**: 颜色选择器和标签输入框在同一行
- **操作按钮**:
  - "添加矩形" - 将输入的矩形添加到列表
  - "清除所有" - 清空所有矩形
- **矩形列表**: 显示所有已添加的矩形，支持选中删除
- **绘图选项**:
  - 显示中心点 ✓
  - 显示网格 ✓
  - 等比例坐标 ✓
- **操作按钮**:
  - "绘制图形" - 在右侧显示所有矩形
  - "保存图片" - 保存当前图形

### 右侧绘图区域
- 实时显示矩形绘制结果
- 支持缩放和平移
- 显示坐标轴和图例

## 📝 示例坐标

### 示例1: 嵌套矩形
```
矩形1: Left=-0.70, Right=4.30, Back=-0.01, Front=3.78, 颜色=蓝色, 标签=Box 1 (Outer)
矩形2: Left=-0.38, Right=0.52, Back=1.46, Front=3.46, 颜色=红色, 标签=Box 2 (Inner)
```

### 示例2: 分布矩形
```
矩形1: Left=1, Right=5, Back=2, Front=6, 颜色=绿色
矩形2: Left=3, Right=8, Back=1, Front=4, 颜色=橙色
矩形3: Left=6, Right=9, Back=3, Front=7, 颜色=紫色
```

## 🔧 依赖安装

### 1. 激活Python环境
```bash
activate radar
```

### 2. 安装依赖
```bash
pip install matplotlib numpy
```

或者使用requirements.txt文件：
```bash
pip install -r requirements.txt
```

## 💡 使用技巧

1. **坐标输入**: 支持多种格式输入坐标
   - 空格分隔: `1 5 2 6`
   - 逗号分隔: `1,5,2,6`
   - 混合分隔: `1, 5 2,6`
2. **坐标顺序**: Left可以大于Right，Back可以大于Front，程序会自动处理
3. **快速添加**: 输入完坐标后可以直接点击"添加矩形"按钮
4. **删除矩形**: 在列表中选中矩形后点击"删除选中"按钮
5. **保存格式**: 推荐使用PNG格式获得最佳图片质量
6. **颜色区分**: 为不同矩形使用不同颜色便于识别

## ⚠️ 注意事项

1. 确保安装了matplotlib和numpy依赖
2. 输入坐标必须是有效的数字
3. 坐标值可以是正数或负数
4. 如果GUI启动失败，请检查tkinter是否可用
