<script setup lang="ts">
import { h, ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import type { ExamMinimal } from "@/types/adminManageExams"
import { useExamsStore } from "@/stores/useAdminManageExams"

import type {
  ColumnFiltersState,
  ExpandedState,
  SortingState,
  VisibilityState,
} from "@tanstack/vue-table"
import {
  createColumnHelper,
  getCoreRowModel,
  getExpandedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from "@tanstack/vue-table"
import { ChevronsUpDown, ChevronDown } from "lucide-vue-next"
import { cn, valueUpdater } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { FlexRender } from "@tanstack/vue-table"
import { toast } from "vue-sonner"   // ✅ correct Sonner import

const router = useRouter()
const route = useRoute()
const examStore = useExamsStore()

// Get exam ID from route params
const examId = computed(() => route.params.id as string)

onMounted(() => {
  if (examId.value) {
    // If we have an exam ID, load that specific exam
    examStore.loadExamById(examId.value)
  } else {
    // Otherwise, load all exams for the table view
    examStore.loadExams()
  }
})

const exams = computed(() => examStore.exams)
const currentExam = computed(() => examStore.currentExam)
const loading = computed(() => examStore.loading)
const error = computed(() => examStore.error)

// Utility functions
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatTime = (timeString: string) => {
  return timeString
}

const columnHelper = createColumnHelper<ExamMinimal>()

const handleDelete = async (uuid: string, title: string) => {
  if (confirm(`Are you sure you want to delete "${title}"?`)) {
    try {
      await examStore.deleteExam(uuid)
      toast.success("Exam deleted successfully") // ✅ Sonner style
    } catch (err) {
      toast.error("Failed to delete exam") // ✅ Sonner style
    }
  }
}

const columns = [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
      h(Checkbox, {
        checked:
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate"),
        "onUpdate:checked": (value: boolean) =>
          table.toggleAllPageRowsSelected(!!value),
        ariaLabel: "Select all",
      }),
    cell: ({ row }) =>
      h(Checkbox, {
        checked: row.getIsSelected(),
        "onUpdate:checked": (value: boolean) =>
          row.toggleSelected(!!value),
        ariaLabel: "Select row",
      }),
    enableSorting: false,
    enableHiding: false,
  }),

  columnHelper.accessor("title", {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        },
        () => ["Exam Title", h(ChevronsUpDown, { class: "ml-2 h-4 w-4" })],
      ),
    cell: (info) => info.getValue(),
  }),

  columnHelper.accessor("date", {
    header: "Date",
    cell: ({ row }) => new Date(row.original.date).toLocaleDateString(),
  }),

  columnHelper.accessor("start_time", {
    header: "Start Time",
    cell: ({ row }) => row.original.start_time,
  }),

  columnHelper.accessor("duration_minutes", {
    header: "Duration",
    cell: ({ row }) => `${row.original.duration_minutes} min`,
  }),

  columnHelper.display({
    id: "status",
    header: "Status",
    cell: ({ row }) =>
      h(
        "span",
        { class: row.original.is_active ? "text-green-600" : "text-red-600" },
        row.original.is_active ? "Active" : "Inactive",
      ),
  }),

  columnHelper.display({
    id: "actions",
    header: "Actions",
    cell: ({ row }) =>
      h("div", { class: "flex gap-2" }, [
        h(
          Button,
          {
            size: "sm",
            variant: "outline",
            onClick: () =>
              router.push({
                name: "AdminViewManageExams",
                params: { id: row.original.uuid },
              }),
          },
          () => "Manage"
        ),
        h(
          Button,
          {
            size: "sm",
            variant: "destructive",
            onClick: () =>
              handleDelete(row.original.uuid, row.original.title),
          },
          () => "Delete"
        ),
      ]),
  }),
]

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})
const rowSelection = ref<Record<string, boolean>>({})
const expanded = ref<ExpandedState>({})

const table = useVueTable({
  get data() {
    return exams.value
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  onSortingChange: (updaterOrValue) => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, rowSelection),
  onExpandedChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, expanded),
  state: {
    get sorting() {
      return sorting.value
    },
    get columnFilters() {
      return columnFilters.value
    },
    get columnVisibility() {
      return columnVisibility.value
    },
    get rowSelection() {
      return rowSelection.value
    },
    get expanded() {
      return expanded.value
    },
    columnPinning: {
      left: ["select", "title"],
    },
  },
})
</script>

<template>
  <div class="p-6 space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      Loading exam details...
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-red-600 text-center py-8">
      {{ error }}
    </div>

    <!-- Single Exam Detail View (when currentExam exists) -->
    <template v-else-if="currentExam">
      <!-- Header -->
      <div class="space-y-2">
        <h1 class="text-3xl font-bold">{{ currentExam.title }}</h1>
        <p class="text-muted-foreground text-lg">{{ currentExam.description }}</p>
        <div class="flex items-center gap-4">
          <Badge :variant="currentExam.is_active ? 'default' : 'secondary'">
            {{ currentExam.is_active ? 'Active' : 'Inactive' }}
          </Badge>
          <span class="text-sm text-muted-foreground">
            Created: {{ formatDate(currentExam.created_at) }}
          </span>
        </div>
      </div>

      <!-- Exam Details -->
      <Card>
        <CardHeader>
          <CardTitle>Exam Information</CardTitle>
        </CardHeader>
        <CardContent class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <p class="text-sm font-medium text-muted-foreground">Date</p>
            <p>{{ formatDate(currentExam.date) }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Start Time</p>
            <p>{{ formatTime(currentExam.start_time) }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">End Time</p>
            <p>{{ formatTime(currentExam.end_time) }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Duration</p>
            <p>{{ currentExam.duration_minutes }} minutes</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Access Code</p>
            <p class="font-mono">{{ currentExam.access_code }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Total Questions</p>
            <p>{{ currentExam.questions?.length || 0 }}</p>
          </div>
        </CardContent>
      </Card>

      <!-- Questions -->
      <Card v-if="currentExam.questions && currentExam.questions.length > 0">
        <CardHeader>
          <CardTitle>Questions ({{ currentExam.questions.length }})</CardTitle>
          <CardDescription>
            Review all questions and their choices
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-6">
          <div
            v-for="(question, index) in currentExam.questions"
            :key="question.uuid"
            class="border rounded-lg p-4 space-y-3"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <Badge variant="outline">{{ index + 1 }}</Badge>
                  <Badge variant="secondary">{{ question.question_type }}</Badge>
                </div>
                <p class="font-medium">{{ question.text }}</p>
              </div>
            </div>
            
            <!-- Choices for MCQ -->
            <div v-if="question.choices && question.choices.length > 0" class="ml-6 space-y-2">
              <p class="text-sm font-medium text-muted-foreground">Choices:</p>
              <ul class="space-y-1">
                <li
                  v-for="choice in question.choices"
                  :key="choice.uuid"
                  class="flex items-center gap-2"
                >
                  <span class="font-medium">{{ choice.label }}.</span>
                  <span>{{ choice.text }}</span>
                  <Badge v-if="choice.is_correct" variant="default" class="ml-auto">
                    Correct
                  </Badge>
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- No Questions State -->
      <Card v-else>
        <CardContent class="text-center py-8">
          <p class="text-muted-foreground">No questions found for this exam.</p>
        </CardContent>
      </Card>
    </template>

    <!-- Exams Table View (when showing all exams) -->
    <template v-else-if="exams && exams.length > 0">
      <!-- Table Controls -->
      <div class="flex items-center py-4">
        <Input
          :model-value="(table.getColumn('title')?.getFilterValue() as string) ?? ''"
          @update:model-value="table.getColumn('title')?.setFilterValue($event)"
          placeholder="Filter exams..."
          class="max-w-sm"
        />
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="ml-auto">
              Columns <ChevronDown class="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuCheckboxItem
              v-for="column in table
                .getAllColumns()
                .filter((column) => column.getCanHide())"
              :key="column.id"
              class="capitalize"
              :checked="column.getIsVisible()"
              @update:checked="(value) => column.toggleVisibility(!!value)"
            >
              {{ column.id }}
            </DropdownMenuCheckboxItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <!-- Table -->
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
              <TableHead v-for="header in headerGroup.headers" :key="header.id">
                <FlexRender
                  v-if="!header.isPlaceholder"
                  :render="header.column.columnDef.header"
                  :props="header.getContext()"
                />
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <template v-if="table.getRowModel().rows?.length">
              <TableRow
                v-for="row in table.getRowModel().rows"
                :key="row.id"
                :data-state="row.getIsSelected() && 'selected'"
              >
                <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                  <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                </TableCell>
              </TableRow>
            </template>

            <TableRow v-else>
              <TableCell :colspan="columns.length" class="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-end space-x-2 py-4">
        <div class="flex-1 text-sm text-muted-foreground">
          {{ table.getFilteredSelectedRowModel().rows.length }} of
          {{ table.getFilteredRowModel().rows.length }} row(s) selected.
        </div>
        <div class="space-x-2">
          <Button
            variant="outline"
            size="sm"
            :disabled="!table.getCanPreviousPage()"
            @click="table.previousPage()"
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            :disabled="!table.getCanNextPage()"
            @click="table.nextPage()"
          >
            Next
          </Button>
        </div>
      </div>
    </template>

    <!-- No Exams State -->
    <div v-else class="text-center py-8">
      <p class="text-muted-foreground">No exams found.</p>
    </div>
  </div>
</template>