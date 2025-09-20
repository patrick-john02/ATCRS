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
  question: {
    uuid: string
    text: string
    question_type: "mcq" | "essay" | "true_false"
    choices?: Array<{ uuid?: string; label: string; text: string; is_correct: boolean }>
  }
}
interface Emits {
  (e: 'update:open', value: boolean): void
  (e: 'question-updated'): void
}
const props = withDefaults(defineProps<Props>(), {
  question: () => ({
    uuid: "",
    text: "",
    question_type: "mcq",
    choices: [],
  }),
})
const emit = defineEmits<Emits>()
const questionsStore = useQuestionsStore()
const questionText = ref(props.question?.text || "")
const questionType = ref(props.question?.question_type || "mcq")
const choices = ref<Array<{ uuid?: string; label: string; text: string; is_correct: boolean }>>(
  props.question?.choices ? [...props.question.choices] : []
)
const loading = ref(false)
const isDialogOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})
watch(questionType, (newType) => {
  if (newType === "essay") {
    choices.value = []
  } else if (newType === "true_false") {
    choices.value = [
      { label: "A", text: "True", is_correct: false },
      { label: "B", text: "False", is_correct: false }
    ]
  } else if (newType === "mcq" && choices.value.length === 0) {
    choices.value = [
      { label: "A", text: "", is_correct: false },
      { label: "B", text: "", is_correct: false }
    ]
  }
})

// Watch for prop changes to update form data
watch(() => props.question, (newQuestion) => {
  if (newQuestion) {
    questionText.value = newQuestion.text
    questionType.value = newQuestion.question_type
    choices.value = newQuestion.choices ? [...newQuestion.choices] : []
  }
}, { immediate: true, deep: true })

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    // Reset form when dialog opens
    resetForm()
  }
})

const addChoice = () => {
  const nextLabel = String.fromCharCode(65 + choices.value.length)
  choices.value.push({ label: nextLabel, text: "", is_correct: false })
}
const removeChoice = (index: number) => {
  if (choices.value.length > 2) {
    choices.value.splice(index, 1)
    choices.value.forEach((choice, i) => {
      choice.label = String.fromCharCode(65 + i)
    })
  }
}
const setCorrectAnswer = (index: number) => {
  choices.value.forEach((choice, i) => {
    choice.is_correct = i === index
  })
}
const resetForm = () => {
  questionText.value = props.question?.text || ""
  questionType.value = props.question?.question_type || "mcq"
  choices.value = props.question?.choices ? [...props.question.choices] : []
  loading.value = false
}
const handleSubmit = async () => {
  loading.value = true
  try {
    // Update the question
    await questionsStore.updateQuestion(props.question.uuid, {
      text: questionText.value.trim(),
      question_type: questionType.value,
    })

    // Handle choices for MCQ and True/False questions
    if (questionType.value !== "essay") {
      // Get existing choices from props
      const existingChoices = props.question.choices || []
      
      // Update or create choices
      for (let i = 0; i < choices.value.length; i++) {
        const choice = choices.value[i]
        const existingChoice = existingChoices[i]
        
        if (existingChoice && existingChoice.uuid) {
          // Update existing choice
          await questionsStore.updateChoice(existingChoice.uuid, {
            label: choice.label,
            text: choice.text,
            is_correct: choice.is_correct
          })
        } else {
          // Create new choice
          await questionsStore.createChoice({
            question_uuid: props.question.uuid,
            label: choice.label,
            text: choice.text,
            is_correct: choice.is_correct
          })
        }
      }
      
      // Delete removed choices (if current choices are fewer than existing)
      if (existingChoices.length > choices.value.length) {
        for (let i = choices.value.length; i < existingChoices.length; i++) {
          const choiceToDelete = existingChoices[i]
          if (choiceToDelete.uuid) {
            await questionsStore.deleteChoice(choiceToDelete.uuid)
          }
        }
      }
    }
    
    toast.success("Question updated successfully")
    emit('question-updated')
    isDialogOpen.value = false
    resetForm()
  } catch (error: any) {
    console.error('Error updating question:', error)
    toast.error(error.message || "Failed to update question")
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
        <DialogTitle>Edit Question</DialogTitle>
        <DialogDescription>
          Update the details of this question.
        </DialogDescription>
      </DialogHeader>
      <div class="space-y-6">
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
        <div class="space-y-2">
          <Label for="question-text">Question *</Label>
          <Textarea
            id="question-text"
            v-model="questionText"
            placeholder="Enter your question here..."
            rows="3"
          />
        </div>
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
        </div>
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
          {{ loading ? 'Updating...' : 'Update Question' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
