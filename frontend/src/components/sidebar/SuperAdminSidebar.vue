<script setup lang="ts">
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

const data = {
  navMain: [
    {
      title: 'Dashboard',
      url: '/superadmin/dashboard',
      items: [],
    },
    {
      title: 'Admin Management',
      url: '#',
      items: [
        { title: 'All Admins', url: '/superadmin/admins' },
        { title: 'Add New Admin', url: '/superadmin/admins/create' },
      ],
    },
    {
      title: 'User Overview',
      url: '#',
      items: [
        { title: 'All Applicants', url: '/superadmin/applicants' },
        { title: 'All Users', url: '/superadmin/users' },
      ],
    },
    {
      title: 'Course & Department Settings',
      url: '#',
      items: [
        { title: 'Manage Courses', url: '/superadmin/courses' },
        { title: 'Manage Departments', url: '/superadmin/departments' },
      ],
    },
    {
      title: 'Academic Settings',
      url: '#',
      items: [
        { title: 'Academic Years', url: '/superadmin/academic-years' },
        { title: 'School Terms', url: '/superadmin/terms' },
      ],
    },
    {
      title: 'System Monitoring',
      url: '#',
      items: [
        { title: 'Audit Logs', url: '/superadmin/logs' },
        { title: 'Activity Reports', url: '/superadmin/activity' },
      ],
    },
    {
      title: 'System Settings',
      url: '#',
      items: [
        { title: 'Site Configuration', url: '/superadmin/settings' },
        { title: 'Database Backup', url: '/superadmin/backup' },
      ],
    },
  ],
}
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child>
            <a href="#">
              <div class="flex aspect-square size-8 items-center justify-center text-sidebar-primary-foreground">
                <img src="@/assets/imgs/apayao.png" alt="Logo" class="h-8 w-8 object-contain rounded-lg" />
              </div>
              <div class="flex flex-col gap-0.5 leading-none">
                <span class="font-semibold">Super Admin</span>
                <span class="">Dashboard</span>
              </div>
            </a>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="item in data.navMain" :key="item.title">
            <SidebarMenuButton as-child>
              <a :href="item.url" class="font-medium">
                {{ item.title }}
              </a>
            </SidebarMenuButton>
            <SidebarMenuSub v-if="item.items.length">
              <SidebarMenuSubItem v-for="childItem in item.items" :key="childItem.title">
                <SidebarMenuSubButton as-child :is-active="childItem.isActive">
                  <a :href="childItem.url">{{ childItem.title }}</a>
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
