from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained("./Qwen-7B-Chat", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("./Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()


def getInfo(text):
    response, history = model.chat(tokenizer, text, history=None)
    print(response)
    return response


with open('LLM_Cut.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()
with open('qwen2-7b-chat_result.txt', 'a') as wfile:
    text = ''
    for i in data:
        text += i.strip()
        if len(i.strip()) == 0:
            if len(text)==0:
                break
            res = getInfo(text)
            print(res)
            wfile.write("prompt:"+text+'\n')
            wfile.write("answer: "+str(res)+'\n')
            wfile.write('\n')
            text = ''
