# -*- coding: utf-8 -*-
"""費用の「共通の区別」：行＝時期、列＝費目。ホーム以外のすべての費用の表示で、この区別を使う。

時期（行）は、expenses.csv の phase 列を、旅の時期に対応づけたもの。
費目（列）は、expenses.csv の category 列（13区分）を、見やすい7つにまとめたもの。
低・標準・余裕、見積（出典あり）・未確認の別も、同じ集計から出す（二重計上なし）。
"""
from __future__ import annotations

from collections import OrderedDict

# 時期（行）。phase 列 -> 時期キー
PERIODS = OrderedDict([
    ("common", "出発前・共通（保険・予防接種など）"),
    ("baguio", "2〜4月 バギオ（語学留学）"),
    ("africa", "5月 アフリカ周遊"),
    ("capetown", "6〜7月 ケープタウン（語学留学）"),
    ("aug", "8月 周遊"),
])
PHASE_PERIOD = {
    "共通・日本": "common", "フィリピン": "baguio", "アフリカ周遊": "africa",
    "2校目": "capetown", "8月": "capetown",
    "8月 南米・ペルー案": "aug", "アフリカ周遊（8月）": "aug",
}

# 費目（列）。category 列 -> 費目キー
KINDS = OrderedDict([
    ("air", "航空券・長距離移動"),
    ("stay", "宿泊"),
    ("food", "食費・日用品"),
    ("local", "現地交通"),
    ("tour", "観光・ツアー"),
    ("study", "授業料・ビザ"),
    ("misc", "保険・医療・通信"),
])
CATEGORY_KIND = {
    "航空券・長距離移動": "air", "寮・ホームステイ・宿泊": "stay", "食費・日常生活費": "food",
    "現地交通費": "local", "観光・ツアー・ダイビング": "tour", "授業料・入学金・教材費": "study",
    "ビザ・滞在許可": "study", "保険・医療": "misc", "通信費": "misc",
    "出発準備・持ち物": "misc", "日本の固定費": "misc", "税金・社会保険": "misc", "予備費": "misc",
}


def period_of(row) -> str:
    return PHASE_PERIOD.get(row["phase"], "common")


def kind_of(row) -> str:
    return CATEGORY_KIND.get(row["category"], "misc")


def build(rows, scenario="std"):
    """{時期: {費目: 円, "計": 円, "見積": 円, "未確認": 円}}。金額未入力の行は含めない（0円にしない）"""
    t = OrderedDict((p, {**{k: 0.0 for k in KINDS}, "計": 0.0, "見積": 0.0, "未確認": 0.0}) for p in PERIODS)
    for r in rows:
        if r["no_amount"]:
            continue
        v = r["est"][scenario]
        if v is None:
            continue
        cell = t[period_of(r)]
        cell[kind_of(r)] += v
        cell["計"] += v
        cell[r["status"]] += v
    return t


def totals(table):
    out = {k: 0.0 for k in list(KINDS) + ["計", "見積", "未確認"]}
    for cell in table.values():
        for k in out:
            out[k] += cell[k]
    return out
