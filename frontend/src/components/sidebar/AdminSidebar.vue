<script setup lang="ts">
import { useSidebarStore } from '@/stores/sidebar'
import { RouterLink } from 'vue-router'
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
  type SidebarProps,
  SidebarRail,
} from '@/components/ui/sidebar'

const props = defineProps<SidebarProps>()
const sidebarStore = useSidebarStore()

onMounted(() => {
  sidebarStore.initialize()
})

const data = {
  navMain: [
    {
      title: 'Dashboard',
      url: '/admin/dashboard',
      items: [],
    },
    {
      title: 'Applicant Management',
      url: '#',
      items: [
        { title: 'All Applicants', url: '/admin/applicants' },
        { title: 'Pending Applications', url: '/admin/applicants/pending' },
        { title: 'Verified Applicants', url: '/admin/applicants/verified' },
      ],
    },
    {
      title: 'Exam Management',
      url: '#',
      items: [
        { title: 'Question Bank', url: '/admin/exams/questions' },
        { title: 'Create Exam', url: '/admin/exams/create' },
        { title: 'Manage Exams', url: '/admin/exams' },
      ],
    },
    {
      title: 'Exam Results',
      url: '#',
      items: [
        { title: 'View Results', url: '/admin/results' },
        { title: 'Passed Applicants', url: '/admin/results/passed' },
        { title: 'Failed Applicants', url: '/admin/results/failed' },
      ],
    },
    {
      title: 'Course Management',
      url: '#',
      items: [
        { title: 'List of Courses', url: '/admin/courses' },
        { title: 'Add Course', url: '/admin/courses/create' },
      ],
    },
    {
      title: 'User Management',
      url: '#',
      items: [
        { title: 'Admins', url: '/admin/users/admins' },
        { title: 'Students', url: '/admin/users/students' },
      ],
    },
    {
      title: 'Announcements',
      url: '#',
      items: [
        { title: 'Post Announcement', url: '/admin/announcements/create' },
        { title: 'Manage Announcements', url: '/admin/announcements' },
      ],
    },
    {
      title: 'System Settings',
      url: '#',
      items: [
        { title: 'Audit Logs', url: '/admin/settings/logs' },
        { title: 'Site Configuration', url: '/admin/settings/config' },
      ],
    },
  ],
}
</script>


<template>
  <Sidebar
    v-bind="props"
    :open="sidebarStore.isOpen"
    @update:open="sidebarStore.isOpen = $event"
  >
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child>
            <RouterLink to="#">
              <div class="flex aspect-square size-8 items-center justify-center text-sidebar-primary-foreground">
                <img src="@/assets/imgs/apayao.png" alt="Logo" class="h-8 w-8 object-contain rounded-lg" />
              </div>
              <div class="flex flex-col gap-0.5 leading-none">
                <span class="font-semibold">Admin</span>
                <span class="">Dashboard</span>
              </div>
            </RouterLink>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="item in data.navMain" :key="item.title">
            <SidebarMenuButton as-child>
              <RouterLink :to="item.url" class="font-medium">
                {{ item.title }}
              </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuSub v-if="item.items.length">
              <SidebarMenuSubItem v-for="childItem in item.items" :key="childItem.title">
                <SidebarMenuSubButton as-child :is-active="childItem.isActive">
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
