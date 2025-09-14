export interface Choice {
  uuid: string
  question_uuid: string  
  label: string
  text: string
  is_correct: boolean
  created_at: string     
}

export interface Question {
  uuid: string
  exam_uuid: string
  text: string
  question_type: "mcq" | "essay" | "true_false" | string
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

export interface ExamFull extends ExamMinimal {
  questions: Question[]
}

export interface ExamUpdateData {
  title?: string
  description?: string
  date?: string
  start_time?: string
  end_time?: string
  duration_minutes?: number
  access_code?: string
  is_active?: boolean
}

export interface ExamCreateData {
  title: string
  description: string
  date: string
  start_time: string
  end_time: string
  duration_minutes: number
  access_code: string
  is_active: boolean
}