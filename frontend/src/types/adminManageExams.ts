export interface Choice {
  uuid: string
  question: number
  label: string
  text: string
  is_correct: boolean
}

export interface Question {
  uuid: string
  exam: number
  text: string
  question_type: "mcq" | "essay" | "true_false" | string
  correct_choice: string | null
  choices: Choice[]
  created_at: string
}

export interface ExamMinimal {
  uuid: string
  slug: string
  title: string
  description: string
  date: string
  start_time: string
  end_time: string
  duration_minutes: number
  access_code: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ExamFull extends ExamMinimal {
  questions: Question[]
}