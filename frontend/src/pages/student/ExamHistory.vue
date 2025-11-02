<script setup lang="ts">
import { h, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExamHistoryStore } from '@/stores/useExamHistoryStore'
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
import { ChevronDown, ChevronsUpDown, Calendar, Clock, Trophy, BookOpen, RefreshCcw } from 'lucide-vue-next'
import { cn, valueUpdater } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
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
import type { ExamHistoryItem } from '@/types/studentExam'

const router = useRouter()
const examHistoryStore = useExamHistoryStore()

onMounted(() => {
  examHistoryStore.fetchExamHistory()
})

const columnHelper = createColumnHelper<ExamHistoryItem>()
const columns = [
  columnHelper.accessor('exam.title', {
    id: 'title',
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Exam Title', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: ({ row }) => 
      h('div', { class: 'font-medium' }, row.original.exam.title),
  }),
  columnHelper.accessor('exam.date', {
    id: 'date',
    header: 'Exam Date',
    cell: ({ row }) =>
      h('div', { class: 'text-sm' }, 
        new Date(row.original.exam.date).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      ),
  }),
  columnHelper.accessor('status', {
    header: 'Status',
    cell: ({ row }) => {
      const status = row.original.status
      const variants: Record<string, any> = {
        completed: { class: 'bg-green-100 text-green-800 border-green-300' },
        in_progress: { class: 'bg-yellow-100 text-yellow-800 border-yellow-300' },
        not_started: { class: 'bg-gray-100 text-gray-800 border-gray-300' },
      }
      return h(Badge, {
        variant: 'outline',
        class: cn('capitalize', variants[status]?.class)
      }, () => status.replace('_', ' '))
    },
  }),
  columnHelper.accessor('recommendation_score', {
    id: 'score',
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Score', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: ({ row }) => {
      const score = row.original.recommendation_score
      if (score === null) return h('span', { class: 'text-gray-400' }, '-')
      
      const scoreClass = score >= 80 ? 'text-green-600 font-bold' : 
                        score >= 70 ? 'text-blue-600 font-semibold' : 
                        score >= 60 ? 'text-yellow-600' : 'text-red-600'
      
      return h('span', { class: scoreClass }, `${score}%`)
    },
  }),
  columnHelper.accessor('recommended_course', {
    id: 'course',
    header: 'Recommended Course',
    cell: ({ row }) => {
      const course = row.original.recommended_course
      if (!course) return h('span', { class: 'text-gray-400 text-sm' }, 'N/A')
      return h('div', { class: 'flex flex-col' }, [
        h('span', { class: 'font-medium text-sm' }, course.name),
        h('span', { class: 'text-xs text-gray-500' }, course.code),
      ])
    },
  }),
  columnHelper.display({
    id: 'questions',
    header: 'Progress',
    cell: ({ row }) => {
      const { attempted_questions, total_questions } = row.original
      const percentage = total_questions > 0 ? (attempted_questions / total_questions) * 100 : 0
      return h('div', { class: 'flex flex-col gap-1' }, [
        h('span', { class: 'text-sm font-medium' }, `${attempted_questions}/${total_questions}`),
        h('div', { class: 'w-full bg-gray-200 rounded-full h-1.5' }, [
          h('div', {
            class: 'bg-blue-600 h-1.5 rounded-full transition-all',
            style: { width: `${percentage}%` }
          })
        ])
      ])
    },
  }),
  columnHelper.accessor('exam_attempt_number', {
    id: 'attempt',
    header: 'Attempt',
    cell: ({ row }) => 
      h('div', { class: 'text-center' }, 
        h(Badge, { variant: 'outline' }, () => `#${row.original.exam_attempt_number}`)
      ),
  }),
  columnHelper.display({
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => {
      const canContinue = row.original.status === 'in_progress' || row.original.status === 'not_started'
      
      return h('div', { class: 'flex gap-2' }, [
        canContinue && h(Button, {
          size: 'sm',
          onClick: () => router.push({ name: 'take-exam', params: { uuid: row.original.uuid } })
        }, () => row.original.status === 'in_progress' ? 'Continue' : 'Start'),
        
        row.original.status === 'completed' && h(Button, {
          size: 'sm',
          variant: 'outline',
          onClick: () => router.push({ name: 'exam-result', params: { uuid: row.original.uuid } })
        }, () => 'View Results')
      ])
    },
  }),
]

const sorting = ref<SortingState>([{ id: 'date', desc: true }])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})

const table = useVueTable({
  get data() {
    return examHistoryStore.examHistory
  },
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
  initialState: {
    pagination: {
      pageSize: 10,
    },
  },
})

const stats = computed(() => [
  {
    title: 'Total Exams',
    value: examHistoryStore.totalExams,
    icon: BookOpen,
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
  },
  {
    title: 'Average Score',
    value: `${examHistoryStore.averageScore}%`,
    icon: Trophy,
    color: 'text-green-600',
    bgColor: 'bg-green-100',
  },
  {
    title: 'Completed',
    value: examHistoryStore.completedExams.length,
    icon: Calendar,
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
  },
  {
    title: 'In Progress',
    value: examHistoryStore.inProgressExams.length,
    icon: Clock,
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100',
  },
])

async function handleRefresh() {
  await examHistoryStore.fetchExamHistory()
}
</script>

<template>
  <div class="w-full space-y-6 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Exam History</h1>
        <p class="text-gray-500 mt-1">Track your exam performance and progress</p>
      </div>
      <Button @click="handleRefresh" variant="outline" :disabled="examHistoryStore.loading">
        <RefreshCcw :class="['h-4 w-4 mr-2', examHistoryStore.loading && 'animate-spin']" />
        Refresh
      </Button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card v-for="stat in stats" :key="stat.title" class="hover:shadow-md transition-shadow">
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">{{ stat.title }}</p>
              <p class="text-2xl font-bold mt-2">{{ stat.value }}</p>
            </div>
            <div :class="[stat.bgColor, 'p-3 rounded-lg']">
              <component :is="stat.icon" :class="[stat.color, 'h-6 w-6']" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Table Card -->
    <Card class="shadow-md">
      <CardHeader>
        <CardTitle>Exam Records</CardTitle>
        <CardDescription>
          View all your exam attempts and their results
        </CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Filters -->
        <div class="flex gap-2 items-center py-4">
          <Input
            class="max-w-sm"
            placeholder="Search exams..."
            :model-value="table.getColumn('title')?.getFilterValue() as string"
            @update:model-value="table.getColumn('title')?.setFilterValue($event)"
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
                <TableHead
                  v-for="header in headerGroup.headers"
                  :key="header.id"
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
              <template v-if="examHistoryStore.loading">
                <TableRow>
                  <TableCell :colspan="columns.length" class="text-center h-24">
                    <div class="flex items-center justify-center gap-2">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900"></div>
                      <span>Loading exam history...</span>
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
                  <TableCell
                    v-for="cell in row.getVisibleCells()"
                    :key="cell.id"
                  >
                    <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                  </TableCell>
                </TableRow>
              </template>
              
              <TableRow v-else>
                <TableCell :colspan="columns.length" class="text-center h-32">
                  <div class="flex flex-col items-center gap-3 text-gray-500">
                    <BookOpen class="h-12 w-12 text-gray-300" />
                    <div>
                      <p class="font-medium text-lg">No exam history found</p>
                      <p class="text-sm mt-1">Start taking exams to see your history here</p>
                    </div>
                  </div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between space-x-2 py-4">
          <div class="flex-1 text-sm text-muted-foreground">
            Showing {{ table.getState().pagination.pageIndex * table.getState().pagination.pageSize + 1 }} 
            to {{ Math.min((table.getState().pagination.pageIndex + 1) * table.getState().pagination.pageSize, table.getFilteredRowModel().rows.length) }} 
            of {{ table.getFilteredRowModel().rows.length }} exam(s)
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
      </CardContent>
    </Card>
  </div>
</template>