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

    smli2 = dot / Caabs(np.array(vector1)) + Caabs(np.array(vector2))
    # smli2 = Caabs(np.array(vectorText)) + dot / Caabs(np.array(vector1)) + Caabs(np.array(vector2))
    return (smli2)


def bert_cos_similarity(text1, text2):
    # 加载预训练的BERT模型和分词器
    tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese')
    model = BertModel.from_pretrained('./bert-base-chinese')

    # tokenizer = BertTokenizer.from_pretrained('./albert')
    # model = BertModel.from_pretrained('./albert')

    # tokenizer = BertTokenizer.from_pretrained('./roberta')
    # model = BertModel.from_pretrained('./roberta')

    # 对文本进行编码
    encoded_text1 = tokenizer.encode_plus(text1, add_special_tokens=True, padding='max_length', max_length=20, return_tensors='pt')
    encoded_text2 = tokenizer.encode_plus(text2, add_special_tokens=True, padding='max_length', max_length=20, return_tensors='pt')

    # 获取文本的嵌入表示
    with torch.no_grad():
        embeddings1 = model(**encoded_text1)[0][:, 0, :]
        embeddings2 = model(**encoded_text2)[0][:, 0, :]
    # 计算余弦相似度
    similarity = 1 - cosine(np.array(embeddings1)[0], np.array(embeddings2)[0])
    return similarity
