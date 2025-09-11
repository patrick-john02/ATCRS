<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { toast } from "vue-sonner"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Calendar, Clock, FileText, Settings, Trash2, Plus, Eye, Edit, ArrowLeft } from "lucide-vue-next"

import { useExamsStore } from "@/stores/useAdminManageExams"
import { useQuestionsStore } from "@/stores/useAdminManageQuestions"
import CreateQuestionDialog from "@/components/exams/CreateQuestionDialog.vue"

const examStore = useExamsStore()
const questionsStore = useQuestionsStore()
const route = useRoute()
const router = useRouter()
const examId = computed(() => route.params.id as string)
const isEditDialogOpen = ref(false)
const isDeleteDialogOpen = ref(false)
const isQuestionDeleteDialogOpen = ref(false)
const isCreateQuestionDialogOpen = ref(false)
const questionToDelete = ref<string | null>(null)
const editTitle = ref("")
const editDescription = ref("")
const editDate = ref("")
const editStartTime = ref("")
const editEndTime = ref("")
const editDurationMinutes = ref(0)
const editAccessCode = ref("")
const editIsActive = ref(false)

onMounted(async () => {
  if (examId.value) {
    try {
      await examStore.loadExamById(examId.value)
      populateEditForm()
    } catch (error: any) {
      toast.error(error.message || "Failed to load exam")
    }
  }
})

const exam = computed(() => examStore.currentExam)
const loading = computed(() => examStore.loading)
const error = computed(() => examStore.error)

const populateEditForm = () => {
  if (examStore.currentExam) {
    const e = examStore.currentExam
    editTitle.value = e.title
    editDescription.value = e.description
    editDate.value = e.date
    editStartTime.value = e.start_time
    editEndTime.value = e.end_time
    editDurationMinutes.value = e.duration_minutes
    editAccessCode.value = e.access_code
    editIsActive.value = e.is_active
  }
}

const openEditDialog = () => {
  populateEditForm()
  isEditDialogOpen.value = true
}

const handleSave = async () => {
  if (!exam.value) return
  
  try {
    await examStore.updateExam(exam.value.uuid, {
      title: editTitle.value,
      description: editDescription.value,
      date: editDate.value,
      start_time: editStartTime.value,
      end_time: editEndTime.value,
      duration_minutes: editDurationMinutes.value,
      access_code: editAccessCode.value,
      is_active: editIsActive.value,
    })
    toast.success("Exam updated successfully")
    isEditDialogOpen.value = false
  } catch (err: any) {
    toast.error(err.message || "Failed to update exam")
  }
}

const handleToggleStatus = async () => {
  if (!exam.value) return
  
  try {
    await examStore.toggleExamStatus(exam.value.uuid)
    toast.success(`Exam ${!exam.value.is_active ? 'activated' : 'deactivated'} successfully`)
  } catch (err: any) {
    toast.error(err.message || "Failed to toggle exam status")
  }
}

const handleDelete = async () => {
  if (!exam.value) return
  
  try {
    await examStore.deleteExam(exam.value.uuid)
    toast.success("Exam deleted successfully")
    router.push({ name: "AdminManageExams" })
  } catch (err: any) {
    toast.error(err.message || "Failed to delete exam")
  }
}

const generateAccessCode = () => {
  const code = Math.random().toString(36).substr(2, 8).toUpperCase()
  editAccessCode.value = code
}

const handleAddQuestion = () => {
  isCreateQuestionDialogOpen.value = true
}

const handleQuestionCreated = async () => {
  if (examId.value) {
    try {
      await examStore.loadExamById(examId.value)
      toast.success("Question added successfully")
    } catch (error: any) {
      toast.error(error.message || "Failed to refresh exam data")
    }
  }
}

const handleEditQuestion = (questionId: string) => {
  toast.info("Question editing feature coming soon")
}

const handleViewQuestion = (questionId: string) => {
  toast.info("Question detail view coming soon")
}

const handleDeleteQuestion = (questionId: string) => {
  questionToDelete.value = questionId
  isQuestionDeleteDialogOpen.value = true
}

const confirmDeleteQuestion = async () => {
  if (!questionToDelete.value) return
  
  try {
    await questionsStore.deleteQuestion(questionToDelete.value)
    toast.success("Question deleted successfully")
    
    if (examId.value) {
      await examStore.loadExamById(examId.value)
    }
  } catch (error: any) {
    toast.error(error.message || "Failed to delete question")
  } finally {
    isQuestionDeleteDialogOpen.value = false
    questionToDelete.value = null
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatTime = (timeString: string) => {
  return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const examStats = computed(() => {
  if (!exam.value) return null
  
  const totalQuestions = exam.value.questions?.length || 0
  const mcqQuestions = exam.value.questions?.filter(q => q.question_type === 'mcq').length || 0
  const essayQuestions = exam.value.questions?.filter(q => q.question_type === 'essay').length || 0
  const trueFalseQuestions = exam.value.questions?.filter(q => q.question_type === 'true_false').length || 0
  
  return {
    totalQuestions,
    mcqQuestions,
    essayQuestions,
    trueFalseQuestions
  }
})

const getQuestionTypeDisplay = (type: string) => {
  const types: Record<string, string> = {
    'mcq': 'Multiple Choice',
    'essay': 'Essay',
    'true_false': 'True/False'
  }
  return types[type] || type.toUpperCase()
}

const getQuestionTypeVariant = (type: string): "default" | "secondary" | "outline" => {
  const variants: Record<string, "default" | "secondary" | "outline"> = {
    'mcq': 'default',
    'essay': 'secondary',
    'true_false': 'outline'
  }
  return variants[type] || 'outline'
}
</script>

<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <Button 
          @click="() => router.push({ name: 'AdminManageExams' })" 
          variant="ghost" 
          size="sm"
          class="px-2"
        >
          <ArrowLeft class="w-4 h-4" />
        </Button>
        <div>
          <h1 class="text-3xl font-bold tracking-tight">Exam Management</h1>
          <p class="text-muted-foreground">
            Manage exam details, questions, and settings
          </p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="text-center space-y-3">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
        <p class="text-muted-foreground">Loading exam details...</p>
      </div>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <div class="mx-auto flex items-center justify-center w-12 h-12 rounded-full bg-red-100">
        <FileText class="h-6 w-6 text-red-600" />
      </div>
      <h3 class="mt-2 text-sm font-semibold text-gray-900">Error Loading Exam</h3>
      <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
      <div class="mt-6">
        <Button @click="() => router.push({ name: 'AdminManageExams' })" variant="outline">
          Back to Exams
        </Button>
      </div>
    </div>

    <!-- Exam Details -->
    <div v-else-if="exam" class="space-y-6">
      <Card>
        <CardHeader>
          <div class="flex items-start justify-between">
            <div class="space-y-2">
              <div class="flex items-center gap-3">
                <h2 class="text-2xl font-bold">{{ exam.title }}</h2>
                <Badge :variant="exam.is_active ? 'default' : 'secondary'">
                  {{ exam.is_active ? 'Active' : 'Inactive' }}
                </Badge>
              </div>
              <p class="text-muted-foreground" v-if="exam.description">{{ exam.description }}</p>
              <p class="text-sm text-muted-foreground">
                Created: {{ formatDate(exam.created_at) }} | 
                Updated: {{ formatDate(exam.updated_at) }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <Button @click="openEditDialog" size="sm">
                <Settings class="w-4 h-4 mr-2" />
                Edit
              </Button>
              <Button 
                @click="handleToggleStatus" 
                :variant="exam.is_active ? 'secondary' : 'default'"
                size="sm"
                :disabled="loading"
              >
                {{ exam.is_active ? 'Deactivate' : 'Activate' }}
              </Button>
              <AlertDialog v-model:open="isDeleteDialogOpen">
                <Button variant="destructive" size="sm" @click="isDeleteDialogOpen = true">
                  <Trash2 class="w-4 h-4 mr-2" />
                  Delete
                </Button>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete Exam</AlertDialogTitle>
                    <AlertDialogDescription>
                      Are you sure you want to delete "{{ exam.title }}"? This action cannot be undone and will remove all associated questions and student responses.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel @click="isDeleteDialogOpen = false">Cancel</AlertDialogCancel>
                    <AlertDialogAction 
                      @click="handleDelete" 
                      class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                      :disabled="loading"
                    >
                      {{ loading ? 'Deleting...' : 'Delete Exam' }}
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
        </CardHeader>
      </Card>

      <!-- Exam Information Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center space-x-2">
              <Calendar class="h-5 w-5 text-blue-500" />
              <div class="space-y-1">
                <p class="text-sm font-medium leading-none">Date</p>
                <p class="text-sm text-muted-foreground">
                  {{ formatDate(exam.date) }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Time Card -->
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center space-x-2">
              <Clock class="h-5 w-5 text-green-500" />
              <div class="space-y-1">
                <p class="text-sm font-medium leading-none">Time Range</p>
                <p class="text-sm text-muted-foreground">
                  {{ formatTime(exam.start_time) }} - {{ formatTime(exam.end_time) }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Duration Card -->
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center space-x-2">
              <Clock class="h-5 w-5 text-orange-500" />
              <div class="space-y-1">
                <p class="text-sm font-medium leading-none">Duration</p>
                <p class="text-sm text-muted-foreground">
                  {{ exam.duration_minutes }} minutes
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Questions Card -->
        <Card>
          <CardContent class="pt-6">
            <div class="flex items-center space-x-2">
              <FileText class="h-5 w-5 text-purple-500" />
              <div class="space-y-1">
                <p class="text-sm font-medium leading-none">Questions</p>
                <p class="text-sm text-muted-foreground">
                  {{ examStats?.totalQuestions || 0 }} total
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Exam Details -->
      <Card>
        <CardHeader>
          <CardTitle>Access & Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div>
                <Label class="text-sm font-medium text-muted-foreground">Access Code</Label>
                <p class="font-mono text-lg font-semibold bg-muted px-3 py-2 rounded-md inline-block">
                  {{ exam.access_code }}
                </p>
              </div>
              <div>
                <Label class="text-sm font-medium text-muted-foreground">Status</Label>
                <div class="mt-1">
                  <Badge :variant="exam.is_active ? 'default' : 'secondary'">
                    {{ exam.is_active ? 'Active - Students can access' : 'Inactive - Hidden from students' }}
                  </Badge>
                </div>
              </div>
            </div>
            <div class="space-y-4" v-if="examStats">
              <div>
                <Label class="text-sm font-medium text-muted-foreground">Question Breakdown</Label>
                <div class="space-y-2 mt-2">
                  <div class="flex justify-between text-sm">
                    <span>Multiple Choice:</span>
                    <span class="font-medium">{{ examStats.mcqQuestions }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span>Essay Questions:</span>
                    <span class="font-medium">{{ examStats.essayQuestions }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span>True/False:</span>
                    <span class="font-medium">{{ examStats.trueFalseQuestions }}</span>
                  </div>
                  <Separator />
                  <div class="flex justify-between text-sm font-semibold">
                    <span>Total:</span>
                    <span>{{ examStats.totalQuestions }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Questions Section -->
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-4">
          <div class="space-y-1">
            <CardTitle class="text-xl">Questions</CardTitle>
            <p class="text-sm text-muted-foreground">
              Manage exam questions and their choices
            </p>
          </div>
          <Button size="sm" @click="handleAddQuestion">
            <Plus class="w-4 h-4 mr-2" />
            Add Question
          </Button>
        </CardHeader>
        <CardContent>
          <div v-if="exam.questions && exam.questions.length > 0" class="space-y-4">
            <div
              v-for="(question, index) in exam.questions"
              :key="question.uuid"
              class="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1 space-y-3">
                  <div class="flex items-center gap-2">
                    <Badge variant="outline" class="font-mono text-xs">
                      Q{{ index + 1 }}
                    </Badge>
                    <Badge :variant="getQuestionTypeVariant(question.question_type)">
                      {{ getQuestionTypeDisplay(question.question_type) }}
                    </Badge>
                  </div>
                  
                  <div class="space-y-2">
                    <p class="font-medium text-sm leading-relaxed">{{ question.text }}</p>
                    
                    <!-- Choices for MCQ/True-False -->
                    <div v-if="question.choices && question.choices.length > 0" class="ml-4 space-y-2">
                      <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        Answer Choices:
                      </p>
                      <div class="grid grid-cols-1 gap-2">
                        <div
                          v-for="choice in question.choices"
                          :key="choice.uuid"
                          class="flex items-start gap-3 text-sm p-2 rounded-md"
                          :class="choice.is_correct ? 'bg-green-50 border-l-2 border-l-green-500' : 'bg-muted/30'"
                        >
                          <span class="font-semibold text-xs min-w-[20px] mt-0.5 uppercase">
                            {{ choice.label }}.
                          </span>
                          <span class="flex-1">{{ choice.text }}</span>
                          <Badge v-if="choice.is_correct" variant="default" size="sm" class="text-xs">
                            Correct
                          </Badge>
                        </div>
                      </div>
                    </div>
                    
                    <div v-else-if="question.question_type === 'essay'" class="ml-4">
                      <p class="text-xs text-muted-foreground italic">
                        This is an essay question. Students will provide written responses.
                      </p>
                    </div>
                  </div>
                  
                  <p class="text-xs text-muted-foreground">
                    Created: {{ formatDate(question.created_at) }}
                  </p>
                </div>
                
                <div class="flex items-center gap-1 ml-4">
                  <Button size="sm" variant="ghost" @click="handleViewQuestion(question.uuid)">
                    <Eye class="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="ghost" @click="handleEditQuestion(question.uuid)">
                    <Edit class="w-4 h-4" />
                  </Button>
                  <Button 
                    size="sm" 
                    variant="ghost" 
                    @click="handleDeleteQuestion(question.uuid)"
                    class="text-destructive hover:text-destructive"
                  >
                    <Trash2 class="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>

          <!-- No Questions State -->
          <div v-else class="text-center py-12">
            <FileText class="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 class="mt-4 text-lg font-semibold text-gray-900">No questions yet</h3>
            <p class="mt-2 text-sm text-muted-foreground max-w-sm mx-auto">
              Get started by adding your first question to this exam. You can create multiple choice, essay, or true/false questions.
            </p>
            <div class="mt-6">
              <Button @click="handleAddQuestion">
                <Plus class="w-4 h-4 mr-2" />
                Add Your First Question
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Edit Exam Dialog -->
    <Dialog v-model:open="isEditDialogOpen">
      <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Edit Exam</DialogTitle>
          <DialogDescription>Update the exam details below.</DialogDescription>
        </DialogHeader>

        <div class="space-y-6">
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Basic Information</h4>
            <div class="grid grid-cols-1 gap-4">
              <div>
                <Label for="title">Title *</Label>
                <Input id="title" v-model="editTitle" placeholder="Enter exam title" />
              </div>
              <div>
                <Label for="description">Description</Label>
                <Textarea 
                  id="description" 
                  v-model="editDescription" 
                  placeholder="Enter exam description"
                  rows="3"
                />
              </div>
            </div>
          </div>

          <Separator />

          <div class="space-y-4">
            <h4 class="text-sm font-medium">Schedule & Settings</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label for="date">Date *</Label>
                <Input id="date" type="date" v-model="editDate" />
              </div>
              <div>
                <Label for="duration">Duration (minutes) *</Label>
                <Input 
                  id="duration" 
                  type="number" 
                  v-model.number="editDurationMinutes" 
                  min="1"
                  placeholder="120"
                />
              </div>
              <div>
                <Label for="start_time">Start Time *</Label>
                <Input id="start_time" type="time" v-model="editStartTime" />
              </div>
              <div>
                <Label for="end_time">End Time *</Label>
                <Input id="end_time" type="time" v-model="editEndTime" />
              </div>
            </div>
          </div>

          <Separator />

          <!-- Access & Status -->
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Access & Status</h4>
            <div class="space-y-4">
              <div>
                <Label for="access_code">Access Code *</Label>
                <div class="flex gap-2">
                  <Input 
                    id="access_code" 
                    v-model="editAccessCode" 
                    placeholder="Enter access code"
                    class="font-mono flex-1"
                  />
                  <Button 
                    type="button" 
                    variant="outline" 
                    @click="generateAccessCode"
                    class="px-3"
                  >
                    Generate
                  </Button>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <Switch id="is_active" v-model:checked="editIsActive" />
                <Label for="is_active">Active (students can access this exam)</Label>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter class="mt-6">
          <Button variant="outline" @click="isEditDialogOpen = false">Cancel</Button>
          <Button @click="handleSave" :disabled="loading || !editTitle.trim()">
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <CreateQuestionDialog
      :open="isCreateQuestionDialogOpen"
      @update:open="(value) => isCreateQuestionDialogOpen = value"
      :exam-id="examId"
      @question-created="handleQuestionCreated"
    />

    <AlertDialog v-model:open="isQuestionDeleteDialogOpen">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Question</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete this question? This action cannot be undone and will remove the question and all its associated choices.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel @click="() => { isQuestionDeleteDialogOpen = false; questionToDelete = null; }">
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction 
            @click="confirmDeleteQuestion" 
            class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            Delete Question
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>