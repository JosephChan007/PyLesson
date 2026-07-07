from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

# 1. 定义 State
class State(TypedDict):
    query: str
    classification: str
    response: str

# 2. 定义 Node
def classify(state: State) -> dict:
    q = state["query"]
    if "代码" in q:
        return {"classification": "code"}
    elif "bug" in q:
        return {"classification": "bug"}
    return {"classification": "general"}

def handle_code(state: State) -> dict:
    return {"response": f"代码问题: {state['query']}"}

def handle_bug(state: State) -> dict:
    return {"response": f"BUG问题: {state['query']}"}

def handle_general(state: State) -> dict:
    return {"response": f"通用问题: {state['query']}"}

def route(state: State) -> Literal["handle_code", "handle_bug", "handle_general"]:
    if state["classification"] == "code":
        return "handle_code"
    elif state["classification"] == "bug":
        return "handle_bug"
    return "handle_general"
# 3. 条件路由

# 4. 构建图
builder = StateGraph(State)
builder.add_node("classify", classify)
builder.add_node("handle_code", handle_code)
builder.add_node("handle_general", handle_general)
builder.add_node("handle_bug", handle_bug)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("handle_code", END)
builder.add_edge("handle_general", END)
builder.add_edge("handle_bug", END)

graph = builder.compile()
# result = graph.invoke({"query": "有 代码 怎么修"})
# result = graph.invoke({"query": "有 bug 怎么修"})
result = graph.invoke({"query": "有 问题 怎么修"})
print(result["response"])  # → "代码问题: 代码有 bug 怎么修"





