import api from '@/utils/axios'
import type { UpcomingExam } from '../types/applicantUpcomingExams'

export const getUpcomingExams = async (): Promise<UpcomingExam[]> => {
  try {
    const response = await api.get<UpcomingExam[]>('/upcoming-exams')
    return response.data
  } catch (error: any) {
    console.error('Failed to fetch upcoming exams:', error)
    throw error
  }
}


export const applyToExamAPI = async (exam: UpcomingExam) => {
  try {
    const response = await api.post(`/upcoming-exams/${exam.uuid}/apply/`) // plural
    return response.data
  } catch (err: any) {
    console.error('Failed to apply to exam:', err)
    throw err
  }
}