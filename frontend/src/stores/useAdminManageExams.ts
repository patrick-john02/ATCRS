import { defineStore } from "pinia"
import type { ExamMinimal, ExamFull, ExamUpdateData, ExamCreateData } from "@/types/adminManageExams"
import { 
  fetchExams, 
  fetchExamById, 
  deleteExam, 
  updateExam, 
  createExam, 
  toggleExamStatus 
} from "@/services/AdminManageExam"

export const useExamsStore = defineStore("exams", {
  state: () => ({
    exams: [] as ExamMinimal[],
    currentExam: null as ExamFull | null,
    loading: false,
    error: null as string | null,
  }),

  getters: {
    activeExams: (state) => state.exams.filter(exam => exam.is_active),
    inactiveExams: (state) => state.exams.filter(exam => !exam.is_active),
    totalExams: (state) => state.exams.length,
    totalActiveExams: (state) => state.exams.filter(exam => exam.is_active).length,
  },

  actions: {
    async loadExams() {
      this.loading = true
      this.error = null
      try {
        this.exams = await fetchExams()
      } catch (err: any) {
        this.error = err.message || "Failed to fetch exams"
        throw err
      } finally {
        this.loading = false
      }
    },

    async loadExamById(uuid: string) {
      this.loading = true
      this.error = null
      try {
        this.currentExam = await fetchExamById(uuid)
      } catch (err: any) {
        this.error = err.message || "Failed to fetch exam"
        throw err
      } finally {
        this.loading = false
      }
    },

    async createExam(data: ExamCreateData) {
      this.loading = true
      this.error = null
      try {
        const newExam = await createExam(data)
        this.exams.unshift(newExam)
        return newExam
      } catch (err: any) {
        this.error = err.message || "Failed to create exam"
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateExam(uuid: string, data: ExamUpdateData) {
      this.loading = true
      this.error = null
      try {
        const updatedExam = await updateExam(uuid, data)
        
        // Update the exam in the list
        const index = this.exams.findIndex(exam => exam.uuid === uuid)
        if (index !== -1) {
          this.exams[index] = { ...this.exams[index], ...data }
        }
        
        // Update current exam if it's the same one
        if (this.currentExam && this.currentExam.uuid === uuid) {
          this.currentExam = updatedExam
        }
        
        return updatedExam
      } catch (err: any) {
        this.error = err.message || "Failed to update exam"
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteExam(uuid: string) {
      this.loading = true
      this.error = null
      try {
        await deleteExam(uuid)
        this.exams = this.exams.filter(exam => exam.uuid !== uuid)
        
        // Clear current exam if it's the deleted one
        if (this.currentExam && this.currentExam.uuid === uuid) {
          this.currentExam = null
        }
      } catch (err: any) {
        this.error = err.message || "Failed to delete exam"
        throw err
      } finally {
        this.loading = false
      }
    },

    async toggleExamStatus(uuid: string) {
      this.loading = true
      this.error = null
      try {
        const exam = this.exams.find(e => e.uuid === uuid)
        if (!exam) throw new Error("Exam not found")

        const updatedExam = await toggleExamStatus(uuid, !exam.is_active)
        
        // Update the exam in the list
        const index = this.exams.findIndex(exam => exam.uuid === uuid)
        if (index !== -1) {
          this.exams[index].is_active = updatedExam.is_active
        }
        
        // Update current exam if it's the same one
        if (this.currentExam && this.currentExam.uuid === uuid) {
          this.currentExam.is_active = updatedExam.is_active
        }
        
        return updatedExam
      } catch (err: any) {
        this.error = err.message || "Failed to toggle exam status"
        throw err
      } finally {
        this.loading = false
      }
    },

    clearCurrentExam() {
      this.currentExam = null
    },

    clearError() {
      this.error = null
    }
  },
})