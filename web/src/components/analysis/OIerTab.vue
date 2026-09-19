<script setup>
import { ref, computed } from 'vue'
import AnalysisChart from './AnalysisChart.vue'
import {
  computeOIerStats, computeOIAwardStats,
  MEDAL_ORDER, MEDAL_LABELS, MEDAL_COLORS, fmtPct,
} from '../../utils/analysis'

const props = defineProps({
  dataset: { type: Object, required: true },
})

const stats = computed(() => computeOIerStats(props.dataset))

// 最高 OI 奖项分布：赛区选择（null = 全部）
const awardRegion = ref(null)
const regionOptions = computed(() => {
  const seen = new Map()
  for (const t of props.dataset.teams) {
    if (!seen.has(t.regionId)) seen.set(t.regionId, t.regionName)
  }
  return [...seen.entries()].map(([id, name]) => ({ id, name }))
})
const awardStats = computed(() => computeOIAwardStats(props.dataset, awardRegion.value))

// 各奖牌档选手中 OIer 占比
const playerRateOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params) => {
      const tier = MEDAL_ORDER[params[0].dataIndex]
      const s = stats.value.playerTiers[tier]
      return `${MEDAL_LABELS[tier]}选手<br/>OIer：${s.oier} / ${s.total}（${fmtPct(s.rate)}）`
    },
  },
  grid: { left: 50, right: 20, top: 30, bottom: 30 },
  xAxis: {
    type: 'category',
    data: MEDAL_ORDER.map(t => MEDAL_LABELS[t]),
    axisLabel: { interval: 0 },
  },
  yAxis: { type: 'value', name: 'OIer 占比', axisLabel: { formatter: '{value}%' }, max: 100 },
  series: [{
    type: 'bar',
    data: MEDAL_ORDER.map(t => {
      const s = stats.value.playerTiers[t]
      return { value: Number((s.rate * 100).toFixed(1)), itemStyle: { color: MEDAL_COLORS[t] } }
    }),
    label: { show: true, position: 'top', formatter: ({ value }) => value + '%' },
    barMaxWidth: 60,
  }],
}))

// 各奖牌档队伍的 OIer 人数构成（堆叠百分比）
const oiColors = ['#dcdfe6', '#a0cfff', '#409eff', '#1d6fd8']
const teamCompOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params) => {
      const tier = MEDAL_ORDER[params[0].dataIndex]
      const s = stats.value.teamTiers[tier]
      const lines = params.map(p => `${p.marker}${p.seriesName}：${s.counts[p.seriesIndex]} 队（${p.value}%）`)
      return `${MEDAL_LABELS[tier]}队伍（共 ${s.total} 队）<br/>` + lines.join('<br/>')
    },
  },
  legend: { top: 0 },
  grid: { left: 50, right: 20, top: 36, bottom: 30 },
  xAxis: {
    type: 'category',
    data: MEDAL_ORDER.map(t => MEDAL_LABELS[t]),
    axisLabel: { interval: 0 },
  },
  yAxis: { type: 'value', name: '队伍占比', axisLabel: { formatter: '{value}%' }, max: 100 },
  series: [0, 1, 2, 3].map(n => ({
    name: `${n} 名 OIer`,
    type: 'bar',
    stack: 'total',
    barMaxWidth: 60,
    itemStyle: { color: oiColors[n] },
    data: MEDAL_ORDER.map(t => {
      const s = stats.value.teamTiers[t]
      return s.total ? Number((s.counts[n] / s.total * 100).toFixed(1)) : 0
    }),
  })),
}))

// 金牌选手最高 OI 奖项分布（横向柱，按等级排序）
const awardOption = computed(() => {
  const items = awardStats.value.items
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const p = params[0]
        const d = items[p.dataIndex]
        return `${d.label}<br/>人数：${d.count}（${fmtPct(d.count / Math.max(awardStats.value.withOi, 1))}，占有 OI 记录者）`
      },
    },
    grid: { left: 110, right: 40, top: 10, bottom: 30 },
    xAxis: { type: 'value', name: '人数' },
    yAxis: {
      type: 'category',
      inverse: true,
      data: items.map(d => d.label),
      axisLabel: { width: 100, overflow: 'truncate' },
    },
    series: [{
      type: 'bar',
      barMaxWidth: 18,
      itemStyle: { color: '#409eff', borderRadius: [0, 4, 4, 0] },
      data: items.map(d => d.count),
    }],
  }
})
</script>

<template>
  <div>
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <h3 class="text-base font-semibold text-gray-800 mb-1">各奖牌档选手的 OIer 占比</h3>
        <p class="text-xs text-gray-400 mb-2">选手按 学校+姓名 跨赛区去重，取当年最高奖牌；OIer 指有 OI 获奖记录的选手</p>
        <AnalysisChart :option="playerRateOption" />
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <h3 class="text-base font-semibold text-gray-800 mb-1">各奖牌档队伍的 OIer 人数构成</h3>
        <p class="text-xs text-gray-400 mb-2">按队伍内 OIer 人数（0~3 名）统计队伍占比；2 人队按实际人数归入对应档</p>
        <AnalysisChart :option="teamCompOption" />
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 mt-4">
      <div class="flex flex-wrap items-center gap-3 mb-1">
        <h3 class="text-base font-semibold text-gray-800">金牌选手的最高 OI 奖项分布</h3>
        <el-select
          v-model="awardRegion"
          placeholder="全部赛区"
          clearable
          size="small"
          class="w-44"
        >
          <el-option v-for="r in regionOptions" :key="r.id" :label="r.name" :value="r.id" />
        </el-select>
      </div>
      <p class="text-xs text-gray-400 mb-2">
        奖项等级：CSP-J / NOIP普及 &lt; CSP-S / NOIP / 春季测试 / NGOI &lt; WC / APIO &lt; NOI / CTSC 等 &lt; IOI；
        统计 {{ awardStats.total }} 名金牌选手（所选赛区金牌队伍成员，按 学校+姓名 去重），其中 {{ awardStats.withOi }} 人有 OI 记录
      </p>
      <AnalysisChart v-if="awardStats.items.length" :option="awardOption" :height="Math.max(320, awardStats.items.length * 26 + 60) + 'px'" />
      <p v-else class="text-sm text-gray-500 py-8 text-center">该范围内金牌选手均无 OI 记录。</p>
    </div>
  </div>
</template>
