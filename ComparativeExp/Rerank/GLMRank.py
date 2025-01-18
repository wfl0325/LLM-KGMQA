from zhipuai import ZhipuAI

client = ZhipuAI(api_key="") #

answerlist = []


def getInfo(text):

    message  = [
            {"role": "user", "content": text}
        ]
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=message,
    )
    return (response.choices[0].message.content)

if __name__ == '__main__':
    with open('LLM_Cut.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    with open('LLM_result.txt', 'a') as wfile:
        text = ''
        for i in data:
            text += i.strip()
            if len(i.strip()) == 0:
                if len(text)==0:
                    break
                res = getInfo(text)
                print(res)
                wfile.write(text+'\n')
                wfile.write(res+'\n')
                wfile.write('\n')
                text = ''