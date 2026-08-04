<script setup>
import { ref, onMounted } from 'vue'
import { loadSchoolTags } from '../utils/dataLoader'

const props = defineProps({
  teams: { type: Array, required: true },
})

const emit = defineEmits(['teamClick', 'schoolClick', 'playerClick'])

const tags = ref({ set985: new Set(), set211: new Set() })
onMounted(async () => { tags.value = await loadSchoolTags() })

const rowMedalClass = ({ row }) => {
  if (!row.medal) return ''
  const m = row.medal.toLowerCase()
  if (m.includes('gold')) return 'row-medal-gold'
  if (m.includes('silver')) return 'row-medal-silver'
  if (m.includes('bronze')) return 'row-medal-bronze'
  return ''
}
</script>

<template>
  <el-table
    :data="teams"
    stripe
    border
    size="small"
    max-height="70vh"
    :row-class-name="rowMedalClass"
  >
    <el-table-column prop="rank" label="排名" width="70" align="center" fixed />
    <el-table-column prop="org_rank" label="校内" width="60" align="center" />

    <el-table-column label="学校" min-width="160" show-overflow-tooltip>
      <template #default="{ row }">
        <span class="text-blue-600 cursor-pointer hover:underline" @click.stop="emit('schoolClick', row.school)">
          {{ row.school }}
        </span>
        <el-tag v-if="tags.set985.has(row.school)" size="small" type="danger" class="ml-1">985</el-tag>
        <el-tag v-if="tags.set211.has(row.school)" size="small" type="warning" class="ml-1">211</el-tag>
      </template>
    </el-table-column>

    <el-table-column label="队伍" min-width="130" show-overflow-tooltip>
      <template #default="{ row }">
        <span class="cursor-pointer hover:text-blue-600" @click.stop="emit('teamClick', row)">
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
            <span
              class="text-gray-700 cursor-pointer hover:text-blue-600 hover:underline"
              @click.stop="emit('playerClick', row.members[0].name)"
            >{{ row.members[0].name }}</span>
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
            <span
              class="text-gray-700 cursor-pointer hover:text-blue-600 hover:underline"
              @click.stop="emit('playerClick', row.members[1].name)"
            >{{ row.members[1].name }}</span>
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
            <span
              class="text-gray-700 cursor-pointer hover:text-blue-600 hover:underline"
              @click.stop="emit('playerClick', row.members[2].name)"
            >{{ row.members[2].name }}</span>
            <span v-if="row.members[2].oi?.length" class="ml-0.5">☀️</span>
          </span>
        </el-tooltip>
      </template>
    </el-table-column>
  </el-table>
</template>
