# 最小 ReAct Agent（5 行核心代码）
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """搜索互联网"""
    return "搜索结果..."

llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, [search], prompt="...")
executor = AgentExecutor(agent=agent, tools=[search])

result = executor.invoke({"input": "北京今天天气"})
print(result["output"])