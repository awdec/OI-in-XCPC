#!/usr/bin/env python3
"""
将 2025 ICPC/CCPC xlsx 文件转换为前端可用的 JSON 数据。
输出目录: web/public/data/
"""

import os
import re
import json
import pandas as pd
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "web" / "public" / "data"

# 赛区元数据
CONTEST_META = {
    "xian":       {"org": "ICPC",     "city_cn": "西安",   "name": "ICPC 西安"},
    "chengdu":    {"org": "ICPC",     "city_cn": "成都",   "name": "ICPC 成都"},
    "wuhan":      {"org": "ICPC",     "city_cn": "武汉",   "name": "ICPC 武汉"},
    "nanjing":    {"org": "ICPC",     "city_cn": "南京",   "name": "ICPC 南京"},
    "shenyang":   {"org": "ICPC",     "city_cn": "沈阳",   "name": "ICPC 沈阳"},
    "shanghai":   {"org": "ICPC",     "city_cn": "上海",   "name": "ICPC 上海"},
    "haerbin":    {"org": "CCPC",     "city_cn": "哈尔滨", "name": "CCPC 哈尔滨"},
    "jinan":      {"org": "CCPC",     "city_cn": "济南",   "name": "CCPC 济南"},
    "zhengzhou":  {"org": "CCPC",     "city_cn": "郑州",   "name": "CCPC 郑州"},
    "chongqing":  {"org": "CCPC",     "city_cn": "重庆",   "name": "CCPC 重庆"},
    "hangzhou":   {"org": "EC-Final", "city_cn": "杭州",   "name": "EC-Final 杭州"},
}

# 题号列表
PROBLEM_LETTERS = list("ABCDEFGHIJKLM")


def parse_submission(raw):
    """
    解析提交记录，返回结构化数据。
    格式示例:
      '+1(170)' -> {status: 'solved', attempts: 2, time: 170}
      '-1'      -> {status: 'unsolved', attempts: 1, time: null}
      '-5'      -> {status: 'unsolved', attempts: 5, time: null}
      '-'       -> {status: 'none', attempts: 0, time: null}
    """
    if pd.isna(raw):
        return {"status": "none", "attempts": 0, "time": None}

    raw = str(raw).strip()

    # 通过: +N(M) 表示第N+1次提交正确，用时M分钟
    m = re.match(r'\+(\d+)\((\d+)\)', raw)
    if m:
        return {
            "status": "solved",
            "attempts": int(m.group(1)) + 1,
            "time": int(m.group(2))
        }

    # 未通过但有提交: -N
    m = re.match(r'-(\d+)', raw)
    if m:
        return {
            "status": "unsolved",
            "attempts": int(m.group(1)),
            "time": None
        }

    # 未提交: -
    if raw == '-':
        return {"status": "none", "attempts": 0, "time": None}

    # 数字形式（某些文件可能直接是 -1, -5 等整数）
    try:
        val = int(float(raw))
        if val < 0:
            return {"status": "unsolved", "attempts": abs(val), "time": None}
        elif val == 0:
            return {"status": "none", "attempts": 0, "time": None}
    except (ValueError, TypeError):
        pass

    return {"status": "none", "attempts": 0, "time": None}


def parse_team(row, problem_cols, has_coaches=False, oi_records=None):
    """将一行数据解析为队伍记录。"""
    problems = {}
    for letter in PROBLEM_LETTERS:
        if letter in problem_cols:
            problems[letter] = parse_submission(row[letter])
        else:
            problems[letter] = {"status": "none", "attempts": 0, "time": None}

    school = str(row["Organization"]).strip() if pd.notna(row["Organization"]) else ""
    members = []
    for col in ["Member1", "Member2", "Member3"]:
        if col in row and pd.notna(row[col]):
            name = str(row[col]).strip()
            key = f"{name}@{school}"
            oi = oi_records.get(key, []) if oi_records else []
            members.append({"name": name, "oi": oi})

    coaches = []
    if has_coaches and "Coaches" in row and pd.notna(row["Coaches"]):
        coaches.append(str(row["Coaches"]).strip())

    record = {
        "rank": int(row["Rank"]) if pd.notna(row["Rank"]) else None,
        "org_rank": int(row["Organization Rank"]) if pd.notna(row.get("Organization Rank")) else None,
        "school": school,
        "team": str(row["Team"]).strip() if pd.notna(row["Team"]) else "",
        "solved": int(row["Solved"]) if pd.notna(row["Solved"]) else 0,
        "penalty": int(row["Penalty"]) if pd.notna(row["Penalty"]) else 0,
        "problems": problems,
        "members": members,
        "unofficial": str(row.get("Unofficial", "N")).strip().upper() == "Y",
        "girl": str(row.get("Girl", "N")).strip().upper() == "Y",
        "icpc_id": str(row["ICPC ID"]).strip() if pd.notna(row.get("ICPC ID")) else None,
    }

    if has_coaches:
        record["coaches"] = coaches

    if "Medal" in row and pd.notna(row.get("Medal")):
        record["medal"] = str(row["Medal"]).strip()

    return record


def detect_problem_columns(columns):
    """从列名中识别题目列（A~M）。"""
    return [c for c in columns if c in PROBLEM_LETTERS]


def load_oi_records():
    """加载 OI 奖项记录。"""
    oi_path = ROOT / "oi_records.json"
    if not oi_path.exists():
        print("警告: oi_records.json 不存在，跳过 OI 记录嵌入")
        return {}
    with open(oi_path, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_file(xlsx_path, contest_id, oi_records):
    """转换单个 xlsx 文件为 JSON。"""
    xls = pd.ExcelFile(xlsx_path)
    result = {
        "id": contest_id,
        **CONTEST_META[contest_id],
        "sheets": {}
    }

    for sheet_name in xls.sheet_names:
        if sheet_name != "正式队伍":
            continue
        df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
        if len(df) == 0:
            continue

        problem_cols = detect_problem_columns(df.columns.tolist())
        has_coaches = "Coaches" in df.columns

        teams = []
        for _, row in df.iterrows():
            try:
                team = parse_team(row, problem_cols, has_coaches, oi_records)
                teams.append(team)
            except Exception as e:
                print(f"  警告: 跳过一行 ({sheet_name}): {e}")

        result["sheets"][sheet_name] = teams
        print(f"  {sheet_name}: {len(teams)} 支队伍")

    return result


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    xlsx_files = sorted(ROOT.glob("*.xlsx"))
    if not xlsx_files:
        print("错误: 未找到 xlsx 文件")
        return

    contests_index = []
    oi_records = load_oi_records()

    for xlsx_path in xlsx_files:
        # 从文件名提取赛区 ID
        stem = xlsx_path.stem  # e.g. "2025 ICPC xian"
        parts = stem.split()
        if len(parts) >= 3:
            contest_id = parts[-1].lower()
        else:
            print(f"跳过: {xlsx_path.name} (无法解析赛区)")
            continue

        if contest_id not in CONTEST_META:
            print(f"跳过: {xlsx_path.name} (未知赛区 {contest_id})")
            continue

        print(f"处理: {xlsx_path.name} -> {contest_id}.json")
        data = convert_file(xlsx_path, contest_id, oi_records)

        # 写入单赛区 JSON
        output_path = OUTPUT_DIR / f"{contest_id}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 构建索引
        total_teams = len(data["sheets"].get("所有队伍", []))
        top_team = data["sheets"].get("正式队伍", [{}])[0] if data["sheets"].get("正式队伍") else {}

        contests_index.append({
            "id": contest_id,
            "name": CONTEST_META[contest_id]["name"],
            "org": CONTEST_META[contest_id]["org"],
            "city": CONTEST_META[contest_id]["city_cn"],
            "teams": total_teams,
            "champion": {
                "school": top_team.get("school", ""),
                "team": top_team.get("team", ""),
                "solved": top_team.get("solved", 0),
                "penalty": top_team.get("penalty", 0),
            } if top_team else None
        })

    # 写入索引文件
    index_path = OUTPUT_DIR / "contests.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(contests_index, f, ensure_ascii=False, indent=2)

    # 复制 OI 记录到前端数据目录
    import shutil
    oi_src = ROOT / "oi_records.json"
    if oi_src.exists():
        shutil.copy2(oi_src, OUTPUT_DIR / "oi_records.json")
        print("已同步 oi_records.json")

    print(f"\n完成! 共转换 {len(contests_index)} 个赛区")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
