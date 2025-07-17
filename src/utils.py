# src/utils.py
import json
import logging
from typing import List, Dict, Tuple


def load_json_file(file_path: str) -> Dict:
    """安全地加载JSON文件。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Error: Data file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error: Could not decode JSON from {file_path}")
        return {}


def group_paths_by_relation(paths: List[Tuple[str, str, str]]) -> List[str]:
    """
    将三元组列表按头实体和关系进行分组，格式化为 "A->r->B、C" 的字符串。

    Args:
        paths (List[Tuple[str, str, str]]): e.g., [('A', 'r1', 'B'), ('A', 'r1', 'C')]

    Returns:
        List[str]: e.g., ['A->r1->B、C']
    """
    if not paths:
        return []

    grouped = {}
    for head, rel, tail in paths:
        key = (head, rel)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(tail)

    formatted_paths = []
    for (head, rel), tails in grouped.items():
        tails_str = "、".join(tails)
        formatted_paths.append(f"{head}->{rel}->{tails_str}")

    return formatted_paths


def parse_path_string(path_str: str) -> Tuple[str, str, List[str]]:
    """
    解析 "A->r->B、C" 格式的字符串。
    """
    parts = path_str.split('->')
    if len(parts) != 3:
        logging.warning(f"Could not parse path string: {path_str}")
        return "", "", []
    head, rel, tails_str = parts
    tails = tails_str.split('、')
    return head, rel, tails