// Manages the state of admin dashboard data
import { defineStore } from "pinia"
import type { Dashboard, CourseStatistics } from "@/types/adminDashbord"
import { fetchDashboard, fetchCourseStatistics } from "@/services/adminDashboard"

export const useAdminDashboardStore = defineStore("adminDashboard", {
  state: () => ({
    dashboard: null as Dashboard | null,
    courseStats: [] as CourseStatistics[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async loadDashboard() {
        this.loading = true
        this.error = null
        try {
        this.dashboard = await fetchDashboard()
        this.courseStats = await fetchCourseStatistics()
        } catch (err: any) {
        this.error = err.message || "Failed to fetch dashboard data"
        } finally {
        this.loading = false
        }
    },
    }
})
