from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 1. 创建向量库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

class AgentMemory:
    """Agent 工作记忆"""

    def __init__(self):
        self.short_term = []      # 当前对话历史
        self.long_term = []       # 长期记忆 ID 列表
        self.working = {}         # 当前任务状态

    def add_to_working(self, key: str, value: any):
        """存入工作记忆（当前任务）"""
        self.working[key] = value

    def get_from_working(self, key: str) -> any:
        """从工作记忆取出"""
        return self.working.get(key)

    def clear_working(self):
        """任务完成，清空工作记忆"""
        self.working = {}

    def save_to_long_term(self, text: str):
        """保存重要信息到长期记忆"""
        vectorstore.add_texts([text])
        self.long_term.append(text)

# 使用
memory = AgentMemory()
memory.add_to_working("search_results", [...])  # 搜索结果
memory.add_to_working("current_step", 3)        # 当前步骤
memory.add_to_working("total_steps", 5)         # 总步骤

# 任务完成
memory.save_to_long_term("用户关注 Python 项目")
memory.clear_working()