import requests
import json


def getTrueOrFalse(question):
    url = "https://api.baichuan-ai.com/v1/chat/completions"
    api_key = ""
    ques = question
    ques = f"""
    介绍一下安徽建筑大学
    """
    data = {
        "model": "Baichuan2-Turbo",
        "messages": [
            {
                "role": "user",
                "content": ques
            }
        ],
        "stream": True
    }

    json_data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, data=json_data, headers=headers, timeout=60, stream=True)

    if response.status_code == 200:
        # print("请求成功！")
        # print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))

        complete_response = ""

        for line in response.iter_lines():
            if line:
                # 去掉前缀并移除空白字符
                line_str = line.decode('utf-8').strip()
                if line_str.startswith("data:"):
                    try:
                        # 将 "data: " 之后的内容解析为 JSON
                        decoded_line = json.loads(line_str.lstrip("data: "))
                        # 提取内容并拼接
                        if "choices" in decoded_line and decoded_line["choices"][0]["delta"].get("content"):
                            complete_response += decoded_line["choices"][0]["delta"]["content"]
                    except json.JSONDecodeError as e:
                        print()
                        # print("JSON解析错误:", e)
                        # print("错误的行内容:", line_str)

        print("百川返回的答案：", complete_response)
        return complete_response
    else:
        print("请求失败，状态码:", response.status_code)
        print("请求失败，body:", response.text)
        print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))

if __name__ == "__main__":
    getTrueOrFalse("wefds")
