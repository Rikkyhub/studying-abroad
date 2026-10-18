# -*- coding: utf-8 -*-
"""地域別ページ（areas/*.md）の AUTO ブロックを作る関数群（依存は標準ライブラリのみ）。

- 地域は baguio（バギオ）・africa（アフリカ周遊）・capetown（ケープタウン）・common（日本国内・保険・共通）。
- 費用は data/expenses.csv の phase 列から地域へ対応づける（PHASE_REGION）。
- tasks.csv・timeline.csv・pages.csv の region 列は ';' 区切りで複数地域を書ける（空欄は地域に属さない）。
- 返すのはすべて Markdown の文字列。build.py が AUTO ブロックへ埋め、build_html.py が HTML にする。
- CSV は生成器の内部入力であり、読者向けのリンクは作らない。
"""
from __future__ import annotations

import re
from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import quote_plus, urlparse

REGION_LABEL = OrderedDict([
    ("baguio", "バギオ"),
    ("africa", "アフリカ周遊"),
    ("capetown", "ケープタウン"),
    ("common", "日本国内・保険・共通"),
])
REGION_FILE = {k: f"areas/{k}.md" for k in REGION_LABEL}
# expenses.csv の phase 列 -> 地域
PHASE_REGION = {"フィリピン": "baguio", "アフリカ周遊": "africa", "2校目": "capetown", "8月": "capetown", "共通・日本": "common"}
REGION_CURRENCIES = {"baguio": ["PHP", "USD"], "africa": ["ZAR", "USD"], "capetown": ["ZAR"], "common": []}
SCEN = OrderedDict([("low", "低予算"), ("std", "標準"), ("high", "余裕")])
DONE = ("完了", "不要")
KIND_LABEL = {"school": "学校", "sightseeing": "観光", "diving": "ダイビング", "airport": "空港", "hospital": "病院", "other": "その他"}
MAPS_URL = "https://www.google.com/maps/search/?api=1&query="
FX_NOTE = ("参考レート（銀行の仲値）です。現金の両替・ATM・カード決済では、売り買いの差（スプレッド）や手数料が"
           "加わるため、実際に受け取る額・支払う額とは一致しません。")
# 資料に出てくる価格の円換算例: (地域, 品目, 通貨, 金額, 出典ページ)。通貨ごとに別々に換算し、合算しない
PRICE_EXAMPLES = [
    ("baguio", "スービックのファンダイブ 1本（器材込）", "PHP", 2300, "research/baguio-diving.html"),
    ("baguio", "アニラオのファンダイブ 3本", "USD", 137, "research/baguio-diving.html"),
    ("capetown", "シモンズタウン ボート2本（Pisces Divers）", "ZAR", 3600, "research/capetown-diving.html"),
    ("capetown", "キルステンボッシュ植物園 入場（2026年掲示）", "ZAR", 270, "research/capetown-sightseeing.html"),
]


def split_regions(s: str) -> list[str]:
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def in_region(value: str, region: str) -> bool:
    return region in split_regions(value)


# ---------------------------------------------------------------- 共通の小物
def md_table(header, rows, aligns=None):
    sep = ["---:" if aligns and aligns[k] == "r" else "---" for k in range(len(header))]
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(sep) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "／").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def yen(v):
    return "未計上" if v is None else f"¥{round(v):,}"


def mdp(path: str) -> str:
    """リポジトリ内の資料パスを Markdown 側に向ける（生成HTMLでは build_html が .html に書き換える）"""
    if path.startswith(("research/", "docs/", "blog/", "areas/")) and path.endswith(".html"):
        return path[:-5] + ".md"
    return path


def safe_url(u: str) -> str:
    return u.replace("(", "%28").replace(")", "%29").replace(" ", "%20")


def host_link(u: str) -> str:
    host = urlparse(u).netloc.removeprefix("www.")
    return f"[{host}]({safe_url(u)})"


def ref_cell(refs: str) -> str:
    links = [host_link(x.strip()) for x in (refs or "").split(";") if x.strip()]
    return "<br>".join(links) or "－"


def dnum(s):
    try:
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        return None
    return d if d.is_finite() and d > 0 else None


def fmt(d: Decimal, places: int = 2) -> str:
    q = d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    s = f"{q:,.{places}f}"
    return s[:-(places + 1)] if s.endswith("." + "0" * places) else s


def task_sort_key(t):
    try:
        lead = int(t["lead_days"])
    except (KeyError, ValueError):
        lead = -9999
    return (t["priority"] or "9", -lead, t["id"])


# ---------------------------------------------------------------- ブロック
def timeline_block(timeline, region):
    rs = sorted((r for r in timeline if in_region(r.get("region", ""), region)), key=lambda r: (int(r["sort"] or 0), r["id"]))
    if not rs:
        return "この地域に対応する旅程の行はありません。"
    return md_table(["時期（モデル）", "内容", "状態", "概要"], [[r["period"], f"**{r['title']}**", r["status"], r["summary"]] for r in rs])


def tasks_block(tasks, region):
    rs = sorted((t for t in tasks if in_region(t.get("region", ""), region) and t["status"] not in DONE), key=task_sort_key)
    if not rs:
        return "この地域に対応する未完了の確認事項はありません。"
    body = [[t["priority"], t["task"], t["deadline_note"], f"{t['status']}<br>{t['deadline_kind']}", t["next_action"] or "－"] for t in rs]
    return (md_table(["優先", "作業", "期限（目安）", "状態・期限の種類", "次のアクション"], body, aligns=["r", "l", "l", "l", "l"])
            + "\n\n優先度は1が最優先です。期限は暦日ではなく、出発日などを基準にした相対的な目安です"
              "（期限の種類：公式期限＝制度上の期限／学校・機関の個別期限＝各機関の案内に従う／推奨目安＝このモデルの提案／要確認）。"
              "一般的な確認項目で、個人の進捗ではありません。")


def region_rows(rows, region):
    return [r for r in rows if PHASE_REGION.get(r["phase"]) == region]


def region_totals(rows, region):
    """地域の小計（円換算済みの est を使う）。{全体/見積/未確認: {low,std,high}} 未計上の行は含めない"""
    out = {"all": dict.fromkeys(SCEN), "見積": dict.fromkeys(SCEN), "未確認": dict.fromkeys(SCEN)}
    for r in region_rows(rows, region):
        if r["no_amount"]:
            continue
        for s in SCEN:
            v = r["est"][s]
            if v is None:
                continue
            for key in ("all", r["status"]):
                out[key][s] = (out[key][s] or 0.0) + v
    return out  # 金額が1件もないものは None（「未計上」と表示。0円にしない）


def _local(r):
    cur = r["currency"] or "JPY"
    for s in ("std", "low", "high"):
        raw = (r.get(f"{s}_local") or "").replace(",", "").strip()
        if raw:
            v = float(raw)
            tail = "" if s == "std" else f"（{SCEN[s]}のみ）"
            return (f"{cur} {v:,.0f}{tail}") if cur != "JPY" else "円建て"
    return "－"


def cost_block(rows, region):
    rs = region_rows(rows, region)
    if not rs:
        return "この地域に計上された費用はありません。"
    body = []
    for r in rs:
        item = r["item"] + (f"（{r['payee']}）" if r["payee"] and r["payee"] != "—" else "")
        if r["source"].startswith("http"):
            item += f" [出典]({safe_url(r['source'])})"
        body.append([item, r["status"], _local(r)] + [yen(r["est"][s]) for s in SCEN])
    t = region_totals(rows, region)
    for label, key in (("**小計：公開価格表からの匿名の見積（見積と未確認の合計）**", "all"), ("うち 見積（出典あり）", "見積"), ("うち 未確認（出典なし・推定）", "未確認")):
        body.append([label, "－", "－"] + [(f"**{yen(t[key][s])}**" if key == "all" else ("－" if t[key][s] is None else yen(t[key][s]))) for s in SCEN])
    out = [md_table(["項目", "区分", "現地通貨（標準）", "低予算", "標準", "余裕"], body, aligns=["l", "l", "l", "r", "r", "r"]),
           "",
           "金額は公開価格表からの**匿名の見積**です（実際の支払額ではありません）。通貨が異なる行は、下の「通貨と円換算」の参考レートで円に換算して"
           "合計しています（円未満は四捨五入）。区分の「未確認」は出典なしの推定または金額未入力で、見積と区別して表示しています。"]
    unp = []
    for r in rs:
        if r["no_amount"]:
            unp.append(f"{r['id']} {r['item']}（すべて未計上）")
        elif r["unpriced"]:
            unp.append(f"{r['id']} {r['item']}（{'・'.join(SCEN[s] for s in r['unpriced'])}が未計上）")
    out += ["", "**未計上（合計に含まれない項目）**：" + ("、".join(unp) if unp else "なし")
            + "。「未計上」は金額が入っていないことを示し、0円ではありません。"]
    notes = [f"- {r['id']}：{r['note']}" for r in rs if r["note"]]
    if notes:
        out += ["", "**前提と備考**", ""] + notes
    return "\n".join(out)


def docs_block(pages, region):
    rs = sorted((p for p in pages if in_region(p.get("region", ""), region)), key=lambda r: (r["group"] != "research", int(r["sort"] or 0), r["id"]))
    if not rs:
        return "この地域に対応する資料はありません。"
    body = [[p["area"], f"[{p['title']}](../{mdp(p['path'])})", p["summary"], ref_cell(p["refs"]), p["verified_at"] or "－"] for p in rs]
    return md_table(["分野", "資料", "内容", "参考（一次情報）", "最終確認日"], body) + "\n\n「参考」は各資料が根拠にした公式・一次情報へのリンクです。"


def places_block(places, region):
    rs = [p for p in places if p["area"] == region]
    if not rs:
        return "この地域に登録された場所はありません。"
    body = []
    for p in rs:
        src = p["source"]
        s = host_link(src) if src.startswith("http") else (f"[資料](../{mdp(src)})" if src else "－")
        body.append([p["name"], KIND_LABEL.get(p["kind"], p["kind"]), f"[Google マップ]({MAPS_URL}{quote_plus(p['maps_query'])})", p["note"] or "－", s])
    return (md_table(["名称", "種類", "地図", "備考", "出典"], body)
            + "\n\n公共の施設・名所・ダイビングショップ・空港だけを載せています。地図リンクは Google マップの検索結果を開きます（営業・安全の保証ではありません）。")


def fx_block(fx_records, region):
    cur = REGION_CURRENCIES.get(region, [])
    recs = [r for c in cur for r in fx_records if r["currency"] == c]
    if not recs:
        return "この地域の費用は円建てが中心で、通貨の換算表はありません。外貨が出てくる場合は、ほかの地域のページの換算表を参照してください。"
    body = []
    for r in recs:
        rate = dnum(r["jpy_per_unit"])
        name = f"{r['name_ja']}（{r['currency']}）"
        if rate:
            src = f"{r['rate_date']}　{host_link(r['source'])}" if r["source"].startswith("http") else r["rate_date"]
            body.append([name, fmt(rate), fmt(rate * 100), fmt(Decimal(10000) / rate), src])
        else:
            body.append([name, "未確認", "未確認", "未確認", "未確認"])
    out = [md_table(["通貨", "1単位＝円", "100単位＝円", "1万円＝現地通貨", "レート日・出典"], body, aligns=["l", "r", "r", "r", "l"]),
           "", FX_NOTE + "通貨が違う金額は、換算前に足し合わせていません。"]
    rates = {r["currency"]: dnum(r["jpy_per_unit"]) for r in fx_records}
    ex = [(lab, c, a, pg) for (rg, lab, c, a, pg) in PRICE_EXAMPLES if rg == region]
    if ex:
        rows = []
        for lab, c, a, pg in ex:
            rate = rates.get(c)
            rows.append([lab, f"{c} {a:,}", (fmt(rate * a, 0) + " 円") if rate else "未確認", f"[資料](../{mdp(pg)})"])
        out += ["", "資料に出てくる価格の円換算例（参考）", "",
                md_table(["品目（資料の掲示額）", "現地通貨", "円換算（参考）", "出典"], rows, aligns=["l", "r", "r", "l"])]
    return "\n".join(out)


def extract_table(md: str, heading_prefix: str) -> list[str]:
    """Markdown 中の指定見出し以降の最初の表（行のリスト）を返す"""
    lines = md.replace("\r\n", "\n").split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.startswith("## ") and ln[3:].startswith(heading_prefix)), None)
    if start is None:
        return []
    tbl = []
    for ln in lines[start + 1:]:
        if ln.startswith("|"):
            tbl.append(ln)
        elif tbl:
            break
        elif ln.startswith("## "):
            break
    return tbl


def routes_block(root: Path):
    src = root / "research" / "africa-route-comparison.md"
    if not src.exists():
        return "ルート案は [アフリカ周遊ルート比較](../research/africa-route-comparison.md) を参照してください。"
    tbl = extract_table(src.read_text(encoding="utf-8"), "1. ルート定義")
    if not tbl:
        return "ルート案は [アフリカ周遊ルート比較](../research/africa-route-comparison.md) を参照してください。"
    return ("\n".join(tbl) + "\n\nMNL＝マニラ、NBO＝ナイロビ、ADD＝アディスアベバ、TNR＝アンタナナリボ、JNB＝ヨハネスブルグ、CPT＝ケープタウン、DAR＝ダルエスサラーム。"
            "どれも未確定の案です。区間別の比較・入国条件・危険情報・価格モデルは [アフリカ周遊ルート比較](../research/africa-route-comparison.md) にあります。")


def maps_block(root: Path):
    world, africa = (root / "maps" / "world-map.html").exists(), (root / "maps" / "africa-map.html").exists()
    out = []
    if world and africa:
        out += ["- [世界地図（移動の全体像）](../maps/world-map.html)", "- [アフリカ地図（周遊ルート案）](../maps/africa-map.html)"]
    else:
        out += ["世界地図とアフリカ地図は別のPRで準備中で、このブランチにはまだありません。公開後にここへリンクを追加します。"]
    out += ["", "主要な空港・国境・国立公園の地図リンクは、上の「場所と地図」の表と [アフリカ周遊ルート比較（主要地点のGoogle Mapsリンク）](../research/africa-route-comparison.md) にあります。"]
    return "\n".join(out)


def all_blocks(region, *, rows, tasks, timeline, pages, places, fx_records, root):
    b = {
        "timeline": timeline_block(timeline, region),
        "tasks": tasks_block(tasks, region),
        "cost": cost_block(rows, region),
        "docs": docs_block(pages, region),
        "places": places_block(places, region),
        "fx": fx_block(fx_records, region),
    }
    if region == "africa":
        b["routes"] = routes_block(root)
        b["maps"] = maps_block(root)
    return b
