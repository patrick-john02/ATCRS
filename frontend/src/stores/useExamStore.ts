// stores/useExamStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { examService } from '@/services/examService'
import type {
  TakeExamResponse,
  SubmitAnswerRequest,
  CompleteExamResponse,
} from '@/types/studentExam'

export const useExamStore = defineStore('exam', () => {
  const currentExam = ref<TakeExamResponse | null>(null)
  const currentQuestionIndex = ref(0)
  const selectedAnswers = ref<Map<string, string>>(new Map())
  const loading = ref(false)
  const error = ref<string | null>(null)
  const timeRemaining = ref<number>(0)
  const tabSwitchCount = ref(0)
  const questionStartTime = ref<number>(Date.now())
  const completionResult = ref<CompleteExamResponse | null>(null)

  // Computed
  const currentQuestion = computed(() => {
    if (!currentExam.value || currentQuestionIndex.value >= currentExam.value.questions.length) {
      return null
    }
    return currentExam.value.questions[currentQuestionIndex.value]
  })

  const progress = computed(() => {
    if (!currentExam.value) return 0
    return (currentExam.value.attempted_questions / currentExam.value.total_questions) * 100
  })

  const isLastQuestion = computed(() => {
    if (!currentExam.value) return false
    return currentQuestionIndex.value === currentExam.value.questions.length - 1
  })

  const isFirstQuestion = computed(() => {
    return currentQuestionIndex.value === 0
  })

  // Actions
  async function loadExam(examUuid: string) {
    loading.value = true
    error.value = null
    try {
      const data = await examService.getTakeExam(examUuid)
      currentExam.value = data
      
      // Initialize timer
      if (data.started_at) {
        const startTime = new Date(data.started_at).getTime()
        const durationMs = data.exam_details.duration_minutes * 60 * 1000
        const elapsed = Date.now() - startTime
        timeRemaining.value = Math.max(0, Math.floor((durationMs - elapsed) / 1000))
      }
      
      questionStartTime.value = Date.now()
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to load exam'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchExamResult(uuid: string) {
  loading.value = true
  error.value = null
  try {
    const data = await examService.getExamHistoryDetail(uuid)
    completionResult.value = {
      message: 'Exam completed successfully',
      score: data.recommendation_score || 0,
      correct_answers: data.correct_answers,
      total_questions: data.total_questions,
      recommended_course: data.recommended_course?.name || null,
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to fetch exam result'
    throw err
  } finally {
    loading.value = false
  }
}

  function selectAnswer(questionUuid: string, choiceUuid: string) {
    selectedAnswers.value.set(questionUuid, choiceUuid)
  }

  async function submitAnswer() {
    if (!currentExam.value || !currentQuestion.value) return

    const selectedChoiceUuid = selectedAnswers.value.get(currentQuestion.value.uuid)
    if (!selectedChoiceUuid) {
      error.value = 'Please select an answer before submitting'
      return
    }

    loading.value = true
    error.value = null
    
    try {
      const timeSpent = Math.floor((Date.now() - questionStartTime.value) / 1000)
      
      const data: SubmitAnswerRequest = {
        question_uuid: currentQuestion.value.uuid,
        choice_uuid: selectedChoiceUuid,
        time_spent_seconds: timeSpent,
        tab_switch_count: tabSwitchCount.value,
      }

      const response = await examService.submitAnswer(currentExam.value.uuid, data)
      
      if (currentExam.value) {
        currentExam.value.attempted_questions = response.attempted_questions
      }
      
      // Reset for next question
      tabSwitchCount.value = 0
      questionStartTime.value = Date.now()
      
      return response
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to submit answer'
      throw err
    } finally {
      loading.value = false
    }
  }

  function nextQuestion() {
    if (currentExam.value && currentQuestionIndex.value < currentExam.value.questions.length - 1) {
      currentQuestionIndex.value++
      questionStartTime.value = Date.now()
    }
  }

  function previousQuestion() {
    if (currentQuestionIndex.value > 0) {
      currentQuestionIndex.value--
      questionStartTime.value = Date.now()
    }
  }

  function goToQuestion(index: number) {
    if (currentExam.value && index >= 0 && index < currentExam.value.questions.length) {
      currentQuestionIndex.value = index
      questionStartTime.value = Date.now()
    }
  }

  async function completeExam(): Promise<CompleteExamResponse> {
    if (!currentExam.value) throw new Error('No exam loaded')

    loading.value = true
    error.value = null
    
    try {
      const response = await examService.completeExam(currentExam.value.uuid)
      completionResult.value = response
      return response
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to complete exam'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearCompletionResult() {
  completionResult.value = null
}

  function incrementTabSwitch() {
    tabSwitchCount.value++
  }

  function decrementTimer() {
    if (timeRemaining.value > 0) {
      timeRemaining.value--
    }
  }

  function reset() {
    currentExam.value = null
    currentQuestionIndex.value = 0
    selectedAnswers.value.clear()
    loading.value = false
    error.value = null
    timeRemaining.value = 0
    tabSwitchCount.value = 0
    questionStartTime.value = Date.now()
  }

  return {
    // State
    currentExam,
    currentQuestionIndex,
    selectedAnswers,
    loading,
    error,
    timeRemaining,
    tabSwitchCount,
    completionResult,
    
    // Computed
    currentQuestion,
    progress,
    isLastQuestion,
    isFirstQuestion,
    
    // Actions
    loadExam,
    selectAnswer,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    goToQuestion,
    completeExam,
    incrementTabSwitch,
    decrementTimer,
    reset,
    clearCompletionResult,

    fetchExamResult
  }
})