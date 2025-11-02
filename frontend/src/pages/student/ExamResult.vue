<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router' // ✅ include useRoute
import { useExamStore } from '@/stores/useExamStore'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Trophy, 
  CheckCircle, 
  XCircle, 
  Award,
  Home,
  RotateCcw,
  ArrowRight
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute() // ✅ added route
const examStore = useExamStore()
const result = computed(() => examStore.completionResult)
const loading = ref(true)

const scorePercentage = computed(() => {
  if (!result.value) return 0
  return result.value.score
})

const isPassed = computed(() => scorePercentage.value >= 70)

const scoreColor = computed(() => {
  const score = scorePercentage.value
  if (score >= 80) return 'text-green-600'
  if (score >= 70) return 'text-blue-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
})

const scoreBgColor = computed(() => {
  const score = scorePercentage.value
  if (score >= 80) return 'bg-green-50 border-green-200'
  if (score >= 70) return 'bg-blue-50 border-blue-200'
  if (score >= 60) return 'bg-yellow-50 border-yellow-200'
  return 'bg-red-50 border-red-200'
})

const performanceMessage = computed(() => {
  const score = scorePercentage.value
  if (score >= 90) return { title: 'Outstanding!', message: 'Excellent performance! You have mastered the material.' }
  if (score >= 80) return { title: 'Great Job!', message: 'Very good performance! You have a strong understanding.' }
  if (score >= 70) return { title: 'Good Work!', message: 'Good performance! You have passed the exam.' }
  if (score >= 60) return { title: 'Fair Performance', message: 'You did okay, but there is room for improvement.' }
  return { title: 'Needs Improvement', message: 'Keep studying and try again. You can do better!' }
})

// ✅ async mount logic
onMounted(async () => {
  if (route.params.uuid && !result.value) {
    try {
      await examStore.fetchExamResult(route.params.uuid as string)
    } catch (error) {
      console.error('Failed to load exam result:', error)
      router.push({ name: 'exam-history' })
      return
    }
  }

  if (!result.value) {
    router.push({ name: 'exam-history' })
    return
  }

  loading.value = false
})

// ✅ use arrow functions for template recognition
const goToHistory = () => {
  examStore.clearCompletionResult()
  router.push({ name: 'exam-history' })
}

const goToDashboard = () => {
  examStore.clearCompletionResult()
  router.push({ name: 'StudentDashboard' })
}
</script>


<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-4 md:p-6">
    <!-- Loading State -->
    <div v-if="loading" class="max-w-4xl mx-auto">
      <Card class="shadow-xl">
        <CardContent class="p-12 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p class="mt-4 text-gray-600">Loading exam results...</p>
        </CardContent>
      </Card>
    </div>

    <div class="max-w-4xl mx-auto space-y-6">
      <!-- Result Header -->
      <Card :class="['shadow-xl border-t-4', isPassed ? 'border-t-green-500' : 'border-t-red-500']">
        <CardHeader class="text-center pb-4">
          <div class="flex justify-center mb-4">
            <div :class="['p-4 rounded-full', isPassed ? 'bg-green-100' : 'bg-red-100']">
              <component 
                :is="isPassed ? Trophy : XCircle" 
                :class="['h-16 w-16', isPassed ? 'text-green-600' : 'text-red-600']" 
              />
            </div>
          </div>
          <CardTitle class="text-3xl font-bold mb-2">
            {{ performanceMessage.title }}
          </CardTitle>
          <CardDescription class="text-lg">
            {{ performanceMessage.message }}
          </CardDescription>
        </CardHeader>
      </Card>

      <!-- Score Card -->
      <Card :class="['shadow-lg border-2', scoreBgColor]">
        <CardContent class="pt-6">
          <div class="text-center space-y-4">
            <div>
              <p class="text-gray-600 text-lg mb-2">Your Score</p>
              <p :class="['text-6xl font-bold', scoreColor]">
                {{ scorePercentage }}%
              </p>
            </div>
            
            <Progress :model-value="scorePercentage" class="h-3" />
            
            <div class="flex justify-center gap-8 pt-4">
              <div class="text-center">
                <div class="flex items-center justify-center gap-2 mb-1">
                  <CheckCircle class="h-5 w-5 text-green-600" />
                  <p class="text-2xl font-bold text-green-600">{{ result?.correct_answers }}</p>
                </div>
                <p class="text-sm text-gray-600">Correct</p>
              </div>
              
              <div class="h-12 w-px bg-gray-300"></div>
              
              <div class="text-center">
                <div class="flex items-center justify-center gap-2 mb-1">
                  <XCircle class="h-5 w-5 text-red-600" />
                  <p class="text-2xl font-bold text-red-600">
                    {{ (result?.total_questions || 0) - (result?.correct_answers || 0) }}
                  </p>
                </div>
                <p class="text-sm text-gray-600">Incorrect</p>
              </div>
              
              <div class="h-12 w-px bg-gray-300"></div>
              
              <div class="text-center">
                <div class="flex items-center justify-center gap-2 mb-1">
                  <Award class="h-5 w-5 text-blue-600" />
                  <p class="text-2xl font-bold text-blue-600">{{ result?.total_questions }}</p>
                </div>
                <p class="text-sm text-gray-600">Total</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Recommended Course Card -->
      <Card v-if="result?.recommended_course" class="shadow-lg border-2 border-purple-200 bg-purple-50">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Award class="h-6 w-6 text-purple-600" />
            Recommended Course
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xl font-bold text-gray-900">{{ result.recommended_course }}</p>
              <p class="text-sm text-gray-600 mt-1">Based on your exam performance</p>
            </div>
            <Badge class="bg-purple-600 text-white px-4 py-2 text-base">
              Recommended
            </Badge>
          </div>
        </CardContent>
      </Card>

      <!-- Pass/Fail Status -->
      <Card :class="['shadow-lg border-2', isPassed ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50']">
        <CardContent class="pt-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div :class="['p-3 rounded-full', isPassed ? 'bg-green-100' : 'bg-red-100']">
                <component 
                  :is="isPassed ? CheckCircle : XCircle" 
                  :class="['h-8 w-8', isPassed ? 'text-green-600' : 'text-red-600']" 
                />
              </div>
              <div>
                <p class="text-lg font-semibold text-gray-900">
                  {{ isPassed ? 'Congratulations! You Passed!' : 'You Did Not Pass' }}
                </p>
                <p class="text-sm text-gray-600">
                  {{ isPassed ? 'You have successfully completed the exam.' : 'Passing score is 70%. Keep practicing!' }}
                </p>
              </div>
            </div>
            <Badge 
              :variant="isPassed ? 'default' : 'destructive'" 
              class="px-4 py-2 text-base"
            >
              {{ isPassed ? 'PASSED' : 'FAILED' }}
            </Badge>
          </div>
        </CardContent>
      </Card>

      <!-- Action Buttons -->
      <Card class="shadow-lg">
        <CardContent class="pt-6">
          <div class="flex flex-col sm:flex-row gap-3">
            <Button 
              @click="goToDashboard" 
              class="flex-1"
              variant="outline"
            >
              <Home class="h-4 w-4 mr-2" />
              Go to Dashboard
            </Button>
            
            <Button 
              @click="goToHistory" 
              class="flex-1"
              variant="outline"
            >
              <RotateCcw class="h-4 w-4 mr-2" />
              View Exam History
            </Button>
            
            <Button 
              v-if="!isPassed"
              @click="router.push({ name: 'upcoming-exams' })"
              class="flex-1"
            >
              <ArrowRight class="h-4 w-4 mr-2" />
              Try Another Exam
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>