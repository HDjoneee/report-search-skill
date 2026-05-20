"""
关键词提取模块
使用 TF-IDF 从报告摘要/结论中提取高频关键词
"""

import re
from collections import Counter
from typing import List, Dict, Tuple

# 英文停用词
ENGLISH_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
    'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
    'then', 'once', 'if', 'because', 'until', 'while', 'although', 'though',
    'after', 'before', 'above', 'below', 'between', 'into', 'through',
    'during', 'under', 'again', 'further', 'then', 'once', 'any', 'about',
    'show', 'shown', 'study', 'result', 'paper', 'method', 'approach',
    'use', 'used', 'using', 'based', 'propose', 'proposed', 'present',
    'presented', 'demonstrate', 'demonstrated', 'find', 'found', 'show',
    'however', 'therefore', 'thus', 'hence', 'conclusion', 'conclusions',
    'abstract', 'introduction', 'related', 'work', 'research', 'analysis'
}

# 中文停用词
CHINESE_STOPWORDS = {
    '的', '了', '和', '是', '在', '我', '有', '个', '人', '这',
    '不', '也', '就', '都', '要', '会', '能', '对', '于', '与',
    '从', '到', '以', '及', '等', '其', '所', '为', '但', '可',
    '或', '如', '因', '由', '该', '当', '此', '中', '将', '被',
    '已', '被', '进行', '表明', '表明', '本文', '研究', '方法',
    '结果', '结论', '通过', '使用', '基于', '提出', '显示'
}


def tokenize(text: str) -> List[str]:
    """将文本分词"""
    if not text:
        return []

    # 英文：转小写，提取单词
    english_words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    # 中文：按字符分词（简单实现）
    chinese_chars = list(text)

    return english_words + chinese_chars


def remove_stopwords(tokens: List[str], lang: str = 'en') -> List[str]:
    """去除停用词"""
    if lang == 'en':
        stopwords = ENGLISH_STOPWORDS
    else:
        stopwords = CHINESE_STOPWORDS

    return [t for t in tokens if t not in stopwords and len(t) > 1]


def calculate_tf(texts: List[str], top_n: int = 20) -> List[Tuple[str, float]]:
    """
    计算词频（TF）

    Args:
        texts: 文本列表（如摘要/结论列表）
        top_n: 返回前 N 个关键词

    Returns:
        [(关键词, TF值), ...] 按频率降序排列
    """
    all_tokens = []
    for text in texts:
        tokens = tokenize(text)
        filtered = remove_stopwords(tokens)
        all_tokens.extend(filtered)

    counter = Counter(all_tokens)
    total = len(all_tokens)

    # 计算 TF 值并排序
    tf_scores = [(word, count / total) for word, count in counter.most_common(top_n)]
    return tf_scores


def extract_keywords(reports: List[Dict], top_n: int = 20) -> Dict:
    """
    从报告列表中提取关键词

    Args:
        reports: 报告字典列表，每个包含 title, key_findings, abstract 等字段
        top_n: 返回前 N 个关键词

    Returns:
        {
            'keywords': [(关键词, 频率), ...],
            'word_cloud_data': [(word, count), ...],  # 词云格式
            'total_words': int
        }
    """
    texts = []

    for report in reports:
        # 提取标题
        if 'title' in report:
            texts.append(report['title'])

        # 提取结论
        if 'key_findings' in report and isinstance(report['key_findings'], list):
            texts.extend(report['key_findings'])

        # 提取摘要
        if 'abstract' in report:
            texts.append(report['abstract'])

    # 计算 TF
    keywords = calculate_tf(texts, top_n)

    # 生成词云数据
    word_cloud_data = [(word, int(freq * 1000)) for word, freq in keywords]

    return {
        'keywords': keywords,
        'word_cloud_data': word_cloud_data,
        'total_words': len(keywords)
    }


def generate_keyword_markdown(keywords_data: Dict, topic: str) -> str:
    """
    生成关键词 Markdown 格式输出

    Args:
        keywords_data: extract_keywords 的返回值
        topic: 研究主题

    Returns:
        Markdown 格式的字符串
    """
    keywords = keywords_data['keywords']

    md = f"## 关键词提取结果：{topic}\n\n"
    md += "| 排名 | 关键词 | TF 值 |\n"
    md += "|------|--------|-------|\n"

    for i, (word, tf) in enumerate(keywords, 1):
        md += f"| {i} | {word} | {tf:.4f} |\n"

    md += f"\n**共提取 {len(keywords)} 个关键词**\n"

    return md


# 示例用法
if __name__ == '__main__':
    sample_reports = [
        {
            'title': 'Attention Is All You Need',
            'key_findings': [
                'Transformer architecture achieves state-of-the-art results',
                'Training time reduced by 60% compared to RNN models',
                'Achieved 28.4 BLEU score on WMT 2014 English-to-German'
            ]
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'key_findings': [
                'BERT achieves 93.2% accuracy on SQuAD 1.1',
                'GLUE score of 80.5% with single model',
                'Pre-training significantly improves downstream tasks'
            ]
        }
    ]

    result = extract_keywords(sample_reports, top_n=10)
    print(generate_keyword_markdown(result, "Transformer Models"))
