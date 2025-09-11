<script setup lang="ts">
import { useSidebarStore } from '@/stores/sidebar'
// import { Toaster } from 'vue-sonner'

const sidebarStore = useSidebarStore()
sidebarStore.initialize()
</script>

<template>
  <div>
    <RouterView />
    <!-- Global toast provider -->
    <!-- <Toaster richColors position="bottom-right" /> -->
  </div>
</template>


<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
