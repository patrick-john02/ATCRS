import api from "@/utils/axios";
import type { ExamSummary } from "@/types/applicantExamSummary";

export async function fetchExamSummary(): Promise<ExamSummary[]> {
  const response = await api.get<ExamSummary[]>("/exam-summary");
  return response.data;
}
