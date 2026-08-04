<script setup>
import { ref, onMounted, computed } from 'vue'
import { loadContestsIndex, loadContestData } from '../utils/dataLoader'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const contestsIndex = ref([])
const selectedIds = ref([])
const compareData = ref([])
const loading = ref(false)

onMounted(async () => {
  contestsIndex.value = await loadContestsIndex()
})

const loadCompare = async () => {
  if (!selectedIds.value.length) return
  loading.value = true
  const data = await Promise.all(selectedIds.value.map(id => loadContestData(id)))
  compareData.value = data.map(c => {
    const formal = c.sheets['正式队伍'] || []
    const totalSolved = formal.reduce((s, t) => s + t.solved, 0)
    const avgSolved = formal.length > 0 ? (totalSolved / formal.length).toFixed(2) : 0
    const maxSolved = Math.max(...formal.map(t => t.solved))
    return {
      name: c.name,
      id: c.id,
      teams: formal.length,
      totalSolved,
      avgSolved: Number(avgSolved),
      maxSolved,
    }
  })
  loading.value = false
}

const teamsChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 100, right: 30, top: 20, bottom: 30 },
  xAxis: { type: 'value', name: '队伍数' },
  yAxis: { type: 'category', data: compareData.value.map(d => d.name) },
  series: [{
    type: 'bar',
    data: compareData.value.map(d => d.teams),
    itemStyle: { color: '#409eff', borderRadius: [0, 4, 4, 0] },
  }],
}))

const avgChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 100, right: 30, top: 20, bottom: 30 },
  xAxis: { type: 'value', name: '平均解题数' },
  yAxis: { type: 'category', data: compareData.value.map(d => d.name) },
  series: [{
    type: 'bar',
    data: compareData.value.map(d => d.avgSolved),
    itemStyle: { color: '#67c23a', borderRadius: [0, 4, 4, 0] },
  }],
}))
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-6">跨赛区对比</h2>

    <div class="bg-white rounded-lg p-5 shadow-sm mb-6">
      <div class="text-sm text-gray-600 mb-3">选择要对比的赛区（可多选）</div>
      <el-checkbox-group v-model="selectedIds" class="flex flex-wrap gap-2 mb-4">
        <el-checkbox-button v-for="c in contestsIndex" :key="c.id" :value="c.id">
          {{ c.name }}
        </el-checkbox-button>
      </el-checkbox-group>
      <el-button type="primary" :disabled="!selectedIds.length" @click="loadCompare">
        对比 {{ selectedIds.length }} 个赛区
      </el-button>
    </div>

    <div v-if="loading" class="flex justify-center py-10">
      <el-icon class="is-loading text-3xl text-blue-500"><Loading /></el-icon>
    </div>

    <div v-if="compareData.length && !loading">
      <!-- 对比表格 -->
      <el-table :data="compareData" stripe border class="mb-6">
        <el-table-column prop="name" label="赛区" min-width="160" />
        <el-table-column prop="teams" label="正式队伍数" width="120" align="center" />
        <el-table-column prop="maxSolved" label="最高解题数" width="120" align="center" />
        <el-table-column prop="avgSolved" label="平均解题数" width="120" align="center" />
        <el-table-column prop="totalSolved" label="总解题数" width="120" align="center" />
      </el-table>

      <!-- 图表 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg p-4 shadow-sm">
          <h3 class="text-base font-semibold text-gray-700 mb-2">参赛队伍数对比</h3>
          <v-chart :option="teamsChartOption" style="height: 300px" autoresize />
        </div>
        <div class="bg-white rounded-lg p-4 shadow-sm">
          <h3 class="text-base font-semibold text-gray-700 mb-2">平均解题数对比</h3>
          <v-chart :option="avgChartOption" style="height: 300px" autoresize />
        </div>
      </div>
    </div>
  </div>
</template>
