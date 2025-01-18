import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.rcParams['font.family'] = 'SimHei'


# 数据
x = ['GPT-4', 'GPT-3.5', 'Spark3.5', 'GLM4']
y1 = [86.6, 76.6, 93.3, 99.9]   # 都是1-hop问题
y2 = [16.6, 26.6, 46.7, 83.3]
y3 = [13.3, 15, 15,86.6]

# 创建画布和子图对象
fig, ax = plt.subplots()

# 绘制第一组柱状图
ax.bar(np.arange(len(x))-0.2, y1, width=0.2, align='center', label='1-hop')

# 绘制第二组柱状图
ax.bar(np.arange(len(x)), y2, width=0.2, align='center', label='2-hop')

# 绘制第三组柱状图
ax.bar(np.arange(len(x))+0.2, y3, width=0.2, align='center', label='3-hop')


# 设置标题和坐标轴标签
ax.set_title('Comparison of the accuracy of each LLMs')
# ax.set_xlabel('Question Type')
ax.set_ylabel('Acc(%)')

# 设置横坐标刻度及标签
ax.set_xticks(np.arange(len(x)))
ax.set_xticklabels(x)

# 添加图例
ax.legend(loc='upper right')

# 保存图形
plt.savefig('my_bar_chart.png', dpi=500)

# 显示图形
plt.show()
