// composables/useExamHistory.ts
import { ref, onMounted } from 'vue'
import { examService } from '@/services/examService'
import type { ExamHistoryItem } from '@/types/studentExam'

export function useExamHistory() {
  const examHistory = ref<ExamHistoryItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchExamHistory() {
    loading.value = true
    error.value = null
    try {
      examHistory.value = await examService.getExamHistory()
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch exam history'
      console.error('Error fetching exam history:', err)
    } finally {
      loading.value = false
    }
  }

  async function refreshHistory() {
    await fetchExamHistory()
  }

  onMounted(() => {
    fetchExamHistory()
  })

  return {
    examHistory,
    loading,
    error,
    refreshHistory,
  }
}