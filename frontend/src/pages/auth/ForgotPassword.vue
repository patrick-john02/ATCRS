<script lang="ts">
export const description = 'A login page with form and image.'
</script>

<script setup lang="ts">
import ForgotPass from '@/components/auth/ForgotPass.vue';
</script>

<template>
  <div class="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
    <div class="w-full max-w-sm md:max-w-3xl">
      <ForgotPass />
    </div>
  </div>
</template>
