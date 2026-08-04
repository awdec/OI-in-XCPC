#!/usr/bin/env python3
"""
遍历所有 xlsx 文件，提取 (学校, 姓名) 二元组，去重后输出到 web/public/data/players.json。
"""

import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "players.json"


def main():
    xlsx_files = sorted(ROOT.glob("*.xlsx"))
    if not xlsx_files:
        print("错误: 未找到 xlsx 文件")
        return

    pairs = set()

    for xlsx_path in xlsx_files:
        xls = pd.ExcelFile(xlsx_path)
        for sheet_name in xls.sheet_names:
            if sheet_name != "正式队伍":
                continue
            df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
            for _, row in df.iterrows():
                school = row.get("Organization")
                if pd.isna(school):
                    continue
                school = str(school).strip()
                for col in ["Member1", "Member2", "Member3"]:
                    name = row.get(col)
                    if pd.notna(name):
                        pairs.add((school, str(name).strip()))

    result = sorted(pairs, key=lambda x: (x[0], x[1]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"共提取 {len(result)} 个去重选手 (学校+姓名)")
    print(f"输出: {OUTPUT}")


if __name__ == "__main__":
    main()
