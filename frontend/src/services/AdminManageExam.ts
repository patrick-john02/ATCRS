import api from "@/utils/axios"
import type { ExamMinimal, ExamFull, ExamUpdateData } from "@/types/adminManageExams"

export async function fetchExams(): Promise<ExamMinimal[]> {
  const response = await api.get<ExamMinimal[]>("/exams/")
  return response.data
}

export async function fetchExamById(uuid: string): Promise<ExamFull> {
  const response = await api.get<ExamFull>(`/exams/${uuid}/`)
  return response.data
}

export async function createExam(
  data: Omit<ExamMinimal, "uuid" | "created_at" | "updated_at" | "slug">
): Promise<ExamMinimal> {
  const response = await api.post<ExamMinimal>("/exams/", data)
  return response.data
}

export async function updateExam(uuid: string, data: ExamUpdateData): Promise<ExamFull> {
  const response = await api.patch<ExamFull>(`/exams/${uuid}/`, data)
  return response.data
}

export async function deleteExam(uuid: string): Promise<void> {
  await api.delete(`/exams/${uuid}/`)
}

export async function toggleExamStatus(uuid: string, isActive: boolean): Promise<ExamFull> {
  const response = await api.patch<ExamFull>(`/exams/${uuid}/`, { is_active: isActive })
  return response.data
}