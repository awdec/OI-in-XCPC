<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/compare', label: '跨赛区对比', icon: '📊' },
]
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-14">
          <div class="flex items-center gap-2 cursor-pointer" @click="router.push('/')">
            <span class="text-xl">🏆</span>
            <h1 class="text-lg font-bold text-gray-800">2025 ICPC/CCPC 比赛结果</h1>
          </div>
          <nav class="flex gap-1">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="route.path === item.path
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
            >
              {{ item.icon }} {{ item.label }}
            </router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- 页面内容 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view />
    </main>
  </div>
</template>
