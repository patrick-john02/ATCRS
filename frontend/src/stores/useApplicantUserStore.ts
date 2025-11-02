import { defineStore } from "pinia"
import type { ViewApplicants } from "@/types/viewApplicants"
import { createApplicantUser, fetchApplicantUsers, updateApplicantUser } from "@/services/applicantUsers"

export const useApplicantUsersStore = defineStore("applicantUsers", {
  state: () => ({
    applicant: [] as ViewApplicants[],
    loading: false,
    error: null as string | null,
  }),

actions: {
  async loadApplicants() {
    this.loading = true
    this.error = null
    try {
      this.applicant = await fetchApplicantUsers()
    } catch (err: any) {
      this.error = err.message || "Failed to fetch applicant users"
    } finally {
      this.loading = false
    }
  },

  async createApplicant(data: Omit<ViewApplicants, "id" | "application_status" | "exam_status" | "exam_score"> & { password: string }) {
    this.loading = true
    this.error = null
    try {
      const newApplicant = await createApplicantUser(data)
      await this.loadApplicants()
      this.applicant.unshift(newApplicant)
      return newApplicant
    } catch (err: any) {
      this.error = err.message || "Failed to create applicant"
      throw err
    } finally {
      this.loading = false
    }
  },

  async updateApplicant(id: number, data: Partial<ViewApplicants> & { password?: string }) {
    this.loading = true
    this.error = null
    try {
      const updated = await updateApplicantUser(id, data)
      await this.loadApplicants()
      const index = this.applicant.findIndex(a => a.id === id)
      if (index !== -1) {
        this.applicant[index] = updated
      }
      return updated
    } catch (err: any) {
      this.error = err.message || "Failed to update applicant"
      throw err
    } finally {
      this.loading = false
    }
  },
}
})