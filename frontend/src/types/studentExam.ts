// types/studentExam.ts
export interface Choice {
  uuid: string
  label: string
  text: string
}

export interface Question {
  uuid: string
  text: string
  question_type: 'mcq' | 'essay' | 'true_false'
  choices: Choice[]
}

export interface ExamDetails {
  uuid: string
  title: string
  description: string
  duration_minutes: number
  total_questions: number
}

export interface TakeExamResponse {
  uuid: string
  exam_details: ExamDetails
  questions: Question[]
  started_at: string
  status: 'not_started' | 'in_progress' | 'completed'
  total_questions: number
  attempted_questions: number
  exam_attempt_number: number
}

export interface SubmitAnswerRequest {
  question_uuid: string
  choice_uuid: string
  time_spent_seconds?: number
  tab_switch_count?: number
}

export interface SubmitAnswerResponse {
  message: string
  is_correct: boolean
  attempted_questions: number
  total_questions: number
}

export interface CompleteExamResponse {
  message: string
  score: number
  correct_answers: number
  total_questions: number
  recommended_course: string | null
}

export interface ExamProgress {
  attempted_questions: number
  total_questions: number
  time_started: string
  duration_minutes: number
}

export interface ExamHistoryItem {
  uuid: string
  exam: {
    uuid: string
    title: string
    description: string
    date: string
  }
  status: string
  score: number | null
  recommendation_score: number | null
  recommended_course: {
    code: string
    name: string
  } | null
  started_at: string | null
  completed_at: string | null
  exam_attempt_number: number
  total_questions: number
  attempted_questions: number
  correct_answers: number
  accuracy: number | null
}