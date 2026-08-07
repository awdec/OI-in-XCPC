# ICPC/CCPC 比赛结果展示平台

支持多年份（2020-2024）的 ICPC、CCPC 各赛区比赛结果前端应用。

## 赛区数据

### 2020 赛季
| 赛区 | 正式队伍数 |
|--------|-----------|
| 昆明  ICPC | 763 |
| 上海  ICPC | 635 |
| 南京  ICPC | 554 |
| 济南  ICPC | 496 |
| 沈阳  ICPC | 269 |
| 绵阳  CCPC | 268 |
| 长春  CCPC | 267 |
| 威海  CCPC | 267 |
| 秦皇岛  CCPC | 243 |

*其他年份数据待补充*

## 功能

- **首页** — 年份选择，显示所有可用年份
- **年份首页** — 该年份所有赛区卡片总览，显示冠军信息和队伍数量
- **赛区详情** — 排名表格、搜索过滤、学校类型筛选、OI 人数筛选
- **全部成绩** — 跨赛区汇总表格，支持搜索学校/队伍/队员，按比赛、学校类型、OI 人数、奖项筛选，二进制偏移分页
- **学校详情** — 某学校在所有赛区的参赛记录，含比赛名、985/211 标签
- **选手详情** — 选手参赛记录与 OI 获奖经历
- **公告** — 静态公告页面
- **队伍详情** — 题目提交状态、队员信息、奖牌
- **OI 标记** — 有 OI 获奖记录的选手显示 ☀️ 标记，悬停查看获奖详情
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
python scripts/convert_xlsx.py         # 主脚本：xlsx → 赛区 JSON（支持多年份）
python scripts/extract_players.py      # 提取选手列表
python scripts/extract_oi_records.py   # 匹配 OI 记录（需要 raw.txt）
```

输出到 `web/public/data/{year}/` 目录。

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

## 部署

项目通过 GitHub Actions 自动部署到 GitHub Pages。每次 push 到 `main` 分支会自动触发构建和部署。

首次部署需在仓库 Settings → Pages → Source 中选择 **GitHub Actions**。

## 项目结构

```
├── scripts/
│   ├── convert_xlsx.py          # xlsx → JSON 主脚本（支持多年份）
│   ├── extract_players.py       # 提取选手列表
│   └── extract_oi_records.py    # 匹配 OI 记录（按年份）
├── xcpc/
│   ├── 2020/                    # 2020 赛季原始成绩文件
│   ├── 2021/                    # 待补充
│   ├── 2022/                    # 待补充
│   ├── 2023/                    # 待补充
│   └── 2024/                    # 待补充
├── raw.txt                       # OI 原始记录（~25MB）
├── CLAUDE.md                     # Claude Code 项目指引
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Pages 自动部署
├── web/
│   ├── public/
│   │   ├── data/                 # 预处理后的 JSON 数据
│   │   │   ├── years.json        # 可用年份索引
│   │   │   ├── 2020/             # 2020 赛季数据
│   │   │   │   ├── contests.json
│   │   │   │   ├── kunming.json
│   │   │   │   ├── oi_records.json
│   │   │   │   └── ...
│   │   │   ├── 985.json          # 学校标签（全局）
│   │   │   └── 211.json
│   │   └── favicon.svg           # 网站图标（紫色闪电）
│   ├── src/
│   │   ├── views/                # 页面
│   │   │   ├── Home.vue          # 首页（年份选择）
│   │   │   ├── YearHome.vue      # 年份首页（赛区列表）
│   │   │   ├── Contest.vue       # 赛区详情
│   │   │   ├── Summary.vue       # 全部成绩汇总
│   │   │   ├── School.vue        # 学校详情
│   │   │   ├── Player.vue        # 选手详情
│   │   │   └── Announcement.vue  # 公告
│   │   ├── components/           # 组件
│   │   │   ├── RankTable.vue     # 排名表格
│   │   │   ├── TeamDetail.vue    # 队伍详情弹窗
│   │   │   ├── SchoolStats.vue   # 学校统计图表
│   │   │   └── ProblemHeatmap.vue # 题目热力图
│   │   ├── utils/
│   │   │   ├── dataLoader.js     # 数据加载（带缓存，支持多年份）
│   │   │   └── formatters.js     # 解析/聚合工具
│   │   ├── App.vue               # 根组件（导航栏）
│   │   └── main.js               # 入口（路由 + Element Plus）
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```
