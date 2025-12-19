import { useEffect, useState } from "react";
import SurveyCard from "../components/SurveyCard";
import { getQuestions, getSummary } from "../api/survey";

type SummaryStep = {
  step: number;
  label: string;
  value: string;
};

type Summary = {
  title: string;
  text: string;
  steps?: SummaryStep[];
};

export default function Survey() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

  const currentQuestion = questions[step];

  // -------------------------------
  // LOAD QUESTIONS
  // -------------------------------
  useEffect(() => {
    getQuestions().then(setQuestions);
  }, []);

  // -------------------------------
  // LOAD SUMMARY (AFTER LAST STEP)
  // -------------------------------
  useEffect(() => {
    if (!currentQuestion && questions.length && !summary) {
      setLoadingSummary(true);
      getSummary(answers)
        .then(setSummary)
        .finally(() => setLoadingSummary(false));
    }
  }, [currentQuestion, questions.length, answers, summary]);

  // -------------------------------
  // LOADING
  // -------------------------------
  if (!questions.length) {
    return <p>Laden…</p>;
  }

  // -------------------------------
  // FINISH (SUMMARY)
  // -------------------------------
  if (!currentQuestion) {
    if (loadingSummary || !summary) {
      return <p>⏳ Ergebnis wird berechnet…</p>;
    }

    return (
      <div className="survey-finish">
        <h2 className="survey-finish__title">{summary.title}</h2>

        <p className="survey-finish__text">
          {summary.text}
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
