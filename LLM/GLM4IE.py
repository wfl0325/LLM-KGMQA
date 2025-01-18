from zhipuai import ZhipuAI

client = ZhipuAI(api_key="") #


# from LLM.GPT35 import *   #仅在使用GPT系列模型时打开注释，否则不予打开
from LLM.sparkAPI import *
from LLM.API_Qwen_Access import chat_with_model
answerlist = []


def getInfo(text):
    """
    这里是星火3.5的调用
    """
    # result = getSpark(text)
    # answerlist.append(result)
    # if len(answerlist) > 1:
    #     return answerlist[-1][len(answerlist[-2]):]
    # else:
    #     return (result)
    # return result[-1]

    """
    这里是GLM4的调用
    """

    # message  = [
    #         {"role": "user", "content": text},
    #     ]
    # response = client.chat.completions.create(
    #     # model="glm-4-flash",  # 填写需要调用的模型名称
    #     model="glm-4",  # 填写需要调用的模型名称
    #     messages=message,
    #     # top_p=0.1
    # )
    # return (response.choices[0].message.content)


    """
    这里是GPT的调用
    """
    # result = extract_information(text=text)
    # return result

    """
    这里是Qwen的调用
    """
    result = chat_with_model(text)
    return result


if __name__ == '__main__':
    with open('LLM_Cut.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    with open('GPT35-turbo_result.txt', 'a') as wfile:
        text = ''
        for i in data:
            text += i.strip()
            if len(i.strip()) == 0:
                if len(text)==0:
                    break
                res = getInfo(text)
                print(res)
                wfile.write("prompt:"+text+'\n')
                wfile.write("answer: "+res+'\n')
                wfile.write('\n')
                text = ''
