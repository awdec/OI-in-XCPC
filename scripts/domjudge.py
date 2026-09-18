#!/usr/bin/env python3
"""
DOMjudge 榜单导出格式的解析工具。

区别于 XCPCIO Board 导出（单个"正式队伍"sheet，+1(170) 式提交记录），
DOMjudge 导出的特征是: 无"正式队伍" sheet， Official/Main 等表首行为
'# / R# / S# / Markers / ... / Organization / Name / Team Members / Score / Time',
题目列表头为 'A (386/963)' 式统计, 提交记录为 'AC/1/0:26:17' / 'FB/2/2:19:30' / 'RJ/6' 式。
"""

import re
import pandas as pd

PROBLEM_LETTERS = list("ABCDEFGHIJKLM")

# 表头名 → 含义: '# ' 列含排名与奖牌标注（如 "1 (金奖)"）
PROBLEM_HEADER_RE = re.compile(r"^([A-M])\s*\(\d+/\d+\)$")
SUBMISSION_RE = re.compile(r"^([A-Za-z]+)/(\d+)(?:/(\d+):(\d+):(\d+))?$")
TIME_RE = re.compile(r"^(\d+):(\d+):(\d+)$")

# 中文奖牌 → 前端 medalClass/medalText 匹配的英文值
MEDAL_MAP = {
    "金奖": "Gold", "金牌": "Gold",
    "银奖": "Silver", "银牌": "Silver",
    "铜奖": "Bronze", "铜牌": "Bronze",
    "优胜奖": "Honorable",
    "冠军": "Winner",
}

SOLVED_TOKENS = {"AC", "FB", "OK", "SV"}


def _is_header_domjudge(header_values):
    cols = {str(c).strip() for c in header_values if pd.notna(c)}
    return {"Organization", "Name", "Team Members", "Score"} <= cols


def is_domjudge_format(xls):
    """判断 ExcelFile 是否为 DOMjudge 榜单导出格式（无"正式队伍" sheet）。"""
    if "正式队伍" in xls.sheet_names:
        return False
    for name in ("Official", "Main"):
        if name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=name, header=None, nrows=1)
            return _is_header_domjudge(df.iloc[0])
    return False


def _header_map(df):
    """解析首行表头，返回 (表头名→列号 dict, [(题号, 列号)])。"""
    header = [str(c).strip() if pd.notna(c) else "" for c in df.iloc[0]]
    cols = {}
    for i, h in enumerate(header):
        if h and h not in cols:
            cols[h] = i
    problem_cols = []
    for i, h in enumerate(header):
        m = PROBLEM_HEADER_RE.match(h)
        if m:
            problem_cols.append((m.group(1), i))
    return cols, problem_cols


def _minutes(raw):
    """'22:49:00' → 1369（分钟）；已是数字则原样取整。"""
    s = str(raw).strip()
    m = TIME_RE.match(s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    try:
        return int(float(s))
    except ValueError:
        return 0


def parse_submission(raw):
    """
    解析 DOMjudge 提交记录为项目提交结构。
      'AC/1/0:26:17' → {status: solved, attempts: 1, time: 26}
      'FB/2/2:19:30' → {status: solved, attempts: 2, time: 139}（首次通关也是一次通过）
      'RJ/6'         → {status: unsolved, attempts: 6, time: None}
      NaN / ''       → {status: none, attempts: 0, time: None}
    """
    if pd.isna(raw):
        return {"status": "none", "attempts": 0, "time": None}
    m = SUBMISSION_RE.match(str(raw).strip())
    if not m:
        return {"status": "none", "attempts": 0, "time": None}
    token, attempts, h, mi, _sec = m.groups()
    attempts = int(attempts)
    if token.upper() in SOLVED_TOKENS:
        time = int(h) * 60 + int(mi) if h is not None else None
        return {"status": "solved", "attempts": attempts, "time": time}
    return {"status": "unsolved", "attempts": attempts, "time": None}


def parse_rank_medal(raw):
    """'# ' 列 → (排名, 英文奖牌)。'1 (金奖)' → (1, 'Gold')；'*' → (None, None)。"""
    if pd.isna(raw):
        return None, None
    s = str(raw).strip()
    m = re.search(r"[（(](.+?)[）)]", s)
    medal = MEDAL_MAP.get(m.group(1).strip()) if m else None
    num = re.match(r"^(\d+)", s)
    rank = int(num.group(1)) if num else None
    return rank, medal


def _split_members(raw):
    if pd.isna(raw):
        return []
    return [p.strip() for p in str(raw).split(",") if p.strip()]


def read_domjudge_teams(xlsx_path, sheet_name="Official", problem_letters=PROBLEM_LETTERS):
    """
    读取 DOMjudge 榜单的一个 sheet，返回与"正式队伍"原始行等价的中间结构列表:
    { rank, medal, school, team, members[], solved, penalty, problems }
    """
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None)
    cols, problem_cols = _header_map(df)
    rank_col = cols.get("#", 0)
    school_col = cols["Organization"]
    team_col = cols["Name"]
    members_col = cols["Team Members"]
    solved_col = cols["Score"]
    penalty_col = cols["Time"]

    teams = []
    for _, row in df.iloc[1:].iterrows():
        school = row.iloc[school_col]
        if pd.isna(school) or not str(school).strip():
            continue
        problems = {}
        for letter in problem_letters:
            idx = next((i for l, i in problem_cols if l == letter), None)
            if idx is not None:
                problems[letter] = parse_submission(row.iloc[idx])
            else:
                problems[letter] = {"status": "none", "attempts": 0, "time": None}

        solved = row.iloc[solved_col]
        penalty = row.iloc[penalty_col]
        rank, medal = parse_rank_medal(row.iloc[rank_col])
        teams.append({
            "rank": rank,
            "medal": medal,
            "school": str(school).strip(),
            "team": str(row.iloc[team_col]).strip() if pd.notna(row.iloc[team_col]) else "",
            "members": _split_members(row.iloc[members_col]),
            "solved": int(float(solved)) if pd.notna(solved) else 0,
            "penalty": _minutes(penalty) if pd.notna(penalty) else 0,
            "problems": problems,
        })
    return teams


def read_domjudge_girl_teams(xlsx_path):
    """从"女队" sheet 提取 (学校, 队名) 集合，用于给对应队伍打 girl 标记。"""
    xls = pd.ExcelFile(xlsx_path)
    if "女队" not in xls.sheet_names:
        return set()
    df = pd.read_excel(xls, sheet_name="女队", header=None)
    cols, _ = _header_map(df)
    school_col = cols.get("Organization")
    team_col = cols.get("Name")
    if school_col is None or team_col is None:
        return set()
    result = set()
    for _, row in df.iloc[1:].iterrows():
        school, team = row.iloc[school_col], row.iloc[team_col]
        if pd.notna(school) and pd.notna(team):
            result.add((str(school).strip(), str(team).strip()))
    return result
