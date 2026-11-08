# -*- coding: utf-8 -*-
"""Read an editable Markdown table for estimated travel costs.

No new user-maintained CSV. Older CSV expenses remain an internal legacy
input for non-Fermi rows. Fermi amounts are computed in-memory from Markdown
while generating the summary and pages.
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("research/africa-budget-fermi.md")
START = "<!-- FERMIBUDGET:START -->"
END = "<!-- FERMIBUDGET:END -->"
CATEGORIES = {
    "AF-11": ("食費", "食費・日常生活費", "南部アフリカ", "35日間の食費（地域別単価×日数）", "2027-05"),
    "AF-12": ("現地交通", "現地交通費", "南部アフリカ", "VFA・Livingstone・Kasane間の日中送迎（区間数×単価）", "2027-05"),
    "AF-14": ("観光", "観光・ツアー・ダイビング", "マダガスカル", "マダガスカル自然観光とガイド（回数×単価）", "2027-05"),
    "AF-15": ("宿泊", "寮・ホームステイ・宿泊", "マダガスカル", "マダガスカル宿泊費（食費はAF-11）", "2027-05"),
    "AF-20": ("サファリ", "観光・ツアー・ダイビング", "ボツワナ", "チョベのサファリ・ボート（回数×仮単価）", "2027-05"),
    "AF-22": ("現地交通", "現地交通費", "マダガスカル", "マダガスカル日中の道路移動（回数×単価）", "2027-05"),
    "AF-23": ("宿泊", "寮・ホームステイ・宿泊", "南部アフリカ", "モーリシャス宿泊（泊数×単価）", "2027-05"),
    "AF-24": ("宿泊", "寮・ホームステイ・宿泊", "南部アフリカ", "ヨハネスブルグ宿泊（泊数×単価）", "2027-05"),
    "AF-25": ("宿泊", "寮・ホームステイ・宿泊", "南部アフリカ", "VFA・Livingstone・Kasane宿泊（泊数×単価）", "2027-05"),
    "AF-26": ("宿泊", "寮・ホームステイ・宿泊", "南アフリカ", "ケープタウン入学前宿泊（泊数×単価）", "2027-06"),
}
SCENARIOS = ("low", "std", "high")
HEADINGS = ("ID", "区分", "対象・費目", "数量", "単位", "節約単価", "標準単価", "余裕単価")


def _number(value, row):
    if not re.fullmatch(r"\d{1,3}(?:,\d{3})*|\d+", value):
        raise ValueError(f"Fermi Markdown row {row}: invalid integer {value!r}")
    return int(value.replace(",", ""))


def read_assumptions(root=ROOT):
    """Return individual cost assumptions as dictionaries. Fail closed on drift."""
    path = Path(root) / SOURCE
    source = path.read_text(encoding="utf-8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("Fermi Markdown must contain exactly one START/END table")
    body = source.split(START, 1)[1].split(END, 1)[0]
    entries = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if tuple(cells) == HEADINGS or all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != len(HEADINGS):
            raise ValueError(f"Fermi Markdown: {len(cells)} cells, expected {len(HEADINGS)}: {line}")
        expense_id, kind, segment, q, unit, low, std, high = cells
        if expense_id not in CATEGORIES:
            raise ValueError(f"Fermi Markdown: unknown ID {expense_id}")
        if kind != CATEGORIES[expense_id][0]:
            raise ValueError(f"Fermi Markdown: invalid category for {expense_id}: {kind}")
        if unit not in ("日", "泊", "回"):
            raise ValueError(f"Fermi Markdown: invalid unit for {expense_id}")
        quantity = _number(q, line)
        prices = [_number(v, line) for v in (low, std, high)]
        if not quantity or any(v < 0 for v in prices) or prices != sorted(prices):
            raise ValueError(f"Fermi Markdown: invalid quantity / price order {expense_id}")
        entries.append({"id": expense_id, "kind": kind, "segment": segment,
                        "quantity": quantity, "unit": unit, "prices": prices})
    if not entries or set(CATEGORIES).difference({x["id"] for x in entries}):
        raise ValueError("Fermi Markdown: missing budget estimates")
    # A source table with the exact same country/segment more than once could double-count.
    keys = [(x["id"], x["segment"]) for x in entries]
    if len(set(keys)) != len(keys):
        raise ValueError("Fermi Markdown: duplicated ID+segment")
    return entries


def aggregate(root=ROOT):
    entries = read_assumptions(root)
    totals = defaultdict(lambda: [0, 0, 0])
    for entry in entries:
        for i, unit_price in enumerate(entry["prices"]):
            totals[entry["id"]][i] += entry["quantity"] * unit_price
    return dict(totals)


def apply_to_expenses(expenses, root=ROOT):
    """Use Markdown amounts in the in-memory build without touching expenses.csv."""
    totals = aggregate(root)
    by_id = {r["id"]: r for r in expenses}
    if len(by_id) != len(expenses):
        raise ValueError("expenses.csv has duplicate IDs")
    for expense_id, values in totals.items():
        _, category, country, item, period = CATEGORIES[expense_id]
        if expense_id in by_id:
            row = by_id[expense_id]
            if any(row.get(s + "_local", "").strip() for s in SCENARIOS):
                raise ValueError(f"{expense_id}: Fermi Markdown would double-count populated legacy CSV amount")
        else:
            row = {key: "" for key in expenses[0]}
            row["id"] = expense_id
            row["phase"] = "アフリカ周遊"
            row["period_start"] = period
            row["period_end"] = period
            row["due_date"] = "2027-04"
            expenses.append(row)
        row.update({"category": category, "country": country, "item": item,
                    "payee": "仮単価モデル（未検証）", "status": "未確認",
                    "currency": "JPY", "source": "https://github.com/Rikkyhub/studying-abroad/issues/80",
                    "issue": "https://github.com/Rikkyhub/studying-abroad/issues/80",
                    "note": "フェルミ推定（数量×単価）の入力正本は research/africa-budget-fermi.md。"
                            "2027年実売・市場平均ではなく仮の価格。二重計上を確認。",
                    "collected_on": "2026-11-09", "recheck_by": "2027-04-01",
                    **{f"{s}_local": str(values[i]) for i, s in enumerate(SCENARIOS)}})
    return expenses
