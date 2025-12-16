import { useState } from "react";

interface SurveyCardProps {
  question: any;
  statistic?: React.ReactNode;
  onSubmit: (value: string) => void;
  loading?: boolean;
}

export default function SurveyCard({
  question,
  statistic,
  onSubmit,
  loading,
}: SurveyCardProps) {
  const [value, setValue] = useState("");

  return (
    <div className="survey-card">
      <h2 className="survey-question">
        {question.question_text}
      </h2>

      {question.input_type === "select" && (
        <select
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="survey-select"
        >
          <option value="">Bitte wählen…</option>
          {question.options?.map((o: any) => (
            <option key={o.id} value={o.id}>
              {o.label}
            </option>
          ))}
        </select>
      )}

      {statistic && (
        <div className="survey-statistic">
          {statistic}
        </div>
      )}

      <button
        onClick={() => onSubmit(value)}
        disabled={!value || loading}
        className="survey-button"
      >
        {loading ? "Laden…" : "Weiter"}
      </button>
    </div>
  );
}
