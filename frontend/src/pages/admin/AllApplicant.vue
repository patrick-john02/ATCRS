<script setup lang="ts">
import { h, ref, computed, onMounted, reactive } from 'vue'
import { useApplicantUsersStore } from '@/stores/useApplicantUserStore'
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
import { Label } from '@/components/ui/label'
import type { ViewApplicants } from '@/types/viewApplicants'

const applicantStore = useApplicantUsersStore()

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  contact_number: '',
  address: '',
  birthdate: '',
  password: ''
})

const isDialogOpen = ref(false)
const iseditDialogOpen = ref(false)
const selectedApplicant = ref<any>(null)

const openEditModal = (row: any) => {
  selectedApplicant.value = row.original
  iseditDialogOpen.value = true
}



const handleSubmit = async () => {
  try {
    await applicantStore.addAdmin(form)
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
    isDialogOpen.value = false
  } catch (error) {
    console.error('Failed to add applicants:', error)
  }
}

onMounted(() => {
  if (applicantStore.applicant.length === 0) {
    applicantStore.loadApplicants()
  }
})

const columnHelper = createColumnHelper<ViewApplicants>()

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
  columnHelper.accessor('first_name', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['First Name', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('last_name', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Last Name', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('username', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Username', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => h('div', { class: 'font-mono' }, info.getValue()),
  }),
  columnHelper.accessor('email', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Email', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: info => h('div', { class: 'lowercase' }, info.getValue()),
  }),
  columnHelper.accessor('contact_number', {
    header: 'Contact',
    cell: info => info.getValue(),
  }),
  
  columnHelper.accessor('birthdate', {
    header: ({ column }) =>
      h(
        Button,
        {
          variant: 'ghost',
          onClick: () =>
            column.toggleSorting(column.getIsSorted() === 'asc'),
        },
        () => ['Birthdate', h(ChevronsUpDown, { class: 'ml-2 h-4 w-4' })],
      ),
    cell: ({ row }) =>
      new Date(row.original.birthdate).toLocaleDateString(),
  }),
columnHelper.display({
  id: 'actions',
  header: () => 'Action',
  cell: ({ row }) =>
    h('div', { class: 'flex gap-2' }, [
      h(
        Button,
        {
          size: 'sm',
          variant: 'outline',
          onClick: () => openEditModal(row), 
        },
        () => 'Edit'
      ),
      h(
        Button,
        {
          size: 'sm',
          variant: 'destructive',
          onClick: () => console.log('Delete:', row.original.id),
        },
        () => 'Delete'
      ),
    ]),
})
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
    return applicantStore.applicant
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
    <Alert v-if="applicantStore.error" variant="destructive">
      <AlertDescription>
        {{ applicantStore.error }}
      </AlertDescription>
    </Alert>

    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex flex-1 flex-col gap-2 sm:flex-row sm:items-center">
        <Input
          class="max-w-sm"
          placeholder="Filter by email..."
          :model-value="table.getColumn('email')?.getFilterValue() as string"
          @update:model-value="table.getColumn('email')?.setFilterValue($event)"
        />
        <Input
          class="max-w-sm"
          placeholder="Filter by first name..."
          :model-value="table.getColumn('first_name')?.getFilterValue() as string"
          @update:model-value="table.getColumn('first_name')?.setFilterValue($event)"
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
              Add Applicant
            </Button>
          </DialogTrigger>
          <DialogContent class="sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>Add New Applicant User</DialogTitle>
              <DialogDescription>
                Fill out the form to create a new Applicant user.
              </DialogDescription>
            </DialogHeader>

            <!-- Form inside Dialog -->
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <Label for="username">Username</Label>
                  <Input id="username" v-model="form.username" required />
                </div>
                <div>
                  <Label for="email">Email</Label>
                  <Input id="email" v-model="form.email" type="email" required />
                </div>
                <div>
                  <Label for="first_name">First Name</Label>
                  <Input id="first_name" v-model="form.first_name" required />
                </div>
                <div>
                  <Label for="last_name">Last Name</Label>
                  <Input id="last_name" v-model="form.last_name" required />
                </div>
                <div>
                  <Label for="contact_number">Contact</Label>
                  <Input id="contact_number" v-model="form.contact_number" required />
                </div>
                <div>
                  <Label for="address">Address</Label>
                  <Input id="address" v-model="form.address" required />
                </div>
                <div>
                  <Label for="birthdate">Birthdate</Label>
                  <Input id="birthdate" v-model="form.birthdate" type="date" required />
                </div>

                <div class="col-span-2">
                  <Label for="password">Password</Label>
                  <Input id="password" v-model="form.password" type="password" required />
                </div>
              </div>

              <DialogFooter>
                <Button type="submit" :disabled="applicantStore.loading">
                  <Loader2 v-if="applicantStore.loading" class="mr-2 h-4 w-4 animate-spin" />
                  Save
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>

    <Dialog v-model:open="iseditDialogOpen">
  <DialogContent class="sm:max-w-[500px]">
    <DialogHeader>
      <DialogTitle>Edit Applicant</DialogTitle>
      <DialogDescription>
        Update the applicant details below.
      </DialogDescription>
    </DialogHeader>

    <div v-if="selectedApplicant">
      <p><b>ID:</b> {{ selectedApplicant.id }}</p>
      <p><b>Name:</b> {{ selectedApplicant.first_name }} {{ selectedApplicant.last_name }}</p>
      <!-- you can also bind inputs here for editing -->
    </div>

    <DialogFooter>
      <Button variant="outline" @click="iseditDialogOpen = false">Cancel</Button>
      <Button @click="console.log('Save changes')">Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>


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
            <template v-if="!applicantStore.loading && table.getRowModel().rows.length">
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
            <TableRow v-else-if="applicantStore.loading">
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