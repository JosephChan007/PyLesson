from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# State: 消息累积
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 追加模式

# 工具
def search(query: str) -> str:
    """搜索互联网"""
    return f"搜索结果: {query}..."

tools = [search]
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0,
).bind_tools(tools)

# Agent 节点
def agent_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 路由：工具还是结束？
def should_continue(state: AgentState) -> Literal["tools", END]:
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END

# 构建
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")  # ← 循环！

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage(content="搜索 LangGraph 教程")]})
print(result["messages"][-1].content)