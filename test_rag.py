# test_rag.py
import os, json, pathlib
from dotenv import load_dotenv
from rag_chain import rag_reason

# .env のパスを明示的に指定して読み込む
BASE = pathlib.Path(__file__).parent
load_dotenv(BASE / ".env")

# テスト用プロンプト
prompt = (
    "INTJ型の人は戦略的で計画的です。"
    "おすすめ職業は研究者やコンサルタントです。"
    "なぜ向いているのか200文字以内で説明してください。"
)

# 実行
reason, docs = rag_reason(prompt)

print("🧠 Reason:\n", reason, "\n")
print("📑 Sources:")
for doc in docs:
    src = doc.metadata.get("job", doc.metadata.get("source"))
    print(f"- ({src}) {doc.page_content[:100]}…")
