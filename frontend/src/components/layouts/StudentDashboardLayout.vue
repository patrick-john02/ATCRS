<script setup lang="ts">
import { Bell, User } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import StudentSidebar from '../sidebar/StudentSidebar.vue'
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
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

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const breadcrumbs = computed(() => {
  return route.matched
    .filter(r => r.name)
    .map(r => {
      const name = typeof r.meta?.breadcrumb === 'string'
        ? r.meta.breadcrumb
        : String(r.name)

      return {
        name,
        to: { name: r.name as string } // router-link compatible
      }
    })
})


function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <SidebarProvider>
    <StudentSidebar />
    <SidebarInset>
      <header class="flex h-16 items-center justify-between gap-4 border-b px-4">
        <!-- Left: Sidebar + Breadcrumb -->
        <div class="flex items-center gap-4">
          <SidebarTrigger />
          <Separator orientation="vertical" class="h-5" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem
                v-for="(crumb, index) in breadcrumbs"
                :key="index"
              >
                <template v-if="index < breadcrumbs.length - 1">
                  <BreadcrumbLink as-child>
                    <router-link :to="crumb.to">{{ crumb.name }}</router-link>
                  </BreadcrumbLink>
                  <BreadcrumbSeparator />
                </template>
                <template v-else>
                  <BreadcrumbPage>{{ crumb.name }}</BreadcrumbPage>
                </template>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        <!-- Right: Notification + Profile -->
        <div class="flex items-center gap-4">
          <!-- <Button variant="ghost" size="icon">
            <Bell class="h-5 w-5" />
          </Button> -->

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
              <!-- <DropdownMenuItem>
                <User class="mr-2 h-4 w-4" /> Profile
              </DropdownMenuItem> -->
              <DropdownMenuItem @click="logout">
                <span class="text-red-500">Logout</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <!-- Child pages go here -->
      <main class="flex-1 p-4">
        <router-view />
      </main>
    </SidebarInset>
  </SidebarProvider>
</template>
