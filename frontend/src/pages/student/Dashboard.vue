<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Skeleton } from '@/components/ui/skeleton'
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  GraduationCap, 
  Calendar,
  Award,
  Target,
  TrendingUp,
  School
} from 'lucide-vue-next'
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

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

const getScoreColor = (score: number | null) => {
  if (!score) return 'text-gray-500';
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
};

const averageScore = computed(() => {
  if (!examStore.summaries.length) return 0;
  const total = examStore.summaries.reduce((sum, exam) => sum + (exam.recommendation_score || 0), 0);
  return Math.round(total / examStore.summaries.length);
});
</script>

<template>
  <div class="container mx-auto space-y-6 p-6">
    <!-- Welcome Header -->
    <div class="space-y-1">
      <h1 class="text-3xl font-bold tracking-tight">Dashboard</h1>
      <p class="text-muted-foreground">Welcome back! Here's your academic overview.</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid gap-4 md:grid-cols-3">
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-muted-foreground">Exams Taken</p>
              <p class="text-3xl font-bold">{{ examStore.summaries.length }}</p>
            </div>
            <div class="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <GraduationCap class="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-muted-foreground">Average Score</p>
              <p class="text-3xl font-bold" :class="getScoreColor(averageScore)">
                {{ averageScore }}%
              </p>
            </div>
            <div class="h-12 w-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <TrendingUp class="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-muted-foreground">Best Score</p>
              <p class="text-3xl font-bold text-green-600">
                {{ Math.max(...examStore.summaries.map(e => e.recommendation_score || 0), 0) }}%
              </p>
            </div>
            <div class="h-12 w-12 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Award class="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="grid gap-6 md:grid-cols-3">
      <!-- Profile Card -->
      <Card class="md:col-span-1">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <User class="h-5 w-5" />
            My Profile
          </CardTitle>
          <CardDescription>Your personal information</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="profileStore.loading" class="space-y-4">
            <div class="flex items-center space-x-4">
              <Skeleton class="h-20 w-20 rounded-full" />
              <div class="space-y-2">
                <Skeleton class="h-4 w-32" />
                <Skeleton class="h-3 w-24" />
              </div>
            </div>
          </div>
          
          <div v-else-if="profileStore.error" class="text-sm text-destructive">
            {{ profileStore.error }}
          </div>
          
          <div v-else-if="profileStore.profile" class="space-y-6">
            <div class="flex flex-col items-center text-center space-y-4">
              <Avatar class="h-24 w-24 border-4 border-background shadow-lg">
                <AvatarImage :src="profileStore.profile.profile_photo_url || '/apayao.png'" />
                <AvatarFallback class="text-lg">
                  {{ getInitials(profileStore.profile.full_name) }}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 class="text-xl font-semibold">{{ profileStore.profile.full_name }}</h3>
                <p class="text-sm text-muted-foreground mt-1">Applicant</p>
              </div>
            </div>

            <Separator />

            <div class="space-y-4">
              <div class="flex items-start gap-3">
                <Mail class="h-4 w-4 text-muted-foreground mt-0.5" />
                <div class="flex-1 space-y-1">
                  <p class="text-xs text-muted-foreground">Email</p>
                  <p class="text-sm font-medium">{{ profileStore.profile.email }}</p>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <Phone class="h-4 w-4 text-muted-foreground mt-0.5" />
                <div class="flex-1 space-y-1">
                  <p class="text-xs text-muted-foreground">Contact</p>
                  <p class="text-sm font-medium">{{ profileStore.profile.contact_number || 'N/A' }}</p>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <MapPin class="h-4 w-4 text-muted-foreground mt-0.5" />
                <div class="flex-1 space-y-1">
                  <p class="text-xs text-muted-foreground">Address</p>
                  <p class="text-sm font-medium">{{ profileStore.profile.address || 'N/A' }}</p>
                </div>
              </div>

              <div class="flex items-start gap-3">
                <GraduationCap class="h-4 w-4 text-muted-foreground mt-0.5" />
                <div class="flex-1 space-y-1">
                  <p class="text-xs text-muted-foreground">Course Applied</p>
                  <p class="text-sm font-medium">{{ profileStore.profile.course_applied_name || 'Not specified' }}</p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Exams and Recommendation -->
      <div class="md:col-span-2 space-y-6">
        <!-- Completed Exams -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <School class="h-5 w-5" />
              Exam History
            </CardTitle>
            <CardDescription>Your past exam performance and results</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="examStore.loading" class="space-y-3">
              <Skeleton class="h-12 w-full" />
              <Skeleton class="h-12 w-full" />
              <Skeleton class="h-12 w-full" />
            </div>
            
            <div v-else-if="examStore.error" class="text-sm text-destructive">
              {{ examStore.error }}
            </div>
            
            <div v-else-if="examStore.summaries.length" class="space-y-4">
              <div
                v-for="exam in examStore.summaries"
                :key="exam.exam_title + exam.exam_attempt_number"
                class="flex items-center justify-between p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
              >
                <div class="flex-1 space-y-1">
                  <div class="flex items-center gap-2">
                    <h4 class="font-semibold">{{ exam.exam_title }}</h4>
                    <Badge variant="outline" class="text-xs">
                      Attempt #{{ exam.exam_attempt_number }}
                    </Badge>
                  </div>
                  <div class="flex items-center gap-4 text-sm text-muted-foreground">
                    <div class="flex items-center gap-1">
                      <Target class="h-3 w-3" />
                      <span>{{ exam.correct_answers }}/{{ exam.total_questions }}</span>
                    </div>
                    <div v-if="exam.recommended_course" class="flex items-center gap-1">
                      <GraduationCap class="h-3 w-3" />
                      <span>{{ exam.recommended_course }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="text-right">
                  <p class="text-2xl font-bold" :class="getScoreColor(exam.recommendation_score)">
                    {{ exam.recommendation_score ?? 'N/A' }}%
                  </p>
                  <p class="text-xs text-muted-foreground">Score</p>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-12">
              <School class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p class="text-sm text-muted-foreground">No completed exams found.</p>
            </div>
          </CardContent>
        </Card>

        <!-- Course Recommendation -->
        <Card v-if="examStore.summaries.length" class="border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Award class="h-5 w-5 text-blue-600" />
              Course Recommendation
            </CardTitle>
            <CardDescription>Based on your most recent exam results</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="flex items-start gap-4">
              <div class="h-12 w-12 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                <GraduationCap class="h-6 w-6 text-white" />
              </div>
              <div class="flex-1 space-y-2">
                <div>
                  <p class="text-sm text-muted-foreground">Recommended Course</p>
                  <p class="text-2xl font-bold text-blue-600">
                    {{ examStore.summaries[0].recommended_course || 'Not Available' }}
                  </p>
                </div>
                <div class="flex items-center gap-2">
                  <Badge variant="secondary" class="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                    {{ examStore.summaries[0].recommendation_score ?? '-' }}% Match
                  </Badge>
                  <Badge variant="outline">
                    Latest Result
                  </Badge>
                </div>
                <p class="text-sm text-muted-foreground leading-relaxed pt-2">
                  Based on your test performance, this course aligns well with your demonstrated skills and aptitudes.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>