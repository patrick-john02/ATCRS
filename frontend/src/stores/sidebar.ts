// src/stores/sidebar.ts
import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true, // default: sidebar is open
  }),
  actions: {
    toggleSidebar() {
      this.isOpen = !this.isOpen
      this.persistState()
    },
    openSidebar() {
      this.isOpen = true
      this.persistState()
    },
    closeSidebar() {
      this.isOpen = false
      this.persistState()
    },
    // Persist state to localStorage
    persistState() {
      try {
        localStorage.setItem('sidebar-state', JSON.stringify({ isOpen: this.isOpen }))
      } catch (error) {
        console.warn('Failed to persist sidebar state:', error)
      }
    },
    // Load state from localStorage
    loadPersistedState() {
      try {
        const saved = localStorage.getItem('sidebar-state')
        if (saved) {
          const { isOpen } = JSON.parse(saved)
          this.isOpen = isOpen
        }
      } catch (error) {
        console.warn('Failed to load persisted sidebar state:', error)
        // Fallback to default state
        this.isOpen = true
      }
    },
    // Initialize the store
    initialize() {
      this.loadPersistedState()
    }
  },
})