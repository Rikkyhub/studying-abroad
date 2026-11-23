"""7か月・8月ペルー案の表示モデル。旧案の航空券とは排他的に集計する。"""
import json
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parents[1]


def ledger(rows, scenario="std"):
    result = []
    for r in rows:
        std, low = r["est"]["std"], r["est"]["low"]
        amount = r["est"][scenario]
        # Largest remainders keep the monthly yen amounts additive.
        allocation = r["alloc"]
        months = {m: None for m in allocation}
        if amount is not None:
            months = {m: int(amount*w) for m, w in allocation.items()}
            order = sorted(months, key=lambda m: months[m]-amount*allocation[m])
            for m in order[:amount-sum(months.values())]:
                months[m] += 1
        result.append(dict(id=r["id"], item=r["item"], phase=r["phase"], country=r["country"],
                           category=r["category"], note=r["note"] if r["id"].startswith("SA8-") or r["id"] == "AF-16" else "", amount=amount, months=months, source=r["source"],
                           saving=None if std is None or low is None else max(0, std-low)))
    if len({r["id"] for r in result}) != len(result):
        raise ValueError("予算明細のIDが重複しています")
    return result


def render():
    _, rows, *_ = build.load_model()
    data = {scenario: ledger(rows, scenario) for scenario in build.SCENARIOS}
    return (ROOT / "app/budget.html").read_text(encoding="utf8").replace(
        "@@ROWS@@", json.dumps(data, ensure_ascii=False).replace("<", r"\u003c"))
