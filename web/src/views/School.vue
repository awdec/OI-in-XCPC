<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadAllContests, loadSchoolTags } from '../utils/dataLoader'
import TeamDetail from '../components/TeamDetail.vue'

const route = useRoute()
const router = useRouter()

const schoolName = computed(() => decodeURIComponent(route.params.name))
const allTeams = ref([])
const loading = ref(true)
const selectedTeam = ref(null)
const showTeamDetail = ref(false)
const schoolTags = ref({ set985: new Set(), set211: new Set() })

const stats = computed(() => {
  const totalSolved = allTeams.value.reduce((s, t) => s + t.solved, 0)
  const bestRank = Math.min(...allTeams.value.map(t => t.rank || Infinity))
  return { count: allTeams.value.length, totalSolved, bestRank }
})

const loadData = async () => {
  loading.value = true
  schoolTags.value = await loadSchoolTags()
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
    <div v-if="loading" class="flex justify-center py-20">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-else>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ schoolName }}</h2>
      <div class="flex gap-6 text-sm text-gray-500 mb-6">
        <span>参赛队伍: <b class="text-gray-700">{{ stats.count }}</b></span>
        <span>最佳排名: <b class="text-green-600">#{{ stats.bestRank }}</b></span>
      </div>

      <el-table
        :data="allTeams"
        stripe
        border
        size="small"
        max-height="70vh"
        :row-class-name="({ row }) => {
          if (!row.medal) return ''
          const m = row.medal.toLowerCase()
          if (m.includes('gold')) return 'row-medal-gold'
          if (m.includes('silver')) return 'row-medal-silver'
          if (m.includes('bronze')) return 'row-medal-bronze'
          return ''
        }"
      >
        <el-table-column prop="_contest" label="比赛名" min-width="180" fixed />
        <el-table-column prop="rank" label="排名" width="70" align="center" />
        <el-table-column label="学校" min-width="160" show-overflow-tooltip>
          <template #default="{ row }">
            <router-link :to="`/school/${encodeURIComponent(row.school)}`" class="text-blue-600 hover:underline" @click.stop>
              {{ row.school }}
            </router-link>
            <el-tag v-if="schoolTags.set985.has(row.school)" size="small" type="danger" class="ml-1">985</el-tag>
            <el-tag v-else-if="schoolTags.set211.has(row.school)" size="small" type="warning" class="ml-1">211</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="队伍" min-width="130" show-overflow-tooltip>
          <template #default="{ row }">
            <span class="cursor-pointer hover:text-blue-600" @click.stop="selectedTeam = row; showTeamDetail = true">
              {{ row.team }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="选手1" min-width="100">
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
                  :to="`/player/${encodeURIComponent(row.members[0].name)}`"
                  class="text-gray-700 hover:text-blue-600 hover:underline"
                  @click.stop
                >{{ row.members[0].name }}</router-link>
                <span v-if="row.members[0].oi?.length" class="ml-0.5">☀️</span>
              </span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="选手2" min-width="100">
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
                  :to="`/player/${encodeURIComponent(row.members[1].name)}`"
                  class="text-gray-700 hover:text-blue-600 hover:underline"
                  @click.stop
                >{{ row.members[1].name }}</router-link>
                <span v-if="row.members[1].oi?.length" class="ml-0.5">☀️</span>
              </span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="选手3" min-width="100">
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
                  :to="`/player/${encodeURIComponent(row.members[2].name)}`"
                  class="text-gray-700 hover:text-blue-600 hover:underline"
                  @click.stop
                >{{ row.members[2].name }}</router-link>
                <span v-if="row.members[2].oi?.length" class="ml-0.5">☀️</span>
              </span>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <TeamDetail v-model:visible="showTeamDetail" :team="selectedTeam" :contest-name="selectedTeam?._contest" />
    </div>
  </div>
</template>
