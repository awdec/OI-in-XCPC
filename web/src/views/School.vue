<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadAllContests } from '../utils/dataLoader'
import RankTable from '../components/RankTable.vue'
import TeamDetail from '../components/TeamDetail.vue'

const route = useRoute()
const router = useRouter()

const schoolName = computed(() => decodeURIComponent(route.params.name))
const allTeams = ref([])
const loading = ref(true)
const selectedTeam = ref(null)
const showTeamDetail = ref(false)

const stats = computed(() => {
  const totalSolved = allTeams.value.reduce((s, t) => s + t.solved, 0)
  const bestRank = Math.min(...allTeams.value.map(t => t.rank || Infinity))
  return { count: allTeams.value.length, totalSolved, bestRank }
})

const loadData = async () => {
  loading.value = true
  const contests = await loadAllContests()
  const teams = []
  contests.forEach(c => {
    const formal = c.sheets['正式队伍'] || []
    formal.forEach(t => {
      if (t.school === schoolName.value) {
        teams.push({ ...t, _contest: c.name })
      }
    })
  })
  allTeams.value = teams.sort((a, b) => (a.rank || 999) - (b.rank || 999))
  loading.value = false
}

onMounted(loadData)
watch(() => route.params.name, loadData)
</script>

<template>
  <div>
    <el-button text @click="router.back()" class="mb-4">← 返回</el-button>

    <div v-if="loading" class="flex justify-center py-20">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-else>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ schoolName }}</h2>
      <div class="flex gap-6 text-sm text-gray-500 mb-6">
        <span>参赛队伍: <b class="text-gray-700">{{ stats.count }}</b></span>
        <span>总解题数: <b class="text-blue-600">{{ stats.totalSolved }}</b></span>
        <span>最佳排名: <b class="text-green-600">#{{ stats.bestRank }}</b></span>
      </div>

      <RankTable
        :teams="allTeams"
        @team-click="(t) => { selectedTeam = t; showTeamDetail = true }"
      />

      <TeamDetail v-model:visible="showTeamDetail" :team="selectedTeam" :contest-name="selectedTeam?._contest" />
    </div>
  </div>
</template>
