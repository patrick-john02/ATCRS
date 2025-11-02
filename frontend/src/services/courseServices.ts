// single line comment: service functions to fetch admin-managed courses from backend
import api from '@/utils/axios'
import type { AdminManageCourse } from '@/types/courses'

export const fetchAdminManageCourses = async (): Promise<AdminManageCourse[]> => {
  const response = await api.get('/admin-manage-courses')
  return response.data
}

export const createCourse = async (payload: Omit<AdminManageCourse, 'id'>): Promise<AdminManageCourse> => {
  const response = await api.post('/admin-manage-courses/', payload)
  return response.data
}

export const updateCourse = async (id: number, payload: Partial<AdminManageCourse>): Promise<AdminManageCourse> => {
  const response = await api.put(`/admin-manage-courses/${id}/`, payload)
  return response.data
}

export const deleteCourse = async (id: number): Promise<void> => {
  await api.delete(`/admin-manage-courses/${id}/`)
}
