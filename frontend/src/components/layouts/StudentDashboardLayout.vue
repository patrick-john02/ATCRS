<script setup lang="ts">
import StudentSidebar from '../sidebar/StudentSidebar.vue'
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { Bell, User } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

function logout() {
  auth.logout()
  window.location.href = '/login'
}
</script>

<template>
  <SidebarProvider>
    <StudentSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center justify-between gap-4 border-b px-4">
        <!-- Left section: Sidebar + Breadcrumb -->
        <div class="flex items-center gap-4">
          <SidebarTrigger />
          <Separator orientation="vertical" class="h-5" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem class="hidden md:block">
                <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator class="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Current Page</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        <!-- Right section: Notification + Profile -->
        <div class="flex items-center gap-4">
          <!-- Notification Bell -->
          <Button variant="ghost" size="icon">
            <Bell class="h-5 w-5" />
          </Button>

          <!-- Profile Dropdown -->
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Avatar class="cursor-pointer">
                <AvatarImage src="" alt="User" />
                <AvatarFallback>
                  {{ auth.user?.first_name?.[0] ?? 'U' }}
                </AvatarFallback>
              </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="w-40">
              <DropdownMenuItem>
                <User class="mr-2 h-4 w-4" /> Profile
              </DropdownMenuItem>
              <DropdownMenuItem @click="logout">
                <span class="text-red-500">Logout</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <main class="flex-1 p-4">
        <slot />
      </main>
    </SidebarInset>
  </SidebarProvider>
</template>
