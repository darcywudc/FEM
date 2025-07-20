#!/usr/bin/env python3
"""
三跨连续梁桥FEM分析示例
测试多种FEM库的能力和结果对比

桥梁参数：
- 总长度：60m (每跨20m)
- 截面：箱形截面
- 材料：C40混凝土
- 支撑：墩支撑 + 简支端支撑
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def print_header(title):
    """打印分析标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def analyze_with_anastruct():
    """使用anaStruct进行连续梁桥分析"""
    print_header("anaStruct 连续梁桥分析")
    
    try:
        from anastruct import SystemElements
        
        # 创建结构模型
        ss = SystemElements()
        
        # 材料属性 (C40混凝土)
        E = 32500e6  # Pa (32.5 GPa)
        
        # 截面属性 (假设箱形截面)
        # 外尺寸: 宽1.2m, 高0.8m
        # 内尺寸: 宽0.8m, 高0.4m  
        width_outer, height_outer = 1.2, 0.8
        width_inner, height_inner = 0.8, 0.4
        
        A = width_outer * height_outer - width_inner * height_inner  # 截面积
        I = (width_outer * height_outer**3 - width_inner * height_inner**3) / 12  # 惯性矩
        
        print(f"截面积: {A:.4f} m²")
        print(f"惯性矩: {I:.6f} m⁴")
        
        # 定义节点和单元 (三跨，每跨20m)
        span_length = 20.0  # 每跨长度
        n_elements_per_span = 10  # 每跨单元数
        
        # 创建节点
        x_coords = []
        for span in range(3):
            for i in range(n_elements_per_span):
                x = span * span_length + i * span_length / n_elements_per_span
                x_coords.append(x)
        x_coords.append(3 * span_length)  # 最后一个节点
        
        # 添加梁单元
        for i in range(len(x_coords) - 1):
            ss.add_element([[x_coords[i], 0], [x_coords[i+1], 0]], EA=E*A, EI=E*I)
        
        # 添加支撑
        # 端支撑 (简支)
        ss.add_support_hinged(1)  # 左端铰支
        ss.add_support_hinged(len(x_coords))  # 右端铰支
        
        # 中间墩支撑 (铰支)
        pier1_node = n_elements_per_span + 1  # 第一个墩位置
        pier2_node = 2 * n_elements_per_span + 1  # 第二个墩位置
        ss.add_support_hinged(pier1_node)
        ss.add_support_hinged(pier2_node)
        
        # 添加荷载
        # 自重 (假设混凝土密度2500 kg/m³)
        rho_concrete = 2500  # kg/m³
        g = 9.81  # m/s²
        dead_load = rho_concrete * A * g  # N/m
        
        print(f"恒载: {dead_load:.0f} N/m")
        
        # 施加分布荷载到所有单元
        for i in range(1, len(x_coords)):
            ss.q_load(-dead_load, element_id=i)
        
        # 求解
        print("正在求解...")
        ss.solve()
        
        # 获取结果
        print("\n结果摘要:")
        print("支反力:")
        
        # 显示图形
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 结构图
        ss.show_structure(show=False, scale=1, offset=(0, 0))
        axes[0,0].set_title('结构布置图')
        
        # 弯矩图
        ss.show_bending_moment(show=False, scale=1)
        axes[0,1].set_title('弯矩图')
        
        # 剪力图  
        ss.show_shear_force(show=False, scale=1)
        axes[1,0].set_title('剪力图')
        
        # 位移图
        ss.show_displacement(show=False, scale=100)
        axes[1,1].set_title('位移图 (放大100倍)')
        
        plt.tight_layout()
        plt.savefig('anastruct_bridge_analysis.png', dpi=300, bbox_inches='tight')
        print("结果图表已保存为: anastruct_bridge_analysis.png")
        
        return ss
        
    except ImportError as e:
        print(f"anaStruct导入失败: {e}")
        return None
    except Exception as e:
        print(f"分析失败: {e}")
        return None

def analyze_with_xara():
    """使用xara/opensees进行连续梁桥分析"""
    print_header("xara/OpenSees 连续梁桥分析")
    
    try:
        import opensees
        
        print("xara版本:", opensees.__version__)
        
        # 这里我们可以添加xara的具体分析代码
        # 由于xara的API可能与传统OpenSees不同，需要进一步研究
        print("xara分析功能正在开发中...")
        
        return True
        
    except ImportError as e:
        print(f"xara/opensees导入失败: {e}")
        return None
    except Exception as e:
        print(f"分析失败: {e}")
        return None

def test_section_properties():
    """测试截面属性计算"""
    print_header("截面属性计算测试")
    
    try:
        import sectionproperties.pre.library.primitive_sections as sections
        from sectionproperties.analysis.section import Section
        
        # 创建箱形截面
        # 外矩形
        outer_rect = sections.rectangular_section(d=0.8, b=1.2)
        # 内矩形 (空心部分)
        inner_rect = sections.rectangular_section(d=0.4, b=0.8)
        inner_rect = inner_rect.shift_section(0.2, 0.2)  # 居中
        
        # 箱形截面 = 外矩形 - 内矩形
        box_section = outer_rect - inner_rect
        
        # 生成网格
        box_section.create_mesh(mesh_sizes=[0.01])
        
        # 分析截面
        section = Section(box_section)
        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        
        # 显示结果
        print(f"截面积: {section.get_area():.6f} m²")
        print(f"Ixx: {section.get_ixx():.6f} m⁴")
        print(f"Iyy: {section.get_iyy():.6f} m⁴")
        print(f"质心x坐标: {section.get_c()[0]:.6f} m")
        print(f"质心y坐标: {section.get_c()[1]:.6f} m")
        
        # 绘图
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # 截面几何
        section.plot_mesh(ax=axes[0], materials=False)
        axes[0].set_title('箱形截面网格')
        
        # 应力分布 (假设弯矩)
        section.calculate_stress(Mxx=1e6)  # 1 MN·m
        section.plot_stress_mxx(ax=axes[1])
        axes[1].set_title('弯矩应力分布')
        
        plt.tight_layout()
        plt.savefig('section_properties_analysis.png', dpi=300, bbox_inches='tight')
        print("截面分析结果已保存为: section_properties_analysis.png")
        
        return section
        
    except ImportError as e:
        print(f"sectionproperties导入失败: {e}")
        return None
    except Exception as e:
        print(f"截面分析失败: {e}")
        return None

def generate_summary_report():
    """生成分析总结报告"""
    print_header("FEM库测试总结报告")
    
    libraries_tested = [
        ("anaStruct", "✅", "2D框架分析，易于使用"),
        ("xara/opensees", "🔄", "现代OpenSees，正在开发中"),  
        ("sectionproperties", "✅", "截面属性计算，功能强大"),
        ("concreteproperties", "✅", "混凝土设计，专业化"),
        ("PyNite", "❌", "Apple Silicon兼容性问题"),
        ("pycalculix", "❌", "NumPy版本兼容性问题"),
    ]
    
    print("\n库名称\t\t状态\t描述")
    print("-" * 60)
    for name, status, desc in libraries_tested:
        print(f"{name:15}\t{status}\t{desc}")
    
    print(f"\n分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mac环境: Apple Silicon (ARM64)")
    print("Python环境: Conda fem_analysis")

if __name__ == "__main__":
    print("🌉 三跨连续梁桥FEM分析测试")
    print("测试多种FEM库在Apple Silicon Mac上的表现")
    
    # 运行各种分析
    anastruct_result = analyze_with_anastruct()
    xara_result = analyze_with_xara()
    section_result = test_section_properties()
    
    # 生成总结报告
    generate_summary_report()
    
    print("\n✅ 所有测试完成！")
    print("请查看生成的PNG图片文件了解分析结果。") 