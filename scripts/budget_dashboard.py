"""7か月・8月ペルー案の表示モデル。旧案の航空券とは排他的に集計する。"""
import json
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://github.com/Rikkyhub/studying-abroad/blob/main/research/africa-south-america-2027-comparison.md"


def south_america(fx):
    # 第7章の単価を21暦日・20泊に適用。ロッジ代が取得できたら宿食込みの日を控除する。
    entries = [
        ("hotel", "宿泊（20泊）", "寮・ホームステイ・宿泊", 20, "JPY", 2000, 3000),
        ("food", "食費（21日）", "食費・日常生活費", 21, "JPY", 1000, 1500),
        ("train", "PeruRail 往復（片道の参考下限×2）", "現地交通費", 2, "USD", None, 35),
        ("bus", "マチュピチュ往復バス（徒歩案あり）", "現地交通費", 1, "USD", 0, 24),
        ("entry", "マチュピチュ入場（参考 S/152・円換算未取得）", "観光・ツアー・ダイビング", 1, "JPY", None, None),
        ("lodge", "イキトスのツアー（宿・食との重なりを除く追加額）", "観光・ツアー・ダイビング", 1, "JPY", None, None),
        ("out", "ケープタウン→サンパウロ→リマ", "航空券・長距離移動", 1, "JPY", None, None),
        ("dom", "リマ⇄クスコ・イキトスの国内移動", "航空券・長距離移動", 1, "JPY", None, None),
        ("return", "リマ→日本", "航空券・長距離移動", 1, "JPY", None, None),
    ]
    for key, item, category, qty, currency, low, std in entries:
        rate = fx.get(currency, {}).get("rate")
        yield dict(id="SA8-"+key, item=item, phase="8月 南米・ペルー案",
                   country="国際移動" if key in ("out", "return") else "ペルー",
                   category=category, source=SOURCE, alloc={"2027-08": 1},
                   est={k: qty*v*rate if v is not None and rate is not None else None
                        for k, v in (("low", low), ("std", std))})


def ledger(rows, fx):
    # PH-11 includes PH-12. SC-08 is the direct return. August Africa is an alternative.
    included = [r for r in rows if r["id"] not in {"PH-12", "SC-08"}
                and r["phase"] != "アフリカ周遊（8月）"]
    result = []
    for r in [*included, *south_america(fx)]:
        std, low = r["est"]["std"], r["est"]["low"]
        amount = round(std) if std is not None else None
        # Largest remainders keep the monthly yen amounts additive.
        allocation = r["alloc"]
        months = {m: None for m in allocation}
        if amount is not None:
            months = {m: int(amount*w) for m, w in allocation.items()}
            order = sorted(months, key=lambda m: months[m]-amount*allocation[m])
            for m in order[:amount-sum(months.values())]:
                months[m] += 1
        result.append(dict(id=r["id"], item=r["item"], phase=r["phase"], country=r["country"],
                           category=r["category"], amount=amount, months=months, source=r["source"],
                           saving=None if std is None or low is None else max(0, amount-round(low))))
    if len({r["id"] for r in result}) != len(result):
        raise ValueError("予算明細のIDが重複しています")
    return result


def render():
    _, rows, _, _, _, fx, _, _ = build.load_model()
    data = ledger(rows, fx)
    return (ROOT / "app/budget.html").read_text(encoding="utf8").replace(
        "@@ROWS@@", json.dumps(data, ensure_ascii=False).replace("<", r"\u003c"))
