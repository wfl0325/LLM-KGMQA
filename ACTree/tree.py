import ahocorasick
town_path = 'D:\\王飞龙\\PostgraduateLife\\论文\KGGPT\\Neo4jQA\\data\\disease.txt'


def build_actree(wordlist):
    actree = ahocorasick.Automaton()

    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    # print("actree: ", actree)
    return actree


def check_town(question, region_tree):
    region_wds = []
    for i in region_tree.iter(question):
        wd = i[1][1]
        region_wds.append(wd)
    stop_wds = []
    for wd1 in region_wds:
        for wd2 in region_wds:
            if wd1 in wd2 and wd1 != wd2:
                stop_wds.append(wd1)
    final_wds = [i for i in region_wds if i not in stop_wds]
    return final_wds
    # final_dict = {i: wdtype_dict.get(i) for i in final_wds}
    # return final_dict

def getACTAnswer(text):
    town_wds = [i.strip() for i in open(town_path, encoding='utf-8') if i.strip()]
    region_words = set(town_wds)
    # print("WSDE")
    region_tree = build_actree(list(region_words))
    final_wds = check_town(text, region_tree)
    return final_wds

if __name__ == "__main__":
    getACTAnswer('你是三河古镇吗撒旦是插电')