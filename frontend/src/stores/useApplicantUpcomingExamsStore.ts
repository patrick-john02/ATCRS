import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UpcomingExam } from '../types/applicantUpcomingExams'
import { getUpcomingExams } from '../services/applicantUpcomingExamsServices'

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

  return {
    exams,
    loading,
    error,
    fetchExams,
  }
})
