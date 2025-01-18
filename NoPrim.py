# This is a sample Python script.
import json
import ast
import smiliarity
from ACTree.tree import *
from LLM.GLM4IE import *
MAX_INTER_LENGTH = 50
from py2neo import Graph
from utils import getTime
import time

g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="")


def getIntersection(keshi, buwei, question):
    with open('./data/KeshiDisea.json', 'r',encoding='utf-8') as kefile:
        keshi_data = json.load(kefile)
    with open('./data/classfify.json', 'r', encoding='utf-8') as buweifile:
        buwei_data = json.load(buweifile)
    keshi_list = (keshi_data[keshi])
    buwei_list = (buwei_data[buwei])
    Inter_list = []
    if len(keshi_list) > len(buwei_list):
        for i in keshi_list:
            if i in buwei_list:
                Inter_list.append(i)
    else:
        for i in buwei_list:
            if i in keshi_list:
                Inter_list.append(i)


    print("交集大小为： ",len(Inter_list))
    print("交集为： ",Inter_list)

    if len(Inter_list) > MAX_INTER_LENGTH:
        """
        @ 开始计算相似度
        
        """
        print("交集大小过大，开始计算相似度......")
        word_similar_dict = {}
        similarity_list = []
        key_word_prompt = f"""
                               我现在需要根据用户输入的关于疾病的问题与已有的疾病名称进行相似度匹配，查找与用户输入的相似度最高的疾病名称。但是用户输入的句子中可能含有无关信息，请你分析用户的输入提取出疾病关键词语，方便我计算相似度。
                               注意：请直接返回你提取的关键词语且必须是与疾病名称相关，无需其他额外的回复或分析。返回的格式就是字符串即可。
                               用户输入的句子为： {question}
                                """
        key_word = getInfo(key_word_prompt)
        print("提取的关键词为： ",key_word)
        for word in Inter_list:
            """
            直接使用用户句子进行相似度计算
            """
            similariy = smiliarity.bert_cos_similarity(question, word)
            print(question, word, similariy)
            word_similar_dict.update({similariy: word})
            similarity_list.append(similariy)
        top_20_elements = sorted(similarity_list, reverse=True)[:50]

        # Get the indices of the top 20 elements in the original list
        top_20_word = [word_similar_dict[elem] for elem in top_20_elements]
        print(top_20_word)


        entity_find_prompt = f"""
                            现在我需要根据用户输入的关于疾病的句子以及候选实体列表，查询出与用户问题最匹配的实体。注意你的答案只能从候选实体列表中返回，并且直接答案，无需其他额外的回复或分析。
                            用户问题为：{question}
                            候选列表：{top_20_word}
                            """
        entity = getInfo(entity_find_prompt)
        print("最终查询的相关实体为： ", entity)
        return entity


    else:
        entity_find_prompt = f"""
                                    现在我需要根据用户输入的关于疾病的句子以及候选实体列表，查询出与用户问题最匹配的实体。注意你的答案只能从候选实体列表中返回，并且直接答案，无需其他额外的回复或分析。
                                    用户问题为：{question}
                                    候选列表：{Inter_list}
                                    如果候选列表中不存在该实体请直接返回“无”。
                                    """
        entity = getInfo(entity_find_prompt)
        if entity =='无':
            print("系统查不到相关信息！")
            exit()
        print("最终查询的相关实体为： ", entity)
        return entity


def getEntity(question):
    KESHI = ['内科', '呼吸内科', '儿科', '小儿内科', '急诊科', '其他科室', '其他综合', '肿瘤科', '肿瘤内科',
             '外科', '心胸外科', '感染科', '传染科', '儿科综合', '妇产科', '产科', '普外科', '心内科', '肿瘤外科',
             '神经内科', '风湿免疫科', '五官科', '眼科', '内分泌科', '小儿外科', '耳鼻喉科', '妇科', '康复科',
             '消化内科', '肛肠科', '肝病', '皮肤性病科', '皮肤科', '肝胆外科', '血液科', '遗传病科', '肾内科',
             '泌尿外科', '泌尿内科', '中医科', '中医综合', '烧伤科', '男科', '骨外科', '神经外科', '精神科',
             '口腔科', '营养科', '性病科', '心理科', '生殖健康', '不孕不育', '减肥']
             # '口腔科', '营养科', '性病科', '心理科', '生殖健康', '不孕不育', '整形美容科', '减肥']
    keshi_prompt = f"""
            请根据用户输入的疾病相关问题或疾病的名称给出对应就诊的科室，注意科室只能从已给的列表中查询，并且直接给出答案即可，不需要额外的回答和分析。
            用户问题或疾病的名称为：{question}
            科室列表：{KESHI}
            """
    keshi_result = getInfo(keshi_prompt)
    print("该问题对应的科室为：",keshi_result)

    buwei_prompt = f"""
            请根据用户输入的疾病相关问题，结合你已有的知识，对这个包含疾病信息的句子的患病部位进行分类。本次任务患病部位分为四类，颈部及以上部分记为“Head”，腰部到颈部记为“Body”，腰部以下记为“Tail”，未知的分类记为“Other”。
            请在回答中直接返回答案，注意你的答案只能从Head、Body、Tail、Other中选择。
            用户问题为: {question}
            """
    buwei_result = getInfo(buwei_prompt)
    print("该问题对应的部位为：", buwei_result)

    entity = getIntersection(keshi_result, buwei_result, question)
    return entity


key_dict = {
            '医保疾病' : 'yibao_status',
            "患病比例" : "get_prob",
            "易感人群" : "easy_get",
            "传染方式" : "get_way",
            "就诊科室" : "cure_department",
            "治疗方式" : "cure_way",
            "治疗周期" : "cure_lasttime",
            "治愈率" : "cured_prob",
            '药品明细': 'drug_detail',
            '药品推荐': 'recommand_drug',
            '推荐食品': 'recommand_eat',
            '忌食': 'not_eat',
            '宜食': 'do_eat',
            '症状': 'symptom',
            '检查': 'check',
            '成因': 'cause',
            '预防措施': 'prevent',
            '所属类别': 'category',
            '简介': 'desc',
            '名称': 'name',
            '常用药品' : 'common_drug',
            '治疗费用': 'cost_money',
            '并发症': 'acompany'
        }

def getReAndEnd(entity, visited=None, current_depth=0, max_depth=3, path=None, paths_dict=None):
    if visited is None:
        visited = set()  # 初始化已访问节点的集合
    if path is None:
        path = []  # 初始化路径列表
    if paths_dict is None:
        paths_dict = {}  # 初始化路径字典

    # 如果当前节点已经访问过或者达到最大深度，则返回，避免循环或超出深度
    if entity in visited or current_depth >= max_depth:
        # 如果当前路径不为空，将其添加到路径字典中
        if path:
            # 将路径添加到字典中，以起始节点为键
            start_node = path[0][0]
            if start_node not in paths_dict:
                paths_dict[start_node] = []
            paths_dict[start_node].append(path)
        return paths_dict

    visited.add(entity)  # 将当前节点添加到已访问集合中

    queryOne_Re = f"MATCH (n)-[r]->(e) WHERE n.name='{entity}' RETURN r, e"
    result = g.run(queryOne_Re).data()
    if len(result) == 0:
        # print("******",queryOne_Re)
        start_node = path[0][0]
        if start_node not in paths_dict:
            paths_dict[start_node] = []
        paths_dict[start_node].append(path)
        return paths_dict
    for i in result:
        # 创建当前路径的三元组
        triple = (entity, i['r']['name'], i['e']['name'])
        # print("*************",triple)
        # 将当前路径的三元组添加到路径列表中
        path.append(triple)


        # print(i['e']['name'], visited, current_depth + 1, max_depth, path, paths_dict)
        # 递归调用，继续遍历下一个节点，深度加1
        paths_dict = getReAndEnd(i['e']['name'], visited, current_depth + 1, max_depth, path, paths_dict)

        # 在返回之前，清除当前路径，以便开始新的路径
        path = []

    return paths_dict


def removeRemain(text):
    input_str = text

    # 将字符串转换为字典格式
    triples = {}
    key, relation, tail_entities_str = input_str.split("->")
    tail_entities = tail_entities_str.split("、")
    triples[key] = {relation: tail_entities}

    # 减少尾实体，只保留一个
    for key, value in triples.items():
        for relation, tail_entities in value.items():
            triples[key][relation] = tail_entities[:1]

    # 将字典转换回字符串格式
    output_str = "{}->{}->{}".format(key, relation, tail_entities[0])
    return (output_str)

def getNextPath(path, text):
    print("最相关的知识为：",text)
    if text.startswith("'"):
        text = text.replace("'","")
    data = text.split('->')
    if len(data) != 3:
        print("返回最相关的一条路径错误，模型输出为：", data)
        return
    mytriple = (data[0], data[1], data[2])

    leval1 = path[data[2]]

    # leval1.append(info_list[0])
    leval1KP = []
    preRea = ''
    preHead = ''
    end_list = []
    count = 0
    for i in leval1:
        # print(i)
        head = i[0][0]
        relation = i[0][1]
        tail = i[0][2]
        if relation != preRea and count != 0:
            knowledgePath = preHead + "->" + preRea + "->" + "、".join(end_list)
            # print(knowledgePath)
            leval1KP.append(knowledgePath)
            # print(knowledgePath)
            end_list = []
            end_list.append(tail)  # 虽然已经不一样了，把当前实体加进去，防止丢失。
            if count == len(leval1) - 1:
                knowledgePath = head + "->" + relation + "->" + "、".join(end_list)
                # print(knowledgePath)
                leval1KP.append(knowledgePath)
        else:
            end_list.append(tail)

        preRea = relation
        preHead = head
        count += 1
    if len(end_list) != 0:
        knowledgePath = preHead + "->" + preRea + "->" + "、".join(end_list)
        # print(knowledgePath)
        leval1KP.append(knowledgePath)
    level1Rela = []
    for i in leval1KP:
        print(i)
        rela = (i.split("->")[1])
        level1Rela.append(rela)

    return leval1KP, level1Rela

def FinallAnswer(question, knowledge):
    answer_prompt = f"""
                    请根据用户输入的问题并根据你自己的知识储备，回答用户问题,要求回答尽量详尽，同时注意语言逻辑顺序，符合语境。
                    用户问题为：{question}，
                    从知识图谱中查询到的知识三元组为：{knowledge}
                    """
    return getInfo(answer_prompt)

def find_relation(question, entity):
    path = getReAndEnd(entity)
    leval1 = path[entity]
    leval1KP = []
    preRea = ''
    preHead = ''
    end_list = []
    count = 0
    for i in leval1:
        # print(i)
        head = i[0][0]
        relation = i[0][1]
        tail = i[0][2]
        if relation != preRea and count != 0:
            knowledgePath = preHead + "->" + preRea + "->" + "、".join(end_list)
            leval1KP.append(knowledgePath)
            end_list = []
            end_list.append(tail)   # 虽然已经不一样了，把当前实体加进去，防止丢失。
            if count == len(leval1)-1:
                knowledgePath = head + "->" + relation + "->" + "、".join(end_list)
                leval1KP.append(knowledgePath)
        else:
            end_list.append(tail)

        preRea = relation
        preHead = head
        count+=1
    if len(end_list) != 0:
        knowledgePath = preHead + "->" + preRea + "->" + "、".join(end_list)
        # print(knowledgePath)
        leval1KP.append(knowledgePath)
    level1Rela = []
    for i in leval1KP:
        print(i)
        rela = (i.split("->")[1])
        level1Rela.append(rela)

    """
    下面考虑token消耗问题，将”目前的关系“进行精简，即将知识三元组的尾实体只留一个就行了
    """
    sample_leval1KP = []
    for i in leval1KP:
        sample_leval1KP.append(removeRemain(i))
    judge_prompt = f"""请根据用户的具体问题，判断用户的所有问题是否都能从知识路径中直接找到对应的知识路径。如果每个问题都能在知识路径中找到对应的知识路径，请回答“是”。如果至少有一个问题在知识路径中找不到对应的知识路径，请回答“否”。
                         用户问题为：{question}
                         目前的知识路径为：{path[entity]}，
                         请注意：形如（'A','r','B'）表示，A的r是B。例如：荨麻疹->并发症->喉水肿，表示荨麻疹的并发症是喉水肿。
                         另外，请将经过分析后的结果直接返回，直接返回”是“或者”否“，无需进行额外的分析与回复。
                         """
    # 请直接回复现在已有的关系是否支撑用户问答，完全可以则回复”是“，如果有不能回答的则必须回复”否“。
    print("一级判断提示：", judge_prompt)
    # exit()
    relstion_result = getInfo(judge_prompt)
    print("一级判断结果：",relstion_result)
    # exit()
    start_time = time.time()

    if '是' in relstion_result:   # 此时子图信息足够支撑用户回答，下面将该时刻的子图作为提示交给大模型进行回答
        print("该问题是系统判定只需要一级路径即可满足回答")
        answer = (FinallAnswer(question, path[entity]))
        end_time = time.time()
        elapsed_time = end_time - start_time  # 计算时间差
        print("响应时间为：", elapsed_time)
        print(answer)

    elif '否' in relstion_result:   # 此时子图信息不能够支撑用户回答，下面考虑进行下一跳路径搜索
        # 进行两跳查询
        # 同样的，要进行下一跳路径搜素，先考虑对无关子图进行剪枝判断子图大小，如果过大，考虑剪枝。
        prim_prompt = f"""请按照用户问题的顺序，从给定的列表中推理出下一级知识路径，选择符合逻辑的一个元素直接返回，请注意，返回的内容必须是列表中的元素，不能随意改变列表中元素，并且符合逐级推理的要求。
                            用户问题：{question}
                            Let’s think step by step，选择符合逻辑的下一级路径信息，并从下面的列表中选择并返回：{path}
                            **************************************             
                            另外，请按照示例返回列表中的一个元素组成的一条知识路径，不要返回多条路径或者多个元素组成的路径，只要返回最符合逻辑推理的一个list列表中的一个元素的一条路径，另外无需进行额外的分析与回复。
                            示例：例如找到的路径为：('荨麻疹','并发症','喉水肿')，则你应该返回“荨麻疹->并发症->喉水肿”。
                            只要返回3个字符串组成的知识路径即可，不要返回多个元素组成的路径如：五软->并发症->肌肉萎缩->好评药品->利鲁唑片
                            直接返回路径即可，不要其他额外的分析与回复。
                            """
        print("查询最相关的语句的提示： ",prim_prompt)
        text = getInfo(prim_prompt)
        if text.startswith("'"):
            text = text.replace("'", "")
        data = text.split('->')
        #  下面对一级路径中与用户最相关的知识进行二级路径搜索
        print("*********最相关的知识为***********：\n",text)  # 荨麻疹->并发症->喉水肿
        # exit()
        leval2KP, level2Rela = getNextPath(path, text)


        sample_leval2KP = []
        for i in leval2KP:
            sample_leval2KP.append(removeRemain(i))

        judge_2prompt = f"""请根据用户的问题，结合目前的一级和二级路径知识进行推理，判断用户的问题是否能从下面知识路径中找到问题对应的知识路径。如果用户有多个问题，则每个问题都能在知识路径中找到对应的知识路径，请回答“是”。如果用户的多个问题中至少有一个问题在知识路径中找不到对应的知识路径，请回答“否”。Let’s think step by step。
                                用户问题为：{question}
                                目前的一级路径知识为：{path[entity]}
                                目前的二级路径知识为：{path[data[2]]}
                                请注意：形如A->r->B表示，A的r是B。例如：荨麻疹->并发症->喉水肿，表示荨麻疹的并发症是喉水肿。
                                另外，请直接返回”是“或者”否“，无需进行额外的分析与回复。
                                """
        print("两跳结果判断语句：",judge_2prompt)

    # 请直接回复现在已有的关系是否支撑用户问答，完全可以则回复”是“，如果有不能回答的则必须回复”否“。
        relstion_2result = getInfo(judge_2prompt)
        print("两跳结果：",relstion_2result)
        # exit()
        print("***************")
        if '是' in relstion_2result:  # 此时子图信息足够支撑用户回答，下面将该时刻的子图作为提示交给大模型进行回答
            print("该问题是系统判定只需要二级路径即可满足回答")
            pre2pathKnowledge = path[entity]+path[data[2]]
            # start_time = time.time()

            print(FinallAnswer(question, pre2pathKnowledge))
            end_time = time.time()
            elapsed_time = end_time - start_time  # 计算时间差
            print("响应时间为：", elapsed_time)
            # 判断子图大小，如果过大，考虑剪枝。
        elif '否' in relstion_2result:  # 此时子图信息不能够支撑用户回答，下面考虑进行下一跳路径搜索
            print("下面开始三级知识路径查询")

            # 从下面的list列表中选择与用户问题最相关的一个元素直接返回，不要输出其他任何内容。请注意你返回的内容必须是给定的列表中的元素。


            prim_prompt = f"""
                请按照用户问题的顺序和第一级路径信息，推理出下一级知识路径，并从给定的列表中选择符合逻辑的选项直接返回，不要输出其他任何内容。请注意，返回的内容必须是列表中的元素，并且符合逐级推理的要求。
                路径信息：{text}
                用户问题：{question}
                选择符合逻辑的下一级路径信息，因为我会根据你选择的知识路径去查询下一级知识，从下面的列表中选择并返回：
                {path}
                另外，请按照示例返回列表中的一个元素组成的一条知识路径，不要返回多条路径或者多个元素组成的路径，只要返回最符合逻辑推理的一个list列表中的一个元素的一条路径，另外无需进行额外的分析与回复。
                示例：例如找到的路径为：('荨麻疹','并发症','喉水肿')，则你应该返回“荨麻疹->并发症->喉水肿”。
                只要返回3个字符串组成的知识路径即可，不要返回多个元素组成的路径如：五软->并发症->肌肉萎缩->好评药品->利鲁唑片
                直接返回路径即可，不要其他额外的分析与回复。
                """
            print("查询最相关的语句的提示： ", prim_prompt)
            text2 = getInfo(prim_prompt)
            #  下面对一级路径中与用户最相关的知识进行三级路径搜索
            print("*********最相关的知识为***********：\n", text2)  # 荨麻疹->并发症->喉水肿
            # exit()
            leval3KP, level3Rela = getNextPath(path, text2)

            sample_leval3KP = []
            for i in leval3KP:
                sample_leval3KP.append(removeRemain(i))

            judge_3prompt = f"""请根据用户的具体问题，结合目前的一级、二级以及三级路径知识进行逐级推理，判断用户的问题是否都能从知识路径中找到对应的知识路径。如果每个问题都能在知识路径中找到对应的知识路径，请回答“是”。如果至少有一个问题在知识路径中找不到对应的知识路径，请回答“否”。
                                            用户问题为：{question}
                                            已经确定的一级路径知识为：{text}
                                            已经确定的二级路径知识为：{text2}
                                            目前的三级路径知识为：{path}
                                            Let’s think step by step，请注意：形如A->r->B表示，A的r是B。例如：荨麻疹->并发症->喉水肿，表示荨麻疹的并发症是喉水肿。
                                            另外，请直接返回”是“或者”否“，无需进行额外的分析与回复。
                                            """
            print("三跳结果判断语句：", judge_3prompt)

            # 请直接回复现在已有的关系是否支撑用户问答，完全可以则回复”是“，如果有不能回答的则必须回复”否“。
            relstion_3result = getInfo(judge_3prompt)
            print("三跳结果：", relstion_3result)
            # exit()
            print("***************")
            if '是' in relstion_3result:  # 此时子图信息足够支撑用户回答，下面将该时刻的子图作为提示交给大模型进行回答
                print("该问题是系统判定只需要三级路径即可满足回答")
                pre3pathKnowledge = leval1KP + leval2KP + leval3KP
                # start_time = time.time()

                print(FinallAnswer(question, pre3pathKnowledge))
                end_time = time.time()
                elapsed_time = end_time - start_time  # 计算时间差
                print("响应时间为：", elapsed_time)
                # 判断子图大小，如果过大，考虑剪枝。
            else:
                print("System Error!")

    #针对一级路径进行剪枝
    pruning_prompt = f"""请输出你认为与用户意图不相关的一个或者几个关系，以列表的形式返回。例如：返回的关系列表应为['治疗方式', '药品推荐']
                    注意，你回答的答案只能从关系列表中选择，另外请直接返回列表结果，无需额外的分析与输出
                    用户问题为：{question}
                    目前的关系为：{level1Rela}
                    """
    relstion_result = getInfo(pruning_prompt)

    # 打印所有知识路径
    for start_node, paths in path.items():
        print(f"Paths starting from {start_node}:")
        for path in paths:
            print(" -> ".join([f"({triple[0]}, {triple[1]}, {triple[2]})" for triple in path]))

    query = f"match (n:Disease) where n.name='{entity}' return n"
    result = g.run(query).data()
    node = result[0]['n']
    relation_list = []
    for i in node:
        key = [key for key, val in key_dict.items() if val == i]
        relation_list.append(key)
    prompt = f"""
            请根据用户输入的问题，进行意图识别。判断关系列表中与用户输入最相关的一个或者几个关系，以列表的形式返回。例如用户输入的问题为：“我发现我有抬头纹怎么办？”，返回的关系列表应为['治疗方式', '药品推荐','就诊科室','推荐食品']
            注意，你回答的答案只能从关系列表中选择，另外请直接返回列表结果，无需额外的分析与输出
            关系列表：{relation_list}
            用户问题为：{question}
            """
    relstion_result = getInfo(prompt)
    print("用户意图为：",relstion_result)
    relstion_result = ast.literal_eval(relstion_result)  # 字符串强转成列表，这个列表可以包含多个关系，即多种意图


    relation_result_list =[]
    for i in relstion_result:
        query = f"MATCH(n)- [r]->(m)  WHERE n.name = '{entity}' AND r.name = '{i}' RETURN m"
        resu = g.run(query).data()
        for m in resu:
            end = m['m']['name']
            triple = f"<{entity}, {i}, {end}>"
            relation_result_list.append(triple)
    if len(relation_result_list) ==0:
        answer_prompt = f"""请根据用户输入的问题并根据你自己的知识储备，回答用户问题,要求回答尽量详尽，同时注意语言逻辑顺序，符合语境。
                                        用户问题为：{question}，
                                        从知识图谱中查询到的知识三元组为：{relation_result_list}
                              """
        final_answer = getInfo(answer_prompt)

        print("结合知识图谱查询以及大语言模型的整合，最终答案为：", final_answer)
    else:
        answer_prompt = f"""请根据用户输入的问题和已经从知识图谱中查询到的知识三元组并根据你自己的知识储备，回答用户问题,要求回答尽量详尽，符合语境。
                                用户问题为：{question}，
                                从知识图谱中查询到的知识三元组为：{relation_result_list}
                                """
        print("从知识图谱中查询到的知识三元组为： ", relation_result_list)

        final_answer = getInfo(answer_prompt)

        print("结合知识图谱查询以及大语言模型的整合，最终答案为：", final_answer)




def print_hi(question):

    ACT_res = getACTAnswer(question)
    if len(ACT_res) != 0:
        """
        直接进行多跳的关系路径推理
        """
        print(ACT_res)
        for i in ACT_res:
            find_relation(question, i)
    else:
        entity = getEntity(question)
        find_relation(question, entity)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    find_relation('我发现我有抬头纹怎么办?开什么药吃', '荨麻疹')
    question = '我发现我有抬头纹怎么办'
    print_hi(question)

