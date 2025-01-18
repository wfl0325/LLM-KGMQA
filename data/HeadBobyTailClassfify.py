
from LLM.sparkAPI import *
from LLM.GLM4IE import *
def getCLassfify(disease):

    prompt = f"""
            请根据输入的疾病名称，结合你已有的知识，对这个疾病的患病部位进行分类。本次任务患病部位分为四类，颈部及以上部分记为“Head”，腰部到颈部记为“Body”，腰部以下记为“Tail”，未知的分类记为“Other”。
            请在回答中直接返回答案，注意你的答案只能从Head、Body、Tail、Other中选择。
            疾病名称为{disease}
            """
    """
    星火模型
    classfify_result = getAnswer(prompt)
    print(classfify_result)
    """
    GLM_result = getInfo(prompt)

    return GLM_result




def HBTClassfify():
    with open('remaining/disease.txt', 'r') as file:
        data = file.readlines()

    disease_list = []
    classifify_list = []
    with open('classfify.txt', 'a') as file:
        for i in data:
            line = i.strip()
            print(line)
            disease_list.append(line)
            result = getCLassfify(line)
            classifify_list.append(result)
            write_line = line+": "+result+'\n'
            print(write_line)
            file.write(write_line)
    print(disease_list)
    print(classifify_list)
    print("Done")

import json
def statisticKESHI():
    with open('KeshiDisea.json', 'r', encoding='utf-8') as file:
        data = json.load(file)


    KESHI_list = {}
    for i in data:
        print(i, len(data[i]))


def text2json():


    #KESHI_list = ['Head','Body','Tail','Other']
    # 初始化字典，用于保存每个分类对应的疾病列表
    disease_lists = {}
    with open('classfify.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    for i in data:
        print(i)
        line = i.strip().split(": ")
        entity = line[0]
        type = line[1]
        if type in disease_lists:
            disease_lists[type].append(entity)
        else:
            disease_lists[type] = [entity]

    for i in disease_lists:
        print(i + "的数目有： ", len(disease_lists[i]))
    # with open('classfify.json', 'w', encoding='utf-8') as file:
    #      file.write(str(disease_lists))
    # print("DONE")


if __name__=='__main__':
    # statisticKESHI()
    # HBTClassfify()
    text2json()



