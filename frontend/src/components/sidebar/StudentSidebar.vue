<script setup lang="ts">
import { useRoute } from 'vue-router';
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
const route = useRoute()

const props = defineProps<SidebarProps>()

const data = {
  navMain: [
    {
      title: 'Dashboard',
      url: '/student/dashboard',
      items: [],
    },
    // {
    //   title: 'Admission',
    //   url: '#',
    //   items: [
    //     { title: 'Apply for Admission', url: '/student/admission/apply' },
    //     { title: 'Upload Requirements', url: '/student/admission/requirements' },
    //   ],
    // },
    {
      title: 'Online Examination',
      url: '#',
      items: [
        { title: 'View Exams', url: '/student/exam/view' },
        { title: 'Exam History', url: '/student/exam/history' },
      ],
    },
    {
      title: 'Results',
      url: '#',
      items: [
        { title: 'View Scores', url: '/student/results/scores' },
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
              <RouterLink :to="item.url" class="font-medium">
              <a :href="item.url" class="font-medium">
                {{ item.title }}
              </a>
              </RouterLink>
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
