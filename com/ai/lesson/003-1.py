from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 1. 创建向量库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

# 2. 存入记忆
def store_memory(text: str):
    """将文本存入长期记忆"""
    vectorstore.add_texts([text])

# 3. 实际使用
store_memory("用户喜欢 Python，不喜欢 Java")
store_memory("项目使用 FastAPI 框架")
store_memory("用户关注代码质量，要求写测试")

def retrieve_memory(query: str, k: int = 3) -> list:
    """从长期记忆中检索相关内容"""
    return vectorstore.similarity_search(query, k=k)


# 实际使用
user_request = "用户的技术偏好"
relevant = retrieve_memory(user_request)
# → ["用户喜欢 Python，不喜欢 Java", "项目使用 FastAPI 框架"]

# 注入到 prompt
context = "\n".join(relevant)
prompt = f"""
已知用户信息:
{context}

用户请求: {user_request}
"""