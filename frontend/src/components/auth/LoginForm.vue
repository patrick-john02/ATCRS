<script setup lang="ts">
import { toast } from "vue-sonner"
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import apayaoLogo from '@/assets/imgs/apayao.png'

import { useForm, useField } from 'vee-validate'
import { loginSchema } from '@/validators/input'
import { useAuthStore } from '@/stores/auth'
import { useRedirectAfterLogin } from '@/composables/useRedirectAfterLogin'

const auth = useAuthStore()
const {redirectUser} = useRedirectAfterLogin()


const { handleSubmit, errors } = useForm({
  validationSchema: loginSchema
})

const { value: username } = useField<string>('username')
const { value: password } = useField<string>('password')

const onSubmit = handleSubmit(async (values) => {
  try {
    await auth.login(values.username, values.password)
    toast.success('Login successful! Redirecting...')
    redirectUser()
  } catch (error: any) {
    console.error('Login failed', error)

    if (error.response && error.response.status === 401) {
      toast.error('Invalid username or password')
    } else {
      toast.error('Something went wrong. Please try again later.')
    }
  }
})

</script>

<template>
  <div class="flex flex-col gap-6 items-center justify-center min-h-screen px-4">
    <Card class="overflow-hidden w-full max-w-md">
      <CardContent class="p-0">
        <form @submit.prevent="onSubmit" class="p-6 md:p-8">
          <div class="flex flex-col gap-6">
            <div class="flex flex-col items-center text-center space-y-2">
              <img
                :src="apayaoLogo"
                alt="Apayao Logo"
                class="h-12 w-12 object-contain"
              />
              <h1 class="text-2xl font-bold">Welcome back</h1>
              <p class="text-muted-foreground">
                Login to your account
              </p>
            </div>

            <div class="grid gap-2">
              <Label for="username">Username</Label>
              <Input
                id="username"
                type="text"
                placeholder="Enter your username"
                v-model="username"
              />
              <span class="text-red-500 text-sm">{{ errors.username }}</span>
            </div>

            <div class="grid gap-2">
              <div class="flex items-center">
                <Label for="password">Password</Label>
                <RouterLink
                  to="/forgot-password"
                  class="ml-auto text-sm underline-offset-2 hover:underline"
                >
                  Forgot your password?
                </RouterLink>
              </div>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                v-model="password"
              />
              <span class="text-red-500 text-sm">{{ errors.password }}</span>
            </div>

            <Button type="submit" class="w-full">Login</Button>

            


            <div class="text-center text-sm">
              Don’t have an account?
              <RouterLink to="/signup" class="underline underline-offset-4">
                Sign up
              </RouterLink>
            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>