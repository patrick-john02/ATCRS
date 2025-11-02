// single line comment: integrates toast notifications for CRUD actions on courses
<script setup lang="ts">
import { h, ref, onMounted, computed } from 'vue'
import { useCourseStores } from '@/stores/useCourseStores'
import { toast } from 'vue-sonner' // ✅ toast integration
import type {
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import {
  createColumnHelper,
  FlexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import { ChevronDown, ChevronsUpDown, Plus, Pencil, Trash2, AlertCircle } from 'lucide-vue-next'
import { valueUpdater } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Label } from '@/components/ui/label'
import type { AdminManageCourse } from '@/types/courses'

const courseStore = useCourseStores()

const showAddDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedCourse = ref<AdminManageCourse | null>(null)

const newCourse = ref({ code: '', name: '', min_score: 0 })
const editForm = ref<Omit<AdminManageCourse, 'id'>>({
  code: '',
  name: '',
  min_score: '0.00',
})

onMounted(() => {
  courseStore.getCourses()
})

const addCourse = async () => {
  if (!newCourse.value.code || !newCourse.value.name) {
    toast.error('Code and Name are required')
    return
  }

  try {
    await courseStore.addCourse({
      code: newCourse.value.code,
      name: newCourse.value.name,
      min_score: String(newCourse.value.min_score), // ✅ convert number → string
    })
    toast.success('Course added successfully')
    newCourse.value = { code: '', name: '', min_score: 0 }
    showAddDialog.value = false
  } catch (error) {
    toast.error('Failed to add course')
  }
}


const openEditDialog = (course: AdminManageCourse) => {
  selectedCourse.value = course
  editForm.value = { ...course }
  showEditDialog.value = true
}

const updateCourse = async () => {
  if (!selectedCourse.value) return
  try {
    await courseStore.editCourse(selectedCourse.value.id, editForm.value)
    toast.success('Course updated successfully')
    showEditDialog.value = false
  } catch (error) {
    toast.error('Failed to update course')
  }
}

const openDeleteDialog = (course: AdminManageCourse) => {
  selectedCourse.value = course
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!selectedCourse.value) return
  try {
    await courseStore.removeCourse(selectedCourse.value.id)
    toast.success('Course deleted successfully')
    showDeleteDialog.value = false
  } catch (error) {
    toast.error('Failed to delete course')
  }
}

const courses = computed(() => courseStore.courses)

const columnHelper = createColumnHelper<AdminManageCourse>()
const columns = [
  columnHelper.accessor('code', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Code', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => h('div', { class: 'font-medium' }, info.getValue()),
  }),
  columnHelper.accessor('name', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Course Name', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => h('div', info.getValue()),
  }),
  columnHelper.accessor('min_score', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Min Score', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => h('div', { class: 'text-center font-semibold' }, info.getValue()),
  }),
  columnHelper.display({
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) =>
      h('div', { class: 'flex gap-2' }, [
        h(Button, {
          size: 'sm',
          variant: 'outline',
          onClick: () => openEditDialog(row.original),
        }, () => [h(Pencil, { class: 'h-4 w-4' })]),
        h(Button, {
          size: 'sm',
          variant: 'destructive',
          onClick: () => openDeleteDialog(row.original),
        }, () => [h(Trash2, { class: 'h-4 w-4' })]),
      ]),
  }),
]

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})

const table = useVueTable({
  data: courses,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: updaterOrValue =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: updaterOrValue =>
    valueUpdater(updaterOrValue, columnVisibility),
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
  },
})
</script>


<template>
  <div class="w-full space-y-6 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Manage Courses</h1>
        <p class="text-gray-500 mt-1">Add, edit, and manage course offerings</p>
      </div>
      <Button @click="showAddDialog = true">
        <Plus class="h-4 w-4 mr-2" />
        Add Course
      </Button>
    </div>

    <!-- Error Alert -->
    <Alert v-if="courseStore.error" variant="destructive">
      <AlertCircle class="h-4 w-4" />
      <AlertDescription>{{ courseStore.error }}</AlertDescription>
    </Alert>

    <!-- Table Card -->
    <Card>
      <CardHeader>
        <CardTitle>Course List</CardTitle>
        <CardDescription>
          Manage all available courses and their minimum score requirements
        </CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Filters -->
        <div class="flex gap-2 items-center py-4">
          <Input
            class="max-w-sm"
            placeholder="Filter courses..."
            :model-value="table.getColumn('name')?.getFilterValue() as string"
            @update:model-value="table.getColumn('name')?.setFilterValue($event)"
          />
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="outline" class="ml-auto">
                Columns <ChevronDown class="ml-2 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuCheckboxItem
                v-for="column in table.getAllColumns().filter(col => col.getCanHide())"
                :key="column.id"
                class="capitalize"
                :model-value="column.getIsVisible()"
                @update:model-value="val => column.toggleVisibility(!!val)"
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
              <template v-if="courseStore.loading">
                <TableRow>
                  <TableCell :colspan="columns.length" class="text-center h-24">
                    <div class="flex items-center justify-center gap-2">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900"></div>
                      <span>Loading courses...</span>
                    </div>
                  </TableCell>
                </TableRow>
              </template>
              <template v-else-if="table.getRowModel().rows.length">
                <TableRow
                  v-for="row in table.getRowModel().rows"
                  :key="row.id"
                  class="hover:bg-gray-50 transition-colors"
                >
                  <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                    <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                  </TableCell>
                </TableRow>
              </template>
              <TableRow v-else>
                <TableCell :colspan="columns.length" class="text-center h-24">
                  No courses found.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-end space-x-2 py-4">
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
      </CardContent>
    </Card>

    <!-- Add Course Dialog -->
    <Dialog v-model:open="showAddDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add New Course</DialogTitle>
          <DialogDescription>
            Create a new course with code, name, and minimum score requirement.
          </DialogDescription>
        </DialogHeader>
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="code">Course Code</Label>
            <Input id="code" v-model="newCourse.code" placeholder="e.g., CS101" />
          </div>
          <div class="space-y-2">
            <Label for="name">Course Name</Label>
            <Input id="name" v-model="newCourse.name" placeholder="e.g., Computer Science" />
          </div>
          <div class="space-y-2">
            <Label for="min_score">Minimum Score</Label>
            <Input
              id="min_score"
              type="number"
              v-model.number="newCourse.min_score"
              placeholder="e.g., 75"
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showAddDialog = false">Cancel</Button>
          <Button @click="addCourse" :disabled="courseStore.loading">
            {{ courseStore.loading ? 'Adding...' : 'Add Course' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Edit Course Dialog -->
    <Dialog v-model:open="showEditDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Course</DialogTitle>
          <DialogDescription>
            Update course information and minimum score requirement.
          </DialogDescription>
        </DialogHeader>
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="edit-code">Course Code</Label>
            <Input id="edit-code" v-model="editForm.code" />
          </div>
          <div class="space-y-2">
            <Label for="edit-name">Course Name</Label>
            <Input id="edit-name" v-model="editForm.name" />
          </div>
          <div class="space-y-2">
            <Label for="edit-min_score">Minimum Score</Label>
            <Input
              id="edit-min_score"
              type="number"
              v-model.number="editForm.min_score"
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showEditDialog = false">Cancel</Button>
          <Button @click="updateCourse" :disabled="courseStore.loading">
            {{ courseStore.loading ? 'Updating...' : 'Update Course' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog v-model:open="showDeleteDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Course</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete <strong>{{ selectedCourse?.name }}</strong>? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" @click="showDeleteDialog = false">Cancel</Button>
          <Button variant="destructive" @click="confirmDelete" :disabled="courseStore.loading">
            {{ courseStore.loading ? 'Deleting...' : 'Delete' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>