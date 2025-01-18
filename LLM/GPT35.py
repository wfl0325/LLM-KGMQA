from openai import OpenAI

import os
os.environ["http_proxy"] = "http://localhost:7897"
os.environ["https_proxy"] = "http://localhost:7897"

client = OpenAI(api_key='sk-')


# def extract_information(text, model="gpt-4-0125-preview"):
# def extract_information(text, model="gpt-4o-2024-05-13"):
def extract_information(text, model="gpt-3.5-turbo"):
# def extract_information(text, model="gpt-4o"):
# def extract_information(text, model="gpt-4-turbo"):
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
if __name__=='__main__':
    text = f"""
    请根据用户的具体问题，结合目前的一级、二级以及三级路径知识进行逐级推理，判断用户的问题是否都能从知识路径中找到对应的知识路径。如果每个问题都能在知识路径中找到对应的知识路径，请回答“是”。如果至少有一个问题在知识路径中找不到对应的知识路径，请回答“否”。
                                            用户问题为：Poncet综合征的并发症的并发症叫什么，它有哪些症状？
                                            已经确定的一级路径知识为：Poncet综合征->并发症->颈淋巴结结核
                                            已经确定的二级路径知识为：颈淋巴结结核->并发症->创伤性溃疡
                                            目前的三级路径知识为：['创伤性溃疡->推荐食谱->清汤白菜卷', '创伤性溃疡->忌吃->蚝豉', '创伤性溃疡->宜吃->芝麻', '创伤性溃疡->所属科室->普外科', '创伤性溃疡->常用药品->牛黄解毒丸', '创伤性溃疡->好评药品->度米芬含片', '创伤性溃疡->诊断检查->血常规', '创伤性溃疡->症状->创伤', '创伤性溃疡->并发症->牙龈炎', '创伤性溃疡->并发症->牙龈炎']
                                            Let’s think step by step，请注意：形如A->r->B表示，A的r是B。例如：荨麻疹->并发症->喉水肿，表示荨麻疹的并发症是喉水肿。
                                另外，并分析为什么。
    """
    res = extract_information(text)
    print(res)