<script setup lang="ts">
import { h, ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import type { ExamMinimal, ExamCreateData } from "@/types/adminManageExams"
import { useExamsStore } from "@/stores/useAdminManageExams"

import type {
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from "@tanstack/vue-table"
import {
  createColumnHelper,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from "@tanstack/vue-table"
import { ChevronsUpDown, ChevronDown, Plus, Search, Filter, MoreHorizontal, Clock, Users, FileText } from "lucide-vue-next"
import { cn, valueUpdater } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent} from "@/components/ui/card"
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
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
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
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { FlexRender } from "@tanstack/vue-table"
import { toast } from "vue-sonner"

const router = useRouter()
const route = useRoute()
const examStore = useExamsStore()

// Create Exam Dialog State
const isCreateDialogOpen = ref(false)
const isDeleteDialogOpen = ref(false)
const examToDelete = ref<ExamMinimal | null>(null)

// Create exam form
const createForm = ref<ExamCreateData>({
  title: "",
  description: "",
  date: "",
  start_time: "",
  end_time: "",
  duration_minutes: 120,
  access_code: "",
  is_active: true,
})

onMounted(() => {
  examStore.loadExams()
})

const exams = computed(() => examStore.exams)
const loading = computed(() => examStore.loading)
const error = computed(() => examStore.error)

// Generate access code
const generateAccessCode = () => {
  const code = Math.random().toString(36).substr(2, 8).toUpperCase()
  createForm.value.access_code = code
}

// Reset form
const resetCreateForm = () => {
  createForm.value = {
    title: "",
    description: "",
    date: "",
    start_time: "",
    end_time: "",
    duration_minutes: 120,
    access_code: "",
    is_active: true,
  }
}

// Create exam
const handleCreateExam = async () => {
  try {
    await examStore.createExam(createForm.value)
    toast.success("Exam created successfully")
    isCreateDialogOpen.value = false
    resetCreateForm()
  } catch (err: any) {
    toast.error(err.message || "Failed to create exam")
  }
}

// Delete exam
const handleDeleteExam = async () => {
  if (!examToDelete.value) return
  
  try {
    await examStore.deleteExam(examToDelete.value.uuid)
    toast.success("Exam deleted successfully")
    isDeleteDialogOpen.value = false
    examToDelete.value = null
  } catch (err: any) {
    toast.error(err.message || "Failed to delete exam")
  }
}

// Open delete dialog
const openDeleteDialog = (exam: ExamMinimal) => {
  examToDelete.value = exam
  isDeleteDialogOpen.value = true
}

// Toggle exam status
const handleToggleStatus = async (exam: ExamMinimal) => {
  try {
    await examStore.toggleExamStatus(exam.uuid)
    toast.success(`Exam ${exam.is_active ? 'deactivated' : 'activated'} successfully`)
  } catch (err: any) {
    toast.error(err.message || "Failed to toggle exam status")
  }
}

// Format helpers
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
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

const columnHelper = createColumnHelper<ExamMinimal>()

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
          class: "h-8 px-2 lg:px-3"
        },
        () => ["Exam Title", h(ChevronsUpDown, { class: "ml-2 h-4 w-4" })],
      ),
    cell: ({ row }) => h("div", { class: "font-medium" }, row.original.title),
  }),

  columnHelper.accessor("date", {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
          class: "h-8 px-2 lg:px-3"
        },
        () => ["Date", h(ChevronsUpDown, { class: "ml-2 h-4 w-4" })],
      ),
    cell: ({ row }) => formatDate(row.original.date),
  }),

  columnHelper.display({
    id: "time_range",
    header: "Time",
    cell: ({ row }) => 
      h("div", { class: "text-sm" }, [
        h("div", {}, `${formatTime(row.original.start_time)}`),
        h("div", { class: "text-muted-foreground text-xs" }, `${formatTime(row.original.end_time)}`)
      ]),
  }),

  columnHelper.accessor("duration_minutes", {
    header: "Duration",
    cell: ({ row }) => `${row.original.duration_minutes} min`,
  }),

  columnHelper.accessor("access_code", {
    header: "Access Code",
    cell: ({ row }) => h("code", { class: "font-mono text-sm bg-muted px-1 py-0.5 rounded" }, row.original.access_code),
  }),

  columnHelper.display({
    id: "status",
    header: "Status",
    cell: ({ row }) =>
      h(Badge, {
        variant: row.original.is_active ? "default" : "secondary"
      }, () => row.original.is_active ? "Active" : "Inactive"),
  }),

  columnHelper.display({
    id: "actions",
    header: "Actions",
    cell: ({ row }) =>
      h("div", { class: "flex items-center gap-2" }, [
        h(
          DropdownMenu,
          {},
          {
            default: () => [
              h(
                DropdownMenuTrigger,
                {
                  as: Button,
                  variant: "ghost",
                  class: "h-8 w-8 p-0"
                },
                () => h(MoreHorizontal, { class: "h-4 w-4" })
              ),
              h(
                DropdownMenuContent,
                { align: "end" },
                () => [
                  h(
                    DropdownMenuItem,
                    {
                      onClick: () =>
                        router.push({
                          name: "AdminViewManageExams",
                          params: { id: row.original.uuid },
                        }),
                    },
                    () => "View Details"
                  ),
                  h(DropdownMenuSeparator),
                  h(
                    DropdownMenuItem,
                    {
                      onClick: () => handleToggleStatus(row.original),
                    },
                    () => row.original.is_active ? "Deactivate" : "Activate"
                  ),
                  h(DropdownMenuSeparator),
                  h(
                    DropdownMenuItem,
                    {
                      onClick: () => openDeleteDialog(row.original),
                      class: "text-destructive focus:text-destructive"
                    },
                    () => "Delete"
                  ),
                ]
              ),
            ]
          }
        ),
      ]),
  }),
]

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})
const rowSelection = ref<Record<string, boolean>>({})

const table = useVueTable({
  get data() {
    return exams.value
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  onSortingChange: (updaterOrValue) => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, rowSelection),
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
  },
  initialState: {
    pagination: {
      pageSize: 10,
    },
  },
})

// Stats
const examStats = computed(() => {
  const total = exams.value.length
  const active = exams.value.filter(e => e.is_active).length
  const inactive = total - active
  
  return { total, active, inactive }
})
</script>

<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Manage Exams</h1>
        <p class="text-muted-foreground">
          Create, edit, and manage all examinations
        </p>
      </div>
      <Button @click="isCreateDialogOpen = true">
        <Plus class="w-4 h-4 mr-2" />
        Create Exam
      </Button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center space-x-2">
            <FileText class="h-5 w-5 text-blue-500" />
            <div class="space-y-1">
              <p class="text-sm font-medium leading-none">Total Exams</p>
              <p class="text-2xl font-bold">{{ examStats.total }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center space-x-2">
            <Users class="h-5 w-5 text-green-500" />
            <div class="space-y-1">
              <p class="text-sm font-medium leading-none">Active Exams</p>
              <p class="text-2xl font-bold text-green-600">{{ examStats.active }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardContent class="pt-6">
          <div class="flex items-center space-x-2">
            <Clock class="h-5 w-5 text-orange-500" />
            <div class="space-y-1">
              <p class="text-sm font-medium leading-none">Inactive Exams</p>
              <p class="text-2xl font-bold text-orange-600">{{ examStats.inactive }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="text-center space-y-3">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
        <p class="text-muted-foreground">Loading exams...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <div class="mx-auto flex items-center justify-center w-12 h-12 rounded-full bg-red-100">
        <FileText class="h-6 w-6 text-red-600" />
      </div>
      <h3 class="mt-2 text-sm font-semibold text-gray-900">Error Loading Exams</h3>
      <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
      <div class="mt-6">
        <Button @click="examStore.loadExams()" variant="outline">
          Try Again
        </Button>
      </div>
    </div>

    <!-- Exams Table -->
    <div v-else class="space-y-4">
      <!-- Table Controls -->
      <div class="flex items-center justify-between">
        <div class="flex flex-1 items-center space-x-2">
          <div class="relative">
            <Search class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search exams..."
              :model-value="(table.getColumn('title')?.getFilterValue() as string) ?? ''"
              @update:model-value="table.getColumn('title')?.setFilterValue($event)"
              class="pl-8 max-w-sm"
            />
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="outline" size="sm">
                <Filter class="mr-2 h-4 w-4" />
                View
                <ChevronDown class="ml-2 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="w-[150px]">
              <DropdownMenuCheckboxItem
                v-for="column in table
                  .getAllColumns()
                  .filter((column) => column.getCanHide())"
                :key="column.id"
                class="capitalize"
                :checked="column.getIsVisible()"
                @update:checked="(value) => column.toggleVisibility(!!value)"
              >
                {{ column.id.replace('_', ' ') }}
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
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
                class="hover:bg-muted/50"
              >
                <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                  <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                </TableCell>
              </TableRow>
            </template>

            <TableRow v-else>
              <TableCell :colspan="columns.length" class="h-24 text-center">
                <div class="flex flex-col items-center justify-center space-y-2">
                  <FileText class="h-8 w-8 text-muted-foreground" />
                  <p class="text-muted-foreground">No exams found.</p>
                  <Button @click="isCreateDialogOpen = true" size="sm">
                    <Plus class="w-4 h-4 mr-2" />
                    Create Your First Exam
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-between space-x-2 py-4">
        <div class="flex-1 text-sm text-muted-foreground">
          {{ table.getFilteredSelectedRowModel().rows.length }} of
          {{ table.getFilteredRowModel().rows.length }} row(s) selected.
        </div>
        <div class="flex items-center space-x-6 lg:space-x-8">
          <div class="flex items-center space-x-2">
            <p class="text-sm font-medium">Rows per page</p>
            <select
              class="h-8 w-[70px] rounded-md border border-input bg-transparent px-3 py-1 text-xs shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
              :value="table.getState().pagination.pageSize"
              @change="(e) => table.setPageSize(Number(e.target.value))"
            >
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="30">30</option>
              <option value="40">40</option>
              <option value="50">50</option>
            </select>
          </div>
          <div class="flex w-[100px] items-center justify-center text-sm font-medium">
            Page {{ table.getState().pagination.pageIndex + 1 }} of {{ table.getPageCount() }}
          </div>
          <div class="flex items-center space-x-2">
            <Button
              variant="outline"
              class="h-8 w-8 p-0"
              :disabled="!table.getCanPreviousPage()"
              @click="table.setPageIndex(0)"
            >
              <span class="sr-only">Go to first page</span>
              ⇤
            </Button>
            <Button
              variant="outline"
              class="h-8 w-8 p-0"
              :disabled="!table.getCanPreviousPage()"
              @click="table.previousPage()"
            >
              <span class="sr-only">Go to previous page</span>
              ←
            </Button>
            <Button
              variant="outline"
              class="h-8 w-8 p-0"
              :disabled="!table.getCanNextPage()"
              @click="table.nextPage()"
            >
              <span class="sr-only">Go to next page</span>
              →
            </Button>
            <Button
              variant="outline"
              class="h-8 w-8 p-0"
              :disabled="!table.getCanNextPage()"
              @click="table.setPageIndex(table.getPageCount() - 1)"
            >
              <span class="sr-only">Go to last page</span>
              ⇥
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Exam Dialog -->
    <Dialog v-model:open="isCreateDialogOpen">
      <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create New Exam</DialogTitle>
          <DialogDescription>
            Fill in the details below to create a new examination.
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-6">
          <!-- Basic Information -->
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Basic Information</h4>
            <div class="grid grid-cols-1 gap-4">
              <div>
                <Label for="create-title">Title *</Label>
                <Input 
                  id="create-title" 
                  v-model="createForm.title" 
                  placeholder="Enter exam title"
                  required
                />
              </div>
              <div>
                <Label for="create-description">Description</Label>
                <Textarea 
                  id="create-description" 
                  v-model="createForm.description" 
                  placeholder="Enter exam description"
                  rows="3"
                />
              </div>
            </div>
          </div>

          <Separator />

          <!-- Schedule -->
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Schedule</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label for="create-date">Date *</Label>
                <Input 
                  id="create-date" 
                  type="date" 
                  v-model="createForm.date"
                  required
                />
              </div>
              <div>
                <Label for="create-duration">Duration (minutes) *</Label>
                <Input 
                  id="create-duration" 
                  type="number" 
                  v-model.number="createForm.duration_minutes" 
                  min="1"
                  placeholder="120"
                  required
                />
              </div>
              <div>
                <Label for="create-start-time">Start Time *</Label>
                <Input 
                  id="create-start-time" 
                  type="time" 
                  v-model="createForm.start_time"
                  required
                />
              </div>
              <div>
                <Label for="create-end-time">End Time *</Label>
                <Input 
                  id="create-end-time" 
                  type="time" 
                  v-model="createForm.end_time"
                  required
                />
              </div>
            </div>
          </div>

          <Separator />

          <!-- Access -->
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Access Settings</h4>
            <div class="space-y-4">
              <div>
                <Label for="create-access-code">Access Code *</Label>
                <div class="flex gap-2">
                  <Input 
                    id="create-access-code" 
                    v-model="createForm.access_code" 
                    placeholder="Enter access code"
                    class="font-mono flex-1"
                    required
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
                <Switch 
                  id="create-active" 
                  v-model:checked="createForm.is_active" 
                />
                <Label for="create-active">
                  Make exam active immediately
                </Label>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter class="mt-6">
          <Button 
            variant="outline" 
            @click="() => { isCreateDialogOpen = false; resetCreateForm(); }"
          >
            Cancel
          </Button>
          <Button 
            @click="handleCreateExam" 
            :disabled="loading || !createForm.title || !createForm.date"
          >
            {{ loading ? 'Creating...' : 'Create Exam' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <AlertDialog v-model:open="isDeleteDialogOpen">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Exam</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{{ examToDelete?.title }}"? This action cannot be undone and will remove all associated questions and student responses.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel @click="() => { isDeleteDialogOpen = false; examToDelete = null; }">
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction 
            @click="handleDeleteExam" 
            class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            :disabled="loading"
          >
            {{ loading ? 'Deleting...' : 'Delete Exam' }}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>