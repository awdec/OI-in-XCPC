#!/usr/bin/env python3
"""
为 players.json 中的每个选手，从 raw.txt 中提取有效 OI 奖项记录。
规则：根据比赛时的年级推算 2025H2 是否在大一~大五范围内。
输出：根目录 oi_records.json
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw.txt"
PLAYERS = ROOT / "players.json"
OUTPUT = ROOT / "oi_records.json"


def parse_grade(grade_str):
    """解析年级，返回学制编号（高一=10, 高二=11, 高三=12, 初三=9, 初二=8, 初一=7）。"""
    grade_str = grade_str.strip()
    if not grade_str:
        return None
    cn_map = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6}
    # 高中: 高一~高三
    if '高' in grade_str:
        for ch, num in cn_map.items():
            if ch in grade_str:
                return num + 9
        if grade_str.isdigit() and 9 <= int(grade_str) <= 12:
            return int(grade_str)
    # 初中: 初一~初四
    if '初' in grade_str:
        for ch, num in cn_map.items():
            if ch in grade_str:
                return num + 6  # 初一=7, 初二=8, 初三=9, 初四=10
    # 数字年级: 七~九年级
    grade_map = {'七': 7, '八': 8, '九': 9}
    for ch, num in grade_map.items():
        if ch in grade_str:
            return num
    # 阿拉伯数字（6~9 可能是初中）
    if grade_str.isdigit():
        v = int(grade_str)
        if 7 <= v <= 12:
            return v
    return None


def is_spring_competition(comp_name):
    """判断是否为上半年比赛（WC/APIO/NOI），此时年级尚未升级。"""
    name = comp_name.upper()
    return name.startswith('WC') or name.startswith('APIO') or name.startswith('NOI')


def calc_college_year_in_2025(comp_year, grade_num, comp_name=''):
    """
    根据比赛年份和年级，推算 2025H2 的大学年级。
    毕业年 = comp_year + (12 - grade_num)
    大学年级 = 2025 - 毕业年 + 1

    注意：上半年比赛（WC/APIO/NOI）时年级尚未升级，
    需要 +1 来对齐秋天的年级。
    """
    if is_spring_competition(comp_name):
        grade_num += 1
    grad_year = comp_year + (13 - grade_num)
    college_year = 2025 - grad_year + 1
    return college_year


def main():
    with open(PLAYERS, 'r', encoding='utf-8') as f:
        players = json.load(f)

    records = {}
    with open(RAW, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 5:
                continue
            comp_name = parts[0]
            award = parts[1]
            name = parts[2].strip()
            grade = parts[3]
            school = parts[4].strip()

            grade_num = parse_grade(grade)
            if grade_num is None:
                continue

            year_match = re.search(r'(\d{4})', comp_name)
            if not year_match:
                continue
            comp_year = int(year_match.group(1))

            college_year = calc_college_year_in_2025(comp_year, grade_num, comp_name)
            if not (1 <= college_year <= 5):
                continue

            if name not in records:
                records[name] = []
            records[name].append({
                "比赛": comp_name,
                "奖项": award,
                "学校": school,
                "年级": grade,
            })

    result = {}
    matched = 0
    for school, name in players:
        if name in records:
            key = f"{name}@{school}"
            result[key] = records[name]
            matched += 1

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"选手总数: {len(players)}")
    print(f"有 OI 记录且在大一~大五范围: {matched}")
    print(f"输出: {OUTPUT}")


if __name__ == "__main__":
    main()
