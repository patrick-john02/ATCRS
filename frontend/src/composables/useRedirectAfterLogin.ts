import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export function useRedirectAfterLogin() {
  const router = useRouter()
  const auth = useAuthStore()

  function redirectUser() {
    const role = auth.user?.user_type 

    if (role === 'admin') {
      router.push('/admin/dashboard')
    } else if (role === 'superadmin') {
      router.push('/superadmin/dashboard')
    } else if (role === 'applicant') {
      router.push('/student/dashboard')
    } else {
      router.push('/error/Error401') 
    }
  }

  return { redirectUser }
}
