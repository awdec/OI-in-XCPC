<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadContestData, loadSchoolTags } from '../utils/dataLoader'
import { aggregateBySchool } from '../utils/formatters'
import RankTable from '../components/RankTable.vue'
import TeamDetail from '../components/TeamDetail.vue'
import SchoolStats from '../components/SchoolStats.vue'

const route = useRoute()
const router = useRouter()

const contest = ref(null)
const loading = ref(true)
const searchMember = ref('')
const searchTeam = ref('')
const searchSchool = ref('')
const filterSchoolType = ref('')
const filterOiCount = ref('')
const activeTab = ref('rank')
const selectedTeam = ref(null)
const showTeamDetail = ref(false)
const schoolTags = ref({ set985: new Set(), set211: new Set() })

const currentTeams = computed(() => {
  if (!contest.value) return []
  let teams = contest.value.sheets['正式队伍'] || []
  const qSchool = searchSchool.value.trim().toLowerCase()
  const qTeam = searchTeam.value.trim().toLowerCase()
  const qMember = searchMember.value.trim().toLowerCase()
  if (qSchool) teams = teams.filter(t => t.school.toLowerCase().includes(qSchool))
  if (qTeam) teams = teams.filter(t => t.team.toLowerCase().includes(qTeam))
  if (qMember) teams = teams.filter(t => t.members.some(m => m.name.toLowerCase().includes(qMember)))
  if (filterSchoolType.value) {
    const { set985, set211 } = schoolTags.value
    if (filterSchoolType.value === '985') teams = teams.filter(t => set985.has(t.school))
    else if (filterSchoolType.value === '211') teams = teams.filter(t => set211.has(t.school) && !set985.has(t.school))
    else if (filterSchoolType.value === 'other') teams = teams.filter(t => !set211.has(t.school) && !set985.has(t.school))
  }
  if (filterOiCount.value !== '') {
    const n = Number(filterOiCount.value)
    teams = teams.filter(t => t.members.filter(m => m.oi?.length).length === n)
  }
  return teams
})

const schoolStats = computed(() => {
  if (!contest.value) return []
  const formal = contest.value.sheets['正式队伍'] || []
  return aggregateBySchool(formal)
})

const loadContest = async (id) => {
  loading.value = true
  contest.value = await loadContestData(id)
  schoolTags.value = await loadSchoolTags()
  loading.value = false
}

onMounted(() => loadContest(route.params.id))
watch(() => route.params.id, (id) => { if (id) loadContest(id) })

const openTeamDetail = (team) => {
  selectedTeam.value = team
  showTeamDetail.value = true
}

const goSchool = (name) => router.push(`/school/${encodeURIComponent(name)}`)
const goPlayer = (name) => router.push(`/player/${encodeURIComponent(name)}`)
</script>

<template>
  <div v-if="loading" class="flex justify-center py-20">
    <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
  </div>

  <div v-else-if="contest">
    <!-- 赛区标题 -->
    <div class="mb-6">
      <div class="flex items-center gap-3 mb-1">
        <el-button text @click="router.push('/')">← 返回</el-button>
        <h2 class="text-2xl font-bold text-gray-800">{{ contest.name }}</h2>
        <span
          class="text-xs font-medium px-2 py-0.5 rounded-full"
          :class="contest.org === 'ICPC' ? 'bg-blue-100 text-blue-700' : contest.org === 'CCPC' ? 'bg-green-100 text-green-700' : 'bg-purple-100 text-purple-700'"
        >{{ contest.org }}</span>
      </div>
    </div>

    <!-- Tab 切换 -->
    <el-tabs v-model="activeTab" class="mb-4">
      <el-tab-pane label="📋 排名" name="rank" />
      <el-tab-pane label="🏫 学校统计" name="schools" />
    </el-tabs>

    <!-- 排名 Tab -->
    <div v-if="activeTab === 'rank'">
      <!-- 搜索 + 筛选 -->
      <div class="flex flex-wrap items-center gap-3 mb-3">
        <el-input v-model="searchSchool" placeholder="搜索学校" clearable class="w-40" />
        <el-input v-model="searchTeam" placeholder="搜索队伍" clearable class="w-40" />
        <el-input v-model="searchMember" placeholder="搜索队员" clearable class="w-40" />
        <span class="text-sm text-gray-400">共 {{ currentTeams.length }} 支队伍</span>
      </div>
      <div class="flex flex-wrap items-center gap-3 mb-4">
        <el-select v-model="filterSchoolType" placeholder="学校类型" clearable class="w-32">
          <el-option label="985" value="985" />
          <el-option label="211" value="211" />
          <el-option label="其他" value="other" />
        </el-select>
        <el-select v-model="filterOiCount" placeholder="OI 人数" clearable class="w-32">
          <el-option label="0 人" :value="0" />
          <el-option label="1 人" :value="1" />
          <el-option label="2 人" :value="2" />
          <el-option label="3 人" :value="3" />
        </el-select>
      </div>

      <!-- 排名表格 -->
      <RankTable
        :teams="currentTeams"
        @team-click="openTeamDetail"
        @school-click="goSchool"
        @player-click="goPlayer"
      />
    </div>

    <!-- 学校统计 Tab -->
    <div v-if="activeTab === 'schools'">
      <SchoolStats :stats="schoolStats" @school-click="goSchool" />
    </div>

    <!-- 队伍详情弹窗 -->
    <TeamDetail
      v-model:visible="showTeamDetail"
      :team="selectedTeam"
      :contest-name="contest.name"
    />
  </div>
</template>
