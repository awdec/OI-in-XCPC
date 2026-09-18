<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { loadContestsIndex, loadContestData, loadSchoolTags } from '../utils/dataLoader'

const props = defineProps({
  year: {
    type: String,
    required: true
  }
})

const route = useRoute()
const wait = (ms) => new Promise(r => setTimeout(r, ms))

const rows = ref([])
const loading = ref(true)
const error = ref('')
const loadProgress = ref(0)
const loadTotal = ref(0)
const schoolTags = ref({ set985: new Set(), set211: new Set() })
let loadSeq = 0

const PAGE_SIZE = 20
const currentPage = ref(1)

// 搜索与筛选
const searchSchool = ref('')
const searchTeam = ref('')
const searchMember = ref('')
const filterContest = ref('')
const filterSchoolType = ref('')
const filterOiCount = ref('')
const filterMedal = ref('')

const contestOptions = computed(() => [...new Set(rows.value.map(r => r.contestName))])

const filteredRows = computed(() => {
  let data = rows.value
  const qSchool = searchSchool.value.trim().toLowerCase()
  const qTeam = searchTeam.value.trim().toLowerCase()
  const qMember = searchMember.value.trim().toLowerCase()
  if (filterContest.value) data = data.filter(r => r.contestName === filterContest.value)
  if (qSchool) data = data.filter(r => r.school.toLowerCase().includes(qSchool))
  if (qTeam) data = data.filter(r => r.team.toLowerCase().includes(qTeam))
  if (qMember) data = data.filter(r => r.members.some(m => m.name.toLowerCase().includes(qMember)))
  if (filterSchoolType.value) {
    const { set985, set211 } = schoolTags.value
    if (filterSchoolType.value === '985') data = data.filter(r => set985.has(r.school))
    else if (filterSchoolType.value === '211') data = data.filter(r => set211.has(r.school) && !set985.has(r.school))
    else if (filterSchoolType.value === 'other') data = data.filter(r => !set211.has(r.school) && !set985.has(r.school))
  }
  if (filterOiCount.value !== '' && filterOiCount.value != null) {
    const n = Number(filterOiCount.value)
    data = data.filter(r => r.members.filter(m => m.oi?.length).length === n)
  }
  if (filterMedal.value) {
    data = data.filter(r => {
      if (!r.medal) return filterMedal.value === 'other'
      const m = r.medal.toLowerCase()
      if (filterMedal.value === 'gold') return m.includes('gold')
      if (filterMedal.value === 'silver') return m.includes('silver')
      if (filterMedal.value === 'bronze') return m.includes('bronze')
      if (filterMedal.value === 'other') return !m.includes('gold') && !m.includes('silver') && !m.includes('bronze')
      return true
    })
  }
  return data
})

// 筛选条件变化时回到第 1 页
watch([filterContest, searchSchool, searchTeam, searchMember, filterSchoolType, filterOiCount, filterMedal], () => {
  currentPage.value = 1
})

// 页码按钮：当前页 ± 二进制偏移（1, 2, 4, 8, 16），不越界
const totalPages = computed(() => Math.ceil(filteredRows.value.length / PAGE_SIZE))
const pageButtons = computed(() => {
  const cur = currentPage.value
  const total = totalPages.value
  const set = new Set([cur])
  for (let step = 1; step <= 16; step *= 2) {
    if (cur - step >= 1) set.add(cur - step)
    if (cur + step <= total) set.add(cur + step)
  }
  return [...set].sort((a, b) => a - b)
})
const currentRows = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredRows.value.slice(start, start + PAGE_SIZE)
})
const goToPage = (page) => {
  currentPage.value = page
}

const medalOrder = (medal) => {
  if (!medal) return 3
  const m = medal.toLowerCase()
  if (m.includes('gold')) return 0
  if (m.includes('silver')) return 1
  if (m.includes('bronze')) return 2
  return 3
}

const medalLabel = (medal) => {
  if (!medal) return '-'
  const m = medal.toLowerCase()
  if (m.includes('gold')) return '🥇 金牌'
  if (m.includes('silver')) return '🥈 银牌'
  if (m.includes('bronze')) return '🥉 铜牌'
  return medal
}

const medalClass = (medal) => {
  if (!medal) return ''
  const m = medal.toLowerCase()
  if (m.includes('gold')) return 'text-yellow-600 font-semibold'
  if (m.includes('silver')) return 'text-gray-500 font-semibold'
  if (m.includes('bronze')) return 'text-amber-700 font-semibold'
  return ''
}

const loadData = async (year) => {
  const seq = ++loadSeq
  loading.value = true
  error.value = ''
  loadProgress.value = 0
  rows.value = []

  try {
    schoolTags.value = await loadSchoolTags()
    const index = await loadContestsIndex(year)
    if (seq !== loadSeq) return
    loadTotal.value = index.length
    const allData = []
    for (const c of index) {
      allData.push(await loadContestData(year, c.id))
      if (seq !== loadSeq) return
      loadProgress.value++
      await nextTick()
      await wait(120)
    }
    if (seq !== loadSeq) return
    const result = []
    for (const contest of allData) {
      const teams = (contest.sheets['正式队伍'] || [])
        .slice()
        .sort((a, b) => medalOrder(a.medal) - medalOrder(b.medal) || (a.rank || 9999) - (b.rank || 9999))
      for (const t of teams) {
        result.push({
          contestName: contest.name,
          rank: t.rank,
          school: t.school,
          team: t.team,
          members: t.members || [],
          medal: t.medal,
          medalOrder: medalOrder(t.medal),
        })
      }
    }
    rows.value = result
  } catch (e) {
    if (seq !== loadSeq) return
    console.error('加载汇总数据失败:', e)
    rows.value = []
    error.value = '数据加载失败，请稍后重试'
  } finally {
    if (seq === loadSeq) loading.value = false
  }
}

onMounted(() => loadData(props.year))
watch(() => props.year, (newYear) => {
  if (newYear) loadData(newYear)
})
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ year }} 年全部成绩汇总</h2>

    <div v-if="loading" class="flex flex-col items-center py-20">
      <el-progress
        :percentage="loadTotal ? Math.round(loadProgress / loadTotal * 100) : 0"
        :stroke-width="10"
        style="width: 360px"
      />
      <p class="text-gray-500 mt-3 text-sm">正在加载比赛数据（{{ loadProgress }} / {{ loadTotal }}）</p>
    </div>

    <div v-else-if="error" class="flex justify-center py-20">
      <el-result icon="warning" title="加载失败" :sub-title="error" />
    </div>

    <!-- 搜索 + 筛选 -->
    <div v-if="!loading && !error" class="mb-4">
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
        <span class="text-sm text-gray-400">共 {{ filteredRows.length }} 条记录</span>
      </div>
      <div class="flex items-center gap-3">
        <div class="w-48 shrink-0">
          <el-select v-model="filterContest" placeholder="比赛" clearable>
            <el-option v-for="name in contestOptions" :key="name" :label="name" :value="name" />
          </el-select>
        </div>
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
        <div class="w-28 shrink-0">
          <el-select v-model="filterMedal" placeholder="奖项" clearable>
            <el-option label="🥇 金牌" value="gold" />
            <el-option label="🥈 银牌" value="silver" />
            <el-option label="🥉 铜牌" value="bronze" />
            <el-option label="其他" value="other" />
          </el-select>
        </div>
      </div>
    </div>

    <el-table
      v-if="!loading && !error"
      :data="currentRows"
      stripe
      border
      :row-class-name="({ row }) => medalClass(row.medal)"
    >
      <el-table-column prop="contestName" label="比赛名" min-width="180" fixed />
      <el-table-column prop="rank" label="排名" width="80" align="center" />
      <el-table-column label="学校" min-width="180">
        <template #default="{ row }">
          <router-link :to="`/${year}/school/${encodeURIComponent(row.school)}`" class="text-blue-600 hover:underline">
            {{ row.school }}
          </router-link>
          <el-tag v-if="schoolTags.set985.has(row.school)" size="small" type="danger" disable-transitions class="ml-1">985</el-tag>
          <el-tag v-else-if="schoolTags.set211.has(row.school)" size="small" type="warning" disable-transitions class="ml-1">211</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="team" label="队伍名" min-width="180" />
      <el-table-column label="选手 1" min-width="120">
        <template #default="{ row }">
          <el-tooltip v-if="row.members[0]" placement="top" :show-after="300" :disabled="!row.members[0].oi?.length">
            <template #content>
              <div class="max-w-xs">
                <div v-for="(r, j) in row.members[0].oi" :key="j" class="text-xs py-0.5">
                  {{ r['比赛'] }} · {{ r['奖项'] }}
                </div>
              </div>
            </template>
            <span class="inline-flex items-center">
              <router-link
                :to="`/${year}/player/${encodeURIComponent(row.members[0].name)}`"
                class="text-gray-700 hover:text-blue-600 hover:underline"
              >{{ row.members[0].name }}</router-link>
              <span v-if="row.members[0].oi?.length" class="ml-0.5">☀️</span>
            </span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column label="选手 2" min-width="120">
        <template #default="{ row }">
          <el-tooltip v-if="row.members[1]" placement="top" :show-after="300" :disabled="!row.members[1].oi?.length">
            <template #content>
              <div class="max-w-xs">
                <div v-for="(r, j) in row.members[1].oi" :key="j" class="text-xs py-0.5">
                  {{ r['比赛'] }} · {{ r['奖项'] }}
                </div>
              </div>
            </template>
            <span class="inline-flex items-center">
              <router-link
                :to="`/${year}/player/${encodeURIComponent(row.members[1].name)}`"
                class="text-gray-700 hover:text-blue-600 hover:underline"
              >{{ row.members[1].name }}</router-link>
              <span v-if="row.members[1].oi?.length" class="ml-0.5">☀️</span>
            </span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column label="选手 3" min-width="120">
        <template #default="{ row }">
          <el-tooltip v-if="row.members[2]" placement="top" :show-after="300" :disabled="!row.members[2].oi?.length">
            <template #content>
              <div class="max-w-xs">
                <div v-for="(r, j) in row.members[2].oi" :key="j" class="text-xs py-0.5">
                  {{ r['比赛'] }} · {{ r['奖项'] }}
                </div>
              </div>
            </template>
            <span class="inline-flex items-center">
              <router-link
                :to="`/${year}/player/${encodeURIComponent(row.members[2].name)}`"
                class="text-gray-700 hover:text-blue-600 hover:underline"
              >{{ row.members[2].name }}</router-link>
              <span v-if="row.members[2].oi?.length" class="ml-0.5">☀️</span>
            </span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column label="奖项" width="100" align="center">
        <template #default="{ row }">
          <span :class="medalClass(row.medal)">{{ medalLabel(row.medal) }}</span>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div v-if="!loading && !error && filteredRows.length" class="flex items-center justify-center gap-2 mt-4 flex-wrap">
      <span class="text-sm text-gray-500 mr-2">每页 {{ PAGE_SIZE }} 条，共 {{ filteredRows.length }} 条，{{ totalPages }} 页</span>
      <button
        v-for="page in pageButtons"
        :key="page"
        @click="goToPage(page)"
        class="px-3 py-1.5 rounded text-sm font-medium border transition-colors"
        :class="currentPage === page
          ? 'bg-blue-600 text-white border-blue-600'
          : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>
