<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import apayaoLogo from '@/assets/imgs/apayao.png'
</script>

<template>
  <div class="flex flex-col gap-6 items-center justify-center min-h-screen px-4">
    <!-- Centered card -->
    <Card class="overflow-hidden w-full max-w-md">
      <CardContent class="p-6 md:p-8">
        <form class="flex flex-col gap-6">
          <!-- Logo and heading -->
          <div class="flex flex-col items-center text-center space-y-2">
            <img
              :src="apayaoLogo"
              alt="Apayao Logo"
              class="h-12 w-12 object-contain"
            />
            <h1 class="text-2xl font-bold">Forgot your password?</h1>
            <p class="text-muted-foreground text-sm">
              Enter your email and we’ll send you a password reset link.
            </p>
          </div>

          <!-- Email input -->
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="m@example.com"
              required
            />
          </div>

          <!-- Submit button -->
          <Button type="submit" class="w-full">Send Reset Link</Button>

          <!-- Back to login -->
          <div class="text-center text-sm">
            
            <RouterLink
            to="/login"
            class="ml-auto text-sm underline-offset-2 hover:underline"
            >
            Go back to login
            </RouterLink>

          </div>
        </form>
      </CardContent>
    </Card>

    <!-- Footer -->
    <div class="text-center text-xs text-muted-foreground mt-4 [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:text-primary">
      By submitting, you agree to our
      <a href="#"> Terms of Service</a> and
      <a href="#"> Privacy Policy</a>.
    </div>
  </div>
</template>
