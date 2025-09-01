import { defineStore } from "pinia"
import type { ViewAdmin } from "@/types/viewAdmin"
import { fetchAdminUsers } from "@/services/adminUsers"

export const useAdminUsersStore = defineStore("adminUsers", {
  state: () => ({
    admins: [] as ViewAdmin[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async loadAdmins() {
      this.loading = true
      this.error = null
      try {
        this.admins = await fetchAdminUsers()
      } catch (err: any) {
        this.error = err.message || "Failed to fetch admin users"
      } finally {
        this.loading = false
      }
    },
  }
})