// stores/useCourseStores.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminManageCourse } from '@/types/courses'
import api from '@/utils/axios'

export const useCourseStores = defineStore('courseStores', () => {
  const courses = ref<AdminManageCourse[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getCourses = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/admin-manage-courses/')  // Add /api/ prefix
    courses.value = response.data
  } catch (err: any) {
    error.value = err.message || 'Failed to load courses'
  } finally {
    loading.value = false
  }
}

 const addCourse = async (payload: Omit<AdminManageCourse, 'id'>) => {
  loading.value = true
  error.value = null
  try {
    const response = await api.post('/admin-manage-courses/', payload)
    courses.value.push(response.data)
    await getCourses() // Auto-refresh after add
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to add course'
    throw err
  } finally {
    loading.value = false
  }
}

  const editCourse = async (id: number, payload: Partial<AdminManageCourse>) => {
  loading.value = true
  error.value = null
  try {
    const response = await api.patch(`/admin-manage-courses/${id}/`, payload)
    const index = courses.value.findIndex(c => c.id === id)
    if (index !== -1) courses.value[index] = response.data
    await getCourses() // Auto-refresh after edit
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to update course'
    throw err
  } finally {
    loading.value = false
  }
}

const removeCourse = async (id: number) => {
  loading.value = true
  error.value = null
  try {
    await api.delete(`/admin-manage-courses/${id}/`)
    courses.value = courses.value.filter(c => c.id !== id)
    await getCourses() // Auto-refresh after delete
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to delete course'
    throw err
  } finally {
    loading.value = false
  }
}

  return { courses, loading, error, getCourses, addCourse, editCourse, removeCourse }
})