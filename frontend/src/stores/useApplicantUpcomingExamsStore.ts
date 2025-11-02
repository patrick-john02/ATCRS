import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UpcomingExam } from '../types/applicantUpcomingExams'
import { getUpcomingExams, applyToExamAPI } from '../services/applicantUpcomingExamsServices'

export const useApplicantUpcomingExamsStore = defineStore('upcomingExams', () => {
  const exams = ref<UpcomingExam[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchExams = async () => {
    loading.value = true
    error.value = null
    try {
      exams.value = await getUpcomingExams()
    } catch (err: any) {
      error.value = err.message || 'Failed to load exams'
    } finally {
      loading.value = false
    }
  }

  const applyToExam = async (exam: UpcomingExam) => {
    loading.value = true
    error.value = null
    try {
      await applyToExamAPI(exam)
      await fetchExams() // Refresh list
      return true
    } catch (err: any) {
      error.value = err.response?.data?.exam_id?.[0] || err.message || 'Failed to apply to exam'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    exams,
    loading,
    error,
    fetchExams,
    applyToExam,
  }
})