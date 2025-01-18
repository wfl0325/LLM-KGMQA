import requests


def chat_with_model(text, url="http://127.0.0.1:6006/chat"):
    """
    访问 RESTful 接口，与模型对话。

    Args:
        text (str): 用户输入文本。
        url (str): 接口地址，默认为本地服务。

    Returns:
        str: 模型的响应文本。
    """
    try:
        # 请求数据
        payload = {'text': text}
        headers = {'Content-Type': 'application/json'}

        # 发送 POST 请求
        response = requests.post(url, json=payload, headers=headers)

        # 检查响应状态
        if response.status_code == 200:
            return response.json().get('response', 'No response')
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Exception occurred: {e}"


# 示例
if __name__ == "__main__":
    user_input = "你好！介绍一下你自己。"
    response = chat_with_model(user_input)
    print("模型回复:", response)
