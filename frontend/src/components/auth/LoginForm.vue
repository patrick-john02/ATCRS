<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import apayaoLogo from '@/assets/imgs/apayao.png'
</script>

<template>
  <div class="flex flex-col gap-6 items-center justify-center min-h-screen px-4">
    <!-- Wrapper to control width -->
    <Card class="overflow-hidden w-full max-w-md">
      <CardContent class="p-0">
        <form class="p-6 md:p-8">
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
              <Label for="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
              />
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
              <Input id="password" type="password" required />
            </div>

            <Button type="submit" class="w-full">Login</Button>

            <div class="text-center text-sm">
              Don't have an account?
              <RouterLink to="signup" class="underline underline-offset-4">
                Sign up
              </RouterLink>
            </div>
          </div>
        </form>
      </CardContent>
    </Card>

    <!-- Footer -->
    <div class="text-center text-xs text-muted-foreground mt-4 [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:text-primary">
      By clicking continue, you agree to our
      <a href="#"> Terms of Service</a> and
      <a href="#"> Privacy Policy</a>.
    </div>
  </div>
</template>
