# backend/main.py

import os
import json
import pathlib
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from rag_chain import rag_reason
from gpt_compat import explain_compatibility

# ─── 環境変数の読み込み ───
# ① .env 読み込み（APIキー）
load_dotenv(pathlib.Path(__file__).parent.parent / ".env")

# ② JSONファイルの絶対パスを動的に構築
BASE_DIR = pathlib.Path(__file__).parent.parent   # プロジェクトルート
DATA_PATH = BASE_DIR / "data" / "mbti_all_premium_combined.json"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"JSONファイルが見つかりません: {DATA_PATH}")

with open(DATA_PATH, encoding="utf-8") as f:
    mbti_data = json.load(f)

# ─── FastAPIアプリ定義 ───
app = FastAPI(title="MBTI適職診断API")

# CORS設定（開発用：全許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["*"],
)

# ─── リクエスト/レスポンスモデル ───
class DiagnoseRequest(BaseModel):
    mbti_type: str

class DiagnoseResponse(BaseModel):
    traits: List[str]
    jobs: List[str]
    reason: str
    sources: List[Dict[str, Any]]  # {"source": str, "text": str}

class CompatResponse(BaseModel):
    compat_types: List[str]
    compat_reason: str

# ─── /recommend エンドポイント ───
@app.post("/recommend", response_model=DiagnoseResponse)
async def recommend(req: DiagnoseRequest):
    mbti = req.mbti_type.upper()
    if mbti not in mbti_data:
        raise HTTPException(status_code=404, detail="Unknown MBTI type")

    # 特性と職業取得
    raw = mbti_data[mbti]["work"]["strength"]
    traits = [raw] if isinstance(raw, str) else raw
    jobs = mbti_data[mbti].get("recommendedJobs", [])

    # RAGで理由＋ソース取得
    prompt = (
        f"{mbti}型の人は「{', '.join(traits)}」という特性を持ち、"
        f"おすすめ職業は「{', '.join(jobs)}」です。"
        "上記を踏まえ、なぜ向いているかを200文字以内で説明してください。"
    )
    reason, docs = rag_reason(prompt)

    # ソースドキュメント整形
    sources = []
    for doc in docs:
        src = doc.metadata.get("job", doc.metadata.get("source"))
        text = doc.page_content
        sources.append({"source": src, "text": text})

    return {
        "traits": traits,
        "jobs": jobs,
        "reason": reason,
        "sources": sources
    }

# ─── /compat エンドポイント ───
@app.post("/compat", response_model=CompatResponse)
async def compat(req: DiagnoseRequest):
    mbti = req.mbti_type.upper()
    compat = mbti_data[mbti].get("compatibleTypes", [])
    if not compat:
        raise HTTPException(status_code=404, detail="No compatibility data")
    compat_reason = explain_compatibility(mbti, compat)
    return {"compat_types": compat, "compat_reason": compat_reason}
