import json
import shutil
from pathlib import Path

import zvec
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI


class ZvecVectorStore(VectorStore):
    """基于 zvec 的 LangChain VectorStore 封装。"""

    def __init__(self, collection: zvec.Collection, embedding):
        self.collection = collection
        self.embedding = embedding

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        embedding,
        persist_path: Path,
        collection_name: str = "knowledge_base",
    ) -> "ZvecVectorStore":
        if persist_path.exists():
            shutil.rmtree(persist_path)

        dim = len(embedding.embed_query("dimension probe"))
        schema = zvec.CollectionSchema(
            name=collection_name,
            fields=[
                zvec.FieldSchema("page_content", zvec.DataType.STRING),
                zvec.FieldSchema("metadata_json", zvec.DataType.STRING),
            ],
            vectors=[
                zvec.VectorSchema(
                    "embedding",
                    zvec.DataType.VECTOR_FP32,
                    dim,
                    zvec.HnswIndexParam(metric_type=zvec.MetricType.COSINE),
                )
            ],
        )
        collection = zvec.create_and_open(path=str(persist_path), schema=schema)

        vectors = embedding.embed_documents([doc.page_content for doc in documents])
        zvec_docs = [
            zvec.Doc(
                id=f"doc_{i}",
                vectors={"embedding": vector},
                fields={
                    "page_content": doc.page_content,
                    "metadata_json": json.dumps(doc.metadata, ensure_ascii=False),
                },
            )
            for i, (doc, vector) in enumerate(zip(documents, vectors))
        ]
        collection.insert(zvec_docs)
        collection.flush()
        return cls(collection, embedding)

    @classmethod
    def from_texts(
        cls,
        texts: list[str],
        embedding,
        metadatas: list[dict] | None = None,
        persist_path: Path | None = None,
        **kwargs,
    ) -> "ZvecVectorStore":
        metadatas = metadatas or [{} for _ in texts]
        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]
        if persist_path is None:
            raise ValueError("persist_path is required for ZvecVectorStore")
        return cls.from_documents(documents, embedding, persist_path, **kwargs)

    def similarity_search(self, query: str, k: int = 4, **kwargs) -> list[Document]:
        query_vector = self.embedding.embed_query(query)
        results = self.collection.query(
            queries=zvec.Query(field_name="embedding", vector=query_vector),
            topk=k,
            output_fields=["page_content", "metadata_json"],
        )
        docs = []
        for result in results:
            metadata = json.loads(result.fields.get("metadata_json", "{}"))
            docs.append(
                Document(
                    page_content=result.fields["page_content"],
                    metadata=metadata,
                )
            )
        return docs


def load_pdf_documents(path: Path) -> list[Document]:
    reader = PdfReader(str(path))
    docs = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": str(path), "page": page_num},
                )
            )
    return docs


# 1. 加载文档
docs_dir = Path(__file__).resolve().parents[3] / "docs"
docs = [
    Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": str(path)})
    for path in docs_dir.rglob("*.md")
]
for path in docs_dir.rglob("*.pdf"):
    docs.extend(load_pdf_documents(path))

# 2. 分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,       # 每块 512 tokens
    chunk_overlap=64,     # 64 tokens 重叠
    length_function=len,
)
chunks = splitter.split_documents(docs)

# 3. 向量化 & 存储 — 本地 HuggingFace 模型 + zvec 向量库
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
zvec_path = Path(__file__).resolve().parents[3] / ".zvec_data"
vectorstore = ZvecVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_path=zvec_path,
)

# 4. 检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},  # 检索 Top-5
)

# 5. 提示词模板
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是基于知识库的助手。请根据以下参考资料回答问题。

参考资料：
{context}

回答要求：
- 优先使用参考资料中的信息
- 如果资料中没有相关信息，请说"根据现有资料无法回答"
- 回答使用与问题相同的语言"""),
    ("human", "{input}"),
])

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是基于知识库的助手。请根据用户问题回答问题。
你可以使用 search_knowledge_base 工具检索知识库。

回答要求：
- 优先使用知识库中的信息
- 如果资料中没有相关信息，请说"根据现有资料无法回答"
- 回答使用与问题相同的语言"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 6. LLM — 对接本地 LM Studio（OpenAI 兼容 API，默认 http://localhost:1234/v1）
# model 需与 LM Studio 中已加载的模型名称一致
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0,
)

# 7. RAG Chain — 先检索，再把结果传入 LLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# answer = rag_chain.invoke("如何设计一个Agent方案：帮用户规划一次旅行？")
# print(answer)

# 将 RAG 系统注册为 Agent 的 Tool
from langchain.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库，返回与查询最相关的文档片段。"""
    results = retriever.invoke(query)
    return "\n---\n".join([
        f"文档 {i+1}:\n" + doc.page_content
        for i, doc in enumerate(results)
    ])

# 在 Agent 中使用
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

tools = [search_knowledge_base]
agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)

print("=================================0")

# 直接 RAG 问答
answer = rag_chain.invoke("Agent适合什么场景？")
print(answer)

print("=================================1")

# Agent 模式（自动决定何时调用知识库）
result = agent_executor.invoke({
    "input": "Agent的工作原理是什么？"
})
print(result["output"])

print("=================================2")

# 直接 RAG 问答
answer = rag_chain.invoke("Loop-Engineering是什么？")
print(answer)

print("=================================3")

# Agent 模式（自动决定何时调用知识库）
result = agent_executor.invoke({
    "input": "Loop-Engineering为何如此重要？"
})
print(result["output"])

print("=================================4")