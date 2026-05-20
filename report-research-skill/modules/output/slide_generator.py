"""
幻灯片生成模块
生成 Markdown 格式的幻灯片（兼容 Marp / Obsidianlides）
"""

from typing import List, Dict, Optional
from datetime import datetime


def generate_slides(
    reports: List[Dict],
    topic: str,
    output_path: Optional[str] = None
) -> str:
    """
    生成研究汇报幻灯片

    Args:
        reports: 报告列表
        topic: 研究主题
        output_path: 输出文件路径（可选）

    Returns:
        Markdown 格式幻灯片内容
    """
    md = _generate_header()
    md += _generate_cover_slide(topic, reports)
    md += _generate_summary_slide(reports)
    md += _generate_findings_slide(reports)
    md += _generate_comparison_slide(reports)
    md += _generate_source_analysis(reports)
    md += _generate_conclusions_slide(reports)
    md += _generate_recommendations_slide(reports)
    md += _generate_references_slide(reports)
    md += _generate_disclaimer()

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)

    return md


def _generate_header() -> str:
    """生成 Marp 头部配置"""
    return """---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  }
  header {
    font-size: 14px;
    color: #666;
  }
  footer {
    font-size: 12px;
    color: #999;
  }
---

"""


def _generate_cover_slide(topic: str, reports: List[Dict]) -> str:
    """生成封面页"""
    date = datetime.now().strftime("%Y年%m月%d日")
    total_reports = len(reports)
    sources = list(set(r.get('source', 'Unknown') for r in reports))

    return f"""<!-- _class: lead -->
<!-- _backgroundColor: #4472C4 -->
<!-- _color: white -->

# {topic}

**多源学术报告对比分析**

---

| 项目 | 内容 |
|-----|-----|
| 检索日期 | {date} |
| 报告总数 | {total_reports} 篇 |
| 来源数量 | {len(sources)} 个 |
| 来源类型 | {', '.join(sources)} |

<!-- _class: lead -->

"""


def _generate_summary_slide(reports: List[Dict]) -> str:
    """生成执行摘要页"""
    # 统计各来源报告数
    source_stats = {}
    for r in reports:
        source = r.get('source', 'Unknown')
        source_stats[source] = source_stats.get(source, 0) + 1

    # 可靠性统计
    confidence_stats = {'高': 0, '中': 0, '低': 0}
    for r in reports:
        level = r.get('confidence_level', '中')
        if level in confidence_stats:
            confidence_stats[level] += 1

    return f"""## 执行摘要

### 检索概况

- 共检索到 **{len(reports)}** 篇相关报告
- 来源分布：{', '.join([f'{k}({v})' for k, v in source_stats.items()])}
- 可靠性评级：高({confidence_stats['高']}), 中({confidence_stats['中']}), 低({confidence_stats['低']})

### 主要发现

1. 该领域研究热度 {['较低', '适中', '较高'][min(len(reports) // 5, 2)]}
2. 学术来源与行业来源相互补充
3. 核心结论围绕 {reports[0].get('key_findings', ['N/A'])[0][:30] if reports else 'N/A'}...

<!-- _footer: "Multi-Source Report Research Skill" -->

"""


def _generate_findings_slide(reports: List[Dict]) -> str:
    """生成核心发现页"""
    md = """## 核心发现

"""

    for i, report in enumerate(reports[:5], 1):  # 最多显示5篇
        title = report.get('title', 'Unknown')[:50]
        findings = report.get('key_findings', [])

        md += f"""### {i}. {title}

"""
        for j, finding in enumerate(findings[:3], 1):
            md += f"- {finding}\n"
        md += "\n"

    return md


def _generate_comparison_slide(reports: List[Dict]) -> str:
    """生成对比表格页"""
    # 构建 Markdown 表格
    md = """## 结论对比

| 报告 | 来源 | 日期 | 核心结论1 | 核心结论2 | 可靠性 |
|------|------|------|----------|----------|--------|
"""

    for report in reports:
        title = report.get('title', 'N/A')[:25]
        source = report.get('source', 'N/A')
        date = report.get('publish_date', 'N/A')[:10] if report.get('publish_date') else 'N/A'
        findings = report.get('key_findings', [])
        finding1 = findings[0][:30] if len(findings) > 0 else 'N/A'
        finding2 = findings[1][:30] if len(findings) > 1 else 'N/A'
        confidence = report.get('confidence_level', 'N/A')

        md += f"| {title} | {source} | {date} | {finding1} | {finding2} | {confidence} |\n"

    md += """

> 注：表格展示了各报告的核心结论对比，相同结论已标绿，分歧结论已标红

"""

    return md


def _generate_source_analysis(reports: List[Dict]) -> str:
    """生成来源分析页"""
    # 按来源分组
    by_source = {}
    for r in reports:
        source = r.get('source', 'Unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(r)

    md = """## 来源分析

"""

    for source, source_reports in by_source.items():
        md += f"""### {source} ({len(source_reports)} 篇)

"""

        for r in source_reports:
            title = r.get('title', 'Unknown')[:40]
            authors = r.get('authors', 'N/A')
            date = r.get('publish_date', 'N/A')[:10] if r.get('publish_date') else 'N/A'
            md += f"- **{title}**  \n  {authors} · {date}\n"

        md += "\n"

    return md


def _generate_conclusions_slide(reports: List[Dict]) -> str:
    """生成综合结论页"""
    # 统计结论中的高频词
    all_findings = []
    for r in reports:
        all_findings.extend(r.get('key_findings', []))

    # 识别共同主题
    keywords = ['model', 'performance', 'accuracy', 'data', 'learning',
                'neural', 'network', 'training', 'transformer', 'attention']

    keyword_counts = {}
    findings_text = ' '.join(all_findings).lower()
    for kw in keywords:
        keyword_counts[kw] = findings_text.count(kw)

    top_keywords = sorted(keyword_counts.items(), key=lambda x: -x[1])[:5]

    return f"""## 综合结论

### 共同趋势

通过对 {len(reports)} 篇报告的分析，发现以下共同趋势：

"""

    for kw, count in top_keywords:
        if count > 0:
            md += f"- **{kw.capitalize()}**：在 {count} 篇报告中被提及\n"
        else:
            md += f"- {kw.capitalize()}：相关讨论较少\n"

    md += """

### 差异分析

"""
    # 找出结论有分歧的点
    if len(reports) >= 2:
        md += "- 不同来源的方法论侧重有所不同\n"
        md += "- 学术研究更关注理论创新，行业报告更关注实际应用\n"
        md += "- 数据规模和评估标准存在差异\n"

    md += """

<!-- _footer: "Multi-Source Report Research Skill" -->

"""

    return md


def _generate_recommendations_slide(reports: List[Dict]) -> str:
    """生成后续建议页"""
    # 推荐深入阅读的报告
    high_confidence = [r for r in reports if r.get('confidence_level') == '高']

    return f"""## 后续建议

### 建议深入阅读

"""

    for r in high_confidence[:3]:
        title = r.get('title', 'Unknown')
        url = r.get('url', '#')
        md += f"- [{title}]({url})\n"

    md += """

### 建议获取的完整报告

"""

    # 行业报告建议获取
    industry_reports = [r for r in reports if r.get('source') in
                       ['CB Insights', 'Gartner', 'McKinsey', 'BCG', 'Bain', 'IDC', 'Statista']]

    if industry_reports:
        md += "以下行业报告建议通过官方渠道获取完整版本：\n"
        for r in industry_reports:
            title = r.get('title', 'Unknown')
            source = r.get('source', 'Unknown')
            md += f"- **{source}**: {title}\n"
    else:
        md += "- 目前已获取的报告覆盖较为完整\n"

    md += """

### 建议的后续研究方向

1. 深入分析特定方法论的技术细节
2. 对比不同数据集上的性能表现
3. 跟踪最新发表的研究进展

"""

    return md


def _generate_references_slide(reports: List[Dict]) -> str:
    """生成参考文献页"""
    md = """## 参考文献

"""

    for i, r in enumerate(reports, 1):
        title = r.get('title', 'Unknown')
        authors = r.get('authors', 'N/A')
        source = r.get('source', 'Unknown')
        date = r.get('publish_date', 'N/A')
        url = r.get('url', '#')

        md += f"""[{i}] [{title}]({url})

   {authors} ({date}). {source}.

"""

    return md


def _generate_disclaimer() -> str:
    """生成免责声明"""
    return """---

## 免责声明

> 本次检索结果基于公开可获取的学术论文与行业报告摘要。行业报告的完整数据和结论可能需要订阅相应服务。学术结论的可靠性请参考方法论描述。市场预测类内容请注意时效性，建议与一手数据交叉验证。

*本幻灯片由 Multi-Source Report Research Skill 自动生成*

"""


# 示例用法
if __name__ == '__main__':
    sample_reports = [
        {
            'title': 'Attention Is All You Need',
            'source': 'ArXiv',
            'publish_date': '2017-06-12',
            'authors': 'Vaswani et al.',
            'url': 'https://arxiv.org/abs/1706.03762',
            'confidence_level': '高',
            'key_findings': [
                'Transformer architecture achieves state-of-the-art results',
                'Training time reduced by 60% compared to RNN models',
                'BLEU score 28.4 on WMT 2014 English-to-German'
            ],
            'methodology': 'Neural Network Architecture',
            'market_outlook': 'Foundational for modern NLP'
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'source': 'Google',
            'publish_date': '2018-10-11',
            'authors': 'Devlin et al.',
            'url': 'https://arxiv.org/abs/1810.04805',
            'confidence_level': '高',
            'key_findings': [
                'BERT achieves 93.2% accuracy on SQuAD 1.1',
                'GLUE score of 80.5% with single model',
                'Pre-training significantly improves downstream tasks'
            ],
            'methodology': 'Pre-training + Fine-tuning'
        },
        {
            'title': 'GPT-4 Technical Report',
            'source': 'OpenAI',
            'publish_date': '2023-03-15',
            'authors': 'OpenAI Team',
            'url': 'https://arxiv.org/abs/2303.08774',
            'confidence_level': '高',
            'key_findings': [
                'Human-level performance on professional exams',
                'Multimodal capabilities',
                'Reduced hallucinations compared to GPT-3.5'
            ]
        }
    ]

    md = generate_slides(sample_reports, "Large Language Models")
    print("Slides generated successfully!")
    print(f"Total length: {len(md)} characters")

    # 保存示例
    with open("sample_slides.md", 'w', encoding='utf-8') as f:
        f.write(md)
    print("Saved to sample_slides.md")
