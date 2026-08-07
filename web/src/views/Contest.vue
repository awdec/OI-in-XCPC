<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'
import { loadContestData, loadSchoolTags } from '../utils/dataLoader'
import { aggregateBySchool } from '../utils/formatters'
import RankTable from '../components/RankTable.vue'
import TeamDetail from '../components/TeamDetail.vue'
import SchoolStats from '../components/SchoolStats.vue'

const props = defineProps({
  year: {
    type: String,
    required: true
  }
})

const route = useRoute()

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
  if (filterOiCount.value !== '' && filterOiCount.value != null) {
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

const loadContest = async (year, id) => {
  loading.value = true
  contest.value = await loadContestData(year, id)
  schoolTags.value = await loadSchoolTags()
  loading.value = false
}

onMounted(() => loadContest(props.year, route.params.id))
watch(() => route.params.id, (id) => { if (id) loadContest(props.year, id) })

const openTeamDetail = (team) => {
  selectedTeam.value = team
  showTeamDetail.value = true
}
</script>

<template>
  <div v-if="loading" class="flex justify-center py-20">
    <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
  </div>

  <div v-else-if="contest">
    <!-- 赛区标题 -->
    <div class="mb-6">
      <div class="flex items-center gap-3 mb-1">
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
      <div class="flex items-center gap-3 mb-3">
        <div class="w-40 shrink-0">
          <el-input v-model="searchSchool" placeholder="搜索学校" clearable />
        </div>
        <div class="w-40 shrink-0">
          <el-input v-model="searchTeam" placeholder="搜索队伍" clearable />
        </div>
        <div class="w-40 shrink-0">
          <el-input v-model="searchMember" placeholder="搜索队员" clearable />
        </div>
        <span class="text-sm text-gray-400">共 {{ currentTeams.length }} 支队伍</span>
      </div>
      <div class="flex items-center gap-3 mb-4">
        <div class="w-32 shrink-0">
          <el-select v-model="filterSchoolType" placeholder="学校类型" clearable>
            <el-option label="985" value="985" />
            <el-option label="211" value="211" />
            <el-option label="其他" value="other" />
          </el-select>
        </div>
        <div class="w-32 shrink-0">
          <el-select v-model="filterOiCount" placeholder="OI 人数" clearable>
            <el-option label="0 人" :value="0" />
            <el-option label="1 人" :value="1" />
            <el-option label="2 人" :value="2" />
            <el-option label="3 人" :value="3" />
          </el-select>
        </div>
      </div>

      <!-- 排名表格 -->
      <RankTable
        :teams="currentTeams"
        :year="year"
        @team-click="openTeamDetail"
      />
    </div>

    <!-- 学校统计 Tab -->
    <div v-if="activeTab === 'schools'">
      <SchoolStats :stats="schoolStats" />
    </div>

    <!-- 队伍详情弹窗 -->
    <TeamDetail
      v-model:visible="showTeamDetail"
      :team="selectedTeam"
      :contest-name="contest.name"
    />
  </div>
</template>
