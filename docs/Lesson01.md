# 第一课：AI Agent 入门基础

## 学习目标

- 理解 AI Agent 的基本概念和核心架构
- 掌握 Agent 的五大核心组件及其作用
- 能够识别适合使用 Agent 的场景
- 了解主流 Agent 框架的特点

---

## 1.1 什么是 AI Agent？

### 定义

AI Agent（智能体）是一个能够感知环境、做出决策并采取行动的自主系统。与传统程序不同，Agent 具备以下特征：

| 特性 | 说明 |
|------|------|
| **感知能力** | 通过工具和环境接口获取信息 |
| **决策能力** | 基于目标和分析选择行动方案 |
| **行动能力** | 调用工具执行具体操作 |
| **自主性** | 在人类监督下独立完成任务 |

### Agent vs 传统程序

```
传统程序：输入 → 处理 → 输出（固定流程）
Agent    ：感知 → 思考 → 规划 → 行动 → 反思（动态循环）
```

---

## 1.2 Agent 的核心架构

### 五大组件详解

#### 1. LLM（大语言模型）- "大脑"

**作用**：理解任务、生成推理、调用工具

**关键能力**：
- 语义理解与意图识别
- 多步推理与规划
- 代码生成与调试
- 自然语言交互

**常用模型**：
| 模型 | 特点 | 适用场景 |
|------|------|----------|
| GPT-4o | 全能型，上下文长 | 复杂任务 |
| Claude 3.5 Sonnet | 代码能力强 | 开发类 Agent |
| Gemini 1.5 Pro | 超长上下文（200K+） | 文档分析 |
| Llama 3.1 70B | 开源首选 | 私有化部署 |

#### 2. Memory（记忆系统）- "短期 + 长期记忆"

**短期记忆**：
- Context Window：当前对话的上下文
- Session State：会话级别的变量存储

**长期记忆**：
```
┌─────────────────┐     ┌─────────────────┐
│   Working Memory │────▶│ Long-term Memory│
│  (RAM/Redis)     │     │(Vector DB)      │
└─────────────────┘     └─────────────────┘
```

**记忆类型**：
| 类型 | 存储内容 | 检索方式 |
|------|----------|----------|
| Episodic | 具体事件经历 | 语义相似度搜索 |
| Semantic | 抽象知识概念 | 关键词匹配 |
| Procedural | 技能操作序列 | 任务触发调用 |

#### 3. Planning（规划系统）- "任务拆解器"

**核心流程**：
```
用户目标 → 子任务分解 → 执行顺序编排 → 动态调整
```

**常见策略**：
| 策略 | 适用场景 | 复杂度 |
|------|----------|--------|
| **线性规划** | 简单单线程任务 | ★☆☆ |
| **树搜索 (Tree-Search)** | 多分支决策 | ★★★ |
| **图规划 (Graph-of-Thoughts)** | 复杂推理链 | ★★★★ |
| **ReAct** | 需要观察反馈的任务 | ★★☆ |

#### 4. Tools（工具集）- "手脚"

**内置工具**：
```python
# 代码执行环境
CodeInterpreterTool()      # Jupyter Notebook 沙箱
SandboxExecutor()          # Docker 容器隔离

# 系统操作
FileSystemTool()           # 读写文件/目录
ShellTool()                # 运行命令行
BrowserTool()              # Web 浏览与截图

# 数据访问
DatabaseConnector()        # SQL/NoSQL 查询
APIWrapper()               # HTTP 请求封装
```

**自定义工具注册**：
```yaml
tools:
  - name: weather_api
    description: "获取天气信息"
    parameters:
      location: string
      units: enum [celsius, fahrenheit]
    implementation: |
      import requests
      def call(location, units):
          return requests.get(f"https://api.weather.com/{location}")
```

#### 5. Human Feedback（人类反馈）- "刹车与方向盘"

**反馈机制**：
| 类型 | 触发条件 | 处理方式 |
|------|----------|----------|
| **Approval** | Agent 请求确认时 | 继续执行或修改 |
| **Correction** | 用户指出错误时 | 重新规划路径 |
| **Stop** | 用户中断时 | 保存状态并退出 |

---

## 1.3 Agent 的工作流程

### ReAct 范式（Reason + Act）

```
循环：
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Think     │───▶│   Action    │───▶│   Observe   │
  │ (推理)      │     │ (行动)      │     │ (观察)      │
  └─────────────┘     └─────────────┘     └─────────────┘
       ▲                              │
       └──────────────────────────────┘
```

### 完整示例：搜索并总结新闻

**用户输入**："帮我总结一下最近关于 AI Agent 的新闻"

1. **思考**：需要查找最新信息 → 使用搜索引擎
2. **行动**：调用 Google Search API，关键词 "AI agent news June 2024"
3. **观察**：返回搜索结果列表
4. **思考**：结果太多，先访问几个权威来源
5. **行动**：打开 TechCrunch 和 The Verge 的链接
6. **观察**：获取页面内容
7. **思考**：提取关键信息并去重
8. **行动**：生成总结报告
9. **输出**：呈现给用户

---

## 1.4 适合使用 Agent 的场景

### ✅ 推荐场景

| 类别 | 具体任务 |
|------|----------|
| **多步骤自动化** | 跨平台数据收集、报表生成 |
| **复杂决策支持** | 数据分析 + 建议输出 |
| **交互式任务** | 客服机器人、教学助手 |
| **代码相关工作** | 调试辅助、文档生成 |
| **研究分析** | 文献综述、竞品调研 |

### ❌ 不推荐场景

- 简单 CRUD 操作（用传统 API）
- 确定性计算任务（直接写函数）
- 实时性要求极高（<100ms）的场景
- 需要精确控制每一步的流程

---

## 1.5 主流 Agent 框架对比

| 框架 | 语言 | 特点 | 学习曲线 |
|------|------|------|----------|
| **LangChain** | Python/JS | 生态最丰富，文档完善 | ★★☆ |
| **LlamaIndex** | Python | RAG 专用，数据索引强 | ★★★ |
| **AutoGen (Microsoft)** | Python | 多 Agent 协作，企业级 | ★★★★ |
| **Semantic Kernel** | C#/Python | .NET 集成好，微软生态 | ★★★ |
| **Dify / Flowise** | 无代码 | 可视化编排，快速原型 | ★★ |

---

## 1.6 实践练习

### 练习 1：创建你的第一个 Agent

使用 LangChain Python SDK：

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Basic math operations"
    ),
    Tool(
        name="Search",
        func=search_api,  # 假设已定义
        description="Web search"
    )
]

agent = initialize_agent(tools, llm=OpenAI(), agent="zero-shot-react-description")
agent.run("计算 2024 * 365 并告诉我这是多少天")
```

### 练习 2：设计一个 Agent 方案

**任务**：帮用户规划一次旅行

**要求**：列出需要调用的工具、记忆类型、规划策略

---

## 课后思考题

1. Agent 的自主性边界在哪里？如何防止失控？
2. 长上下文（100K+ tokens）对 Agent 能力有什么影响？
3. 多 Agent 协作时，如何避免循环依赖和死锁？
4. 记忆系统的设计中，哪些信息应该长期保存，哪些应该遗忘？

---

## 参考资料

- [LangChain Documentation](https://python.langchain.com/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- 《AI Agents: Building Autonomous Systems》(2024)
- Arxiv: "ReAct: Synergizing Reasoning and Acting in Language Models"
