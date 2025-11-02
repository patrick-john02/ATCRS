<script setup lang="ts">
// Loads and displays live admin dashboard data
import { onMounted, computed  } from "vue"
import { useAdminDashboardStore } from "@/stores/useAdminDashboard"
import ChartBar from "@/components/charts/ChartBar.vue"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const dashboardStore = useAdminDashboardStore()

onMounted(() => {
  dashboardStore.loadDashboard()
})

const chartData = computed(() => ({
  labels: dashboardStore.courseStats.map(c => c.name),
  datasets: [
    {
      label: "Recommended Students",
      backgroundColor: "#3b82f6",
      data: dashboardStore.courseStats.map(c => c.recommended_count),
    },
    {
      label: "Total Applicants",
      backgroundColor: "#008000",
      data: dashboardStore.courseStats.map(c => c.total_applicants),
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: 20 },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { callback: (value: number) => `${value} pts` },
    },
  },
  plugins: { legend: { position: "top" as const } },
}
</script>

<template>
  <div v-if="dashboardStore.loading" class="text-center py-8 text-gray-500">Loading...</div>
  <div v-else-if="dashboardStore.error" class="text-center py-8 text-red-600">
    {{ dashboardStore.error }}
  </div>
  <div v-else-if="dashboardStore.dashboard">
    <div class="grid gap-4 md:grid-cols-3">
      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Total Exams</CardTitle>
          <CardDescription>Number of exams created</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">
            {{ dashboardStore.dashboard.exams_count }}
          </div>
        </CardContent>
      </Card>

      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Total Applicants</CardTitle>
          <CardDescription>Registered users applying</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">
            {{ dashboardStore.dashboard.applicants_count }}
          </div>
        </CardContent>
      </Card>

      <Card class="shadow-sm">
        <CardHeader>
          <CardTitle>Courses Offered</CardTitle>
          <CardDescription>Current active programs</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="text-4xl font-bold">
            {{ dashboardStore.dashboard.course_count }}
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="mt-6 w-full">
      <Card class="shadow-sm w-full">
        <CardHeader>
          <CardTitle>Admission Test Trends & Course Recommendation</CardTitle>
          <CardDescription>
            Visualization of applicant test performance and recommended courses.
          </CardDescription>
        </CardHeader>
        <CardContent class="h-[400px]">
          <ChartBar :chart-data="chartData" :chart-options="chartOptions" />
        </CardContent>
      </Card>
    </div>
  </div>
</template>
