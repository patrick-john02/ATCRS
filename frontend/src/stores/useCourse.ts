import { defineStore } from "pinia"
import type { ViewCourse } from "@/types/course"
import type { ViewApplicants } from "@/types/viewApplicants"
import { fetchCourse, createCourse } from "@/services/course"

export const useCourseStore = defineStore("courses", {
  state: () => ({
    course: [] as ViewCourse[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async loadCourse() {
      this.loading = true
      this.error = null
      try {
        this.course = await fetchCourse()
      } catch (err: any) {
        this.error = err.message || "Failed to fetch courses"
      } finally {
        this.loading = false
      }
    },

    async addAdmin(adminData: Omit<ViewApplicants, "id">) {
      this.loading = true
      this.error = null
      try {
        // If you need to add admin/applicant, you'll need to create the appropriate service
        // For now, I'll assume you have a service method for this
        // const newAdmin = await createApplicant(adminData)
        // You might want to refresh the data or add to local state
        console.log("Adding admin:", adminData)
        // Optionally reload data
        // await this.loadCourse()
      } catch (err: any) {
        this.error = err.message || "Failed to add admin"
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})