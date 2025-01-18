from openai import OpenAI

import os
os.environ["http_proxy"] = "http://localhost:7897"
os.environ["https_proxy"] = "http://localhost:7897"


client = OpenAI('sk-')

def getInfo(text, model="gpt-3.5-turbo"):
  message = [
      {
        "role": "user",
        "content": text
      }
    ]
  completion = client.chat.completions.create(
    model=model,
    messages=message,
  )
  return completion.choices[0].message.content
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