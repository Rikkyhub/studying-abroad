# -*- coding: utf-8 -*-
"""Country-stay estimates for optional August travel, sourced ONLY from Markdown.

Candidates are independent scenarios; until one is explicitly selected, none
affect the global dashboard. No input CSV is generated or edited.
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("research/africa-budget-august.md")
START = "<!-- AUGBUDGET:START -->"
END = "<!-- AUGBUDGET:END -->"
EXPECTED_COLUMNS = ("案", "国・地域", "泊数", "食費日数", "宿泊節約単価",
                    "宿泊標準単価", "宿泊余裕単価", "食費節約単価",
                    "食費標準単価", "食費余裕単価")
SCENARIOS = ("low", "std", "high")


def _int(value):
    if not re.fullmatch(r"(?:\d{1,3}(?:,\d{3})*|\d+)", value):
        raise ValueError(f"invalid August estimate integer: {value!r}")
    return int(value.replace(",", ""))


def read_plan(root=ROOT):
    source = (Path(root) / SOURCE).read_text(encoding="utf-8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("August Markdown requires exactly one budget table")
    selected = re.findall(r"\*\*予算へ反映する案：([^*]+)\*\*", source)
    if len(selected) != 1:
        raise ValueError("August Markdown requires one selected-plan setting")
    active = selected[0].strip()
    section = source.split(START, 1)[1].split(END, 1)[0]
    rows = []
    seen = set()
    for text in section.splitlines():
        text = text.strip()
        if not text.startswith("|"):
            continue
        cells = [v.strip() for v in text.strip("|").split("|")]
        if tuple(cells) == EXPECTED_COLUMNS:
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != len(EXPECTED_COLUMNS):
            raise ValueError(f"August table expects {len(EXPECTED_COLUMNS)} columns: {text}")
        case, country, *numbers = cells
        if not re.fullmatch(r"[A-Z][A-Z0-9_-]*", case):
            raise ValueError(f"invalid August scenario ID: {case}")
        if not country or "|" in country:
            raise ValueError("August country or region name missing")
        nights, food_days, *prices = [_int(v) for v in numbers]
        if (case, country) in seen:
            raise ValueError(f"duplicate August scenario+country: {case} / {country}")
        seen.add((case, country))
        if not (prices[0] <= prices[1] <= prices[2]
                and prices[3] <= prices[4] <= prices[5]):
            raise ValueError(f"August low/standard/high price order invalid: {case} / {country}")
        rows.append({"case": case, "country": country, "nights": nights,
                     "days": food_days, "lodging": prices[:3], "food": prices[3:]})
    cases = {r["case"] for r in rows}
    if not cases or (active != "未定" and active not in cases):
        raise ValueError("August selected scenario does not exist")
    return active, rows


def calculate(root=ROOT):
    active, rows = read_plan(root)
    by_case = defaultdict(lambda: {"nights": 0, "days": 0,
                                   "lodging": [0, 0, 0], "food": [0, 0, 0]})
    for r in rows:
        data = by_case[r["case"]]
        data["nights"] += r["nights"]
        data["days"] += r["days"]
        for j in range(3):
            data["lodging"][j] += r["nights"] * r["lodging"][j]
            data["food"][j] += r["days"] * r["food"][j]
    return active, rows, dict(by_case)


def render_summary_md(root=ROOT):
    active, rows, budgets = calculate(root)
    out = [
        "| 案・国 | 泊数 | 食費日数 | 宿泊費（標準） | 食費（標準） | 部分小計（標準） |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for case in sorted(budgets):
        subset = [r for r in rows if r["case"] == case]
        for r in subset:
            lodging = r["nights"] * r["lodging"][1]
            food = r["days"] * r["food"][1]
            out.append(f"| {case}：{r['country']} | {r['nights']}泊 | "
                       f"{r['days']}日 | ¥{lodging:,} | ¥{food:,} | ¥{lodging+food:,} |")
        x = budgets[case]
        lodging, food = x["lodging"][1], x["food"][1]
        out.append(f"| **案{case}合計** | **{x['nights']}泊** | **{x['days']}日** | "
                   f"**¥{lodging:,}** | **¥{food:,}** | **¥{lodging+food:,}** |")
    out += ["", "| 案 | 低予算（宿＋食） | 標準 | 余裕 |",
            "|---|---:|---:|---:|"]
    for case in sorted(budgets):
        x = budgets[case]
        totals = [x["lodging"][j] + x["food"][j] for j in range(3)]
        out.append(f"| {case} | ¥{totals[0]:,} | ¥{totals[1]:,} | ¥{totals[2]:,} |")
    out += ["", f"**既存の総予算に反映する案：{active}**。"
            + ("未定のため候補の費用は総予算へ一切加算していません。"
               if active == "未定" else f"案{active}の宿泊・食費だけが反映対象です。"),
            "上記は仮の宿泊＋食費だけの試算。"
            "航空券・現地交通・ビザ・サファリ・保険・予備費は別途必要で、"
            "2027年の市場平均・実売価格を示しません。"]
    return "\n".join(out)


def apply_to_expenses(expenses, root=ROOT):
    """Add ONLY the actively selected August route as in-memory budget rows."""
    active, rows = read_plan(root)
    if active == "未定":
        return expenses
    identifiers = {r["id"] for r in expenses}
    template_keys = list(expenses[0])
    for seq, item in enumerate((r for r in rows if r["case"] == active), start=1):
        for kind, quantity, prices, category in (
            ("H", item["nights"], item["lodging"], "寮・ホームステイ・宿泊"),
            ("F", item["days"], item["food"], "食費・日常生活費"),
        ):
            if quantity == 0:
                continue
            row_id = f"AU83-{active}-{seq:02d}-{kind}"
            if row_id in identifiers:
                raise ValueError(f"August estimate would double-count existing ID: {row_id}")
            identifiers.add(row_id)
            row = dict.fromkeys(template_keys, "")
            row.update({
                "id": row_id, "category": category,
                "country": item["country"] if item["country"] != "航空移動日" else "共通",
                "phase": "アフリカ周遊（8月）",
                "item": f"8月 案{active} {item['country']} {kind}: {quantity}" +
                        ("泊" if kind == "H" else "日") + "×仮単価",
                "payee": "編集可能なMarkdown内の仮定（未検証）",
                "period_start": "2027-08", "period_end": "2027-08",
                "due_date": "2027-07", "status": "未確認", "currency": "JPY",
                "source": "https://github.com/Rikkyhub/studying-abroad/issues/83",
                "issue": "https://github.com/Rikkyhub/studying-abroad/issues/83",
                "collected_on": "2026-11-09", "recheck_by": "2027-07-01",
                "note": "research/africa-budget-august.mdの宿泊・食費仮単価。" +
                        "2027年の正式価格・平均額ではなく、航空券・観光・ビザ等は別費目。",
                **{f"{s}_local": str(quantity * prices[j])
                   for j, s in enumerate(SCENARIOS)},
            })
            expenses.append(row)
    return expenses
