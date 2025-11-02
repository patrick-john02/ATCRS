import api from "@/utils/axios"
import type { Dashboard } from "@/types/adminDashbord"

export async function fetchDashboard(): Promise<Dashboard> {
  const response = await api.get<Dashboard>("/admin-dashboard/")
  return response.data
}


export async function fetchCourseStatistics() {
  const response = await api.get("/admin/course-statistics/")
  return response.data
}