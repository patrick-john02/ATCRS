<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'
import apayaoLogo from '@/assets/imgs/apayao.png'

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const defaultValue = 'item-1'

const accordionItems = [
  {
    value: 'item-1',
    title: 'How do I apply?',
    content: 'You can apply by creating an account and completing the online application form. Once submitted, you\'ll receive instructions for your exam schedule.'
  },
  {
    value: 'item-2',
    title: 'What are the exam requirements?',
    content: 'A stable internet connection, a computer or mobile device, and a quiet space are required. Make sure to review the guidelines sent after registration.'
  },
  {
    value: 'item-3',
    title: 'What if I miss the exam schedule?',
    content: 'Contact the admissions office immediately. In some cases, a reschedule can be arranged depending on availability.'
  }
]


</script>

<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <nav class="border-b border-gray-200 py-4 px-6">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <!-- Logo -->
        <div class="flex items-center space-x-2">
          <img :src="apayaoLogo" alt="Apayao Logo" class="h-10 w-auto" />
          <span class="text-xl font-bold text-blue-600"> Apayao State College Admission System</span>
        </div>

        <!-- Login Button -->
        <Button @click="goToLogin">
          Login
        </Button>
      </div>
    </nav>
    

    <!-- Hero Section -->
    <section class="text-center mt-24 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        Welcome to the Admission Test Examination System
      </h1>
      <p class="text-gray-600 text-lg max-w-2xl mx-auto">
        Streamline your entrance exams with a smart, reliable, and easy-to-use online testing platform.
      </p>
    </section>


    <!-- How It Works Section -->
    <section class="mt-32 px-4">
    <h2 class="text-3xl font-bold text-center text-gray-800 mb-10">
        How It Works
    </h2>

    <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">
        <!-- Step 1 -->
        <div class="border rounded-xl p-6 shadow-sm text-center">
        <div class="text-blue-600 text-4xl mb-3">📝</div>
        <h3 class="font-semibold text-lg mb-2">Register an Account</h3>
        <p class="text-gray-600 text-sm">
            Create your personal account using a valid email to begin the application process.
        </p>
        </div>

        <!-- Step 2 -->
        <div class="border rounded-xl p-6 shadow-sm text-center">
        <div class="text-green-600 text-4xl mb-3">📄</div>
        <h3 class="font-semibold text-lg mb-2">Fill up Application</h3>
        <p class="text-gray-600 text-sm">
            Provide your personal and academic details to complete your application.
        </p>
        </div>

        <!-- Step 3 -->
        <div class="border rounded-xl p-6 shadow-sm text-center">
        <div class="text-yellow-500 text-4xl mb-3">🧪</div>
        <h3 class="font-semibold text-lg mb-2">Take the Online Exam</h3>
        <p class="text-gray-600 text-sm">
            Join the scheduled online examination from anywhere using your account.
        </p>
        </div>

        <!-- Step 4 -->
        <div class="border rounded-xl p-6 shadow-sm text-center">
        <div class="text-purple-600 text-4xl mb-3">📊</div>
        <h3 class="font-semibold text-lg mb-2">View Results</h3>
        <p class="text-gray-600 text-sm">
            Get notified when results are out and view your score instantly.
        </p>
        </div>
    </div>
    </section>

    <!-- Features Section -->
    <section class="mt-32 px-4">
    <h2 class="text-3xl font-bold text-center text-gray-800 mb-10">
        Key Features
    </h2>

    <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <!-- Feature 1 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-blue-600 text-3xl mb-3">🔒</div>
        <h3 class="font-semibold text-lg mb-2">Secure Online Testing</h3>
        <p class="text-sm text-gray-600">
            All exams are protected with anti-cheat measures and real-time monitoring.
        </p>
        </div>

        <!-- Feature 2 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-green-600 text-3xl mb-3">📱</div>
        <h3 class="font-semibold text-lg mb-2">Mobile-Friendly Access</h3>
        <p class="text-sm text-gray-600">
            Take exams and check results anytime from your phone or tablet.
        </p>
        </div>

        <!-- Feature 3 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-yellow-500 text-3xl mb-3">⚙️</div>
        <h3 class="font-semibold text-lg mb-2">Auto-Grading</h3>
        <p class="text-sm text-gray-600">
            Automatic scoring for objective questions ensures instant feedback.
        </p>
        </div>

        <!-- Feature 4 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-purple-600 text-3xl mb-3">📈</div>
        <h3 class="font-semibold text-lg mb-2">Result Tracking</h3>
        <p class="text-sm text-gray-600">
            Easily track scores, feedback, and exam history in one place.
        </p>
        </div>

        <!-- Feature 5 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-pink-500 text-3xl mb-3">🛠️</div>
        <h3 class="font-semibold text-lg mb-2">Admin Dashboard</h3>
        <p class="text-sm text-gray-600">
            Powerful admin tools for managing exams, users, and analytics.
        </p>
        </div>

          <!-- Feature 6 -->
        <div class="rounded-xl border p-6 shadow-sm bg-white">
        <div class="text-pink-500 text-3xl mb-3">🛠️</div>
        <h3 class="font-semibold text-lg mb-2">Student Dashboard</h3>
        <p class="text-sm text-gray-600">
            Powerful admin tools for managing exams, users, and analytics.
        </p>
        </div>
    </div>
    </section>


    <section class="mt-32 px-4">
    <h2 class="text-3xl font-bold text-center text-gray-800 mb-10">
      Frequently Asked Questions
    </h2>

    <div class="max-w-3xl mx-auto bg-white p-6 rounded-xl border shadow-sm">
      <Accordion type="single" collapsible :default-value="defaultValue" class="space-y-4">
        <AccordionItem
          v-for="item in accordionItems"
          :key="item.value"
          :value="item.value"
        >
          <AccordionTrigger class="text-left text-lg font-semibold text-gray-900">
            {{ item.title }}
          </AccordionTrigger>
          <AccordionContent class="text-gray-600 mt-2">
            {{ item.content }}
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  </section>

  <section class="mt-32 px-4 mb-20">
    <div class="bg-blue-600 text-white py-12 px-6 rounded-xl max-w-5xl mx-auto text-center shadow-lg">
      <h2 class="text-3xl font-bold mb-4">
        Ready to begin your journey?
      </h2>
      <p class="text-white text-lg mb-6">
        Start your application now and take the first step toward your future.
      </p>
      <Button @click="goToLogin" class="bg-white text-blue-600 hover:bg-gray-100 font-semibold">
        Start Your Application
      </Button>
    </div>
  </section>

  <footer class="bg-gray-100 border-t py-10 px-4 mt-32">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-sm text-gray-700">
      <!-- About Section -->
      <div>
        <h4 class="font-semibold text-base text-gray-900 mb-2">About Apayao State College</h4>
        <p>
          Apayao State College is committed to providing accessible quality education and streamlined digital admission through this system.
        </p>
      </div>

      <!-- Contact Info -->
      <div>
        <h4 class="font-semibold text-base text-gray-900 mb-2">Contact</h4>
        <ul class="space-y-1">
          <li>Email: admissions@asc.edu.ph</li>
          <li>Phone: (078) 123-4567</li>
          <li>Address: Conner, Apayao, Philippines</li>
        </ul>
      </div>

      <!-- Links -->
      <div>
        <h4 class="font-semibold text-base text-gray-900 mb-2">Quick Links</h4>
        <ul class="space-y-1">
          <li><a href="#" class="hover:underline">Terms of Service</a></li>
          <li><a href="#" class="hover:underline">Privacy Policy</a></li>
          <li><a href="#" class="hover:underline">Facebook Page</a></li>
        </ul>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div class="text-center text-xs text-gray-500 mt-8">
      © {{ new Date().getFullYear() }} Apayao State College. All rights reserved.
    </div>
  </footer>
  </div>
</template>