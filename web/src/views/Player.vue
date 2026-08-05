<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadAllContests, loadOIRecords } from '../utils/dataLoader'

const route = useRoute()
const router = useRouter()

const playerName = computed(() => decodeURIComponent(route.params.name))
const activeView = ref('icpc')
const icpcRecords = ref([])
const oiRecords = ref([])
const loading = ref(true)

const loadData = async () => {
  loading.value = true
  const [contests, oi] = await Promise.all([loadAllContests(), loadOIRecords()])

  // ICPC/CCPC 记录
  const results = []
  contests.forEach(c => {
    const teams = c.sheets['正式队伍'] || []
    teams.forEach(t => {
      if (t.members.some(m => m.name === playerName.value)) {
        results.push({
          contest: c.name,
          contestId: c.id,
          school: t.school,
          team: t.team,
          rank: t.rank,
          solved: t.solved,
          penalty: t.penalty,
          medal: t.medal,
        })
      }
    })
  })
  icpcRecords.value = results.sort((a, b) => (a.rank || 999) - (b.rank || 999))

  // OI 记录（按 name@school 的 name 部分匹配，按比赛+奖项去重）
  const name = playerName.value
  const seen = new Set()
  const oiResults = []
  Object.entries(oi).forEach(([key, records]) => {
    if (key.split('@')[0] !== name) return
    records.forEach(r => {
      const dedupKey = `${r['比赛']}|${r['奖项']}`
      if (!seen.has(dedupKey)) {
        seen.add(dedupKey)
        oiResults.push(r)
      }
    })
  })
  oiRecords.value = oiResults

  loading.value = false
}

onMounted(loadData)
watch(() => route.params.name, loadData)
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-20">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-else>
      <h2 class="text-2xl font-bold text-gray-800 mb-4">{{ playerName }}</h2>

      <el-radio-group v-model="activeView" size="default" class="mb-4">
        <el-radio-button value="icpc">ICPC/CCPC ({{ icpcRecords.length }})</el-radio-button>
        <el-radio-button value="oi">OI 奖项 ({{ oiRecords.length }})</el-radio-button>
      </el-radio-group>

      <!-- ICPC/CCPC 记录 -->
      <el-table v-if="activeView === 'icpc'" :data="icpcRecords" stripe border size="small">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column label="赛区" min-width="160">
          <template #default="{ row }">
            <router-link :to="`/contest/${row.contestId}`" class="text-blue-600 hover:underline">
              {{ row.contest }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="学校" min-width="160">
          <template #default="{ row }">
            <router-link :to="`/school/${encodeURIComponent(row.school)}`" class="text-blue-600 hover:underline">
              {{ row.school }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="team" label="队伍" min-width="130" />
        <el-table-column prop="rank" label="排名" width="70" align="center" />
        <el-table-column prop="solved" label="解题" width="65" align="center" />
        <el-table-column prop="penalty" label="罚时" width="75" align="center" />
        <el-table-column label="奖牌" width="80" align="center">
          <template #default="{ row }">
            <span v-if="row.medal" class="text-yellow-600 font-bold">{{ row.medal }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- OI 奖项记录 -->
      <el-table v-if="activeView === 'oi'" :data="oiRecords" stripe border size="small">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="比赛" label="比赛" min-width="160" />
        <el-table-column prop="奖项" label="奖项" min-width="120" />
        <el-table-column prop="年级" label="年级" width="80" align="center" />
        <el-table-column prop="学校" label="学校" min-width="200" />
      </el-table>
    </div>
  </div>
</template>
