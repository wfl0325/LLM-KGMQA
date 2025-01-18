
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = "iic/nlp_gte_sentence-embedding_chinese-base"
pipeline_se = pipeline(Tasks.sentence_embedding,
                       model=model_id,
                       sequence_length=512
                       ) # sequence_length 代表最大文本长度，默认值为128

disease_list = []
with open('disease.txt', 'r') as file:
    data = file.readlines()

for i in data:
    line = i.strip()
    disease_list.append(line)
def returnTopentity(question, top_n):
    inputs = {
        "source_sentence": [question],
        "sentences_to_compare": disease_list
    }

    result = pipeline_se(input=inputs)

    # 提取相似度和句子
    # similarities = result['scores'][:top_n]  # 获取相似度分数
    similarities = result['scores']  # 获取相似度分数
    sentences = inputs["sentences_to_compare"]

    # 将句子和相似度绑定，并按相似度降序排序
    sorted_results = sorted(
        zip(sentences, similarities),
        key=lambda x: x[1],  # 根据相似度排序
        reverse=True
    )
    top_list = []
    # 输出排序结果
    print("按照相似度排序的句子:")

    for i, (sentence, similarity) in enumerate(sorted_results, start=1):
        print(f"{i}. {sentence} (相似度: {similarity:.4f})")
        top_list.append(sentence)
        if i > top_n:
            break
    return top_list


with open('question.txt', 'r') as qfile:
    qdata = qfile.readlines()


with open('GTE_Result.txt', 'a') as wfile:
    for m in qdata:
        print(m)
        qline = m.strip().split("：")
        if len(qline) != 2:
            print(qline)
            exit()
        diease = qline[0]
        question = qline[1]

        top_list = returnTopentity(question, 1)
        wfile.write(diease +":  " +question +"\n")
        wfile.write("GTE预测：  "+ str(top_list))





