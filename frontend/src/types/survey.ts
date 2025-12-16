export interface SurveyQuestion {
  id: number
  step: number
  question_text: string
  input_type: 'select'
  select_api: string
}

export interface Option {
  id: number
  label: string
}

export interface SurveyAnswers {
  country_id?: number
  age_id?: number
  region_id?: number
  category_id?: number
  city_id?: number
}

export interface SurveySummaryStep {
  step: number
  question: string
  text: string
  positive_hint: string
}
