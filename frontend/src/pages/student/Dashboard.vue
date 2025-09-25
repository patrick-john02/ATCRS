<script setup lang="ts">
import { onMounted } from 'vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

import { useApplicantProfileStore } from '@/stores/useApplicantProfileStore';
import { useExamSummaryStore } from '@/stores/useApplicantExamSummary';

const profileStore = useApplicantProfileStore();
const examStore = useExamSummaryStore();

onMounted(async () => {
  await profileStore.fetchProfile();
  await examStore.loadExamSummary();
});
</script>

<template>
  <div class="space-y-6 p-6 bg-gray-50 dark:bg-gray-900 min-h-screen">
    <!-- 1. Profile Card -->
    <Card class="max-w-md mx-auto">
      <CardHeader>
        <CardTitle class="text-2xl">My Profile</CardTitle>
        <CardDescription>Your personal information</CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="profileStore.loading">Loading...</div>
        <div v-else-if="profileStore.error">{{ profileStore.error }}</div>
        <div v-else-if="profileStore.profile" class="flex items-center gap-4">
          <img
            :src="profileStore.profile.profile_photo_url || '/apayao.png'"
            alt="Profile Photo"
            class="w-24 h-24 rounded-full border"
          />
          <div>
            <p class="font-semibold text-lg">{{ profileStore.profile.full_name }}</p>
            <p class="text-sm text-muted-foreground">{{ profileStore.profile.email }}</p>
            <p class="text-sm text-muted-foreground">{{ profileStore.profile.course_applied_name }}</p>
            <p class="text-sm text-muted-foreground">Contact: {{ profileStore.profile.contact_number }}</p>
            <p class="text-sm text-muted-foreground">Address: {{ profileStore.profile.address }}</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 3. Completed Exams -->
    <Card>
      <CardHeader>
        <CardTitle>Completed Exams</CardTitle>
        <CardDescription>View your past exam performance</CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="examStore.loading">Loading...</div>
        <div v-else-if="examStore.error">{{ examStore.error }}</div>
        <div v-else-if="examStore.summaries.length">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-100 dark:bg-gray-800">
                  <th class="px-4 py-2">Exam</th>
                  <th class="px-4 py-2">Score</th>
                  <th class="px-4 py-2">Accuracy</th>
                  <th class="px-4 py-2">Recommendation</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="exam in examStore.summaries"
                  :key="exam.exam_title + exam.exam_attempt_number"
                  class="border-b dark:border-gray-700"
                >
                  <td class="px-4 py-2">{{ exam.exam_title }}</td>
                  <td class="px-4 py-2 font-semibold">{{ exam.score ?? 'N/A' }}</td>
                  <td class="px-4 py-2">{{ exam.recommendation_score ?? 'N/A' }}%</td>
                  <td class="px-4 py-2">{{ exam.recommended_course ?? '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else>No completed exams found.</div>
      </CardContent>
    </Card>

    <!-- 5. Course Recommendation -->
    <Card v-if="examStore.summaries.length">
      <CardHeader>
        <CardTitle>🎯 Course Recommendation</CardTitle>
        <CardDescription>Based on your exam results</CardDescription>
      </CardHeader>
      <CardContent>
        <p class="font-medium text-lg">
          Recommended Course: 
          <span class="text-indigo-600">{{ examStore.summaries[0].recommended_course || '-' }}</span>
        </p>
        <p class="text-sm text-muted-foreground mb-2">
          Confidence: {{ examStore.summaries[0].recommendation_score ?? '-' }}%
        </p>
        <p class="text-sm leading-relaxed">
          Based on your test results, this course aligns well with your skills.
        </p>
      </CardContent>
    </Card>
  </div>
</template>
