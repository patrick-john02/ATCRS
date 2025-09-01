import { defineStore } from "pinia"
import type { ViewApplicants } from "@/types/viewApplicants"
import { fetchApplicantUsers } from "@/services/applicantUsers"

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
  }
})