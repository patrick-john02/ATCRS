import { defineStore } from 'pinia'
import { ref } from 'vue'
// import { apiClient } from '@/lib/api'
import api from '@/utils/axios'

interface Choice {
  uuid?: string
  question_uuid?: string 
  label: string
  text: string
  is_correct: boolean
}
interface Question {
  uuid?: string
  text: string
  question_type: 'mcq' | 'essay' | 'true_false'
  choices?: Choice[]
}

interface CreateQuestionData {
  exam_uuid: string 
  text: string
  question_type: 'mcq' | 'essay' | 'true_false'
  choices?: Choice[]
}


export const useQuestionsStore = defineStore('questions', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

const createQuestion = async (questionData: CreateQuestionData) => {
  loading.value = true
  error.value = null

  try {
    const response = await api.post(`/exams/${questionData.exam_uuid}/questions/`, {
      text: questionData.text,
      question_type: questionData.question_type
    })
    return response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Failed to create question'
    throw err
  } finally {
    loading.value = false
  }
}

  const updateQuestion = async (questionUuid: string, questionData: Partial<Question>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.patch(`/questions/${questionUuid}/`, questionData)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Failed to update question'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteQuestion = async (questionUuid: string) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/questions/${questionUuid}/`)
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete question'
      throw err
    } finally {
      loading.value = false
    }
  }

// const createChoice = async (choiceData: Choice) => {
//   loading.value = true
//   error.value = null

//   try {
//     const response = await api.post(`/questions/${choiceData.question_uuid}/choices/`, {
//       label: choiceData.label,
//       text: choiceData.text,
//       is_correct: choiceData.is_correct
//     })
//     return response.data
//   } catch (err: any) {
//     error.value = err.response?.data?.detail || err.message || 'Failed to create choice'
//     throw err
//   } finally {
//     loading.value = false
//   }
// }


const createChoice = async (choiceData: Choice) => {
  loading.value = true
  error.value = null

  try {
    const response = await api.post(`/choices/`, {
      question_uuid: choiceData.question_uuid,
      label: choiceData.label,
      text: choiceData.text,
      is_correct: choiceData.is_correct
    })
    return response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Failed to create choice'
    throw err
  } finally {
    loading.value = false
  }
}
  const updateChoice = async (choiceUuid: string, choiceData: Partial<Choice>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.patch(`/choices/${choiceUuid}/`, choiceData)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Failed to update choice'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteChoice = async (choiceUuid: string) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/choices/${choiceUuid}/`)
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete choice'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    createQuestion,
    updateQuestion,
    deleteQuestion,
    createChoice,
    updateChoice,
    deleteChoice,
  }
})