// stores/useExamHistoryStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { examService } from '@/services/examService'
import type { ExamHistoryItem } from '@/types/studentExam'

export const useExamHistoryStore = defineStore('examHistory', () => {
  const examHistory = ref<ExamHistoryItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedExam = ref<ExamHistoryItem | null>(null)

  // Computed
  const completedExams = computed(() => 
    examHistory.value.filter(exam => exam.status === 'completed')
  )

  const inProgressExams = computed(() => 
    examHistory.value.filter(exam => exam.status === 'in_progress')
  )

  const notStartedExams = computed(() => 
    examHistory.value.filter(exam => exam.status === 'not_started')
  )

  const totalExams = computed(() => examHistory.value.length)

  const averageScore = computed(() => {
    const completed = completedExams.value.filter(exam => exam.score !== null)
    if (completed.length === 0) return 0
    const total = completed.reduce((sum, exam) => sum + (exam.score || 0), 0)
    return Math.round(total / completed.length)
  })

  const passedExams = computed(() => 
    completedExams.value.filter(exam => (exam.score || 0) >= 70).length
  )

  const failedExams = computed(() => 
    completedExams.value.filter(exam => (exam.score || 0) < 70).length
  )

  // Actions
  async function fetchExamHistory() {
    loading.value = true
    error.value = null
    try {
      const data = await examService.getExamHistory()
      examHistory.value = data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch exam history'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchExamDetail(uuid: string) {
    loading.value = true
    error.value = null
    try {
      const data = await examService.getExamHistoryDetail(uuid)
      selectedExam.value = data
      return data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch exam details'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  function reset() {
    examHistory.value = []
    selectedExam.value = null
    loading.value = false
    error.value = null
  }

  return {
    // State
    examHistory,
    loading,
    error,
    selectedExam,

    // Computed
    completedExams,
    inProgressExams,
    notStartedExams,
    totalExams,
    averageScore,
    passedExams,
    failedExams,

    // Actions
    fetchExamHistory,
    fetchExamDetail,
    clearError,
    reset,
  }
})