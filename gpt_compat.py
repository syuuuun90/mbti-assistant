# gpt_compat.py
import os, openai
from dotenv import load_dotenv
load_dotenv()

def explain_compatibility(my_type: str, others: list) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        f"{my_type}型の人は、{', '.join(others)}型の人と相性が良いとされています。"
        "なぜこの組み合わせが良いのか、日本語で短く説明してください。"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5,
        max_tokens=100
    )
    return resp.choices[0].message.content
