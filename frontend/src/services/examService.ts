// services/examService.ts
import api from "@/utils/axios";
import type {
  TakeExamResponse,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
  CompleteExamResponse,
  ExamProgress,
  ExamHistoryItem,
} from '@/types/studentExam'

export const examService = {
  /**
   * Get exam details and start/resume exam
   * GET /api/take-exam/{uuid}/
   */
  async getTakeExam(examUuid: string): Promise<TakeExamResponse> {
    const response = await api.get(`/take-exam/${examUuid}/`)
    return response.data
  },

  /**
   * Submit an answer for a question
   * POST /api/take-exam/{uuid}/submit_answer/
   */
  async submitAnswer(
    examUuid: string,
    data: SubmitAnswerRequest,
  ): Promise<SubmitAnswerResponse> {
    const response = await api.post(
      `/take-exam/${examUuid}/submit_answer/`,
      data,
    )
    return response.data
  },

  /**
   * Complete and submit the exam
   * POST /api/take-exam/{uuid}/complete/
   */
  async completeExam(examUuid: string): Promise<CompleteExamResponse> {
    const response = await api.post(`/take-exam/${examUuid}/complete/`)
    return response.data
  },

  /**
   * Get current exam progress
   * GET /api/take-exam/{uuid}/progress/
   */
  async getExamProgress(examUuid: string): Promise<ExamProgress> {
    const response = await api.get(`/take-exam/${examUuid}/progress/`)
    return response.data
  },

  /**
   * Get exam history list
   * GET /api/exam-history/
   */
  async getExamHistory(): Promise<ExamHistoryItem[]> {
    const response = await api.get('/exam-history/')
    return response.data
  },

  /**
   * Get specific exam history item details
   * GET /api/exam-history/{uuid}/
   */
  async getExamHistoryDetail(uuid: string): Promise<ExamHistoryItem> {
    const response = await api.get(`/exam-history/${uuid}/`)
    return response.data
  },
}

export default examService