<!-- src/components/charts/ChartBar.vue -->
<script setup lang="ts">
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const props = defineProps<{
  chartData: any
  chartOptions?: any
}>()
</script>

<template>
  <div class="w-full h-full">
    <Bar :data="props.chartData" :options="props.chartOptions" />
  </div>
</template>

<style scoped>
div {
  position: relative;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
