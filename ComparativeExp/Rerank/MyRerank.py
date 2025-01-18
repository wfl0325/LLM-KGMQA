from FlagEmbedding import FlagModel
import numpy as np


def get_top_n_sentences(query, sentences, model, n=1):
    """
    根据查询返回最相关的前n个句子。

    参数：
    - query (str): 查询句子。
    - sentences (list): 候选句子列表。
    - model (FlagModel): FlagModel实例，用于生成嵌入。
    - n (int): 返回的句子数量，默认为1。

    返回：
    - list: 按相关性排序的前n个句子。
    """
    # 生成查询和候选句子的嵌入
    query_embedding = model.encode_queries([query])
    sentences_embeddings = model.encode(sentences)

    # 计算相似度分数
    similarity_scores = query_embedding @ sentences_embeddings.T
    print(similarity_scores)
    # 获取分数最高的n个索引
    top_n_indices = np.argsort(-similarity_scores[0])[:n]

    # 返回对应的句子
    top_n_sentences = [sentences[i] for i in top_n_indices]

    return top_n_sentences


# 示例数据
query = "维生素B12缺乏所致贫血的并发症的并发症叫什么，以及维生素B12缺乏所致贫血的并发症的并发症有哪些症状？"
sentences = ["维生素B12缺乏所致贫血->推荐食谱->西兰花素鸡马蹄冬菇汤、牛奶玉米汤、小麦粥、莲藕乌豆煲乳鸽汤、萝卜豆腐汤、虾皮香芹燕麦粥、荞麦粥、肉片粥",
             "维生素B12缺乏所致贫血->忌吃->杏仁、咸鸭蛋、啤酒、白酒",
             "维生素B12缺乏所致贫血->宜吃->鸡蛋清、鸡蛋、葵花子仁、鸡心",
             "维生素B12缺乏所致贫血->所属科室->营养科",
             "维生素B12缺乏所致贫血->常用药品->参茸卫生丸、阿胶益寿口服液",
             "维生素B12缺乏所致贫血->好评药品->养血安神片、参茸卫生丸、阿胶益寿口服液、阿胶、益气养血口服液、天王补心丸、鹿角胶、复方首乌补液、龟甲胶、鳖甲胶、富马酸亚铁咀嚼片、朱砂安神丸、人参养荣丸、当归养血口服液、新生化颗粒、杞枣口服液、妇科养荣丸、富马酸亚铁胶囊",
             "维生素B12缺乏所致贫血->诊断检查->血液检查、维生素B12、骨髓象分析、维生素B1、叶酸",
             "维生素B12缺乏所致贫血->症状->心脏扩大、反应迟钝、营养不良、无力、嗜睡、呆滞、颤抖、恶心、厌食",
             "维生素B12缺乏所致贫血->并发症->口角炎"
             ]

# 加载模型
model = FlagModel('./bge-reranker-large',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)

# 获取最相关的句子
top_sentences = get_top_n_sentences(query, sentences, model, n=1)

print("最相关的句子：", top_sentences)
