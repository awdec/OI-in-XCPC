<script setup>
import { ref, onMounted } from 'vue'
import { loadYears } from '../utils/dataLoader'

const years = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    years.value = await loadYears()
  } catch (e) {
    console.error('加载年份数据失败:', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">ICPC/CCPC 比赛结果</h2>
      <p class="text-gray-500">选择年份查看各赛区比赛结果</p>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-else-if="years.length === 0" class="text-center py-20 text-gray-500">
      暂无数据
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
      <router-link
        v-for="y in years"
        :key="y.year"
        :to="`/${y.year}/`"
        class="block bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all cursor-pointer group"
      >
        <div class="h-1.5 rounded-t-xl bg-blue-500" />
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-2xl font-bold text-gray-800 group-hover:text-blue-600 transition-colors">
              {{ y.year }}
            </h3>
            <span class="text-sm text-gray-400">赛季</span>
          </div>

          <div class="space-y-2 text-sm text-gray-600">
            <div class="flex items-center gap-2">
              <span class="text-blue-500">🏆</span>
              <span>{{ y.contest_count }} 个赛区</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-green-500">👥</span>
              <span>{{ y.total_teams }} 支队伍</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100">
            <span class="text-blue-500 text-sm font-medium group-hover:text-blue-700 transition-colors">
              查看详情 →
            </span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>
