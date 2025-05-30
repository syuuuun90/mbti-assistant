// frontend/components/MbtiSelector.js
"use client";

export default function MbtiSelector({ onSubmit }) {
  const mbtiTypes = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ISTP","ISFP",
    "ESTJ","ESFJ","ESTP","ESFP",
  ];

  return (
    <div className="flex items-center space-x-2">
      <select
        id="mbti"
        className="border p-2 rounded flex-1"
        defaultValue=""
      >
        <option value="" disabled>
          MBTIタイプを選んでください
        </option>
        {mbtiTypes.map((t) => (
          <option key={t} value={t}>
            {t}
          </option>
        ))}
      </select>
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded"
        onClick={() => {
          const select = document.getElementById("mbti");
          if (select.value) onSubmit(select.value);
        }}
      >
        診断開始
      </button>
    </div>
  );
}
