# 重新定义计算 CRA@n 的代码

# 定义疾病列表和目标疾病
disease_list = ['慢性荨麻疹', '急性荨麻疹', '人工性荨麻疹', '荨麻疹', '荨麻疹和血管性水肿', '血清性荨麻疹', '胆碱能性荨麻疹', '色素性荨麻疹', '寒性荨麻疹', '热性荨麻疹', '接触性荨麻疹', '寒冷性荨麻疹', '过敏性荨麻疹', '荨麻疹性血管炎', '荨麻疹型药疹', '疱疹样湿疹', '疱疹样皮炎', '湿疹', '自体敏感性湿疹', '多形红斑样皮疹', '成人痒疹', '钱币状湿疹', '神经性皮炎', '麻疹样红斑型药疹', '皮肤利什曼病', '传染性湿疹样皮炎', '糙皮病样皮疹', '红皮病', '鲍温样丘疹病', '过敏性湿疹', '迟发性皮肤卟啉病', '皮肤瘙痒症', '过敏性皮肤病', '皮炎', '手湿疹', '皮肤卟啉病', '幼年型疱疹样皮炎', '人为性皮炎', '毛发红糠疹', '自身敏感性皮炎', '特发性皮肤钙化病', '疱疹', '色素性痒疹', '发疹性毳毛囊肿', '变应性皮肤血管炎', '传染性红斑', '单纯糠疹', '接触性皮炎', '小儿湿疹', '多形红斑']
target_disease = "荨麻疹"

# 定义 n 和 N
n = 5  # top n 的范围
N = 1  # 只有一个目标疾病


# 计算每个推荐结果的 rank 值（Equation 10）
def compute_rank(n, position):
    """计算排名分数 (rank)"""
    return 100 / n * (n - position + 1)


# 计算 CRA@n （Equation 9）
def compute_top_n(disease_list, target_disease, n):
    """计算 CRA@n 指标"""
    # 寻找目标疾病在列表中的排名 (1-based)
    target_index = disease_list.index(target_disease) + 1 if target_disease in disease_list else None

    if target_index is None or target_index > n:
        # 目标疾病不在 top n 范围内
        return 0.0
    else:
        # 计算目标疾病的 rank 值
        rank_score = compute_rank(n, target_index)
        # CRA@n 的值 (Equation 9)
        return rank_score / N


# 计算 top@5
top_n_score = compute_top_n(disease_list, target_disease, n)
print(top_n_score)
