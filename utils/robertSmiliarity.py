from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from scipy.spatial.distance import cosine


def Smiliarity(vector1, vector2):
    def Caabs(a):
        result = np.abs(np.sum(a))
        return (result)

    def caluDot(a, b):
        result = np.dot(a, b)
        # print(result)
        return (np.abs(result))

    dot = caluDot(np.array(vector1), np.array(vector2))

    # print(dot)
    # print(Caabs(np.array(vector1)) + Caabs(np.array(vector2)))
    # exit()
    smli2 = dot / Caabs(np.array(vector1)) + Caabs(np.array(vector2))
    # smli2 = Caabs(np.array(vectorText)) + dot / Caabs(np.array(vector1)) + Caabs(np.array(vector2))
    return (smli2)


def bert_cos_similarity(text1, text2):
    # 加载预训练的BERT模型和分词器
    tokenizer = BertTokenizer.from_pretrained('../roberta')
    # tokenizer = BertTokenizer.from_pretrained('../albert')
    model = BertModel.from_pretrained('../roberta')
    # model = BertModel.from_pretrained('../albert')

    # 对文本进行编码
    encoded_text1 = tokenizer.encode_plus(text1, add_special_tokens=True, padding='max_length', max_length=20, return_tensors='pt')
    encoded_text2 = tokenizer.encode_plus(text2, add_special_tokens=True, padding='max_length', max_length=20, return_tensors='pt')

    # 获取文本的嵌入表示
    with torch.no_grad():
        embeddings1 = model(**encoded_text1)[0][:, 0, :]
        embeddings2 = model(**encoded_text2)[0][:, 0, :]
    """similarity = Smiliarity(embeddings1[0], embeddings2[0])
    print(similarity)
    exit()"""
    # 计算余弦相似度
    similarity = 1 - cosine(np.array(embeddings1)[0], np.array(embeddings2)[0])
    # similarity = 1 - cosine(embeddings1.numpy(), embeddings2.numpy())

    return similarity

if __name__=='__main__':
    # text1 = "服务区至高新之间车流量大通行缓慢雁塔入口车多缓行"
    text1 = "阅读理解"
    text2 = "英语完形填空"
    # text2 = "反流食管炎"
    # text2 = "随分而痛"
    # text2 = "绕城高速早高峰到来目前内环方向曲江服务区至高新之间车流量大通行缓慢雁塔入口车多缓行"

    similarity = bert_cos_similarity(text1, text2)
    print("相似度：", similarity)

