import { ref, onMounted } from 'vue'
import api from '@/utils/axios'
import type { AdminUser } from '@/types'

export function useAdminUsers() {
  const admins = ref<AdminUser[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchAdmins = async () => {
    isLoading.value = true
    try {
      const res = await api.get<AdminUser[]>('/admin-users/')
      admins.value = res.data
    } catch (err) {
      error.value = 'Failed to load admins'
    } finally {
      isLoading.value = false
    }
  }

  onMounted(fetchAdmins)

  const createAdminUser = async (data: {
  first_name: string
  last_name: string
  email: string
  password: string
}) => {
  try {
    const res = await api.post('/api/admin-users/', data)
    await fetchAdmins() // Refresh list
    return res.data
  } catch (err) {
    error.value = 'Failed to create admin'
    throw err
  }
}

const updateAdminUser = async (id: number, data: Partial<AdminUser>) => {
  try {
    await api.patch(`/api/admin-users/${id}/`, data)
    await fetchAdmins()
  } catch (err) {
    error.value = 'Failed to update admin'
    throw err
  }
}

const deleteAdminUser = async (id: number) => {
  try {
    await api.delete(`/api/admin-users/${id}/`)
    admins.value = admins.value.filter(admin => admin.id !== id)
  } catch (err) {
    error.value = 'Failed to delete admin'
    throw err
  }
}



  return { 
    admins,
    isLoading,
    error,
    fetchAdmins,
    createAdminUser,
    updateAdminUser,
    deleteAdminUser 
}
}
