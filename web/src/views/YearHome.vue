<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'
import { loadContestsIndex } from '../utils/dataLoader'

const props = defineProps({
  year: {
    type: String,
    required: true
  }
})

const route = useRoute()
const contests = ref([])
const loading = ref(true)

const loadContests = async (year) => {
  loading.value = true
  try {
    contests.value = await loadContestsIndex(year)
  } catch (e) {
    console.error('加载赛区数据失败:', e)
    contests.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadContests(props.year)
})

watch(() => props.year, (newYear) => {
  loadContests(newYear)
})

const orgColor = (org) => {
  if (org === 'ICPC') return 'bg-blue-500'
  if (org === 'CCPC') return 'bg-green-500'
  return 'bg-purple-500'
}

const orgTag = (org) => {
  if (org === 'ICPC') return 'bg-blue-100 text-blue-700'
  if (org === 'CCPC') return 'bg-green-100 text-green-700'
  return 'bg-purple-100 text-purple-700'
}
</script>

<template>
  <div>
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ year }} 赛季各赛区比赛结果</h2>
      <p class="text-gray-500">共 {{ contests.length }} 个赛区，点击卡片查看详情</p>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <router-link
        v-for="c in contests"
        :key="c.id"
        :to="`/${year}/contest/${c.id}`"
        class="block bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all cursor-pointer group"
      >
        <!-- 顶部色条 -->
        <div :class="orgColor(c.org)" class="h-1.5 rounded-t-xl" />

        <div class="p-5">
          <!-- 标题行 -->
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-gray-800 group-hover:text-blue-600 transition-colors">
              {{ c.name }}
            </h3>
            <span :class="orgTag(c.org)" class="text-xs font-medium px-2 py-0.5 rounded-full">
              {{ c.org }}
            </span>
          </div>

          <!-- 冠军信息 -->
          <div v-if="c.champion" class="bg-gray-50 rounded-lg p-3">
            <div class="text-xs text-gray-400 mb-1">🥇 冠军</div>
            <div class="font-medium text-gray-700">{{ c.champion.school }}</div>
            <div class="text-sm text-gray-500 flex items-center gap-2">
              <span>{{ c.champion.team }}</span>
              <span class="text-blue-600">{{ c.champion.solved }} 题</span>
              <span class="text-gray-400">罚时 {{ c.champion.penalty }}</span>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>
