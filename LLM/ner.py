
answerlist = []

from LLM.sparkAPI import *

def getInfo(text):
    """
    这里是星火3.5的调用
    """
    prompt = f"""
            现在你是一个命名实体抽取专家，你需要根据用户输入的语句，尽可能的抽取出时间、地点、经纬度、震级、海拔、人数等实体
            用户输入的语句为：{text}
    """
    result = getSpark(prompt)
    answerlist.append(result)
    if len(answerlist) > 1:
        return answerlist[-1][len(answerlist[-2]):]
    else:
        return (result)
    return result[-1]
text = input('input:')
print(getInfo(text))