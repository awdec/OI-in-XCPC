<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { HeatmapChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, VisualMapComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([HeatmapChart, GridComponent, TooltipComponent, VisualMapComponent, CanvasRenderer])

const props = defineProps({
  contest: Object,
})

const letters = 'ABCDEFGHIJKLM'.split('')

const heatmapData = computed(() => {
  if (!props.contest) return { data: [], sheets: [] }

  const sheetNames = Object.keys(props.contest.sheets)
  const data = []

  sheetNames.forEach((sheet, yi) => {
    const teams = props.contest.sheets[sheet] || []
    if (!teams.length) return

    letters.forEach((letter, xi) => {
      if (!teams[0].problems?.[letter]) return
      let solved = 0, total = 0
      teams.forEach(t => {
        const p = t.problems[letter]
        if (p && p.status !== 'none') {
          total++
          if (p.status === 'solved') solved++
        }
      })
      const rate = total > 0 ? Math.round((solved / total) * 100) : 0
      data.push([xi, yi, rate])
    })
  })

  return { data, sheets: sheetNames }
})

const option = computed(() => ({
  tooltip: {
    formatter: (p) => {
      const [x, y, val] = p.data
      return `题目 ${letters[x]}<br/>分页: ${heatmapData.value.sheets[y]}<br/>通过率: ${val}%`
    }
  },
  grid: { left: 80, right: 40, top: 20, bottom: 60 },
  xAxis: {
    type: 'category',
    data: letters,
    name: '题目',
  },
  yAxis: {
    type: 'category',
    data: heatmapData.value.sheets,
  },
  visualMap: {
    min: 0,
    max: 100,
    calculable: true,
    orient: 'horizontal',
    left: 'center',
    bottom: 0,
    inRange: { color: ['#f56c6c', '#e6a23c', '#67c23a'] },
    text: ['高', '低'],
  },
  series: [{
    type: 'heatmap',
    data: heatmapData.value.data,
    label: { show: true, formatter: (p) => `${p.data[2]}%`, fontSize: 11 },
    emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.5)' } },
  }],
}))
</script>

<template>
  <div class="bg-white rounded-lg p-4 shadow-sm">
    <h3 class="text-lg font-semibold text-gray-800 mb-3">题目通过率热力图</h3>
    <v-chart :option="option" style="height: 300px" autoresize />
  </div>
</template>
