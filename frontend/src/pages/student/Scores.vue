<!-- pages/student/Scores.vue -->

<script setup lang="ts">
import { onMounted } from 'vue';
import { useExamScoresStore } from '@/stores/examScoresStores';
import { format } from 'date-fns';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { FileText, Calendar, Clock, Target, Award, TrendingUp } from 'lucide-vue-next';

const scoresStore = useExamScoresStore();

onMounted(() => {
  scoresStore.fetchRecentScores();
});

const formatDate = (date: string | null) => {
  if (!date) return 'N/A';
  return format(new Date(date), 'MMM dd, yyyy hh:mm a');
};

const getStatusVariant = (status: string): 'default' | 'secondary' | 'destructive' | 'outline' => {
  switch (status) {
    case 'completed':
      return 'default';
    case 'in_progress':
      return 'secondary';
    case 'not_started':
      return 'outline';
    default:
      return 'outline';
  }
};

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
};
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Recent Exam Scores</h1>
      <p class="text-muted-foreground mt-2">View your latest exam results and performance</p>
    </div>

    <!-- Loading State -->
    <div v-if="scoresStore.loading" class="space-y-4">
      <Card v-for="i in 3" :key="i">
        <CardHeader>
          <Skeleton class="h-6 w-3/4" />
          <Skeleton class="h-4 w-1/2 mt-2" />
        </CardHeader>
        <CardContent>
          <div class="grid grid-cols-4 gap-4">
            <Skeleton class="h-16" />
            <Skeleton class="h-16" />
            <Skeleton class="h-16" />
            <Skeleton class="h-16" />
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Error State -->
    <Alert v-else-if="scoresStore.error" variant="destructive">
      <AlertDescription>{{ scoresStore.error }}</AlertDescription>
    </Alert>

    <!-- Empty State -->
    <Card v-else-if="scoresStore.recentScores.length === 0">
      <CardContent class="flex flex-col items-center justify-center py-12">
        <FileText class="h-12 w-12 text-muted-foreground mb-4" />
        <h3 class="text-lg font-semibold mb-1">No exam scores yet</h3>
        <p class="text-sm text-muted-foreground">You haven't completed any exams yet.</p>
      </CardContent>
    </Card>

    <!-- Scores List -->
    <div v-else class="space-y-4">
      <Card v-for="score in scoresStore.recentScores" :key="score.uuid" class="hover:shadow-lg transition-shadow">
        <CardHeader>
          <div class="flex items-start justify-between">
            <div class="flex-1 space-y-2">
              <div class="flex items-center gap-3">
                <CardTitle class="text-xl">{{ score.exam.title }}</CardTitle>
                <Badge :variant="getStatusVariant(score.status)">
                  {{ score.status.replace('_', ' ').toUpperCase() }}
                </Badge>
              </div>
              <CardDescription>{{ score.exam.description }}</CardDescription>
              <div class="flex items-center gap-2 text-xs text-muted-foreground">
                <Target class="h-3 w-3" />
                <span>Attempt #{{ score.exam_attempt_number }}</span>
              </div>
            </div>

            <div v-if="score.recommendation_score !== null" class="text-right">
              <div class="text-4xl font-bold" :class="getScoreColor(score.recommendation_score)">
                {{ score.recommendation_score }}%
              </div>
              <p class="text-xs text-muted-foreground mt-1">Score</p>
            </div>
          </div>
        </CardHeader>

        <CardContent class="space-y-4">
          <!-- Stats Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="space-y-1">
              <p class="text-xs text-muted-foreground flex items-center gap-1">
                <FileText class="h-3 w-3" />
                Total Questions
              </p>
              <p class="text-2xl font-bold">{{ score.total_questions }}</p>
            </div>
            <div class="space-y-1">
              <p class="text-xs text-muted-foreground flex items-center gap-1">
                <TrendingUp class="h-3 w-3" />
                Attempted
              </p>
              <p class="text-2xl font-bold">{{ score.attempted_questions }}</p>
            </div>
            <div class="space-y-1">
              <p class="text-xs text-muted-foreground flex items-center gap-1">
                <Award class="h-3 w-3" />
                Correct Answers
              </p>
              <p class="text-2xl font-bold text-green-600">{{ score.correct_answers }}</p>
            </div>
            <div class="space-y-1">
              <p class="text-xs text-muted-foreground flex items-center gap-1">
                <Target class="h-3 w-3" />
                Accuracy
              </p>
              <p class="text-2xl font-bold">
                {{ score.accuracy !== null ? `${score.accuracy}%` : 'N/A' }}
              </p>
            </div>
          </div>

          <!-- Recommended Course -->
          <Alert v-if="score.recommended_course" class="bg-blue-50 border-blue-200">
            <Award class="h-4 w-4 text-blue-600" />
            <AlertDescription>
              <p class="font-semibold text-blue-900">Recommended Course</p>
              <p class="text-sm text-blue-700 mt-1">
                {{ score.recommended_course.code }} - {{ score.recommended_course.name }}
              </p>
            </AlertDescription>
          </Alert>

          <!-- Timestamps -->
          <div class="pt-4 border-t flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-xs text-muted-foreground">
            <div class="flex items-center gap-1">
              <Clock class="h-3 w-3" />
              <span class="font-medium">Started:</span>
              <span>{{ formatDate(score.started_at) }}</span>
            </div>
            <div v-if="score.completed_at" class="flex items-center gap-1">
              <Calendar class="h-3 w-3" />
              <span class="font-medium">Completed:</span>
              <span>{{ formatDate(score.completed_at) }}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>