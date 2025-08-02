<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apayaoLogo from '@/assets/imgs/apayao.png'
import { useRegister } from '@/composables/useRegister'

import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

// use composable
const { register, errors } = useRegister()

// form fields
const username = ref('')
const email = ref('')
const password = ref('')
const first_name = ref('')
const last_name = ref('')
const birthdate = ref('')
const contact_number = ref('')
const address = ref('')
const high_school = ref('')
const year_graduated = ref<string | number>('')

// submit handler
const handleSubmit = async () => {
  const formValues = {
    username: username.value,
    email: email.value,
    password: password.value,
    first_name: first_name.value,
    last_name: last_name.value,
    birthdate: birthdate.value,
    contact_number: contact_number.value,
    address: address.value,
    high_school: high_school.value,
    year_graduated: year_graduated.value?.toString() || '',
  }

  await register(formValues)
}
</script>


<template>
  <div class="flex flex-col gap-6 items-center justify-center min-h-screen px-4">
    <Card class="overflow-hidden w-full max-w-2xl">
      <CardContent class="p-6 md:p-8">
        <form class="grid gap-4" @submit.prevent="handleSubmit">
          <div class="flex flex-col items-center space-y-2">
            <img :src="apayaoLogo" alt="Apayao Logo" class="h-12 w-12 object-contain" />
            <h1 class="text-2xl font-bold">Create Your Account</h1>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <Label for="first_name">First Name</Label>
              <Input id="first_name" v-model="first_name" />
              <p class="text-sm text-red-500">{{ errors.first_name }}</p>
            </div>
            <div>
              <Label for="last_name">Last Name</Label>
              <Input id="last_name" v-model="last_name" />
              <p class="text-sm text-red-500">{{ errors.last_name }}</p>
            </div>
            <div>
              <Label for="username">Username</Label>
              <Input id="username" v-model="username" />
              <p class="text-sm text-red-500">{{ errors.username }}</p>
            </div>
            <div>
              <Label for="email">Email</Label>
              <Input id="email" type="email" v-model="email" />
              <p class="text-sm text-red-500">{{ errors.email }}</p>
            </div>
            <div>
              <Label for="password">Password</Label>
              <Input id="password" type="password" v-model="password" />
              <p class="text-sm text-red-500">{{ errors.password }}</p>
            </div>
            <div>
              <Label for="birthdate">Birthdate</Label>
              <Input id="birthdate" type="date" v-model="birthdate" />
              <p class="text-sm text-red-500">{{ errors.birthdate }}</p>
            </div>
            <div>
              <Label for="contact_number">Contact Number</Label>
              <Input id="contact_number" v-model="contact_number" />
              <p class="text-sm text-red-500">{{ errors.contact_number }}</p>
            </div>
            <div>
              <Label for="address">Address</Label>
              <Input id="address" v-model="address" />
              <p class="text-sm text-red-500">{{ errors.address }}</p>
            </div>
            <div>
              <Label for="high_school">High School</Label>
              <Input id="high_school" v-model="high_school" />
              <p class="text-sm text-red-500">{{ errors.high_school }}</p>
            </div>
            <div>
              <Label for="year_graduated">Year Graduated</Label>
              <Input id="year_graduated" type="number" v-model="year_graduated" />
              <p class="text-sm text-red-500">{{ errors.year_graduated }}</p>
            </div>
          </div>

          <Button type="submit" class="w-full mt-4">Register</Button>

          <p class="text-center text-sm mt-2">
            Already have an account?
            <RouterLink to="/login" class="underline underline-offset-2 hover:text-primary">Login</RouterLink>
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
