import json
import os
from dotenv import load_dotenv
import streamlit as st

from gpt_reason import generate_reason
from gpt_compat import explain_compatibility
from rag_chain import rag_reason

# ① .env を読む
load_dotenv()

# ② JSON データをロード
with open("data/mbti_all_premium_combined.json", encoding="utf-8") as f:
    mbti_data = json.load(f)

# ③ Streamlit UI
st.title("MBTI × 適職診断ボット（MVP）")

# JSONのキーを使って選択肢を作成
mbti_options = list(mbti_data.keys())
selected_type = st.selectbox("あなたのMBTIタイプを選んでください", mbti_options)

if st.button("診断開始"):
    st.subheader("🔍 診断結果")

    # ④ JSON から特性と職業を取得
    raw_trait = mbti_data[selected_type]["work"]["strength"]
    traits = [raw_trait]
    jobs   = mbti_data[selected_type].get("recommendedJobs", [])

    # 特性を表示
    st.write(f"あなたの特性（{selected_type}）:")
    for t in traits:
        st.write(f"- {t}")

    # おすすめ職業を表示
    st.write("向いている職業の一例：")
    for j in jobs:
        st.write(f"- {j}")

    # ➤ 相性の良いタイプを JSON から取得
    compat = mbti_data[selected_type].get("compatibleTypes", [])
    if compat:
        st.write("🤝 相性の良い他のMBTIタイプ：")
        st.write("、".join(compat))

    # 相性理由も出す
    if compat:
        with st.spinner("AIが相性理由を考えています..."):
            comp_reason = explain_compatibility(selected_type, compat)
        st.write("💬 相性が良い理由：")
        st.info(comp_reason)

    # ⑤ RAGで理由＋ソースを取得
    prompt = (
        f"{selected_type}型の人は「{', '.join(traits)}」の特性をもち、"
        f"おすすめ職業は「{', '.join(jobs)}」です。"
        "上記を踏まえ、なぜ向いているかを200文字以内で説明してください。"
    )
    with st.spinner("AIが診断理由を考えています..."):
        reason, docs = rag_reason(prompt)

    st.write("🧠 向いている理由：")
    st.success(reason)

    st.caption("【根拠テキスト】")
    for doc in docs:
        src = doc.metadata.get("job", doc.metadata["source"])
        st.caption(f"- ({src}) {doc.page_content[:100]}…")
