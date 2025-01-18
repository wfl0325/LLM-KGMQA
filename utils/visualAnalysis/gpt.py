import matplotlib.pyplot as plt
import seaborn as sns

# Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions数据
GLM4Time = [
    [12.362852096557617, 11.081358909606934, 10.35212230682373, 10.6078941822052, 9.031340837478638, 9.960212707519531, 10.604018688201904, 13.851387977600098, 11.33356261253357, 11.481820583343506, 11.456888914108276, 11.95534896850586, 12.443575620651245, 12.645682096481323, 12.667941331863403, 14.146851778030396, 11.830368995666504, 13.900653600692749, 9.651158571243286, 12.995531558990479],
    [12.907323360443115, 15.120949506759644, 14.905471324920654, 13.042134523391724, 11.851834058761597, 16.730565786361694, 16.337852239608765, 15.425352573394775, 15.692398071289062, 13.841091394424438, 16.930233001708984, 11.574539184570312, 18.56629729270935, 13.275298833847046, 13.714169979095459, 15.923599481582642, 14.221746921539307, 14.5589017868042],
    [10.095736980438232, 15.569307804107666, 15.761367321014404, 11.899608373641968, 15.63412070274353, 11.825532674789429, 14.284191846847534, 12.767845869064331, 12.609509706497192, 14.485777139663696, 14.951128959655762, 12.235508680343628, 15.26285171508789, 17.48061490058899, 11.084921836853027, 11.848238468170166, 14.283894777297974, 14.910473585128784]
]

# 创建一个包含所有数据和相应标签的列表
data = []
labels = []

for i, times in enumerate(GLM4Time):
    data.extend(times)
    labels.extend([f'{i+1}-hop'] * len(times))

# 创建箱线图
plt.figure(figsize=(10, 6))
sns.boxplot(x=labels, y=data)

# 设置标题和标签
plt.title('Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions')
plt.xlabel('n-hop')
plt.ylabel('Response time/sseconds)')

# 显示图形
plt.show()

#小提请图
plt.figure(figsize=(10, 6))
sns.violinplot(x=labels, y=data)
plt.title('Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions')
plt.xlabel('n-hop')
plt.ylabel('Response time/s')
plt.savefig('小提琴.png', dpi=500)

plt.show()

import numpy as np

mean_data = [np.mean(times) for times in GLM4Time]
std_data = [np.std(times) for times in GLM4Time]

plt.figure(figsize=(10, 6))
plt.bar(['1-hop', '2-hop', '3-hop'], mean_data, yerr=std_data, capsize=5)
plt.title('Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions')
plt.xlabel('n-hop')
plt.ylabel('响应时间均值 (秒)')
plt.show()


plt.figure(figsize=(10, 6))
sns.stripplot(x=labels, y=data, jitter=True)
plt.title('Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions')
plt.xlabel('n-hop')
plt.ylabel('Response time/s')
plt.show()


# plt.figure(figsize=(10, 6))
# for i, times in enumerate(GLM4Time):
#     sns.kdeplot(times, label=f'{i+1}-hop')
# plt.title('Response time of GLM4 model in 1-hop, 2-hop, and 3-hop questions')
# plt.xlabel('Response time/s')
# plt.ylabel('密度')
# plt.legend()
# plt.show()


