<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useApplicantUpcomingExamsStore } from '@/stores/useApplicantUpcomingExamsStore'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Loader2, Calendar, Clock, Users, BookOpen, AlertCircle, CheckCircle2, XCircle, Search } from 'lucide-vue-next'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import type { UpcomingExam } from '@/types/applicantUpcomingExams'
import { ref } from 'vue'

const examStore = useApplicantUpcomingExamsStore()
const searchQuery = ref('')
const selectedExam = ref<UpcomingExam | null>(null)
const isDialogOpen = ref(false)

onMounted(() => {
  examStore.fetchExams()
})

const filteredExams = computed(() => {
  if (!searchQuery.value) return examStore.exams
  
  return examStore.exams.filter(exam => 
    exam.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    exam.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const openApplyDialog = (exam: UpcomingExam) => {
  selectedExam.value = exam
  isDialogOpen.value = true
}

const confirmApply = async () => {
  if (!selectedExam.value) return
  
  try {
    await examStore.applyToExam(selectedExam.value)
    toast.success('Successfully applied to exam!', {
      description: `You have been registered for ${selectedExam.value.title}`
    })
    isDialogOpen.value = false
    selectedExam.value = null
  } catch (error: any) {
    toast.error('Failed to apply', {
      description: examStore.error || 'Please try again later'
    })
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatTime = (time: string) => {
  return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const getSlotVariant = (availableSlots: number) => {
  if (availableSlots === 0) return 'destructive'
  if (availableSlots <= 5) return 'secondary'
  return 'default'
}

const getSlotIcon = (availableSlots: number) => {
  if (availableSlots === 0) return XCircle
  if (availableSlots <= 5) return AlertCircle
  return CheckCircle2
}

const getUrgencyBadge = (availableSlots: number, maxApplicants: number) => {
  const percentage = (availableSlots / maxApplicants) * 100
  
  if (percentage === 0) return { text: 'Full', variant: 'destructive' as const }
  if (percentage <= 20) return { text: 'Almost Full', variant: 'destructive' as const }
  if (percentage <= 50) return { text: 'Filling Fast', variant: 'secondary' as const }
  return { text: 'Available', variant: 'default' as const }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-background to-muted/20">
    <div class="container mx-auto px-4 py-8 space-y-8">
      <!-- Header Section -->
      <div class="space-y-4">
        <div class="flex flex-col gap-2">
          <h1 class="text-4xl font-bold tracking-tight bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            Upcoming Exams
          </h1>
          <p class="text-lg text-muted-foreground max-w-2xl">
            Browse available admission exams and secure your slot. Apply early as spaces are limited!
          </p>
        </div>

        <!-- Search Bar -->
        <div class="relative max-w-md">
          <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            v-model="searchQuery"
            placeholder="Search exams by title or description..."
            class="pl-10"
          />
        </div>
      </div>

      <!-- Stats Bar -->
      <div class="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader class="pb-3">
            <CardDescription>Total Exams</CardDescription>
            <CardTitle class="text-3xl">{{ examStore.exams.length }}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader class="pb-3">
            <CardDescription>Available Slots</CardDescription>
            <CardTitle class="text-3xl">
              {{ examStore.exams.reduce((sum, exam) => sum + exam.available_slots, 0) }}
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader class="pb-3">
            <CardDescription>Applied Exams</CardDescription>
            <CardTitle class="text-3xl">
              {{ examStore.exams.filter(exam => exam.is_applied).length }}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      <!-- Error Alert -->
      <Alert v-if="examStore.error && !examStore.loading" variant="destructive">
        <AlertCircle class="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          {{ examStore.error }}
        </AlertDescription>
      </Alert>

      <!-- Loading State -->
      <div v-if="examStore.loading" class="flex flex-col items-center justify-center py-20">
        <Loader2 class="h-12 w-12 animate-spin text-primary mb-4" />
        <p class="text-lg font-medium">Loading exams...</p>
        <p class="text-sm text-muted-foreground">Please wait while we fetch the latest exam schedules</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredExams.length === 0" class="flex flex-col items-center justify-center py-20">
        <div class="rounded-full bg-muted p-6 mb-4">
          <BookOpen class="h-12 w-12 text-muted-foreground" />
        </div>
        <h3 class="text-2xl font-semibold mb-2">
          {{ searchQuery ? 'No exams found' : 'No upcoming exams' }}
        </h3>
        <p class="text-muted-foreground text-center max-w-md mb-6">
          {{ searchQuery 
            ? 'Try adjusting your search terms to find what you\'re looking for' 
            : 'There are no exam schedules available at the moment. Check back later for new schedules' 
          }}
        </p>
        <Button v-if="searchQuery" variant="outline" @click="searchQuery = ''">
          Clear Search
        </Button>
      </div>

      <!-- Exams Grid -->
      <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card 
          v-for="exam in filteredExams" 
          :key="exam.uuid"
          class="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 relative overflow-hidden"
          :class="{
            'ring-2 ring-primary': exam.is_applied,
            'opacity-75': exam.available_slots === 0
          }"
        >
          <!-- Applied Badge -->
          <div 
            v-if="exam.is_applied" 
            class="absolute top-0 right-0 bg-primary text-primary-foreground px-3 py-1 text-xs font-semibold rounded-bl-lg"
          >
            ✓ Applied
          </div>

          <CardHeader class="space-y-3">
            <div class="flex items-start justify-between gap-3">
              <div class="space-y-1 flex-1">
                <CardTitle class="text-xl group-hover:text-primary transition-colors line-clamp-2">
                  {{ exam.title }}
                </CardTitle>
                <CardDescription class="line-clamp-2 text-sm">
                  {{ exam.description || 'No description available' }}
                </CardDescription>
              </div>
            </div>

            <!-- Urgency Badge -->
            <div class="flex gap-2">
              <Badge :variant="getUrgencyBadge(exam.available_slots, exam.max_applicants).variant">
                {{ getUrgencyBadge(exam.available_slots, exam.max_applicants).text }}
              </Badge>
              <Badge :variant="getSlotVariant(exam.available_slots)" class="gap-1">
                <component :is="getSlotIcon(exam.available_slots)" class="h-3 w-3" />
                {{ exam.available_slots }} slots left
              </Badge>
            </div>
          </CardHeader>
        
          <CardContent class="space-y-4">
            <Separator />
            
            <div class="space-y-3">
              <!-- Date -->
              <div class="flex items-start gap-3">
                <div class="rounded-lg bg-primary/10 p-2">
                  <Calendar class="h-4 w-4 text-primary" />
                </div>
                <div class="flex-1 space-y-1">
                  <p class="text-xs font-medium text-muted-foreground">Exam Date</p>
                  <p class="text-sm font-semibold">{{ formatDate(exam.date) }}</p>
                </div>
              </div>

              <!-- Time -->
              <div class="flex items-start gap-3">
                <div class="rounded-lg bg-primary/10 p-2">
                  <Clock class="h-4 w-4 text-primary" />
                </div>
                <div class="flex-1 space-y-1">
                  <p class="text-xs font-medium text-muted-foreground">Time & Duration</p>
                  <p class="text-sm font-semibold">
                    {{ formatTime(exam.start_time) }} - {{ formatTime(exam.end_time) }}
                  </p>
                  <p class="text-xs text-muted-foreground">{{ exam.duration_minutes }} minutes</p>
                </div>
              </div>

              <!-- Capacity -->
              <div class="flex items-start gap-3">
                <div class="rounded-lg bg-primary/10 p-2">
                  <Users class="h-4 w-4 text-primary" />
                </div>
                <div class="flex-1 space-y-1">
                  <p class="text-xs font-medium text-muted-foreground">Capacity</p>
                  <div class="flex items-center gap-2">
                    <div class="flex-1 bg-muted rounded-full h-2 overflow-hidden">
                      <div 
                        class="h-full bg-primary transition-all"
                        :style="{ width: `${((exam.max_applicants - exam.available_slots) / exam.max_applicants) * 100}%` }"
                      />
                    </div>
                    <p class="text-xs font-medium">
                      {{ exam.max_applicants - exam.available_slots }}/{{ exam.max_applicants }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Attempts -->
              <div class="flex items-start gap-3">
                <div class="rounded-lg bg-primary/10 p-2">
                  <BookOpen class="h-4 w-4 text-primary" />
                </div>
                <div class="flex-1 space-y-1">
                  <p class="text-xs font-medium text-muted-foreground">Max Attempts</p>
                  <p class="text-sm font-semibold">{{ exam.max_attempts }} attempt{{ exam.max_attempts > 1 ? 's' : '' }}</p>
                </div>
              </div>
            </div>
          </CardContent>

          <CardFooter class="pt-4">
            <Button 
              @click="openApplyDialog(exam)" 
              :disabled="exam.is_applied || exam.available_slots === 0"
              class="w-full"
              :variant="exam.is_applied ? 'outline' : 'default'"
              size="lg"
            >
              <CheckCircle2 v-if="exam.is_applied" class="mr-2 h-4 w-4" />
              <XCircle v-else-if="exam.available_slots === 0" class="mr-2 h-4 w-4" />
              
              <span v-if="exam.is_applied">Already Applied</span>
              <span v-else-if="exam.available_slots === 0">Fully Booked</span>
              <span v-else>Apply Now</span>
            </Button>
          </CardFooter>
        </Card>
      </div>

      <!-- Apply Confirmation Dialog -->
      <Dialog v-model:open="isDialogOpen">
        <DialogContent class="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Confirm Application</DialogTitle>
            <DialogDescription>
              You are about to apply for this exam. Please review the details below.
            </DialogDescription>
          </DialogHeader>

          <div v-if="selectedExam" class="space-y-4 py-4">
            <div class="space-y-2">
              <h4 class="font-semibold text-lg">{{ selectedExam.title }}</h4>
              <p class="text-sm text-muted-foreground">{{ selectedExam.description }}</p>
            </div>

            <Separator />

            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">Date:</span>
                <span class="font-medium">{{ formatDate(selectedExam.date) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">Time:</span>
                <span class="font-medium">
                  {{ formatTime(selectedExam.start_time) }} - {{ formatTime(selectedExam.end_time) }}
                </span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">Duration:</span>
                <span class="font-medium">{{ selectedExam.duration_minutes }} minutes</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">Slots Available:</span>
                <span class="font-medium">{{ selectedExam.available_slots }} / {{ selectedExam.max_applicants }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">Max Attempts:</span>
                <span class="font-medium">{{ selectedExam.max_attempts }}</span>
              </div>
            </div>

            <Alert>
              <AlertCircle class="h-4 w-4" />
              <AlertDescription class="text-sm">
                Once you apply, you cannot withdraw your application. Make sure you can attend on the scheduled date and time.
              </AlertDescription>
            </Alert>
          </div>

          <DialogFooter class="gap-2 sm:gap-0">
            <Button 
              variant="outline" 
              @click="isDialogOpen = false"
              :disabled="examStore.loading"
            >
              Cancel
            </Button>
            <Button 
              @click="confirmApply"
              :disabled="examStore.loading"
            >
              <Loader2 v-if="examStore.loading" class="mr-2 h-4 w-4 animate-spin" />
              Confirm Application
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>