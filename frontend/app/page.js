// frontend/app/page.js
"use client";

import { useState } from "react";
import MbtiSelector from "../components/MbtiSelector";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleDiagnose(type) {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mbti_type: type }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("API呼び出しに失敗しました");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">MBTI 適職診断ボット</h1>
      <MbtiSelector onSubmit={handleDiagnose} />

      {loading && <p className="mt-4">診断中…しばらくお待ちください。</p>}

      {result && (
        <section className="mt-6 space-y-6">
          <div>
            <h2 className="text-xl font-semibold">🧩 特性</h2>
            {result.traits.map((t) => (
              <p key={t}>- {t}</p>
            ))}
          </div>
          <div>
            <h2 className="text-xl font-semibold">💼 職業</h2>
            {result.jobs.map((j) => (
              <p key={j}>- {j}</p>
            ))}
          </div>
          <div>
            <h2 className="text-xl font-semibold">🧠 理由</h2>
            <p>{result.reason}</p>
          </div>
          <div>
            <h2 className="text-xl font-semibold">📑 根拠テキスト</h2>
            {result.sources.map((s, i) => (
              <p key={i} className="text-sm text-gray-500">
                ({s.source}) {s.text.slice(0, 100)}…
              </p>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
