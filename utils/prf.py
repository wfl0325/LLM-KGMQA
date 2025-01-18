
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

# preds = [0, 1, 2, 1, 0, 2, 0, 2, 0, 0, 2, 1, 2, 0, 1]

trues = [1] * 10
trues.append(0)
# trues = [0, 1, 2, 1, 1, 2, 0, 2, 0, 0, 2, 1, 2, 1, 2]

# preds = [1,	1,	2,	1,	1,	1,	1,	1,	1,	1]
# preds = [0,	0,	2,	2,	1,	1,	1,	1,	0,	1,0]  # Spark 50- 100
preds = [1,	0,	2,	2,	1,	1,	1,	1,	1,	1,0]  # Spark x>50
# preds = [0,	0,	2,	2,	1,	1,	1,	1,	1,	2,0]  # Spark x<50
# 准确率 normalize=False则返回做对的个数
acc = accuracy_score(trues, preds)
acc_nums = accuracy_score(trues, preds, normalize=False)
print(acc, acc_nums) # 0.8 12


# labels为指定标签类别，average为指定计算模式
# Acc = accuracy_score(trues, preds)
# micro-precision
micro_p = precision_score(trues, preds, labels=[1, 2, 0], average='micro')
# micro_p = precision_score(trues, preds, labels=[0, 1, 2], average='micro')
# micro-recall
micro_r = recall_score(trues, preds, labels=[1, 2, 0], average='micro')
# micro f1-score
micro_f1 = f1_score(trues, preds, labels=[1, 2, 0], average='micro')

print(micro_p, micro_r, micro_f1) # 0.8 0.8 0.8000000000000002

# # macro-precision
# macro_p = precision_score(trues, preds, labels=[0, 1, 2], average='macro')
# # macro-recall
# macro_r = recall_score(trues, preds, labels=[0, 1, 2], average='macro')
# # macro f1-score
# macro_f1 = f1_score(trues, preds, labels=[0, 1, 2], average='macro')
#
# print(macro_p, macro_r, macro_f1)