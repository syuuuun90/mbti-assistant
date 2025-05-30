# build_vectorstore.py

import json
import os
from dotenv import load_dotenv
from pathlib import Path

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document  # ← 追加

# .env から API キーを読み込む
load_dotenv()

# JSON をロード
DATA_PATH = Path(__file__).parent / "data" / "mbti_all_premium_combined.json"
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

# チャンク分割設定
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# Document オブジェクトのリストを作成
docs = []
for mbti_type, info in data.items():
    desc = info.get("work", {}).get("description", "")
    # 説明文をチャンク化して追加
    for i, chunk in enumerate(text_splitter.split_text(desc)):
        docs.append(
            Document(
                page_content=chunk,
                metadata={"source": mbti_type, "chunk": i}
            )
        )
    # 職業リストも追加
    for job in info.get("recommendedJobs", []):
        docs.append(
            Document(
                page_content=f"{mbti_type} が向いている職業例：{job}",
                metadata={"source": mbti_type, "job": job}
            )
        )

# 埋め込みモデル初期化
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Chroma ストア生成・永続化
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=emb,
    persist_directory="vectorstore",
    collection_name="mbti_docs"
)
vectorstore.persist()

print("✅ vectorstore のビルドが完了しました。")
