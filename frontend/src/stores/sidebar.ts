// src/stores/sidebar.ts
import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true, // default: sidebar is open
  }),
  actions: {
    toggleSidebar() {
      this.isOpen = !this.isOpen
    },
    openSidebar() {
      this.isOpen = true
    },
    closeSidebar() {
      this.isOpen = false
    },
  },
})
