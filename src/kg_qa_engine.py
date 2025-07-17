# src/kg_qa_engine.py
import logging
import time
from typing import List, Dict, Optional, Tuple

from py2neo import Graph

import config
from src.llm_interface import LLMInterface
from src.similarity_utils import calculate_cosine_similarity
from src.utils import load_json_file, group_paths_by_relation, parse_path_string

from ACTree.tree import getACTAnswer


class KnowledgeGraphQA:
    """
    基于知识图谱和大型语言模型的医疗问答引擎。
    """

    def __init__(self):
        """初始化引擎，连接数据库，加载数据和模型。"""
        logging.info("Initializing KnowledgeGraphQA Engine...")

        # 1. 初始化LLM接口
        self.llm = LLMInterface()

        # 2. 连接Neo4j图数据库
        try:
            self.graph = Graph(
                host=config.NEO4J_CONFIG["host"],
                user=config.NEO4J_CONFIG["user"],
                password=config.NEO4J_CONFIG["password"]
            )
            self.graph.run("RETURN 1")  # 测试连接
            logging.info("Successfully connected to Neo4j database.")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise ConnectionError("Could not connect to Neo4j database.") from e

        # 3. 加载静态数据文件
        self.keshi_data = load_json_file(config.DATA_PATHS["keshi_disease"])
        self.buwei_data = load_json_file(config.DATA_PATHS["classify"])
        if not self.keshi_data or not self.buwei_data:
            raise FileNotFoundError("Required data files are missing or empty.")

        logging.info("KnowledgeGraphQA Engine initialized successfully.")

    def _find_entity_candidates(self, department: str, body_part: str) -> List[str]:
        """根据科室和部位找到候选疾病实体的交集。"""
        keshi_list = self.keshi_data.get(department, [])
        buwei_list = self.buwei_data.get(body_part, [])

        # 使用集合操作找到交集
        intersection = list(set(keshi_list) & set(buwei_list))
        logging.info(f"Found {len(intersection)} candidate entities from intersection.")
        logging.debug(f"Candidates: {intersection[:10]}...")  # 只打印前10个
        return intersection

    def _select_best_entity(self, candidates: List[str], question: str) -> Optional[str]:
        """从候选实体中选择最匹配的实体。"""
        if not candidates:
            return None

        # 如果候选者太多，通过相似度筛选
        if len(candidates) > config.MAX_INTERSECTION_LENGTH:
            logging.info("Too many candidates, using similarity ranking...")

            # 1. 提取关键词
            keyword_prompt = config.PROMPTS["extract_keyword"].format(question=question)
            keyword = self.llm.get_response(keyword_prompt)
            logging.info(f"Extracted keyword for similarity: '{keyword}'")

            # 2. 计算相似度
            similarities = {
                candidate: calculate_cosine_similarity(keyword, candidate)
                for candidate in candidates
            }

            # 3. 排序并获取Top K
            sorted_candidates = sorted(similarities, key=similarities.get, reverse=True)
            top_candidates = sorted_candidates[:config.SIMILARITY_TOP_K]
            logging.info(f"Top {len(top_candidates)} candidates after similarity ranking: {top_candidates}")

            # 将筛选后的列表交给LLM最终选择
            candidates_to_llm = top_candidates
        else:
            candidates_to_llm = candidates

        # 使用LLM从列表中选择最终实体
        find_entity_prompt = config.PROMPTS["find_entity_from_list"].format(
            question=question,
            entity_list=candidates_to_llm
        )
        final_entity = self.llm.get_response(find_entity_prompt)

        if final_entity == "无" or not final_entity:
            logging.warning("LLM could not find a matching entity from the list.")
            return None

        logging.info(f"Final entity selected: '{final_entity}'")
        return final_entity

    def extract_main_entity(self, question: str) -> Optional[str]:
        """
        从用户问题中提取核心疾病实体。
        这是原 `getEntity` 和 `getIntersection` 的重构版本。
        """
        # 1. 使用LLM确定科室
        dep_prompt = config.PROMPTS["get_department"].format(
            question=question, department_list=config.DEPARTMENTS_LIST
        )
        department = self.llm.get_response(dep_prompt)
        logging.info(f"Identified department: '{department}'")

        # 2. 使用LLM确定部位
        part_prompt = config.PROMPTS["get_body_part"].format(question=question)
        body_part = self.llm.get_response(part_prompt)
        logging.info(f"Identified body part: '{body_part}'")

        if not department or not body_part:
            logging.error("Failed to determine department or body part.")
            return None

        # 3. 查找候选实体
        candidates = self._find_entity_candidates(department, body_part)

        # 4. 从候选实体中选择最佳实体
        return self._select_best_entity(candidates, question)

    def _find_paths_from_node(self, entity: str) -> List[Tuple[str, str, str]]:
        """从给定实体出发，查找所有一步关系路径。"""
        query = f"MATCH (n)-[r]->(e) WHERE n.name='{entity}' RETURN n.name, r.name, e.name"
        try:
            results = self.graph.run(query).data()
            paths = [(res['n.name'], res['r.name'], res['e.name']) for res in results]
            logging.debug(f"Found {len(paths)} one-hop paths from '{entity}'.")
            return paths
        except Exception as e:
            logging.error(f"Error querying paths from Neo4j for entity '{entity}': {e}")
            return []

    def _iterative_reasoning(self, question: str, start_entity: str) -> str:
        """
        执行多跳推理来寻找答案。
        这是对原 `find_relation` 函数的重大重构，使用循环代替了复杂的if-elif。
        """
        all_knowledge = []
        current_entities = {start_entity}

        for hop in range(1, config.MAX_SEARCH_DEPTH + 1):
            logging.info(f"--- Starting Hop {hop} ---")

            # 在当前跳中发现的新路径
            hop_paths = []
            for entity in current_entities:
                hop_paths.extend(self._find_paths_from_node(entity))

            if not hop_paths:
                logging.warning(f"No further paths found from entities: {current_entities}. Stopping.")
                break

            all_knowledge.extend(hop_paths)
            formatted_knowledge = group_paths_by_relation(all_knowledge)

            # 判断当前知识是否足够回答问题
            judge_prompt = config.PROMPTS["judge_path_sufficiency"].format(
                question=question,
                knowledge_paths=formatted_knowledge
            )
            sufficiency = self.llm.get_response(judge_prompt)
            logging.info(f"Hop {hop} sufficiency check result: '{sufficiency}'")

            if '是' in sufficiency:
                logging.info("Knowledge is sufficient. Generating final answer.")
                break  # 知识足够，跳出循环

            if hop == config.MAX_SEARCH_DEPTH:
                logging.warning("Reached max search depth. Using available knowledge.")
                break  # 达到最大深度，跳出循环

            # 如果知识不足，选择下一跳的路径
            formatted_hop_paths = group_paths_by_relation(hop_paths)
            select_prompt = config.PROMPTS["select_next_hop_path"].format(
                question=question,
                previous_path=f"Starting from '{start_entity}'",  # 简化，可以做得更复杂
                path_options=formatted_hop_paths
            )
            next_path_str = self.llm.get_response(select_prompt)
            logging.info(f"LLM selected next path to expand: '{next_path_str}'")

            _, _, next_tails = parse_path_string(next_path_str)
            if not next_tails:
                logging.warning("Could not determine next entity to expand. Stopping.")
                break

            # 更新下一轮要探索的实体
            current_entities = set(next_tails)

        # 循环结束，生成最终答案
        final_formatted_knowledge = group_paths_by_relation(all_knowledge)
        answer_prompt = config.PROMPTS["generate_final_answer"].format(
            question=question,
            knowledge="\n".join(final_formatted_knowledge)
        )

        start_time = time.time()
        final_answer = self.llm.get_response(answer_prompt)
        elapsed_time = time.time() - start_time
        logging.info(f"Final answer generation took {elapsed_time:.2f} seconds.")

        return final_answer

    def answer(self, question: str) -> str:
        """
        问答系统的主要入口点。
        """
        logging.info(f"Received question: '{question}'")

        # 1. 尝试使用AC自动机进行快速实体匹配
        act_results = getACTAnswer(question)  # 假设此函数返回实体列表
        if act_results:
            main_entity = act_results[0]  # 简单地取第一个结果
            logging.info(f"Entity '{main_entity}' found directly via AC-Trie.")
        else:
            # 2. 如果AC自动机未找到，则通过LLM进行实体链接
            logging.info("No entity found via AC-Trie, starting LLM-based entity extraction.")
            main_entity = self.extract_main_entity(question)

        if not main_entity:
            return "抱歉，我无法在知识库中找到与您问题相关的核心疾病信息，请您尝试换一个更具体的问题。"

        # 3. 找到实体后，开始迭代推理
        final_answer = self._iterative_reasoning(question, main_entity)

        return final_answer