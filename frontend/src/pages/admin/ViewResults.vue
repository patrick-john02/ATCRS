<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
import { useResultsStore } from '@/stores/resultsStore'
import { format } from 'date-fns'
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
import { ChevronDown, ChevronsUpDown, RefreshCcw } from 'lucide-vue-next'
import { valueUpdater } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import type { ExamResult } from '@/types/results'

const resultsStore = useResultsStore()

onMounted(() => {
  resultsStore.fetchAllResults()
  resultsStore.fetchStatistics()
})

const getScoreColor = (score: string) => {
  const numScore = parseFloat(score)
  if (numScore >= 80) return 'text-green-600'
  if (numScore >= 60) return 'text-yellow-600'
  return 'text-red-600'
}

const columnHelper = createColumnHelper<ExamResult>()
const columns = [
  columnHelper.accessor('applicant.name', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Applicant Name', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: ({ row }) => h('div', { class: 'font-medium' }, row.original.applicant.name),
  }),
  columnHelper.accessor('applicant.email', {
    header: 'Email',
    cell: ({ row }) => h('div', { class: 'text-sm' }, row.original.applicant.email),
  }),
  columnHelper.accessor('exam.title', {
    header: 'Exam',
    cell: ({ row }) => h('div', { class: 'font-medium' }, row.original.exam.title),
  }),
  columnHelper.accessor('recommendation_score', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Score', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: ({ row }) =>
      h('div', { class: `font-bold ${getScoreColor(row.original.recommendation_score)}` }, 
        `${row.original.recommendation_score}%`
      ),
  }),
  columnHelper.accessor('correct_answers', {
    header: 'Correct/Total',
    cell: ({ row }) =>
      h('div', { class: 'text-sm' }, 
        `${row.original.correct_answers}/${row.original.total_questions}`
      ),
  }),
  columnHelper.accessor('recommended_course', {
    header: 'Recommended Course',
    cell: ({ row }) => {
      const course = row.original.recommended_course
      return course
        ? h(Badge, { variant: 'secondary' }, () => `${course.code} - ${course.name}`)
        : h(Badge, { variant: 'outline' }, () => 'N/A')
    },
  }),
  columnHelper.accessor('completed_at', {
    header: 'Completed At',
    cell: ({ row }) =>
      h('div', { class: 'text-sm' }, 
        format(new Date(row.original.completed_at), 'MMM dd, yyyy')
      ),
  }),
]

const sorting = ref<SortingState>([{ id: 'completed_at', desc: true }])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})

const table = useVueTable({
  get data() {
    return resultsStore.results
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: updaterOrValue => valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: updaterOrValue => valueUpdater(updaterOrValue, columnVisibility),
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

const handleRefresh = async () => {
  await Promise.all([
    resultsStore.fetchAllResults(),
    resultsStore.fetchStatistics()
  ])
}
</script>

<template>
  <div class="w-full space-y-6 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold">Exam Results</h1>
        <p class="text-muted-foreground mt-1">View all completed exam results and statistics</p>
      </div>
      <Button @click="handleRefresh" variant="outline" :disabled="resultsStore.loading">
        <RefreshCcw :class="['h-4 w-4 mr-2', resultsStore.loading && 'animate-spin']" />
        Refresh
      </Button>
    </div>

    <!-- Statistics Cards -->
    <div v-if="resultsStore.statistics" class="grid gap-4 md:grid-cols-4">
      <Card>
        <CardHeader class="pb-2">
          <CardDescription>Total Exams</CardDescription>
          <CardTitle class="text-3xl">{{ resultsStore.statistics.statistics.total_exams }}</CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader class="pb-2">
          <CardDescription>Average Score</CardDescription>
          <CardTitle class="text-3xl" :class="getScoreColor(resultsStore.statistics.statistics.average_score.toString())">
            {{ resultsStore.statistics.statistics.average_score.toFixed(1) }}%
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader class="pb-2">
          <CardDescription>Passed</CardDescription>
          <CardTitle class="text-3xl text-green-600">{{ resultsStore.statistics.statistics.passed_count }}</CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader class="pb-2">
          <CardDescription>Failed</CardDescription>
          <CardTitle class="text-3xl text-red-600">{{ resultsStore.statistics.statistics.failed_count }}</CardTitle>
        </CardHeader>
      </Card>
    </div>

    <!-- Table -->
    <Card>
      <CardHeader>
        <CardTitle>All Results</CardTitle>
        <CardDescription>Complete list of exam results</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="flex gap-2 items-center py-4">
          <Input
            class="max-w-sm"
            placeholder="Search by name..."
            :model-value="table.getColumn('applicant_name')?.getFilterValue() as string"
            @update:model-value="table.getColumn('applicant_name')?.setFilterValue($event)"
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
              <template v-if="resultsStore.loading">
                <TableRow>
                  <TableCell :colspan="columns.length" class="text-center h-24">
                    <div class="flex items-center justify-center gap-2">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900"></div>
                      <span>Loading results...</span>
                    </div>
                  </TableCell>
                </TableRow>
              </template>
              <template v-else-if="table.getRowModel().rows.length">
                <TableRow
                  v-for="row in table.getRowModel().rows"
                  :key="row.id"
                  class="hover:bg-muted/50"
                >
                  <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                    <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                  </TableCell>
                </TableRow>
              </template>
              <TableRow v-else>
                <TableCell :colspan="columns.length" class="text-center h-24">
                  No results found.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>

        <div class="flex items-center justify-between space-x-2 py-4">
          <div class="flex-1 text-sm text-muted-foreground">
            Showing {{ table.getState().pagination.pageIndex * table.getState().pagination.pageSize + 1 }}
            to {{ Math.min((table.getState().pagination.pageIndex + 1) * table.getState().pagination.pageSize, table.getFilteredRowModel().rows.length) }}
            of {{ table.getFilteredRowModel().rows.length }} result(s)
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