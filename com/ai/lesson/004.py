# 实战：完整 Planning 实现

from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

# Planning Prompt
PLAN_PROMPT = PromptTemplate(
    input_variables=["goal", "tools", "constraints"],
    template="""
    你是一个任务规划师。将以下目标分解为可执行步骤。

    目标: {goal}

    可用工具:
    {tools}

    约束:
    {constraints}

    请生成完整的执行计划:

    ## 计划
    1. [步骤1]
       - 操作:
       - 工具:
       - 依赖:
       - 预期输出:

    2. [步骤2]
       - 操作:
       - 工具:
       - 依赖:
       - 预期输出:

    ## 完成标准
    - 条件1
    - 条件2
    """
)

# 生成计划
chain = LLMChain(llm=llm, prompt=PLAN_PROMPT)
plan = chain.run(
    goal="帮我调研 OpenAI 最新模型",
    tools="search, read_url, write_file",
    constraints="最多 10 步，不要编造信息"
)