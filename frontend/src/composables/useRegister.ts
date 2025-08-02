import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import { RegisterSchema } from '@/validators/input'

export function useRegister() {
  const router = useRouter()
  const errors = ref<Record<string, string>>({})

  const register = async (formValues: Record<string, any>) => {
    errors.value = {}

    try {
      await RegisterSchema.validate(formValues, { abortEarly: false })


      const formData = new FormData()

    formData.append('username', formValues.username)
    formData.append('email', formValues.email)
    formData.append('first_name', formValues.first_name)
    formData.append('last_name', formValues.last_name)


    formData.append('password', formValues.password)
    formData.append('user_type', 'applicant')

    formData.append('birthdate', formValues.birthdate)
    formData.append('contact_number', formValues.contact_number)
    formData.append('address', formValues.address)
    formData.append('high_school', formValues.high_school)
    formData.append('year_graduated', formValues.year_graduated)

    await api.post('/register/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      router.push('/login')
    } catch (error: any) {
      if (error.name === 'ValidationError') {
        const fieldErrors: Record<string, string> = {}
        error.inner.forEach((e: any) => {
          if (e.path) fieldErrors[e.path] = e.message
        })
        errors.value = fieldErrors
      } else if (error.response && error.response.data) {
        const responseErrors: Record<string, string> = error.response.data
        errors.value = responseErrors
        console.error('Backend validation error:', responseErrors)
      } else {
        console.error('Registration error:', error)
      }
    }
  }

  return {
    register,
    errors
  }
}
