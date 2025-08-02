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
      url: '/dashboard',
      items: [],
    },
    {
      title: 'Admission',
      url: '#',
      items: [
        { title: 'Apply for Admission', url: '/admission/apply' },
        { title: 'Admission Status', url: '/admission/status' },
        { title: 'Upload Requirements', url: '/admission/requirements' },
      ],
    },
    {
      title: 'Online Examination',
      url: '#',
      items: [
        { title: 'Exam Instructions', url: '/exam/instructions' },
        { title: 'Take Exam', url: '/exam/start' },
        { title: 'Exam History', url: '/exam/history' },
      ],
    },
    {
      title: 'Results',
      url: '#',
      items: [
        { title: 'View Scores', url: '/results/scores' },
        { title: 'Download Result', url: '/results/download' },
      ],
    },
    {
      title: 'Announcements',
      url: '/announcements',
      items: [],
    },
    {
      title: 'Support',
      url: '#',
      items: [
        { title: 'FAQs', url: '/support/faqs' },
        { title: 'Contact Admin', url: '/support/contact' },
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
                <span class="font-semibold">Student</span>
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
