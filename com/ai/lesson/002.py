from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_classic import create_react_agent, AgentExecutor

# 1. 定义所有可能工具（但不全注册）
@tool
def weather_search(city: str) -> str:
    """搜索指定城市的实时天气。当用户询问天气、温度、湿度、风力时使用。"""
    ...

@tool
def file_read(path: str) -> str:
    """读取本地文件内容。当用户需要查看文件内容时使用。"""
    ...

ALL_TOOLS = {
    "weather_search": weather_search,
    "file_read": file_read,
}

# 2. 动态选择工具
def select_tools(user_request: str, llm: ChatOpenAI) -> list:
    """根据用户请求，选择最相关的工具"""
    prompt = f"""
    用户请求: {user_request}

    可用工具:
    - weather_search: 搜索指定城市的实时天气。当用户询问天气、温度、湿度、风力时使用。
    - file_read: 读取本地文件内容。当用户需要查看文件内容时使用。

    选择最相关的 1-2 个工具，返回 JSON 数组:
    ["tool_name1", "tool_name2"]
    """
    tools_str = llm.invoke(prompt).content
    return [ALL_TOOLS[name] for name in json.loads(tools_str)]

# 3. 执行：动态注册 + 运行
tools = select_tools(user_request, llm)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": user_request})