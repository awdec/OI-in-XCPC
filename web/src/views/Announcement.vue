<script setup>
const announcements = [
  {
    date: '2026-8-5',
    title: '2025 赛季数据已全部更新',
    content: '2025 ICPC/CCPC 赛季全部 11 个赛区的比赛结果已完成录入和校验，包括正式队伍排名、队员信息及 OI 获奖记录。',
  },
  {
    date: '2026-0-4',
    title: '网站功能说明',
    content: '本平台收录了 2025 赛季 ICPC/CCPC 各赛区的比赛结果。您可以通过首页查看各赛区概况，在"全部成绩"页搜索和筛选所有队伍，并查看选手的 OI 竞赛获奖经历。',
  },
]
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-6">📢 公告</h2>

    <div class="space-y-4">
      <div
        v-for="(item, index) in announcements"
        :key="index"
        class="bg-white rounded-lg shadow-sm border border-gray-100 p-5"
      >
        <div class="flex items-center gap-3 mb-2">
          <span class="text-sm text-gray-400">{{ item.date }}</span>
          <h3 class="text-lg font-semibold text-gray-800">{{ item.title }}</h3>
        </div>
        <p class="text-gray-600 leading-relaxed">{{ item.content }}</p>
      </div>
    </div>
  </div>
</template>
