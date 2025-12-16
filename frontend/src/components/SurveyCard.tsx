import { useEffect, useState } from "react";
import { getOptions, getStatistic } from "../api/survey";
export default SurveyCard;
import StatisticBlock from "./StatisticBlock";

type Option = {
  id: number;
  label: string;
};

type Question = {
  id: number;
  step: number;
  question_text: string;
  select_api?: string;
  statistic_api?: string;
  positive_hint?: string;
};

type Answers = Record<string, number>;

type StepConfig = {
  answerKey: string;
  selectParams?: string[];
  statisticParams?: string[];
};

const STEP_CONFIG: Record<number, StepConfig> = {
  1: {
    answerKey: "country_id",
    statisticParams: ["country_id"],
  },
  2: {
    answerKey: "age_id",
    statisticParams: ["country_id", "age_id"],
  },
  3: {
    answerKey: "region_id",
    statisticParams: ["region_id"],
  },
  4: {
    answerKey: "category_id",
    statisticParams: ["region_id", "category_id"],
  },
  5: {
    answerKey: "city_id",
    selectParams: ["region_id"],
    statisticParams: ["region_id", "category_id", "city_id"],
  },
};

interface Props {
  question: Question;
  answers: Answers;
  onNext: (answers: Answers) => void;
}

function SurveyCard({ question, answers = {}, onNext }: Props) {
  const [options, setOptions] = useState<Option[]>([]);
  const [value, setValue] = useState<number | null>(null);
  const [statistic, setStatistic] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const config = STEP_CONFIG[question.step];

  if (!config) {
    console.error("No STEP_CONFIG for step", question.step);
    return null;
  }

  // -------------------------------
  // LOAD OPTIONS
  // -------------------------------

useEffect(() => {
  if (!question.select_api) return;

  const params: Record<string, number> = {};

  config.selectParams?.forEach((key) => {
    if (answers[key] !== undefined) {
      params[key] = answers[key];
    } else {
      console.warn(`Missing select param ${key} for step ${question.step}`);
    }
  });
  console.log("Fetching options for", question.select_api, "with params:", params);
  getOptions(question.select_api, params).then(setOptions);
}, [question.step, question.select_api, answers]);



  // -------------------------------
  // SHOW STATISTIC
  // -------------------------------
  async function handleShowStatistic() {
     if (!config) {
        console.error("No step config for step", question.step);
     return;
     }
    if (!value || !question.statistic_api) return;

    setLoading(true);

    const params: Record<string, number> = {};

    config.statisticParams?.forEach((key) => {
    if (key === config.answerKey) {
        params[key] = value;
        return;
     }

  if (answers && answers[key] !== undefined) {
    params[key] = answers[key];
  }
});

    const stat = await getStatistic(question.statistic_api, params);

    setStatistic(stat);
    setLoading(false);
  }

  // -------------------------------
  // NEXT STEP
  // -------------------------------
  function handleNext() {
    if (!value) return;

    onNext({
      ...answers,
      [config.answerKey]: value,
    });

    setValue(null);
    setStatistic(null);
  }

  // -------------------------------
  // RENDER
  // -------------------------------
  return (
    <div className="survey-card">
      <h2>{question.question_text}</h2>

      <select
        value={value ?? ""}
        onChange={(e) => {
          setValue(Number(e.target.value));
          setStatistic(null);
        }}
      >
        <option value="" disabled>
          Bitte auswählen…
        </option>

        {options.map((o) => (
          <option key={o.id} value={o.id}>
            {o.label}
          </option>
        ))}
      </select>

      {value && !statistic && (
        <button
          onClick={handleShowStatistic}
          disabled={loading}
          className="btn-show-result"
        >
          {loading ? (
            <span className="btn-loading">⏳ Lädt…</span>
          ) : (
            <>
              <span className="btn-icon">📊</span>
              Ergebnis anzeigen
            </>
          )}
        </button>
      )}

      {statistic && (
        <div className="statistic">
          <p className="stat-text">{statistic.text}</p>

          <StatisticBlock raw={statistic.raw} />

          {question.positive_hint && (
            <p className="positive">{question.positive_hint}</p>
          )}

          <button onClick={handleNext} className="btn-primary">
            Weiter →
          </button>
        </div>
      )}
    </div>
  );
}
