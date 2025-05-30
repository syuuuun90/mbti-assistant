# gpt_reason.py

import os
import openai
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

def generate_reason(mbti_type: str, traits: list, jobs: list) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # ◆ フォーマット指定を追加
    system_prompt = (
        "あなたはプロのキャリアアドバイザーです。"
        "回答は「● ● ●」のような３つの短い箇条書きで、日本語200文字以内にまとめてください。"
    )

    # ◆ traits と jobs を両方含めたユーザープロンプト
    user_prompt = (
        f"{mbti_type}型の人は「{', '.join(traits)}」という特性を持ち、"
        f"おすすめの職業は「{', '.join(jobs)}」です。"
        "これらを踏まえ、なぜその職業群に向いているのかを箇条書きで教えてください。"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.3,      # 精度重視で低く設定
        max_tokens=200        # 200トークン以内に制限
    )
    return response.choices[0].message.content


    return response["choices"][0]["message"]["content"]
