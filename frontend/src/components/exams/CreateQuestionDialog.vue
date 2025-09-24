<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { toast } from "vue-sonner"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Plus, Trash2 } from "lucide-vue-next"
import { useQuestionsStore } from "@/stores/useAdminManageQuestions"

interface Props {
  open: boolean
  examId: string
}

interface Emits {
  (e: 'update:open', value: boolean): void
  (e: 'question-created'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const questionsStore = useQuestionsStore()

// Form state
const questionText = ref("")
const questionType = ref<"mcq" | "essay" | "true_false">("mcq")
const choices = ref<Array<{
  label: string
  text: string
  is_correct: boolean
}>>([
  { label: "A", text: "", is_correct: false },
  { label: "B", text: "", is_correct: false }
])

const loading = ref(false)

// Computed
const isDialogOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})

const canSubmit = computed(() => {
  if (!questionText.value.trim()) return false
  
  if (questionType.value === "essay") return true
  
  if (questionType.value === "true_false") {
    // For true/false, just check that at least one is marked correct
    return choices.value.slice(0, 2).some(choice => choice.is_correct)
  }
  
  // MCQ validation - check that all choices have text AND at least one is correct
  const validChoices = choices.value.filter(choice => choice.text.trim())
  return validChoices.length >= 2 && choices.value.some(choice => choice.is_correct)
})

// Watch question type changes
watch(questionType, (newType) => {
  if (newType === "essay") {
    choices.value = []
  } else if (newType === "true_false") {
    choices.value = [
      { label: "A", text: "True", is_correct: false },
      { label: "B", text: "False", is_correct: false }
    ]
  } else if (newType === "mcq") {
    choices.value = [
      { label: "A", text: "", is_correct: false },
      { label: "B", text: "", is_correct: false }
    ]
  }
})

// Methods
const addChoice = () => {
  const nextLabel = String.fromCharCode(65 + choices.value.length) // A, B, C, D...
  choices.value.push({
    label: nextLabel,
    text: "",
    is_correct: false
  })
}

const removeChoice = (index: number) => {
  if (choices.value.length > 2) {
    choices.value.splice(index, 1)
    // Re-assign labels
    choices.value.forEach((choice, i) => {
      choice.label = String.fromCharCode(65 + i)
    })
  }
}

const setCorrectAnswer = (index: number) => {
  // For MCQ and True/False, only one answer can be correct
  choices.value.forEach((choice, i) => {
    choice.is_correct = i === index
  })
}

const resetForm = () => {
  questionText.value = ""
  questionType.value = "mcq"
  choices.value = [
    { label: "A", text: "", is_correct: false },
    { label: "B", text: "", is_correct: false }
  ]
  loading.value = false
}

const handleSubmit = async () => {
  // if (!canSubmit.value) return
  
  loading.value = true
  
  try {
    // Create the question
    const questionData = {
    exam_uuid: props.examId,
    text: questionText.value.trim(),
    question_type: questionType.value,
  }


    const createdQuestion = await questionsStore.createQuestion(questionData)
    
    if (questionType.value !== "essay" && choices.value.length > 0) {
      for (const choice of choices.value) {
        if (choice.text.trim()) {
          await questionsStore.createChoice({
            question_uuid: createdQuestion.uuid,
            label: choice.label,
            text: choice.text.trim(),
            is_correct: choice.is_correct
          })
        }
      }
    }
    
    toast.success("Question created successfully")
    emit('question-created')
    isDialogOpen.value = false
    resetForm()
    
  } catch (error: any) {
    console.error('Error creating question:', error)
    toast.error(error.message || "Failed to create question")
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  isDialogOpen.value = false
  resetForm()
}
</script>
<template>
  <Dialog v-model:open="isDialogOpen">
    <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Add New Question</DialogTitle>
        <DialogDescription>
          Create a new question for this exam. Choose the question type and provide the necessary details.
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-6">
        <!-- Question Type -->
        <div class="space-y-2">
          <Label>Question Type</Label>
          <Select v-model:value="questionType">
            <SelectTrigger>
              <SelectValue placeholder="Select question type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="mcq">Multiple Choice</SelectItem>
              <SelectItem value="essay">Essay</SelectItem>
              <SelectItem value="true_false">True/False</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Question Text -->
        <div class="space-y-2">
          <Label for="question-text">Question *</Label>
          <Textarea
            id="question-text"
            v-model="questionText"
            placeholder="Enter your question here..."
            rows="3"
          />
        </div>

        <!-- Choices Section (for MCQ and True/False) -->
        <div v-if="questionType !== 'essay'" class="space-y-4">
          <div class="flex items-center justify-between">
            <Label class="text-base font-medium">Answer Choices</Label>
            <Button
              v-if="questionType === 'mcq' && choices.length < 6"
              type="button"
              variant="outline"
              size="sm"
              @click="addChoice"
            >
              <Plus class="w-4 h-4 mr-1" />
              Add Choice
            </Button>
          </div>

          <div class="space-y-3">
            <div
              v-for="(choice, index) in choices"
              :key="`${choice.label}-${index}`"
              class="flex items-center gap-3 p-3 border rounded-lg"
            >
              <div class="flex items-center gap-2">
                <span class="font-semibold text-sm min-w-[20px]">{{ choice.label }}.</span>
                <Switch
                  :checked="choice.is_correct"
                  @update:checked="() => setCorrectAnswer(index)"
                />
                <Label class="text-xs text-muted-foreground">Correct</Label>
              </div>
              
              <Input
                v-model="choice.text"
                :placeholder="`Choice ${choice.label}`"
                class="flex-1"
                :disabled="questionType === 'true_false'"
              />
              
              <Button
                v-if="questionType === 'mcq' && choices.length > 2"
                type="button"
                variant="ghost"
                size="sm"
                @click="removeChoice(index)"
                class="text-destructive hover:text-destructive"
              >
                <Trash2 class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <p class="text-xs text-muted-foreground">
            Toggle the correct answer by clicking the switch next to each choice.
          </p>
        </div>

        <!-- Essay Question Note -->
        <div v-else class="p-3 bg-muted/50 rounded-lg">
          <p class="text-sm text-muted-foreground">
            This is an essay question. Students will provide written responses that will need to be manually graded.
          </p>
        </div>
      </div>

      <DialogFooter class="mt-6">
        <Button variant="outline" @click="handleCancel" :disabled="loading">
          Cancel
        </Button>

      <Button @click="handleSubmit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Question' }}
      </Button>

      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>