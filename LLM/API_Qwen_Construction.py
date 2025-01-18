from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

# 初始化模型和分词器
tokenizer = AutoTokenizer.from_pretrained("./Qwen-7B-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("./Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()

# 创建 Flask 应用
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """
    接收用户输入并返回模型生成的响应。
    """
    try:
        # 获取请求数据
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Invalid input, "text" is required'}), 400
        
        text = data['text']
        
        # 调用模型生成响应
        response, history = model.chat(tokenizer, text, history=None)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)
