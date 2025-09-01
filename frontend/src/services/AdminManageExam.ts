import api from "@/utils/axios"
import type { ExamMinimal, ExamFull } from "@/types/adminManageExams"

export async function fetchExams(): Promise<ExamMinimal[]> {
  const response = await api.get<ExamMinimal[]>("/exams/")
  return response.data
}

export async function fetchExamById(uuid: string): Promise<ExamFull> {
  const response = await api.get<ExamFull>(`/exams/${uuid}/`)
  return response.data
}

export async function createExam(
  data: Omit<ExamMinimal, "uuid" | "created_at" | "updated_at">
): Promise<ExamMinimal> {
  const response = await api.post<ExamMinimal>("/exams/", data)
  return response.data
}

export async function deleteExam(uuid: string): Promise<void> {
  await api.delete(`/exams/${uuid}/`)
}