# FEM分析专用环境 🌉

基于Apple Silicon Mac优化的有限元分析环境，专注于桥梁和结构工程分析。

## 项目概述

本项目创建了一个专用的Conda环境，集成了多种FEM（有限元方法）库，特别针对**三跨连续梁桥**分析进行了优化和测试。

### 🎯 主要特性

- ✅ **Apple Silicon原生支持** - 完全兼容M1/M2/M3芯片
- 🌉 **桥梁专业化** - 专门优化的连续梁桥分析
- 📊 **多库对比** - 测试多种FEM库的性能和结果
- 🔧 **开箱即用** - 预配置的分析环境

## 🛠️ 安装的FEM库

| 库名称 | 版本 | 状态 | 适用场景 |
|--------|------|------|----------|
| **OpenSees (xara)** | 0.1.5 | ✅ | 桥梁、地震分析 |
| **anaStruct** | 1.6.1 | ✅ | 2D框架分析 |
| **sectionproperties** | 3.9.0 | ✅ | 截面属性计算 |
| **concreteproperties** | 0.7.0 | ✅ | 混凝土设计 |
| **gmsh** | 4.14.0 | ✅ | 网格生成 |
| **veux** | 0.0.32 | ✅ | 可视化工具 |

### ❌ 不兼容的库
- **PyNite**: Apple Silicon兼容性问题
- **pycalculix**: NumPy版本冲突  
- **传统OpenSeesPy**: x86_64架构限制

## 🌉 三跨连续梁桥示例

### 模型参数
- **总长度**: 60m (每跨20m)
- **截面**: 箱形截面 (外尺寸1.2m×0.8m, 内尺寸0.8m×0.4m)
- **材料**: C40混凝土 (E=32.5GPa)
- **荷载**: 自重分析 (15,696 N/m)
- **支撑**: 4个铰支点（两端支撑 + 两个墩支撑）

### 分析结果
- 截面积: 0.64 m²
- 惯性矩: 0.047 m⁴
- 生成完整的弯矩图、剪力图和位移图

## 🚀 快速开始

### 1. 创建Conda环境
```bash
conda create -n fem_analysis python=3.11 -y
conda activate fem_analysis
```

### 2. 安装基础包
```bash
conda install -c conda-forge numpy scipy matplotlib pandas jupyter notebook -y
```

### 3. 安装FEM库
```bash
pip install opensees anastruct sectionproperties concreteproperties
```

### 4. 运行分析
```bash
python continuous_bridge_analysis.py
```

## 📊 分析示例

### anaStruct分析
```python
from anastruct import SystemElements

# 创建三跨连续梁
ss = SystemElements()
# ... 详细代码见continuous_bridge_analysis.py
```

### 截面属性计算
```python
import sectionproperties.pre.library.primitive_sections as sections

# 创建箱形截面
outer_rect = sections.rectangular_section(d=0.8, b=1.2)
inner_rect = sections.rectangular_section(d=0.4, b=0.8)
box_section = outer_rect - inner_rect
```

## 📁 文件结构

```
findfem/
├── README.md                           # 项目说明
├── continuous_bridge_analysis.py       # 主分析脚本
├── anastruct_bridge_analysis.png       # 分析结果图
└── requirements.txt                     # Python依赖
```

## 🔧 系统要求

- **操作系统**: macOS (Apple Silicon推荐)
- **Python**: 3.11+
- **Conda**: miniforge3推荐
- **内存**: 8GB+
- **存储**: 2GB+

## 📈 分析能力

### 当前支持
- [x] 静力分析
- [x] 线性分析  
- [x] 2D框架分析
- [x] 截面属性计算
- [x] 混凝土设计
- [x] 可视化输出

### 计划扩展
- [ ] 动力分析
- [ ] 非线性分析
- [ ] 3D复杂结构
- [ ] 时程分析
- [ ] 优化设计

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目基于MIT许可证开源。

## 📞 联系

如有问题或建议，请通过GitHub Issues联系。

---

*专为结构工程师打造的FEM分析环境* 🏗️ 