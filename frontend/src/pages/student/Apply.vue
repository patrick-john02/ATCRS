<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApplicantUpcomingExamsStore } from '@/stores/useApplicantUpcomingExamsStore'
import type { UpcomingExam } from '@/types/applicantUpcomingExams'
import { applyToExamAPI } from '@/services/applicantUpcomingExamsServices'

// Pinia store
const store = useApplicantUpcomingExamsStore()
const appliedExams = ref<Set<string>>(new Set())

// Fetch exams from API
onMounted(() => {
  store.fetchExams()
})

// Reactive month/year
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())

// Generate calendar days for the active month
// inside computed calendarDays
const calendarDays = computed(() => {
  const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  return Array.from({ length: daysInMonth }, (_, i) => {
    const date = new Date(currentYear.value, currentMonth.value, i + 1)
    const today = new Date()
    const events = store.exams.filter(e => new Date(e.date).toDateString() === date.toDateString())
      .map(e => {
        const isPast = new Date(e.date) < today
        const alreadyApplied = appliedExams.value.has(e.uuid)
        return {
          ...e,
          applied: !isPast && alreadyApplied,  // disable only future exams if already applied
        }
      })
    return { date, events }
  })
})


// Navigate months
function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value -= 1
  } else {
    currentMonth.value -= 1
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value += 1
  } else {
    currentMonth.value += 1
  }
}

async function applyToExam(event: UpcomingExam) {
  if (!event.uuid) {
    console.error('Exam UUID is missing:', event)
    return
  }
  try {
    await applyToExamAPI(event)
    appliedExams.value.add(event.uuid)
    alert(`You have applied to: ${event.title}`)
  } catch (err: any) {
    alert(`Failed to apply: ${err.response?.data?.detail || err.message}`)
  }
}
const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December']
</script>

<template>
  <div class="p-6 bg-gray-50 dark:bg-gray-900 min-h-screen">
    <div class="flex justify-between items-center mb-4">
      <button class="px-4 py-1 bg-gray-200 rounded" @click="prevMonth">Prev</button>
      <h1 class="text-2xl font-bold">{{ monthNames[currentMonth] }} {{ currentYear }}</h1>
      <button class="px-4 py-1 bg-gray-200 rounded" @click="nextMonth">Next</button>
    </div>

    <div v-if="store.loading">Loading exams...</div>
    <div v-if="store.error">{{ store.error }}</div>

    <div class="grid grid-cols-7 gap-2" v-else>
      <!-- Weekday Headers -->
      <div v-for="day in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="day" class="font-semibold text-center">
        {{ day }}
      </div>

      <!-- Calendar Days -->
      <div v-for="day in calendarDays" :key="day.date.toISOString()" class="border rounded p-2 min-h-[100px] relative">
        <div class="text-sm font-medium">{{ day.date.getDate() }}</div>

        <div v-if="day.events.length" class="mt-1 space-y-1">
          <div
            v-for="event in day.events"
            :key="event.uuid"
            class="bg-indigo-100 dark:bg-indigo-700 text-indigo-800 dark:text-indigo-200 text-xs p-1 rounded flex flex-col gap-1"
          >
            <p class="truncate font-semibold">{{ event.title }}</p>
            <p class="truncate">{{ event.description }}</p>
            <button
              class="mt-1 px-2 py-0.5 bg-indigo-500 text-white text-[10px] rounded hover:bg-indigo-600 disabled:opacity-50"
              :disabled="event.applied"
              @click="applyToExam(event)"
            >
              {{ event.applied ? 'Applied' : 'Apply' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
div.border:hover {
  background-color: rgba(59, 130, 246, 0.1);
}
</style>
