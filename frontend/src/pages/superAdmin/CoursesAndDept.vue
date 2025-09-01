<script setup lang="ts">
import { h, ref, computed, onMounted, reactive } from 'vue'
import { useCourseStore } from '@/stores/useCourse'
import { Label } from '@/components/ui/label'
import type { ViewCourse } from '@/types/course'
import type {
  ColumnFiltersState,
  ExpandedState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import {
  createColumnHelper,
  FlexRender,
  getCoreRowModel,
  getExpandedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import { ChevronDown, ChevronsUpDown, Loader2 } from 'lucide-vue-next'
import { cn, valueUpdater } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

const courseStore = useCourseStore()

// Form reactive object
const form = reactive({
  code: '',
  name: '',
})

const isDialogOpen = ref(false)

const handleSubmit = async () => {
  try {
    await courseStore.addAdmin(form)
    // Reset form
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
    // Close dialog
    isDialogOpen.value = false
  } catch (error) {
    console.error('Failed to add Course:', error)
  }
}

onMounted(() => {
  if (courseStore.course.length === 0) {
    courseStore.loadCourse()
  }
})

const columnHelper = createColumnHelper<ViewCourse>()

const columns = [
  columnHelper.display({
    id: 'select',
    header: ({ table }) =>
      h(Checkbox, {
        modelValue:
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && 'indeterminate'),
        'onUpdate:modelValue': value =>
          table.toggleAllPageRowsSelected(!!value),
        ariaLabel: 'Select all',
      }),
    cell: ({ row }) =>
      h(Checkbox, {
        modelValue: row.getIsSelected(),
        'onUpdate:modelValue': value => row.toggleSelected(!!value),
        ariaLabel: 'Select row',
      }),
    enableSorting: false,
    enableHiding: false,
  }),
  columnHelper.accessor('code', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Course Code', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('name', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Course Name', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => info.getValue(),
  }),
]

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({
  address: false,
  contact_number: false,
})
const rowSelection = ref({})
const expanded = ref<ExpandedState>({})

const table = useVueTable({
  get data() {
    return courseStore.course
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: updaterOrValue =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: updaterOrValue =>
    valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: updaterOrValue =>
    valueUpdater(updaterOrValue, rowSelection),
  onExpandedChange: updaterOrValue =>
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
      left: ['select', 'first_name', 'last_name'],
    },
  },
})

const selectedRowsCount = computed(() => table.getFilteredSelectedRowModel().rows.length)
const totalRowsCount = computed(() => table.getFilteredRowModel().rows.length)
</script>

<template>
  <div class="w-full space-y-4">
    <!-- Error Alert -->
    <Alert v-if="courseStore.error" variant="destructive">
      <AlertDescription>
        {{ courseStore.error }}
      </AlertDescription>
    </Alert>

    <!-- Filters and Controls -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex flex-1 flex-col gap-2 sm:flex-row sm:items-center">
        <Input
          class="max-w-sm"
          placeholder="Filter by Course..."
          :model-value="table.getColumn('course')?.getFilterValue() as string"
          @update:model-value="table.getColumn('course')?.setFilterValue($event)"
        />
        <Input
          class="max-w-sm"
          placeholder="Filter by first name..."
          :model-value="table.getColumn('code')?.getFilterValue() as string"
          @update:model-value="table.getColumn('name')?.setFilterValue($event)"
        />
      </div>

      <div class="flex items-center gap-2">
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline">
              Columns <ChevronDown class="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="w-48">
            <DropdownMenuCheckboxItem
              v-for="column in table.getAllColumns().filter(col => col.getCanHide())"
              :key="column.id"
              class="capitalize"
              :model-value="column.getIsVisible()"
              @update:model-value="val => column.toggleVisibility(!!val)"
            >
              {{ column.id.replace('_', ' ') }}
            </DropdownMenuCheckboxItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <Dialog v-model:open="isDialogOpen">
          <DialogTrigger as-child>
            <Button variant="default">
              Add Course
            </Button>
          </DialogTrigger>
          <DialogContent class="sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>Add New Course</DialogTitle>
              <DialogDescription>
                Fill out the form to create a new Course.
              </DialogDescription>
            </DialogHeader>

            <!-- Form inside Dialog -->
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <Label for="code">Code</Label>
                  <Input id="code" v-model="form.code" required />
                </div>
                <div>
                  <Label for="name">Course Name</Label>
                  <Input id="name" v-model="form.name" type="text" required />
                </div>
               
              </div>

              <DialogFooter>
                <Button type="submit" :disabled="courseStore.loading">
                  <Loader2 v-if="courseStore.loading" class="mr-2 h-4 w-4 animate-spin" />
                  Save
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>

    <!-- Data Table -->
    <div class="rounded-md border">
      <div class="relative overflow-auto max-h-[600px]">
        <Table>
          <TableHeader class="sticky top-0 bg-background z-10">
            <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
              <TableHead
                v-for="header in headerGroup.headers"
                :key="header.id"
                :class="cn(
                  'border-r last:border-r-0',
                  { 'sticky bg-background z-20': header.column.getIsPinned() },
                  header.column.getIsPinned() === 'left' ? 'left-0 border-r-2' : 'right-0',
                )"
              >
                <FlexRender
                  v-if="!header.isPlaceholder"
                  :render="header.column.columnDef.header"
                  :props="header.getContext()"
                />
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <template v-if="!courseStore.loading && table.getRowModel().rows.length">
              <TableRow
                v-for="row in table.getRowModel().rows"
                :key="row.id"
                :data-state="row.getIsSelected() && 'selected'"
                class="hover:bg-muted/50"
              >
                <TableCell
                  v-for="cell in row.getVisibleCells()"
                  :key="cell.id"
                  :class="cn(
                    'border-r last:border-r-0',
                    { 'sticky bg-background z-10': cell.column.getIsPinned() },
                    cell.column.getIsPinned() === 'left' ? 'left-0 border-r-2' : 'right-0',
                  )"
                >
                  <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                </TableCell>
              </TableRow>
            </template>
            <TableRow v-else-if="courseStore.loading">
              <TableCell :colspan="columns.length" class="text-center h-24">
                <div class="flex items-center justify-center">
                  <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                  Loading applicants users...
                </div>
              </TableCell>
            </TableRow>
            <TableRow v-else>
              <TableCell :colspan="columns.length" class="text-center h-24">
                No Applicant users found.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="text-sm text-muted-foreground">
        {{ selectedRowsCount }} of {{ totalRowsCount }} row(s) selected.
      </div>
      <div class="flex items-center gap-2">
        <span class="text-sm text-muted-foreground">
          Page {{ table.getState().pagination.pageIndex + 1 }} of {{ table.getPageCount() }}
        </span>
        <div class="flex items-center gap-2">
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
    </div>
  </div>
</template>