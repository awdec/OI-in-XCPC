<script setup>
import { ref, computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent, CanvasRenderer])

const props = defineProps({
  stats: { type: Array, default: () => [] },
})
const emit = defineEmits(['schoolClick'])

const topN = ref(20)
const chartType = ref('bar')

const topStats = computed(() => props.stats.slice(0, topN.value))

const barOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: 160, right: 30, top: 20, bottom: 30 },
  xAxis: { type: 'value', name: '总解题数' },
  yAxis: {
    type: 'category',
    data: topStats.value.map(s => s.school).reverse(),
    axisLabel: { width: 140, overflow: 'truncate' },
  },
  series: [{
    type: 'bar',
    data: topStats.value.map(s => s.totalSolved).reverse(),
    itemStyle: { color: '#409eff', borderRadius: [0, 4, 4, 0] },
  }],
}))

const teamOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: 160, right: 30, top: 20, bottom: 30 },
  xAxis: { type: 'value', name: '队伍数' },
  yAxis: {
    type: 'category',
    data: topStats.value.map(s => s.school).reverse(),
    axisLabel: { width: 140, overflow: 'truncate' },
  },
  series: [{
    type: 'bar',
    data: topStats.value.map(s => s.teams).reverse(),
    itemStyle: { color: '#67c23a', borderRadius: [0, 4, 4, 0] },
  }],
}))
</script>

<template>
  <div>
    <div class="flex items-center gap-4 mb-4">
      <el-radio-group v-model="chartType" size="default">
        <el-radio-button value="bar">按解题数</el-radio-button>
        <el-radio-button value="teams">按队伍数</el-radio-button>
      </el-radio-group>
      <el-select v-model="topN" class="w-32">
        <el-option :value="10" label="Top 10" />
        <el-option :value="20" label="Top 20" />
        <el-option :value="50" label="Top 50" />
      </el-select>
    </div>

    <div class="bg-white rounded-lg p-4 shadow-sm">
      <v-chart
        :option="chartType === 'bar' ? barOption : teamOption"
        style="height: 500px"
        autoresize
      />
    </div>

    <!-- 详细表格 -->
    <div class="mt-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">学校详细数据</h3>
      <el-table :data="topStats" stripe border size="small" max-height="400">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column label="学校" min-width="180">
          <template #default="{ row }">
            <span class="text-blue-600 cursor-pointer hover:underline" @click="emit('schoolClick', row.school)">
              {{ row.school }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="teams" label="队伍数" width="80" align="center" sortable />
        <el-table-column prop="totalSolved" label="总解题数" width="100" align="center" sortable />
        <el-table-column prop="bestRank" label="最佳排名" width="100" align="center" sortable />
        <el-table-column label="最佳队伍" min-width="150" show-overflow-tooltip>
          <template #default="{ row }">{{ row.bestTeam }}</template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
