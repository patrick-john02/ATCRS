<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const auth = useAuthStore()

// Format join date (optional enhancement)
function formatDate(isoDate: string | undefined) {
  if (!isoDate) return '—'
  return new Date(isoDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
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
        <p><strong>Date Joined:</strong> {{ formatDate(auth.user?.date_joined) }}</p>
        <p>
          <strong>Active:</strong>
          <span :class="auth.user?.is_active ? 'text-green-600' : 'text-red-600'">
            {{ auth.user?.is_active ? 'Yes' : 'No' }}
          </span>
        </p>
      </CardContent>

      <CardFooter class="text-sm text-muted-foreground">
        Last updated just now
      </CardFooter>
    </Card>
  </div>
</template>
