<script setup lang="ts">
import { PanelLeft, Bell, User } from 'lucide-vue-next'
import { useSidebarStore } from '@/stores/sidebar'
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

import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { useAuthStore } from '@/stores/auth'

const { toggleSidebar } = useSidebarStore()
const auth = useAuthStore()

function logout() {
  auth.logout()
  window.location.href = '/login' // or use router.push if using <RouterLink>
}
</script>

<template>
  <header class="flex h-16 shrink-0 items-center gap-2 border-b px-4 justify-between">
    <!-- Left section: Sidebar toggle + Breadcrumb -->
    <div class="flex items-center gap-4">
      <Button
        variant="ghost"
        size="icon"
        class="rounded-md"
        @click="toggleSidebar"
      >
        <PanelLeft class="w-5 h-5" />
      </Button>

      <Separator orientation="vertical" class="h-6" />

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

    <!-- Right section: Notifications + Profile -->
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
</template>
