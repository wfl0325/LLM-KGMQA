import time

def example_function(n):
    """一个简单的示例函数，用于模拟计算"""
    result = 0
    for i in range(n):
        result += i
    return result

def measure_time(func, *args, **kwargs):
    """测量函数运行时间的函数"""
    start_time = time.time()  # 获取当前时间
    result = func(*args, **kwargs)  # 调用函数
    end_time = time.time()  # 再次获取当前时间
    elapsed_time = end_time - start_time  # 计算时间差
    return elapsed_time, result

# # 使用示例函数和测量时间的函数
# elapsed_time, result = measure_time(example_function, 1000000)
# print(elapsed_time, result)

