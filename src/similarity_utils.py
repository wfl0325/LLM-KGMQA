# src/similarity_utils.py
from ..smiliarity import bert_cos_similarity
def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本之间的BERT余弦相似度。
    这是一个包装函数，用于隔离具体的实现。
    """
    return bert_cos_similarity(text1, text2)