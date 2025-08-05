<script setup lang="ts">
import { useSidebarStore } from '@/stores/sidebar'
import Sonner from './components/ui/sonner/Sonner.vue'

const sidebarStore = useSidebarStore()
sidebarStore.initialize()

</script>

<template>
  <div>
      <RouterView/>
      <Sonner position="bottom-right" />
      
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
