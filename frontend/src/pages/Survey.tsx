import { useEffect, useState } from "react";
import SurveyCard from "../components/SurveyCard";
import { getQuestions } from "../api/survey";

export default function Survey() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});

  const currentQuestion = questions[step];

  useEffect(() => {
    getQuestions().then(setQuestions);
  }, []);

  // -------------------------------
  // LOADING
  // -------------------------------
  if (!questions.length) {
    return <p>Laden…</p>;
  }

  // -------------------------------
  // FINISH
  // -------------------------------
  if (!currentQuestion) {
    return (
      <div className="survey-finish">
        <h2 className="survey-finish__title">Vielen Dank 🤍</h2>
        <p className="survey-finish__text">
          Ihre Antworten zeigen:
          <br />
          <strong>Integration ist möglich</strong> – Schritt für Schritt.
        </p>
      </div>
    );
  }

  // -------------------------------
  // QUESTION
  // -------------------------------
  return (
    <SurveyCard
      question={currentQuestion}
      answers={answers}
      onNext={(nextAnswers) => {
        setAnswers(nextAnswers);
        setStep((s) => s + 1);
      }}
    />
  );
}
