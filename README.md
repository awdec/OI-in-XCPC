# 2025 ICPC/CCPC 比赛结果展示平台

展示 2025 赛季 ICPC、CCPC、EC-Final 各赛区比赛结果的前端应用。

## 赛区数据

| 赛区 | 组织方 | 正式队伍数 |
|------|--------|-----------|
| 西安 | ICPC | 399 |
| 成都 | ICPC | 320 |
| 武汉 | ICPC | 446 |
| 南京 | ICPC | 335 |
| 上海 | ICPC | 331 |
| 沈阳 | ICPC | 281 |
| 哈尔滨 | CCPC | 260 |
| 济南 | CCPC | 260 |
| 郑州 | CCPC | 260 |
| 重庆 | CCPC | 260 |
| 杭州 | EC-Final | 280 |

## 功能

- **首页** — 11 个赛区卡片总览，显示冠军信息和队伍数量
- **赛区详情** — 排名表格、分页切换（所有队伍/正式队伍/打星队伍/女队）、搜索过滤
- **队伍详情** — 题目提交状态、队员信息、奖牌
- **学校统计** — 按学校聚合的柱状图和表格
- **题目分析** — 各题通过率热力图
- **选手搜索** — 跨赛区搜索选手参赛记录
- **跨赛区对比** — 选择多个赛区横向对比（队伍数、平均解题数等图表）
- **新标签页打开** — 所有导航链接支持 Ctrl+点击 / 鼠标中键在新标签页打开

## 技术栈

- Vue 3 + Vite
- Element Plus（UI 组件）
- ECharts（图表可视化）
- Vue Router 4（路由，Hash 模式）
- Tailwind CSS 4（样式）

## 快速开始

### 1. 数据预处理

将 xlsx 文件转为 JSON（仅首次或数据更新时需要）：

```bash
pip install openpyxl pandas
python scripts/convert_xlsx.py         # 主脚本：xlsx → 赛区 JSON
python scripts/extract_players.py      # 提取选手列表
python scripts/extract_oi_records.py   # 匹配 OI 记录（需要 raw.txt）
```

输出到 `web/public/data/` 目录。

### 2. 启动前端

```bash
cd web
npm install
npm run dev
```

浏览器打开 http://localhost:5173/

### 3. 生产构建

```bash
cd web
npm run build
```

构建产物在 `web/dist/` 目录，可部署到任意静态服务器。

## 项目结构

```
├── scripts/
│   ├── convert_xlsx.py          # xlsx → JSON 主脚本
│   ├── extract_players.py       # 提取选手列表
│   └── extract_oi_records.py    # 匹配 OI 记录
├── *.xlsx                        # 11 个赛区原始成绩文件
├── raw.txt                       # OI 原始记录（~25MB）
├── CLAUDE.md                     # Claude Code 项目指引
├── web/
│   ├── public/
│   │   ├── data/                 # 预处理后的 JSON 数据
│   │   │   ├── contests.json     # 赛区索引
│   │   │   ├── xian.json         # 各赛区详细数据
│   │   │   ├── oi_records.json   # OI 记录
│   │   │   ├── 985.json / 211.json  # 学校标签
│   │   │   └── ...
│   │   └── favicon.svg           # 网站图标（紫色闪电）
│   ├── src/
│   │   ├── views/                # 页面
│   │   │   ├── Home.vue          # 首页
│   │   │   ├── Contest.vue       # 赛区详情
│   │   │   ├── School.vue        # 学校详情
│   │   │   ├── Player.vue        # 选手详情
│   │   │   └── Compare.vue       # 跨赛区对比
│   │   ├── components/           # 组件
│   │   │   ├── RankTable.vue     # 排名表格
│   │   │   ├── TeamDetail.vue    # 队伍详情弹窗
│   │   │   ├── SchoolStats.vue   # 学校统计图表
│   │   │   └── ProblemHeatmap.vue # 题目热力图
│   │   ├── utils/
│   │   │   ├── dataLoader.js     # 数据加载（带缓存）
│   │   │   └── formatters.js     # 解析/聚合工具
│   │   ├── App.vue               # 根组件（导航栏）
│   │   └── main.js               # 入口（路由 + Element Plus）
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```
