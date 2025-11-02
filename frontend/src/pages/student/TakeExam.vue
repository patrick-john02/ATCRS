<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useExamStore } from '@/stores/useExamStore'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Clock, 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle, 
  AlertTriangle,
  FileText,
  Eye,
  EyeOff,
  Send
} from 'lucide-vue-next'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

const route = useRoute()
const router = useRouter()
const examStore = useExamStore()

const examUuid = route.params.uuid as string
const timerInterval = ref<number | null>(null)
const showSubmitDialog = ref(false)
const showQuestionNav = ref(false)
const showWarning = ref(false)

onMounted(async () => {
  try {
    await examStore.loadExam(examUuid)
    startTimer()
    setupVisibilityListener()
  } catch (error) {
    console.error('Failed to load exam:', error)
  }
})

onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  cleanupVisibilityListener()
  examStore.reset()
})

function startTimer() {
  timerInterval.value = window.setInterval(() => {
    examStore.decrementTimer()
    if (examStore.timeRemaining === 0) {
      handleTimeUp()
    }
  }, 1000)
}

function setupVisibilityListener() {
  document.addEventListener('visibilitychange', handleVisibilityChange)
}

function cleanupVisibilityListener() {
  document.removeEventListener('visibilitychange', handleVisibilityChange)
}

function handleVisibilityChange() {
  if (document.hidden) {
    examStore.incrementTabSwitch()
    showWarning.value = true
    setTimeout(() => {
      showWarning.value = false
    }, 3000)
  }
}

async function handleTimeUp() {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  await handleCompleteExam()
}

const formattedTime = computed(() => {
  const minutes = Math.floor(examStore.timeRemaining / 60)
  const seconds = examStore.timeRemaining % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const timeColor = computed(() => {
  if (examStore.timeRemaining < 300) return 'text-red-600'
  if (examStore.timeRemaining < 600) return 'text-yellow-600'
  return 'text-green-600'
})

const selectedAnswer = computed({
  get: () => {
    if (!examStore.currentQuestion) return ''
    return examStore.selectedAnswers.get(examStore.currentQuestion.uuid) || ''
  },
  set: (value: string) => {
    if (examStore.currentQuestion) {
      examStore.selectAnswer(examStore.currentQuestion.uuid, value)
    }
  },
})

async function handleSubmitAnswer() {
  try {
    await examStore.submitAnswer()
    if (!examStore.isLastQuestion) {
      examStore.nextQuestion()
    }
  } catch (error) {
    console.error('Failed to submit answer:', error)
  }
}

function handlePrevious() {
  examStore.previousQuestion()
}

function handleNext() {
  if (examStore.isLastQuestion) {
    showSubmitDialog.value = true
  } else {
    examStore.nextQuestion()
  }
}

async function handleCompleteExam() {
  try {
    const response = await examStore.completeExam()
    if (timerInterval.value) {
      clearInterval(timerInterval.value)
    }
    // Navigate with UUID from current exam
    router.push({ 
      name: 'exam-result', 
      params: { uuid: examStore.currentExam?.uuid || examUuid }
    })
  } catch (error) {
    console.error('Failed to complete exam:', error)
  }
}

function isQuestionAnswered(questionUuid: string) {
  return examStore.selectedAnswers.has(questionUuid)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-4 md:p-6">
    <!-- Warning Banner -->
    <Transition
      enter-active-class="transition-all duration-300"
      enter-from-class="opacity-0 -translate-y-4"
      leave-active-class="transition-all duration-300"
      leave-to-class="opacity-0 -translate-y-4"
    >
      <Alert v-if="showWarning" class="mb-4 border-yellow-500 bg-yellow-50 max-w-5xl mx-auto">
        <AlertTriangle class="h-4 w-4 text-yellow-600" />
        <AlertDescription class="text-yellow-800">
          Tab switch detected! This activity is being monitored. Count: {{ examStore.tabSwitchCount }}
        </AlertDescription>
      </Alert>
    </Transition>

    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <Card class="mb-6 shadow-lg border-t-4 border-t-blue-600">
        <CardHeader>
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <CardTitle class="text-2xl font-bold text-gray-900">
                {{ examStore.currentExam?.exam_details.title }}
              </CardTitle>
              <CardDescription class="mt-1">
                {{ examStore.currentExam?.exam_details.description }}
              </CardDescription>
            </div>
            
            <div class="flex items-center gap-4">
              <!-- Timer -->
              <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-lg border-2 shadow-sm">
                <Clock :class="['h-5 w-5', timeColor]" />
                <span :class="['text-2xl font-mono font-bold', timeColor]">
                  {{ formattedTime }}
                </span>
              </div>

              <!-- Question Navigator Toggle -->
              <Button
                variant="outline"
                size="sm"
                @click="showQuestionNav = !showQuestionNav"
              >
                <FileText class="h-4 w-4 mr-2" />
                Questions
                <component :is="showQuestionNav ? EyeOff : Eye" class="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>

          <!-- Progress Bar -->
          <div class="mt-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{{ examStore.currentExam?.attempted_questions }} / {{ examStore.currentExam?.total_questions }} answered</span>
            </div>
            <Progress :model-value="examStore.progress" class="h-2" />
          </div>
        </CardHeader>
      </Card>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Question Navigator Sidebar -->
        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 -translate-x-4"
          leave-active-class="transition-all duration-300"
          leave-to-class="opacity-0 -translate-x-4"
        >
          <Card v-if="showQuestionNav" class="lg:col-span-1 shadow-lg h-fit">
            <CardHeader>
              <CardTitle class="text-lg">Questions</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="grid grid-cols-5 lg:grid-cols-4 gap-2">
                <Button
                  v-for="(question, index) in examStore.currentExam?.questions"
                  :key="question.uuid"
                  :variant="examStore.currentQuestionIndex === index ? 'default' : 'outline'"
                  size="sm"
                  class="relative"
                  @click="examStore.goToQuestion(index)"
                >
                  {{ index + 1 }}
                  <CheckCircle
                    v-if="isQuestionAnswered(question.uuid)"
                    class="absolute -top-1 -right-1 h-4 w-4 text-green-600 bg-white rounded-full"
                  />
                </Button>
              </div>
              
              <div class="mt-4 pt-4 border-t space-y-2 text-sm">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 bg-blue-600 rounded"></div>
                  <span>Current</span>
                </div>
                <div class="flex items-center gap-2">
                  <CheckCircle class="w-3 h-3 text-green-600" />
                  <span>Answered</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 border-2 rounded"></div>
                  <span>Not Answered</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </Transition>

        <!-- Main Question Area -->
        <Card :class="['shadow-lg', showQuestionNav ? 'lg:col-span-3' : 'lg:col-span-4']">
          <CardHeader>
            <div class="flex items-center justify-between">
              <Badge variant="secondary" class="text-base px-3 py-1">
                Question {{ examStore.currentQuestionIndex + 1 }} of {{ examStore.currentExam?.total_questions }}
              </Badge>
              <Badge v-if="examStore.currentQuestion?.question_type === 'mcq'" variant="outline">
                Multiple Choice
              </Badge>
            </div>
          </CardHeader>

          <CardContent class="space-y-6">
            <!-- Loading State -->
            <div v-if="examStore.loading && !examStore.currentQuestion" class="text-center py-8">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
              <p class="mt-4 text-gray-600">Loading exam...</p>
            </div>

            <!-- Question Content -->
            <template v-else-if="examStore.currentQuestion">
              <!-- Question Text -->
              <div class="prose max-w-none">
                <p class="text-lg font-medium text-gray-900 leading-relaxed">
                  {{ examStore.currentQuestion?.text }}
                </p>
              </div>

              <!-- Answer Choices -->
              <RadioGroup v-model="selectedAnswer" class="space-y-3">
                <div
                  v-for="choice in examStore.currentQuestion?.choices"
                  :key="choice.uuid"
                  class="flex items-center space-x-3 p-4 rounded-lg border-2 transition-all hover:border-blue-300 hover:bg-blue-50 cursor-pointer"
                  :class="selectedAnswer === choice.uuid ? 'border-blue-600 bg-blue-50' : 'border-gray-200'"
                >
                  <RadioGroupItem :value="choice.uuid" :id="choice.uuid" />
                  <Label
                    :for="choice.uuid"
                    class="flex-1 cursor-pointer font-medium text-gray-900"
                  >
                    <span class="inline-block w-8 h-8 rounded-full bg-gray-200 text-center leading-8 mr-3 font-bold">
                      {{ choice.label }}
                    </span>
                    {{ choice.text }}
                  </Label>
                </div>
              </RadioGroup>

              <!-- Error Message -->
              <Alert v-if="examStore.error" variant="destructive">
                <AlertTriangle class="h-4 w-4" />
                <AlertDescription>{{ examStore.error }}</AlertDescription>
              </Alert>

              <!-- Navigation Buttons -->
              <div class="flex items-center justify-between pt-6 border-t">
                <Button
                  variant="outline"
                  :disabled="examStore.isFirstQuestion"
                  @click="handlePrevious"
                >
                  <ChevronLeft class="h-4 w-4 mr-2" />
                  Previous
                </Button>

                <div class="flex gap-3">
                  <Button
                    :disabled="!selectedAnswer || examStore.loading"
                    @click="handleSubmitAnswer"
                    class="bg-blue-600 hover:bg-blue-700"
                  >
                    <Send class="h-4 w-4 mr-2" />
                    {{ examStore.loading ? 'Submitting...' : 'Submit Answer' }}
                  </Button>

                  <Button
                    v-if="!examStore.isLastQuestion"
                    variant="outline"
                    @click="handleNext"
                  >
                    Next
                    <ChevronRight class="h-4 w-4 ml-2" />
                  </Button>

                  <Button
                    v-else
                    variant="default"
                    class="bg-green-600 hover:bg-green-700"
                    @click="showSubmitDialog = true"
                  >
                    <CheckCircle class="h-4 w-4 mr-2" />
                    Complete Exam
                  </Button>
                </div>
              </div>
            </template>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Submit Exam Dialog -->
    <Dialog v-model:open="showSubmitDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Submit Exam?</DialogTitle>
          <DialogDescription>
            Are you sure you want to submit your exam? You have answered
            <strong>{{ examStore.currentExam?.attempted_questions }}</strong> out of 
            <strong>{{ examStore.currentExam?.total_questions }}</strong> questions.
            <br><br>
            This action cannot be undone and your exam will be graded immediately.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" @click="showSubmitDialog = false">
            Cancel
          </Button>
          <Button @click="handleCompleteExam" :disabled="examStore.loading" class="bg-green-600 hover:bg-green-700">
            <CheckCircle class="h-4 w-4 mr-2" />
            {{ examStore.loading ? 'Submitting...' : 'Yes, Submit Exam' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<style scoped>
.prose p {
  margin: 0;
}
</style>