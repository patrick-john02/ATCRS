<script setup lang="ts">
import { ref } from 'vue'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

// Mock data for applicant applied exams
interface AppliedExam {
  title: string
  date: string
  status: string
}

const appliedExams = ref<AppliedExam[]>([
  { title: 'Math Admission Test', date: '2025-09-20', status: 'Applied' },
  { title: 'Science Admission Test', date: '2025-09-22', status: 'Applied' },
  { title: 'English Proficiency Test', date: '2025-09-24', status: 'Pending' },
])
</script>

<template>
  <div class="p-6 bg-gray-50 dark:bg-gray-900 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Admission Status</h1>

    <div class="rounded-md border bg-white dark:bg-gray-800">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Exam Title</TableHead>
            <TableHead>Date</TableHead>
            <TableHead>Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="exam in appliedExams" :key="exam.title">
            <TableCell>{{ exam.title }}</TableCell>
            <TableCell>{{ exam.date }}</TableCell>
            <TableCell>
              <span
                :class="{
                  'text-green-600': exam.status === 'Applied',
                  'text-yellow-600': exam.status === 'Pending',
                  'text-red-600': exam.status === 'Rejected',
                }"
              >
                {{ exam.status }}
              </span>
            </TableCell>
          </TableRow>

          <TableRow v-if="appliedExams.length === 0">
            <TableCell colspan="3" class="text-center h-24">
              No exams applied yet.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>
</template>
