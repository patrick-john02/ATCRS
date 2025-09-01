import { defineStore } from "pinia"
import type { ExamMinimal, ExamFull } from "@/types/adminManageExams"
import { fetchExams, fetchExamById, deleteExam } from "@/services/AdminManageExam"

export const useExamsStore = defineStore("exams", {
  state: () => ({
    exams: [] as ExamMinimal[],
    currentExam: null as ExamFull | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async loadExams() {
      this.loading = true
      this.error = null
      try {
        this.exams = await fetchExams()
      } catch (err: any) {
        this.error = err.message || "Failed to fetch exams"
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
      } catch (err: any) {
        this.error = err.message || "Failed to delete exam"
      } finally {
        this.loading = false
      }
    },
  },
})
