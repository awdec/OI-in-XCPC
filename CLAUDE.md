# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ICPC/CCPC contest results visualization platform supporting multiple years (2020-2024). Static SPA with no backend — all data is pre-processed from xlsx files into JSON.

## Commands

### Frontend (run from `web/`)
```bash
npm run dev       # Vite dev server on localhost:11451
npm run build     # Production build to web/dist/
npm run preview   # Preview production build
```

### Data Pipeline (run from project root)
Requires Python 3 with `openpyxl` and `pandas`.
```bash
python scripts/convert_xlsx.py         # xlsx → JSON in web/public/data/{year}/
python scripts/extract_players.py      # xlsx → players.json (unique school+name pairs)
python scripts/extract_oi_records.py   # matches raw.txt OI records to players → web/public/data/{year}/oi_records.json
```

`convert_xlsx.py` is the main pipeline — it reads each xlsx file's "正式队伍" sheet and outputs per-contest JSON plus a `contests.json` index. Run it after adding or updating xlsx source files.

## Architecture

### Frontend (`web/src/`)
- **Vue 3 Composition API** (`<script setup>`) + **Vite** + **Element Plus** (Chinese locale) + **ECharts** (tree-shaken via `use()`) + **Tailwind CSS 4**
- **Hash-based routing** (`createWebHashHistory`):
  - `/` → Home (year selection)
  - `/:year/` → YearHome (contest list for that year)
  - `/:year/contest/:id` → Contest detail
  - `/:year/summary` → Summary
  - `/:year/school/:name` → School detail
  - `/:year/player/:name` → Player detail
  - `/announcement` → Announcement (global)
- Views are **lazy-loaded** via dynamic `import()` in `web/src/main.js`
- **No backend/API** — `web/src/utils/dataLoader.js` fetches static JSON from `web/public/data/` with in-memory caching
- `web/src/utils/formatters.js` contains submission parsing (`+1(170)` → solved, 2 attempts, 170 min), medal display, and school aggregation logic

### Data Model (per-contest JSON)
```
{ id, org, city_cn, name, sheets: { "正式队伍": [
  { rank, school, team, solved, penalty,
    problems: { A: { status, attempts, time }, ... },
    members: [{ name, oi: [...] }],
    unofficial, girl, medal, icpc_id }
] } }
```

### Data Pipeline (`scripts/`)
1. `convert_xlsx.py` — primary: xlsx → contest JSON files (supports multiple years)
2. `extract_players.py` — secondary: extracts unique (school, name) pairs across all years
3. `extract_oi_records.py` — enrichment: matches OI competition history from `raw.txt` to XCPC players per year, calculates expected college year based on high school grade at competition time

### Key Data Files
- `web/public/data/years.json` — available years index
- `web/public/data/{year}/contests.json` — contest index per year
- `web/public/data/{year}/{contest_id}.json` — per-contest team data
- `web/public/data/{year}/oi_records.json` — OI history per player per year
- `web/public/data/985.json` / `211.json` — university tier lists (global)
- `raw.txt` — source OI records (root level, not served to frontend)
- `xcpc/{year}/*.xlsx` — source contest result files

## Conventions

- All UI text is in **Chinese** — keep labels, tooltips, and column headers consistent
- Element Plus is imported globally in `main.js` with Chinese locale (`zhCn`)
- Charts use ECharts with explicit component registration for tree-shaking
- No TypeScript, no ESLint, no test framework configured
- `v-model:visible` pattern for dialog visibility in components (e.g., `TeamDetail`)
- **Navigation links** must use `<router-link :to="...">` instead of `@click="router.push(...)"` to support Ctrl+click / middle-click to open in new tab. Only use `@click` for non-link interactions (e.g., opening dialogs, `router.back()`)
