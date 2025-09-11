<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useQuestionsStore } from '@/stores/useAdminManageQuestions'
import { toast } from 'vue-sonner'

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Trash2, Plus } from 'lucide-vue-next'

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


const questionText = ref('')
const questionType = ref<'mcq' | 'essay' | 'true_false'>('mcq')
const choices = ref([
  { label: 'A', text: '', is_correct: false },
  { label: 'B', text: '', is_correct: false },
  { label: 'C', text: '', is_correct: false },
  { label: 'D', text: '', is_correct: false },
])

// Computed
const isValid = computed(() => {
  if (!questionText.value.trim()) return false
  
  if (questionType.value === 'mcq') {

    const validChoices = choices.value.filter(c => c.text.trim())
    const correctChoices = choices.value.filter(c => c.is_correct && c.text.trim())
    return validChoices.length >= 2 && correctChoices.length === 1
  }
  
  if (questionType.value === 'true_false') {

    const correctChoices = choices.value.slice(0, 2).filter(c => c.is_correct)
    return correctChoices.length === 1
  }
  

  return true
})


watch(questionType, (newType) => {
  if (newType === 'true_false') {
    choices.value = [
      { label: 'A', text: 'True', is_correct: false },
      { label: 'B', text: 'False', is_correct: false },
    ]
  } else if (newType === 'mcq') {
    choices.value = [
      { label: 'A', text: '', is_correct: false },
      { label: 'B', text: '', is_correct: false },
      { label: 'C', text: '', is_correct: false },
      { label: 'D', text: '', is_correct: false },
    ]
  }
})


const addChoice = () => {
  if (choices.value.length < 6) {
    const nextLabel = String.fromCharCode(65 + choices.value.length) // A, B, C, D, E, F
    choices.value.push({
      label: nextLabel,
      text: '',
      is_correct: false
    })
  }
}

const removeChoice = (index: number) => {
  if (choices.value.length > 2) {
    choices.value.splice(index, 1)
    // Re-label remaining choices
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

const handleSubmit = async () => {
  if (!isValid.value) return
  
  try {
    const questionData = {
      exam: props.examId,
      text: questionText.value.trim(),
      question_type: questionType.value,
      choices: questionType.value === 'essay' 
        ? [] 
        : choices.value.filter(c => c.text.trim())
    }
    
    await questionsStore.createQuestion(questionData)
    toast.success('Question created successfully')
    emit('question-created')
    handleClose()
  } catch (error: any) {
    toast.error(error.message || 'Failed to create question')
  }
}

const handleClose = () => {
  emit('update:open', false)
  resetForm()
}

const resetForm = () => {
  questionText.value = ''
  questionType.value = 'mcq'
  choices.value = [
    { label: 'A', text: '', is_correct: false },
    { label: 'B', text: '', is_correct: false },
    { label: 'C', text: '', is_correct: false },
    { label: 'D', text: '', is_correct: false },
  ]
}
</script>

<template>
  <Dialog :open="open" @update:open="(value) => emit('update:open', value)">
    <DialogContent class="max-w-3xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Create New Question</DialogTitle>
        <DialogDescription>
          Add a new question to this exam. Choose the question type and configure the options.
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-6">
        <!-- Question Type -->
        <div class="space-y-2">
          <Label>Question Type</Label>
          <Select v-model="questionType">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="mcq">Multiple Choice</SelectItem>
              <SelectItem value="true_false">True/False</SelectItem>
              <SelectItem value="essay">Essay</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Question Text -->
        <div class="space-y-2">
          <Label for="question-text">Question Text *</Label>
          <Textarea
            id="question-text"
            v-model="questionText"
            placeholder="Enter your question here..."
            rows="4"
          />
        </div>

        <!-- Choices (for MCQ and True/False) -->
        <div v-if="questionType !== 'essay'" class="space-y-4">
          <div class="flex items-center justify-between">
            <Label class="text-base font-medium">Answer Choices</Label>
            <Button
              v-if="questionType === 'mcq' && choices.length < 6"
              @click="addChoice"
              type="button"
              variant="outline"
              size="sm"
            >
              <Plus class="w-4 h-4 mr-2" />
              Add Choice
            </Button>
          </div>

          <div class="space-y-3">
            <Card
              v-for="(choice, index) in choices"
              :key="choice.label"
              class="transition-all duration-200"
              :class="choice.is_correct ? 'ring-2 ring-green-500 bg-green-50' : ''"
            >
              <CardContent class="p-4">
                <div class="flex items-start gap-3">
                  <div class="flex flex-col items-center gap-2">
                    <span class="font-semibold text-sm bg-muted px-2 py-1 rounded min-w-[32px] text-center">
                      {{ choice.label }}
                    </span>
                    <Switch
                      :checked="choice.is_correct"
                      @update:checked="() => setCorrectAnswer(index)"
                      size="sm"
                    />
                  </div>
                  
                  <Input
                    v-model="choice.text"
                    :placeholder="`Enter choice ${choice.label}...`"
                    :disabled="questionType === 'true_false'"
                    class="flex-1"
                  />
                  
                  <Button
                    v-if="questionType === 'mcq' && choices.length > 2"
                    @click="removeChoice(index)"
                    type="button"
                    variant="ghost"
                    size="sm"
                    class="text-destructive hover:text-destructive"
                  >
                    <Trash2 class="w-4 h-4" />
                  </Button>
                </div>
                
                <p v-if="choice.is_correct" class="text-xs text-green-600 mt-2 ml-11">
                  ✓ Correct answer
                </p>
              </CardContent>
            </Card>
          </div>

          <!-- Validation hints -->
          <div class="text-sm text-muted-foreground space-y-1">
            <p v-if="questionType === 'mcq'">
              • Add at least 2 choices and select exactly one correct answer
              • You can add up to 6 choices
            </p>
            <p v-else-if="questionType === 'true_false'">
              • Select either True or False as the correct answer
            </p>
          </div>
        </div>

        <!-- Essay note -->
        <div v-else class="p-4 bg-muted/50 rounded-lg">
          <p class="text-sm text-muted-foreground">
            This is an essay question. Students will provide written responses that will need to be manually graded.
          </p>
        </div>
      </div>

      <Separator />

      <DialogFooter>
        <Button variant="outline" @click="handleClose" :disabled="questionsStore.loading">
          Cancel
        </Button>
        <Button 
          @click="handleSubmit" 
          :disabled="!isValid || questionsStore.loading"
        >
          {{ questionsStore.loading ? 'Creating...' : 'Create Question' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>