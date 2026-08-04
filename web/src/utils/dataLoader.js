/**
 * 数据加载与缓存模块
 */

const cache = {}

/**
 * 加载赛区索引
 */
export async function loadContestsIndex() {
  if (cache._index) return cache._index
  const res = await fetch('./data/contests.json')
  cache._index = await res.json()
  return cache._index
}

/**
 * 加载单个赛区数据
 */
export async function loadContestData(contestId) {
  if (cache[contestId]) return cache[contestId]
  const res = await fetch(`./data/${contestId}.json`)
  cache[contestId] = await res.json()
  return cache[contestId]
}

/**
 * 加载所有赛区数据（用于跨赛区搜索/对比）
 */
export async function loadAllContests() {
  const index = await loadContestsIndex()
  const all = await Promise.all(index.map(c => loadContestData(c.id)))
  return all
}

/**
 * 加载 OI 奖项记录
 */
export async function loadOIRecords() {
  if (cache._oi) return cache._oi
  const res = await fetch('./data/oi_records.json')
  cache._oi = await res.json()
  return cache._oi
}

/**
 * 加载 985/211 学校名单
 */
export async function loadSchoolTags() {
  if (cache._tags) return cache._tags
  const [r985, r211] = await Promise.all([fetch('./data/985.json'), fetch('./data/211.json')])
  const [d985, d211] = await Promise.all([r985.json(), r211.json()])
  cache._tags = { set985: new Set(d985), set211: new Set(d211) }
  return cache._tags
}
