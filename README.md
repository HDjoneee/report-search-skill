# Multi-Source Report Research Skill

多源学术/行业报告检索与对比分析工具。输入研究主题，自动从 ArXiv、Google Scholar、Semantic Scholar 及行业智库检索报告，解析 PDF，提取核心结论，生成对比表格和可视化报告。

## 功能特性

### 核心功能

- **多源并行检索**：ArXiv、Semantic Scholar、Google Scholar、CB Insights、Gartner、McKinsey 等
- **PDF 自动解析**：提取报告正文或摘要
- **结构化结论提取**：使用 AI 提取关键发现、研究方法、数据来源
- **对比表格生成**：带颜色标注（一致=绿，分歧=红，缺失=灰）

### 扩展功能（可选）

- **关键词提取**：`modules/analyzer/keywords.py` - TF-IDF 统计
- **Excel 导出**：`modules/output/excel_exporter.py` - 多 Sheet 结构化导出
- **可视化图表**：`modules/output/visualizer.py` - 柱状图、饼图、折线图、热力图
- **幻灯片生成**：`modules/output/slide_generator.py` - Marp/Obsidian 兼容 Markdown

## 目录结构

```
report-research-skill/
├── atope.json                      # Skill 元数据配置
├── skill.md                        # Skill 核心逻辑定义
├── requirements.txt                # Python 依赖
├── README.md                       # 本文件
└── modules/
    ├── analyzer/
    │   └── keywords.py             # 关键词提取
    └── output/
        ├── excel_exporter.py       # Excel 导出
        ├── visualizer.py           # 可视化图表
        └── slide_generator.py      # 幻灯片生成
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/report-research-skill.git
cd report-research-skill

# 安装依赖
pip install -r requirements.txt
```

### 依赖

| 包           | 版本     | 用途                      |
| ------------ | -------- | ------------------------- |
| matplotlib   | >=3.7.0  | 可视化图表                |
| openpyxl     | >=3.1.0  | Excel 导出                |
| requests     | >=2.28.0 | HTTP 请求                 |
| scikit-learn | >=1.3.0  | TF-IDF 关键词提取（可选） |

## 使用方法

### 作为 Claude Code Skill 使用

将 `report-research-skill` 文件夹放入 Claude Code 的 skills 目录，即可在对话中通过关键词触发：

- "检索 [主题] 相关报告"
- "多源对比分析 [主题]"
- "生成可视化图表"
- "导出 Excel"

### 作为 Python 模块使用

```python
from modules.output.excel_exporter import export_to_excel
from modules.output.visualizer import generate_all_charts
from modules.output.slide_generator import generate_slides
from modules.analyzer.keywords import extract_keywords

# 示例报告数据
reports = [
    {
        'title': 'Attention Is All You Need',
        'source': 'ArXiv',
        'publish_date': '2017-06-12',
        'authors': 'Vaswani et al.',
        'url': 'https://arxiv.org/abs/1706.03762',
        'confidence_level': '高',
        'key_findings': [
            'Transformer 架构达到 SOTA',
            '训练时间减少 60%',
            'BLEU 分数 28.4'
        ],
        'methodology': 'Neural Network'
    }
]

# 导出 Excel
export_to_excel(reports, "Transformer Models", "output.xlsx")

# 生成图表
charts = generate_all_charts(reports, "Transformer Models", "./charts")

# 生成幻灯片
slides = generate_slides(reports, "Transformer Models", "slides.md")

# 提取关键词
keywords = extract_keywords(reports, top_n=20)
```

## 模块说明

### keywords.py

提取报告中的高频关键词：

```python
from modules.analyzer.keywords import extract_keywords, generate_keyword_markdown

result = extract_keywords(reports, top_n=20)
md = generate_keyword_markdown(result, "研究主题")
```

### excel_exporter.py

导出结构化 Excel 文件，包含 3 个 Sheet：

| Sheet      | 内容                         |
| ---------- | ---------------------------- |
| 报告元数据 | 标题、来源、日期、作者、链接 |
| 结论对比   | 核心结论、方法论、市场展望   |
| 统计分析   | 来源分布、可靠性评级占比     |

### visualizer.py

生成 5 种可视化图表：

```python
from modules.output.visualizer import generate_all_charts, generate_markdown_with_images

charts = generate_all_charts(reports, topic, output_dir="./charts")
md = generate_markdown_with_images(charts, topic)
```

| 图表         | 说明                   |
| ------------ | ---------------------- |
| findings_bar | 核心结论数量对比柱状图 |
| source_pie   | 来源分布饼图           |
| timeline     | 发布时间折线图         |
| confidence   | 可靠性评级分布         |
| comparison   | 关键词频率对比         |

### slide_generator.py

生成 Marp 格式的 Markdown 幻灯片：

```bash
# 幻灯片包含以下页面
1. 封面页
2. 执行摘要
3. 核心发现
4. 结论对比表格
5. 来源分析
6. 综合结论
7. 后续建议
8. 参考文献
9. 免责声明
```

## 工作流程

```
用户输入主题
    ↓
Step 1: 澄清检索需求（来源/时间/数量/格式）
    ↓
Step 2: 多源并行检索（ArXiv + Semantic Scholar + 行业智库）
    ↓
Step 3: PDF 下载与解析
    ↓
Step 4: 核心结论提取（AI 结构化提取）
    ↓
Step 5: 对比表格生成（颜色标注差异）
    ↓
Step 6: 最终交付（摘要 + 表格 + 参考文献 + 建议）
    ↓
[可选] 扩展功能：关键词提取 / Excel / 可视化 / 幻灯片
```

## 质量控制

- 至少覆盖 3 个不同来源
- 学术 + 行业来源至少各 1 个
- 每篇报告至少提取 3 个含具体数据的结论
- 区分学术结论与行业预测
- 无编造结论（无法提取时标注"信息不足"）

## 免责声明

> 本次检索结果基于公开可获取的学术论文与行业报告摘要。行业报告的完整数据和结论可能需要订阅相应服务。学术结论的可靠性请参考方法论描述。市场预测类内容请注意时效性，建议与一手数据交叉验证。

## License

MIT License

## Contributing

欢迎提交 Issue 和 Pull Request！
