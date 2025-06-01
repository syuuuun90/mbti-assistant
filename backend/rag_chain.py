# rag_chain.py

import os
from dotenv import load_dotenv

# .env から API キーを読み込む
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

# 埋め込み関数に API キーを渡して初期化
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# ベクトルストアを復元
vectorstore = Chroma(
    persist_directory="./vectorstore",
    embedding_function=emb,
    collection_name="mbti_docs"
)
# 類似度検索を使う設定（k件取得）
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAGチェーンの定義
chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    ),
    retriever=retriever,
    return_source_documents=True
)

def rag_reason(query: str):
    """
    query（説明生成用プロンプト）を受け取り、
    (reason: str, source_documents: List[Document]) を返します。
    """
    result = chain({"query": query})
    return result["result"], result["source_documents"]
