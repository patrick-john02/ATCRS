<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Bar } from 'vue-chartjs'
import type { DateValue } from "@internationalized/date"
import type { Ref } from "vue"
import { parseDate } from "@internationalized/date"
import { ref } from "vue"
import { Calendar } from "@/components/ui/calendar"
import { isSameDay } from "@internationalized/date"

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

// Chart data
const chartData = {
  labels: ['BS Computer Science', 'BS Information Technology', 'BS Mathematics'],
  datasets: [
    {
      label: 'Test Scores',
      data: [85, 78, 65],
      backgroundColor: ['#4f46e5', '#10b981', '#f59e0b'],
      borderRadius: 8
    }
  ]
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Course Fit Scores',
      font: { size: 16 }
    }
  },
  scales: {
    y: { beginAtZero: true, max: 100 }
  }
}


const isExamDate = (date: DateValue) => {
  return isSameDay(date, examDateValue)
}

// Data
const hasTakenTest = true
const nextExam = {
  date: 'August 20, 2025',
  time: '9:00 AM',
  venue: 'Room 201, Main Building',
  instructions:
    'Please bring a valid ID, your exam permit, and a pencil. Arrive at least 30 minutes before the exam starts.'
}

// Convert date string to DateValue for calendar highlight
const examDateValue = parseDate('2025-08-20') // YYYY-MM-DD
const value = ref(examDateValue) as Ref<DateValue>
</script>

<template>
  <div class="grid gap-6 md:grid-cols-2">
    <!-- Course Recommendation -->
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow p-6 border">
      <h3 class="text-2xl font-semibold mb-6">🎯 Course Recommendation</h3>

      <div v-if="hasTakenTest">
        <p class="font-medium text-lg">
          Recommended Course:
          <span class="text-indigo-600 font-bold">BS Computer Science</span>
        </p>
        <p class="text-sm text-muted-foreground mb-4">
          Confidence: <span class="font-semibold">85%</span>
        </p>
        <p class="mb-6 leading-relaxed">
          Based on your test results, we recommend BS Computer Science as it aligns well with
          your skills in logic, problem-solving, and analytical thinking.
        </p>
        <div class="max-w-md">
          <Bar :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <div v-else class="text-center">
        <p class="mb-4 text-gray-600 dark:text-gray-300">
          You have not taken the admission test yet.
        </p>
        <Button size="lg">Take Admission Test Now</Button>
      </div>
    </div>

    <!-- Next Scheduled Exam -->
    <Card class="w-full">
      <CardHeader>
        <CardTitle class="flex items-center gap-2 text-2xl">
          📝 Next Scheduled Exam
        </CardTitle>
        <CardDescription>
          Stay prepared — here’s your upcoming exam schedule.
        </CardDescription>
      </CardHeader>

      <CardContent>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
    <!-- Exam details -->
    <div class="space-y-4">
      <div class="space-y-2">
        <p>
          <span class="font-medium">📅 Date:</span> {{ nextExam.date }}
        </p>
        <p>
          <span class="font-medium">⏰ Time:</span> {{ nextExam.time }}
        </p>
        <p>
          <span class="font-medium">📍 Venue:</span> {{ nextExam.venue }}
        </p>
      </div>
      <p class="text-sm text-muted-foreground leading-relaxed">
        {{ nextExam.instructions }}
      </p>
    </div>

    <!-- Calendar -->
    <Calendar
      v-model="value"
      :weekday-format="'short'"
      class="rounded-md border mx-auto"
    >
      <template #day="{ date }">
        <div
          class="relative group flex items-center justify-center w-full h-full cursor-pointer"
        >
          <!-- Highlight exam date -->
          <div
            :class="[
              'w-9 h-9 flex items-center justify-center rounded-full',
              isExamDate(date)
                ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                : 'hover:bg-gray-200 dark:hover:bg-gray-700'
            ]"
          >
            {{ date.day }}
          </div>

          <!-- Tooltip on hover -->
          <div
            v-if="isExamDate(date)"
            class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-900 text-white text-xs rounded px-3 py-2 shadow-lg w-56 z-50"
          >
            <p class="font-bold">📅 {{ nextExam.date }}</p>
            <p>⏰ {{ nextExam.time }}</p>
            <p>📍 {{ nextExam.venue }}</p>
            <p class="mt-1">{{ nextExam.instructions }}</p>
          </div>
        </div>
      </template>
    </Calendar>
  </div>
</CardContent>

    </Card>
  </div>
</template>
