<script setup lang="ts">
import ChartBar from '@/components/charts/ChartBar.vue'

import SuperDashboardLayout from '@/components/layouts/SuperDashboardLayout.vue'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

// Chart.js formatted data
const chartData = {
  labels: [
  'BS Information Technology',
  'BS Computer Science',
  'BS Information Systems',
  'BS Electronics Engineering',
  'BS Industrial Engineering',
  'BS Nursing',
  'BS Criminology'
],
  datasets: [
    {
      label: 'Recommended Students',
      backgroundColor: '#3b82f6',
      data: [34, 45, 29, 15, 22, 18, 30],
    },
    {
      label: 'Applicants',
      backgroundColor: '#008000',
      data: [40, 50, 35, 20, 28, 25, 38],
    },
  ],
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: {
    padding: 20,
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value: number) => `${value} pts`
      }
    }
  },
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
}
</script>

<template>
  <SuperDashboardLayout>
    <!-- Metrics Section -->
    <div class="grid gap-4 md:grid-cols-3">
      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Total Admins</CardTitle>
          <CardDescription>Number of admin accounts</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">12</div>
        </CardContent>
      </Card>
      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Total Applicants</CardTitle>
          <CardDescription>Registered users applying</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">248</div>
        </CardContent>
      </Card>
      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Courses Offered</CardTitle>
          <CardDescription>Current active programs</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">8</div>
        </CardContent>
      </Card>

    </div>
        <!-- Responsive Chart Section in Dashboard.vue -->
      <div class="mt-6 w-full">
        <Card class="shadow-sm w-full">
          <CardHeader>
            <CardTitle>Admission Test Trends & Course Recommendation</CardTitle>
            <CardDescription>
              Visualization of applicant test performance and recommended courses.
            </CardDescription>
          </CardHeader>

          <CardContent class="h-[400px] ">
            <ChartBar :chart-data="chartData" :chart-options="chartOptions" />
          </CardContent>
        </Card>
      </div>

  </SuperDashboardLayout>
</template>
