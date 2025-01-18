from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"  # the device to load the model onto

model_path = '/root/autodl-tmp/Qwen2-7B'
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_path)
print('tokenizer ok')


def getInfo(prompt):
    # prompt = "Give me a short introduction to large language model. response using chinese"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    print(prompt)

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


if __name__ == '__main__':
    with open('LLM_Cut.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    with open('qwen2-7b-chat_result.txt', 'a') as wfile:
        text = ''
        for i in data:
            text += i.strip()
            if len(i.strip()) == 0:
                if len(text) == 0:
                    break
                res = getInfo(text)
                print(res)
                wfile.write("prompt:" + text + '\n')
                wfile.write("answer: " + res + '\n')
                wfile.write('\n')
                text = ''