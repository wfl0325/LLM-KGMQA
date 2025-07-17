# src/llm_interface.py
import time
import logging

from LLM.GLM4IE import getInfo

class LLMInterface:
    """封装与大语言模型交互的接口"""
    def __init__(self, model_name="GLM4IE"):
        self.model_name = model_name
        logging.info(f"LLM Interface initialized with model: {self.model_name}")

    def get_response(self, prompt: str) -> str:
        """
        发送Prompt给LLM并获取响应。

        Args:
            prompt (str): 发送给模型的提示。

        Returns:
            str: 模型的文本响应。
        """
        try:
            start_time = time.time()
            response = getInfo(prompt)
            elapsed_time = time.time() - start_time
            logging.debug(f"LLM call took {elapsed_time:.2f} seconds.")
            return response.strip().strip("'\"")
        except Exception as e:
            logging.error(f"Error calling LLM: {e}")
            return "" # 返回空字符串表示出错