<script setup>
import { computed } from 'vue'
import { formatSubmission, problemClass, medalText, medalClass } from '../utils/formatters'

const props = defineProps({
  visible: Boolean,
  team: Object,
  contestName: String,
})
const emit = defineEmits(['update:visible'])

const problems = computed(() => {
  if (!props.team?.problems) return []
  return Object.entries(props.team.problems).map(([letter, p]) => ({
    letter,
    ...p,
    display: formatSubmission(p),
    cssClass: problemClass(p),
  }))
})
</script>

<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="emit('update:visible', $event)"
    :title="team ? `${team.school} — ${team.team}` : ''"
    width="600px"
    destroy-on-close
  >
    <div v-if="team">
      <!-- 基本信息 -->
      <div class="grid grid-cols-3 gap-4 mb-5">
        <div>
          <div class="text-xs text-gray-400">排名</div>
          <div class="text-xl font-bold text-gray-800">#{{ team.rank }}</div>
        </div>
        <div>
          <div class="text-xs text-gray-400">解题数</div>
          <div class="text-xl font-bold text-blue-600">{{ team.solved }}</div>
        </div>
        <div>
          <div class="text-xs text-gray-400">罚时</div>
          <div class="text-xl font-bold text-gray-600">{{ team.penalty }}</div>
        </div>
      </div>

      <div class="flex gap-2 mb-4">
        <el-tag v-if="team.medal" :class="medalClass(team.medal)">{{ medalText(team.medal) }}</el-tag>
        <el-tag v-if="team.unofficial" type="warning">打星队伍</el-tag>
        <el-tag v-if="team.girl" type="danger">女队</el-tag>
      </div>

      <!-- 题目状态 -->
      <div class="mb-5">
        <div class="text-sm font-medium text-gray-700 mb-2">题目状态</div>
        <div class="flex flex-wrap gap-2">
          <div v-for="p in problems" :key="p.letter" class="text-center">
            <div class="text-xs text-gray-400 mb-1">{{ p.letter }}</div>
            <div
              class="w-16 py-1.5 rounded text-sm font-medium"
              :class="p.cssClass"
            >
              {{ p.display }}
            </div>
            <div v-if="p.status === 'solved'" class="text-xs text-gray-400 mt-1">
              {{ p.time }}min / {{ p.attempts }}次
            </div>
          </div>
        </div>
      </div>

      <!-- 队员 -->
      <div>
        <div class="text-sm font-medium text-gray-700 mb-2">队员</div>
        <div class="flex flex-wrap gap-2">
          <el-tag v-for="m in team.members" :key="m.name" type="info">{{ m.name }}</el-tag>
        </div>
        <div v-if="team.coaches?.length" class="mt-2">
          <div class="text-sm text-gray-500">教练: {{ team.coaches.join(', ') }}</div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>
