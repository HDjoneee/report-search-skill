"""
可视化图表模块
使用 matplotlib 生成对比图表
"""

import matplotlib
matplotlib.use('Agg')  # 非交互式后端

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from typing import List, Dict, Optional, Tuple
from collections import Counter
import base64
from io import BytesIO
import os

# 设置中文字体支持
def setup_chinese_font():
    """设置中文字体"""
    # 尝试多种中文字体
    font_paths = [
        # Windows
        'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        # Linux
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            font_manager.fontManager.addfont(font_path)
            prop = font_manager.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = prop.get_name()
            return True

    # 如果没有找到中文字体，使用 sans-serif
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    return False

setup_chinese_font()

# 设置颜色主题
COLORS = {
    'primary': '#4472C4',
    'secondary': '#ED7D31',
    'accent': '#A5A5A5',
    'success': '#70AD47',
    'warning': '#FFC000',
    'danger': '#FF6B6B',
    'grid': '#E0E0E0'
}

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def generate_bar_chart(
    reports: List[Dict],
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> str:
    """
    生成结论数量对比柱状图

    Args:
        reports: 报告列表
        output_path: 输出路径（可选）
        figsize: 图形大小

    Returns:
        PNG 图片的 Base64 编码或文件路径
    """
    titles = [r.get('title', 'Unknown')[:30] for r in reports]
    findings_counts = [len(r.get('key_findings', [])) for r in reports]

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.bar(range(len(titles)), findings_counts, color=COLORS['primary'])

    # 添加数值标签
    for bar, count in zip(bars, findings_counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )

    ax.set_xticks(range(len(titles)))
    ax.set_xticklabels(titles, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Number of Key Findings', fontsize=11)
    ax.set_title('Key Findings Count by Report', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(findings_counts) + 2)
    ax.grid(axis='y', alpha=0.3, color=COLORS['grid'])

    plt.tight_layout()

    return save_or_return_figure(fig, output_path)


def generate_pie_chart(
    reports: List[Dict],
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    生成来源分布饼图

    Args:
        reports: 报告列表
        output_path: 输出路径（可选）
        figsize: 图形大小

    Returns:
        PNG 图片的 Base64 编码或文件路径
    """
    source_counts = Counter(r.get('source', 'Unknown') for r in reports)

    fig, ax = plt.subplots(figsize=figsize)

    colors = list(COLORS.values())[:len(source_counts)]
    wedges, texts, autotexts = ax.pie(
        source_counts.values(),
        labels=source_counts.keys(),
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.02] * len(source_counts),
        shadow=False,
        startangle=90
    )

    # 美化文本
    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    ax.set_title('Report Sources Distribution', fontsize=14, fontweight='bold')

    plt.tight_layout()

    return save_or_return_figure(fig, output_path)


def generate_timeline_chart(
    reports: List[Dict],
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 6)
) -> str:
    """
    生成时间分布折线图

    Args:
        reports: 报告列表
        output_path: 输出路径（可选）
        figsize: 图形大小

    Returns:
        PNG 图片的 Base64 编码或文件路径
    """
    # 统计每月发布数量
    date_counts = Counter()
    for report in reports:
        date_str = report.get('publish_date', '')
        if date_str:
            # 提取年月
            if len(date_str) >= 7:
                year_month = date_str[:7]
                date_counts[year_month] += 1

    if not date_counts:
        # 如果没有有效日期，生成提示图
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, 'No date information available',
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return save_or_return_figure(fig, output_path)

    # 排序日期
    sorted_dates = sorted(date_counts.items())

    fig, ax = plt.subplots(figsize=figsize)

    dates = [d[0] for d in sorted_dates]
    counts = [d[1] for d in sorted_dates]

    ax.plot(dates, counts, marker='o', linewidth=2, markersize=8,
            color=COLORS['primary'], markerfacecolor=COLORS['secondary'])

    # 填充区域
    ax.fill_between(dates, counts, alpha=0.3, color=COLORS['primary'])

    # 添加数值标签
    for x, y in zip(dates, counts):
        ax.annotate(str(y), (x, y), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=10)

    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Number of Reports', fontsize=11)
    ax.set_title('Report Publication Timeline', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3, color=COLORS['grid'])
    ax.set_ylim(0, max(counts) + 1)

    plt.tight_layout()

    return save_or_return_figure(fig, output_path)


def generate_confidence_chart(
    reports: List[Dict],
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (8, 6)
) -> str:
    """
    生成可靠性评级分布柱状图

    Args:
        reports: 报告列表
        output_path: 输出路径（可选）
        figsize: 图形大小

    Returns:
        PNG 图片的 Base64 编码或文件路径
    """
    confidence_counts = Counter(r.get('confidence_level', '未知') for r in reports)

    # 确保顺序
    order = ['高', '中', '低', '高', 'Medium', 'Low', 'Unknown', '未知']
    sorted_items = sorted(confidence_counts.items(), key=lambda x: order.index(x[1]) if x[1] in order else 99)

    labels = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    # 颜色映射
    color_map = {'高': COLORS['success'], '中': COLORS['warning'], '低': COLORS['danger']}
    colors = [color_map.get(label, COLORS['primary']) for label in labels]

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.bar(labels, counts, color=colors)

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )

    ax.set_ylabel('Number of Reports', fontsize=11)
    ax.set_title('Confidence Level Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, color=COLORS['grid'])

    # 添加图例
    legend_patches = [
        mpatches.Patch(color=COLORS['success'], label='High'),
        mpatches.Patch(color=COLORS['warning'], label='Medium'),
        mpatches.Patch(color=COLORS['danger'], label='Low')
    ]
    ax.legend(handles=legend_patches, loc='upper right')

    plt.tight_layout()

    return save_or_return_figure(fig, output_path)


def generate_comparison_matrix(
    reports: List[Dict],
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 8)
) -> str:
    """
    生成多维度对比矩阵热力图

    Args:
        reports: 报告列表
        output_path: 输出路径（可选）
        figsize: 图形大小

    Returns:
        PNG 图片的 Base64 编码或文件路径
    """
    # 提取每个报告的结论关键词
    report_labels = [r.get('title', 'Unknown')[:25] for r in reports]

    # 统计关键词频率
    all_findings_text = ' '.join([
        ' '.join(r.get('key_findings', [])) for r in reports
    ])

    # 简单统计方法词
    method_keywords = ['neural', 'transformer', 'attention', 'deep', 'learning',
                       'ml', 'ai', 'data', 'analysis', 'model', 'network']
    method_counts = {kw: all_findings_text.lower().count(kw) for kw in method_keywords}

    # 选择前10个关键词
    top_methods = sorted(method_counts.items(), key=lambda x: -x[1])[:10]

    fig, ax = plt.subplots(figsize=figsize)

    # 创建数据矩阵
    data = []
    for report in reports:
        report_text = ' '.join(report.get('key_findings', [])).lower()
        row = [report_text.count(m[0]) for m in top_methods]
        data.append(row)

    # 绘制热力图（使用条形图代替）
    x = range(len(top_methods))
    width = 0.8 / len(reports)

    for i, (report, row) in enumerate(zip(report_labels, data)):
        offset = (i - len(reports) / 2 + 0.5) * width
        ax.bar([xi + offset for xi in x], row, width, label=report)

    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in top_methods], rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title('Method/Keyword Frequency Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(axis='y', alpha=0.3, color=COLORS['grid'])

    plt.tight_layout()

    return save_or_return_figure(fig, output_path)


def save_or_return_figure(fig, output_path: Optional[str]) -> str:
    """保存图片或返回 Base64 编码"""
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return output_path
    else:
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        plt.close(fig)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')


def generate_all_charts(
    reports: List[Dict],
    topic: str,
    output_dir: str = "."
) -> Dict[str, str]:
    """
    生成所有图表

    Args:
        reports: 报告列表
        topic: 研究主题
        output_dir: 输出目录

    Returns:
        {'chart_name': 'file_path_or_base64', ...}
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_topic = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in topic)

    charts = {}

    charts['findings_bar'] = generate_bar_chart(
        reports,
        os.path.join(output_dir, f"{safe_topic}_findings_bar.png")
    )

    charts['source_pie'] = generate_pie_chart(
        reports,
        os.path.join(output_dir, f"{safe_topic}_source_pie.png")
    )

    charts['timeline'] = generate_timeline_chart(
        reports,
        os.path.join(output_dir, f"{safe_topic}_timeline.png")
    )

    charts['confidence'] = generate_confidence_chart(
        reports,
        os.path.join(output_dir, f"{safe_topic}_confidence.png")
    )

    charts['comparison'] = generate_comparison_matrix(
        reports,
        os.path.join(output_dir, f"{safe_topic}_comparison.png")
    )

    return charts


def generate_markdown_with_images(charts: Dict[str, str], topic: str) -> str:
    """
    生成带有图片引用的 Markdown

    Args:
        charts: generate_all_charts 返回的字典
        topic: 研究主题

    Returns:
        Markdown 格式字符串
    """
    md = f"## 可视化分析：{topic}\n\n"

    md += "### 核心结论数量对比\n"
    md += f"![核心结论对比]({charts.get('findings_bar', '')}){{ width=80% }}\n\n"

    md += "### 来源分布\n"
    md += f"![来源分布]({charts.get('source_pie', '')}){{ width=60% }}\n\n"

    md += "### 发布时间线\n"
    md += f"![时间线]({charts.get('timeline', '')}){{ width=80% }}\n\n"

    md += "### 可靠性分布\n"
    md += f"![可靠性分布]({charts.get('confidence', '')}){{ width=50% }}\n\n"

    md += "### 关键词对比\n"
    md += f"![关键词对比]({charts.get('comparison', '')}){{ width=80% }}\n\n"

    return md


# 示例用法
if __name__ == '__main__':
    sample_reports = [
        {
            'title': 'Attention Is All You Need',
            'source': 'ArXiv',
            'publish_date': '2017-06-12',
            'confidence_level': '高',
            'key_findings': [
                'Transformer architecture achieves state-of-the-art',
                'Training time reduced by 60%',
                'BLEU score 28.4 on WMT 2014'
            ]
        },
        {
            'title': 'BERT Pre-training',
            'source': 'Google',
            'publish_date': '2018-10-11',
            'confidence_level': '高',
            'key_findings': [
                'BERT achieves 93.2% accuracy',
                'GLUE score 80.5%',
                'Pre-training improves downstream tasks'
            ]
        },
        {
            'title': 'GPT-4 Technical Report',
            'source': 'OpenAI',
            'publish_date': '2023-03-15',
            'confidence_level': '高',
            'key_findings': [
                'Human-level performance on exams',
                'Multimodal capabilities',
                'Reduced hallucinations'
            ]
        }
    ]

    charts = generate_all_charts(sample_reports, "Large Language Models")
    print("Charts generated:")
    for name, path in charts.items():
        print(f"  {name}: {path}")

    md = generate_markdown_with_images(charts, "Large Language Models")
    print("\nMarkdown:\n", md[:500])
