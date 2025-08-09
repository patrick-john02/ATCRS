<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const auth = useAuthStore()
</script>

<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-semibold">My Profile</h1>

    <Card class="w-full max-w-md">
      <CardHeader>
        <CardTitle>{{ auth.user?.first_name }} {{ auth.user?.last_name }}</CardTitle>
        <CardDescription>Account Information</CardDescription>
      </CardHeader>

      <CardContent class="space-y-2">
        <p><strong>Name:</strong> {{ auth.user?.first_name }} {{ auth.user?.last_name }}</p>
        <p><strong>Email:</strong> {{ auth.user?.email }}</p>
      </CardContent>
    </Card>
  </div>
</template>
