<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useExamsStore } from "@/stores/useAdminManageExams"
import { toast } from "vue-sonner"

// ShadCN UI
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
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

// Store + Router
const examStore = useExamsStore()
const route = useRoute()
const router = useRouter()

const examId = computed(() => route.params.id as string)

// Dialog state
const isEditDialogOpen = ref(false)

// Editable exam fields
const editTitle = ref("")
const editDescription = ref("")

// Load exam
onMounted(async () => {
  if (examId.value) {
    await examStore.loadExamById(examId.value)

    if (examStore.currentExam) {
      editTitle.value = examStore.currentExam.title
      editDescription.value = examStore.currentExam.description
    }
  }
})

const exam = computed(() => examStore.currentExam)
const loading = computed(() => examStore.loading)
const error = computed(() => examStore.error)

// Save changes
const handleSave = async () => {
  if (!exam.value) return
  try {
    await examStore.updateExam(exam.value.uuid, {
      title: editTitle.value,
      description: editDescription.value,
    })
    toast.success("Exam updated successfully")
    isEditDialogOpen.value = false
  } catch (err: any) {
    toast.error(err.message || "Failed to update exam")
  }
}

// Delete exam
const handleDelete = async () => {
  if (!exam.value) return
  if (confirm(`Are you sure you want to delete "${exam.value.title}"?`)) {
    try {
      await examStore.deleteExam(exam.value.uuid)
      toast.success("Exam deleted successfully")
      router.push({ name: "AdminManageExams" })
    } catch (err: any) {
      toast.error(err.message || "Failed to delete exam")
    }
  }
}
</script>

<template>
  <div class="p-6 space-y-6">
    <!-- Loading -->
    <div v-if="loading" class="text-gray-500">Loading exam details...</div>

    <!-- Error -->
    <div v-else-if="error" class="text-red-600">{{ error }}</div>

    <!-- Exam Details -->
    <div v-else-if="exam" class="space-y-6">
      <!-- Exam Header -->
      <Card>
        <CardHeader>
          <CardTitle class="text-2xl font-bold flex justify-between items-center">
            {{ exam!.title }}
            <Badge :variant="exam!.is_active ? 'default' : 'secondary'">
              {{ exam!.is_active ? "Active" : "Inactive" }}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent class="space-y-2 text-gray-700">
          <p>{{ exam.description }}</p>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            <p><strong>Date:</strong> {{ exam.date }}</p>
            <p><strong>Time:</strong> {{ exam.start_time }} - {{ exam.end_time }}</p>
            <p><strong>Duration:</strong> {{ exam.duration_minutes }} mins</p>
            <p><strong>Access Code:</strong> {{ exam.access_code }}</p>
          </div>
          <div class="flex gap-2 mt-4">
            <Button @click="isEditDialogOpen = true">Edit Exam</Button>
            <Button variant="destructive" @click="handleDelete">Delete Exam</Button>
          </div>
        </CardContent>
      </Card>

      <!-- Questions Section -->
      <Card>
        <CardHeader>
          <CardTitle class="text-xl font-semibold">Questions</CardTitle>
        </CardHeader>
        <CardContent>
          <ul v-if="exam.questions?.length" class="space-y-4">
            <li
              v-for="q in exam.questions"
              :key="q.uuid"
              class="p-4 border rounded-lg bg-white shadow-sm"
            >
              <p class="font-medium text-gray-900 mb-2">
                {{ q.text }}
                <Badge class="ml-2" variant="outline">{{ q.question_type.toUpperCase() }}</Badge>
              </p>

              <!-- Choices -->
              <ul class="ml-6 list-disc text-gray-700 space-y-1">
                <li
                  v-for="c in q.choices"
                  :key="c.uuid"
                  :class="c.is_correct ? 'font-semibold text-green-600' : ''"
                >
                  {{ c.label }}. {{ c.text }}
                  <span v-if="c.is_correct" class="ml-1">(Correct)</span>
                </li>
              </ul>
            </li>
          </ul>

          <p v-else class="text-gray-500">No questions added yet.</p>

          <div class="mt-4">
            <Button size="sm" @click="() => router.push({ name: 'AddQuestion', params: { examId: exam!.uuid } })">
              Add Question
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Edit Exam Dialog -->
    <Dialog v-model:open="isEditDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Exam</DialogTitle>
          <DialogDescription>Update the exam details below.</DialogDescription>
        </DialogHeader>

        <div class="space-y-4">
          <div>
            <Label for="title">Title</Label>
            <Input id="title" v-model="editTitle" />
          </div>
          <div>
            <Label for="description">Description</Label>
            <Input id="description" v-model="editDescription" />
          </div>
        </div>

        <DialogFooter class="mt-4">
          <Button variant="outline" @click="isEditDialogOpen = false">Cancel</Button>
          <Button @click="handleSave">Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
