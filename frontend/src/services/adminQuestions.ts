import api from "@/utils/axios"

export interface QuestionCreateData {
  exam: string | number
  text: string
  question_type: 'mcq' | 'essay' | 'true_false'
}

export interface QuestionUpdateData {
  text?: string
  question_type?: 'mcq' | 'essay' | 'true_false'
}

export interface ChoiceCreateData {
  question: string | number
  label: string
  text: string
  is_correct: boolean
}

export interface ChoiceUpdateData {
  label?: string
  text?: string
  is_correct?: boolean
}

// Question CRUD operations
export async function createQuestion(data: QuestionCreateData) {
  const response = await api.post('/questions/', data)
  return response.data
}

export async function updateQuestion(uuid: string, data: QuestionUpdateData) {
  const response = await api.patch(`/questions/${uuid}/`, data)
  return response.data
}

export async function deleteQuestion(uuid: string) {
  await api.delete(`/questions/${uuid}/`)
}

export async function fetchQuestionById(uuid: string) {
  const response = await api.get(`/questions/${uuid}/`)
  return response.data
}

// Choice CRUD operations
export async function createChoice(data: ChoiceCreateData) {
  const response = await api.post('/choices/', data)
  return response.data
}

export async function updateChoice(uuid: string, data: ChoiceUpdateData) {
  const response = await api.patch(`/choices/${uuid}/`, data)
  return response.data
}

export async function deleteChoice(uuid: string) {
  await api.delete(`/choices/${uuid}/`)
}

export async function fetchChoicesByQuestion(questionUuid: string) {
  const response = await api.get(`/choices/?question=${questionUuid}`)
  return response.data
}