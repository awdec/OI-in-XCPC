<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 从路由中获取年份
const currentYear = computed(() => route.params.year || null)

// 导航项（年份相关）
const yearNavItems = computed(() => {
  if (!currentYear.value) return []
  return [
    { path: `/${currentYear.value}/`, label: '赛区列表', icon: '🏠' },
    { path: `/${currentYear.value}/summary`, label: '全部成绩', icon: '📊' },
    { path: `/${currentYear.value}/players`, label: '选手成绩', icon: '👤' },
    { path: `/${currentYear.value}/analysis`, label: '数据分析', icon: '📈' },
  ]
})

// 全局导航项
const globalNavItems = [
  { path: '/', label: '年份选择', icon: '📅' },
  { path: '/announcement', label: '公告', icon: '📢' },
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
            <h1 class="text-lg font-bold text-gray-800">
              {{ currentYear ? `${currentYear} ICPC/CCPC 比赛结果` : 'ICPC/CCPC 比赛结果' }}
            </h1>
          </div>
          <nav class="flex gap-1">
            <!-- 全局导航 -->
            <router-link
              v-for="item in globalNavItems"
              :key="item.path"
              :to="item.path"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="route.path === item.path
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
            >
              {{ item.icon }} {{ item.label }}
            </router-link>
            <!-- 年份导航 -->
            <router-link
              v-for="item in yearNavItems"
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
