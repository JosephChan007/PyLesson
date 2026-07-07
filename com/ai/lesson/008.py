from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# 工具
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"计算错误: {e}"


def search(query: str) -> str:
    """搜索互联网"""
    return f"搜索结果: {query}..."

# self_correcting_agent.py — 完整可运行
class State(TypedDict):
    messages: Annotated[list, add_messages]
    quality_score: float
    correction_count: int

tools = [calculator, search]
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0,
)
eval_llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0,
)

def agent(state: State):
    """主 Agent: 调用 LLM + 工具"""
    response = llm.bind_tools(tools).invoke([
        SystemMessage("你是精确的助手，不确定时用工具验证。"),
        *state["messages"]
    ])
    return {"messages": [response]}

def evaluate(state: State):
    """LLM 自我评分 (0-1)"""
    last = state["messages"][-1]
    score = float(eval_llm.invoke(
        f"评分(0-1): {last.content}"
    ).content.strip())
    return {"quality_score": score}

def correct(state: State):
    """修正低分回答"""
    last = state["messages"][-1]
    response = llm.invoke([
        SystemMessage("修正以下回答的错误"),
        HumanMessage(f"评分{state['quality_score']}:\n{last.content}")
    ])
    return {
        "messages": [response],
        "correction_count": state["correction_count"] + 1
    }

# 路由
def after_agent(state) -> Literal["tools", "evaluate"]:
    return "tools" if state["messages"][-1].tool_calls else "evaluate"

def after_eval(state) -> Literal["correct", END]:
    if state["quality_score"] < 0.7 and state["correction_count"] < 2:
        return "correct"
    return END

# 构建
builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_node("evaluate", evaluate)
builder.add_node("correct", correct)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", after_agent)
builder.add_edge("tools", "agent")       # 工具→Agent 循环
builder.add_conditional_edges("evaluate", after_eval)
builder.add_edge("correct", "evaluate")   # 修正后重新评估

graph = builder.compile()

# 执行：Agent 回答 → 自我评分 → 低分则修正 → 重新评估
result = graph.invoke({
    "messages": [HumanMessage(content="计算 123 * 456 等于多少？")],
    "quality_score": 0.0,
    "correction_count": 0,
})

print(f"评分: {result['quality_score']}")
print(f"修正次数: {result['correction_count']}")
print(result["messages"][-1].content)