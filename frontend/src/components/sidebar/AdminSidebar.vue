<script setup lang="ts">
import { useSidebarStore } from '@/stores/sidebar'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
  type SidebarProps,
} from '@/components/ui/sidebar'

const props = defineProps<SidebarProps>()
const sidebarStore = useSidebarStore()
const route = useRoute()

onMounted(() => {
  sidebarStore.initialize()
})

const navMain = [
  {
    title: 'Dashboard',
    url: '/admin/dashboard',
    items: [],
  },
  {
    title: 'Applicant Management',
    url: null,
    items: [
      { title: 'Applicants', url: '/admin/applicants' },
      // { title: 'Pending Applications', url: '/admin/applicants/pending' },
      // { title: 'Verified Applicants', url: '/admin/applicants/verified' },
    ],
  },
  {
    title: 'Exam Management',
    url: null,
    items: [
      // { title: 'Question Bank', url: '/admin/exams/questions' },
      // { title: 'Create Exam', url: '/admin/exams/create' },
      { title: 'Manage Exams', url: '/admin/exams' },
    ],
  },
  {
    title: 'Exam Results',
    url: null,
    items: [
      { title: 'View Results', url: '/admin/results' },
      { title: 'Passed Applicants', url: '/admin/results/passed' },
      // { title: 'Failed Applicants', url: '/admin/results/failed' },
    ],
  },
  {
    title: 'Course Management',
    url: null,
    items: [
      { title: 'Manage Courses', url: '/admin/courses' },
      // { title: 'Add Course', url: '/admin/courses/create' },
    ],
  },
  {
    title: 'User Management',
    url: null,
    items: [
      { title: 'Admins', url: '/admin/users/admins' },
      { title: 'Students', url: '/admin/users/students' },
    ],
  },
  {
    title: 'Announcements',
    url: null,
    items: [
      { title: 'Post Announcement', url: '/admin/announcements/create' },
      { title: 'Manage Announcements', url: '/admin/announcements' },
    ],
  },

]
</script>

<template>
  <Sidebar v-bind="props" :open="sidebarStore.isOpen" @update:open="sidebarStore.isOpen = $event">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child>
            <RouterLink to="/admin/dashboard">
              <div class="flex aspect-square size-8 items-center justify-center">
                <img src="@/assets/imgs/apayao.png" alt="Logo" class="h-8 w-8 object-contain rounded-lg" />
              </div>
              <div class="flex flex-col gap-0.5 leading-none">
                <span class="font-semibold">Admin</span>
                <span>Dashboard</span>
              </div>
            </RouterLink>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="item in navMain" :key="item.title">
            <SidebarMenuButton v-if="item.url" as-child>
              <RouterLink :to="item.url" class="font-medium">
                {{ item.title }}
              </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuButton v-else class="font-medium cursor-default">
              {{ item.title }}
            </SidebarMenuButton>

            <SidebarMenuSub v-if="item.items.length">
              <SidebarMenuSubItem v-for="childItem in item.items" :key="childItem.title">
                <SidebarMenuSubButton as-child :is-active="route.path === childItem.url">
                  <RouterLink :to="childItem.url">{{ childItem.title }}</RouterLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>

    <SidebarRail />
  </Sidebar>
</template>
