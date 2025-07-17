# a_main_entry_point.py
import logging
from src.kg_qa_engine import KnowledgeGraphQA


def setup_logging():
    """配置日志记录器。"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


if __name__ == '__main__':
    setup_logging()

    try:
        # 1. 创建问答引擎实例
        qa_system = KnowledgeGraphQA()

        # 2. 提出问题
        question = '我发现我有脑挫裂伤怎么办？'

        # 3. 获取答案
        answer = qa_system.answer(question)

        # 4. 打印最终结果
        print("\n" + "=" * 50)
        print(f"用户问题: {question}")
        print("=" * 50)
        print(f"智能问答系统回复:\n{answer}")
        print("=" * 50)

    except ConnectionError as e:
        logging.error(f"A critical connection error occurred: {e}")
    except FileNotFoundError as e:
        logging.error(f"A required data file was not found: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main process: {e}", exc_info=True)