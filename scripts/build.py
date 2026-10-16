# -*- coding: utf-8 -*-
"""
集計・ダッシュボード生成スクリプト（studying-abroad）

使い方（リポジトリのルートで実行）:
    python3 scripts/build.py           集計して生成物を更新
    python3 scripts/build.py --check   検証のみ。生成物が CSV と一致しなければ失敗（CI用）

- data/*.csv（正本）を読み込み、以下を再生成する。
    * Markdown の <!-- AUTO:名前 --> 〜 <!-- /AUTO:名前 --> の間だけ
    * index.html（全体を再生成）
- CSV 自体は一切書き換えない（実績・証憑の記録を勝手に変更しないため）。
- 標準ライブラリのみ使用。
"""
import csv
import datetime as dt
import html
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ---------------------------------------------------------------- 定義
CATEGORIES = [
    "授業料・入学金・教材費",
    "寮・ホームステイ・宿泊",
    "食費・日常生活費",
    "航空券・長距離移動",
    "現地交通費",
    "観光・ツアー・ダイビング",
    "ビザ・滞在許可",
    "保険・医療",
    "通信費",
    "出発準備・持ち物",
    "日本の固定費",
    "税金・社会保険",
    "予備費",
]
EXPENSE_STATUS = ["確定", "見積", "未確認", "実績"]
TASK_STATUS = ["未着手", "進行中", "要確認", "完了", "保留", "不要"]
ARTICLE_STATUS = ["未着手", "資料収集中", "下書き", "公開可能", "公開済み"]
SCENARIOS = OrderedDict([("low", "低予算"), ("std", "標準"), ("high", "余裕")])
# 集計上の「月」。期間が無い費用は支払予定日の月、どちらも無ければ「出発前」。
MONTHS = OrderedDict([
    ("pre", "出発前"),
    ("2027-02", "2月 フィリピン"),
    ("2027-03", "3月 フィリピン"),
    ("2027-04", "4月 フィリピン"),
    ("2027-05", "5月 アフリカ周遊"),
    ("2027-06", "6月 2校目"),
    ("2027-07", "7月 2校目"),
    ("post", "帰国後"),
])
TRIP_START = dt.date(2027, 2, 1)


_META = {}


def today():
    """集計基準日。data/meta.csv の as_of（生成物を決定的にするため実行日は使わない）"""
    return dt.date.fromisoformat(_META.get("as_of", "2026-10-17"))


# ---------------------------------------------------------------- 読み込み
def read_csv(name):
    path = DATA / name
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in list(r):
            r[k] = (r[k] or "").strip()
    return rows


def num(s):
    s = (s or "").replace(",", "").replace("¥", "").strip()
    if s == "":
        return None
    return float(s)


def date(s):
    s = (s or "").strip()
    if not s:
        return None
    return dt.date.fromisoformat(s)


def yen(v, dash="—"):
    if v is None:
        return dash
    return f"¥{round(v):,}"


def man(v):
    """万円表記（ダッシュボード用）"""
    if v is None:
        return "—"
    return f"{v / 10000:,.1f}万円"


# ---------------------------------------------------------------- 計算
def load_fx():
    fx = {"JPY": {"rate": 1.0, "date": "", "source": ""}}
    for r in read_csv("fx.csv"):
        fx[r["currency"]] = {"rate": num(r["jpy_per_unit"]), "date": r["rate_date"], "source": r["source"]}
    return fx


def month_key(d):
    if d < TRIP_START:
        return "pre"
    k = f"{d.year:04d}-{d.month:02d}"
    return k if k in MONTHS else "post"


def allocate(row):
    """費用を月へ按分する比率 {月キー: 比率}"""
    ps, pe = date(row["period_start"]), date(row["period_end"])
    if ps and pe and pe >= ps:
        days = defaultdict(int)
        d = ps
        while d <= pe:
            days[month_key(d)] += 1
            d += dt.timedelta(days=1)
        total = sum(days.values())
        return {k: v / total for k, v in days.items()}
    due = date(row["due_date"]) or ps
    return {month_key(due) if due else "pre": 1.0}


def compute(expenses, fx, problems):
    out = []
    for r in expenses:
        cur = r["currency"] or "JPY"
        rate = fx.get(cur, {}).get("rate")
        if rate is None:
            problems.append(f"{r['id']}: 通貨 {cur} の為替レートが data/fx.csv にありません")
            rate = 0
        est = {}
        for s in SCENARIOS:
            v = num(r[f"{s}_local"])
            est[s] = None if v is None else v * rate
        if est["std"] is None:
            est["std"] = est["low"] if est["low"] is not None else est["high"]
        if est["low"] is None:
            est["low"] = est["std"]
        if est["high"] is None:
            est["high"] = est["std"]
        paid = num(r["paid_jpy"]) or 0.0
        actual = num(r["actual_jpy"])
        fc = {}
        for s in SCENARIOS:
            if actual is not None:
                fc[s] = actual  # 実績確定後は実績のみを使う
            else:
                fc[s] = max(est[s] or 0.0, paid)  # 支払済み分は見積に含める（二重計上しない）
        no_amount = all(num(r[f"{s}_local"]) is None for s in SCENARIOS) and actual is None
        out.append({**r, "rate": rate, "est": est, "no_amount": no_amount, "paid": paid, "actual": actual,
                    "forecast": fc, "remaining": max(fc["std"] - paid, 0.0), "alloc": allocate(r)})
    return out


def summarize(rows, funds):
    S = {}
    S["forecast"] = {s: sum(r["forecast"][s] for r in rows) for s in SCENARIOS}
    S["paid"] = sum(r["paid"] for r in rows)
    S["paid_verified"] = sum(r["paid"] for r in rows if r["evidence"] and r["status"] in ("確定", "実績"))
    S["remaining"] = S["forecast"]["std"] - S["paid"]
    settled = [r for r in rows if r["actual"] is not None]
    S["actual"] = sum(r["actual"] for r in settled)
    S["actual_count"] = len(settled)
    S["all_settled"] = len(settled) == len(rows) and rows
    S["count"] = len(rows)
    S["no_amount"] = [r for r in rows if r["no_amount"]]
    S["by_status"] = defaultdict(float)
    for r in rows:
        S["by_status"][r["status"]] += r["forecast"]["std"]
    S["by_cat"] = OrderedDict((c, {"forecast": 0.0, "paid": 0.0, "low": 0.0, "high": 0.0}) for c in CATEGORIES)
    S["by_month"] = OrderedDict((m, {"forecast": 0.0, "paid": 0.0}) for m in MONTHS)
    S["by_country"] = defaultdict(float)
    for r in rows:
        c = S["by_cat"][r["category"]]
        c["forecast"] += r["forecast"]["std"]
        c["low"] += r["forecast"]["low"]
        c["high"] += r["forecast"]["high"]
        c["paid"] += r["paid"]
        S["by_country"][r["country"] or "共通"] += r["forecast"]["std"]
        for m, ratio in r["alloc"].items():
            S["by_month"][m]["forecast"] += r["forecast"]["std"] * ratio
            S["by_month"][m]["paid"] += r["paid"] * ratio
    # 資金
    budget = {r["id"]: num(r["amount_jpy"]) for r in funds if r["type"] == "予算"}
    avail_rows = [r for r in funds if r["type"] == "資金"]
    entered = [num(r["amount_jpy"]) for r in avail_rows if num(r["amount_jpy"]) is not None]
    S["budget_ideal"] = budget.get("budget_ideal")
    S["budget_cap"] = budget.get("budget_cap")
    S["available"] = sum(entered) if entered else None  # 未入力なら None
    S["available_rows"] = avail_rows
    # 利用可能資金 = これから支払いに使える資金（支払済み分は含めない前提）
    S["gap"] = None if S["available"] is None else S["available"] - S["remaining"]
    S["vs_ideal"] = {s: S["budget_ideal"] - S["forecast"][s] for s in SCENARIOS}
    S["vs_cap"] = {s: S["budget_cap"] - S["forecast"][s] for s in SCENARIOS}
    return S


# ---------------------------------------------------------------- 検証
def validate(expenses, tasks, articles, timeline, problems):
    ids = defaultdict(int)
    for r in expenses:
        ids[r["id"]] += 1
        if r["category"] not in CATEGORIES:
            problems.append(f"{r['id']}: 費目「{r['category']}」が定義外です")
        if r["status"] not in EXPENSE_STATUS:
            problems.append(f"{r['id']}: 区分「{r['status']}」は {'/'.join(EXPENSE_STATUS)} のいずれかにしてください")
        if r["status"] in ("確定", "見積") and not (r["source"] or r["evidence"]):
            problems.append(f"{r['id']}: 区分が{r['status']}なのに根拠（source/evidence）が空です")
        if r["status"] == "実績" and not r["actual_jpy"]:
            problems.append(f"{r['id']}: 区分が実績なのに actual_jpy が空です")
        if r["actual_jpy"] and r["status"] != "実績":
            problems.append(f"{r['id']}: actual_jpy があるので区分を「実績」にしてください")
        if r["actual_jpy"] and not r["evidence"]:
            problems.append(f"{r['id']}: 実績に証憑（evidence）が未記入です")
        if r["paid_jpy"] and r["status"] != "未確認" and not r["evidence"]:
            problems.append(f"{r['id']}: 証憑がない支払済み額は区分を「未確認」にしてください")
        if re.search(r"\d{6,}|@", r["evidence"]):
            problems.append(f"{r['id']}: evidence 欄に番号・メール等の個人情報らしき値があります（公開リポジトリ）")
        if r["status"] == "確定" and r["paid_jpy"] and not r["evidence"]:
            problems.append(f"{r['id']}: 支払済みですが領収書等の証憑（evidence）が未記入です")
        for k in ("period_start", "period_end", "due_date", "paid_date", "collected_on"):
            try:
                date(r[k])
            except ValueError:
                problems.append(f"{r['id']}: {k}「{r[k]}」は YYYY-MM-DD 形式にしてください")
        for k in ("low_local", "std_local", "high_local", "paid_jpy", "actual_jpy", "actual_local", "actual_fx"):
            try:
                num(r[k])
            except ValueError:
                problems.append(f"{r['id']}: {k}「{r[k]}」が数値ではありません")
    for r in expenses:
        if r["issue"] and not r["issue"].startswith("https://github.com/Rikkyhub/studying-abroad/issues/"):
            problems.append(f"{r['id']}: issue 列は Issue の URL にしてください")
        try:
            date(r["recheck_by"])
        except ValueError:
            problems.append(f"{r['id']}: recheck_by は YYYY-MM-DD 形式にしてください")
    for r in tasks:
        if r["priority"] not in ("1", "2", "3", "4"):
            problems.append(f"{r['id']}: 優先度は 1〜4（1が最優先）にしてください")
    for r in tasks:
        ids[r["id"]] += 1
        if r["status"] not in TASK_STATUS:
            problems.append(f"{r['id']}: 進捗「{r['status']}」は {'/'.join(TASK_STATUS)} のいずれかにしてください")
        try:
            date(r["deadline"])
        except ValueError:
            problems.append(f"{r['id']}: 期限「{r['deadline']}」は YYYY-MM-DD 形式にしてください")
    for r in articles:
        ids[r["id"]] += 1
        if r["status"] not in ARTICLE_STATUS:
            problems.append(f"{r['id']}: 記事状態「{r['status']}」は {'/'.join(ARTICLE_STATUS)} のいずれかにしてください")
    for r in timeline:
        ids[r["id"]] += 1
    for k, n in ids.items():
        if n > 1:
            problems.append(f"ID {k} が {n} 回使われています（IDは一意にしてください）")


# ---------------------------------------------------------------- Markdown 生成
def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "／").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def md_link(src):
    if src.startswith("http"):
        return f"[出典]({src})"
    return src


def gen_budget_summary(S):
    fc = S["forecast"]
    lines = [
        f"集計日: {today().isoformat()}（`python3 scripts/build.py` で再計算）",
        "",
        md_table(["#", "指標", "金額", "説明"], [
            [1, "6か月間の総費用予測（標準）", yen(fc["std"]), f"低予算 {yen(fc['low'])} ／ 余裕 {yen(fc['high'])}"],
            [2, "支払済み総額", yen(S["paid"]), "expenses.csv の paid_jpy 合計"],
            [3, "今後必要な支払額（標準）", yen(S["remaining"]), "総費用予測 − 支払済み（二重計上なし）"],
            [4, "利用可能資金", yen(S["available"], "未入力"), "data/funds.csv の「資金」行の合計（これから使える資金）"],
            [5, "今後の資金不足額・余剰額", "未算出（資金が未入力）" if S["gap"] is None else (("余剰 " if S["gap"] >= 0 else "不足 ") + yen(abs(S["gap"]))), "利用可能資金 − 今後必要な支払額"],
            [6, "理想予算250万円に対する残額", yen(S["vs_ideal"]["std"]), f"低予算 {yen(S['vs_ideal']['low'])} ／ 余裕 {yen(S['vs_ideal']['high'])}（マイナス＝超過）"],
            [6, "上限300万円に対する残額", yen(S["vs_cap"]["std"]), f"低予算 {yen(S['vs_cap']['low'])} ／ 余裕 {yen(S['vs_cap']['high'])}（マイナス＝超過）"],
            [7, "最終的な実費総額", yen(S["actual"]) + ("" if S["all_settled"] else f"（{S['actual_count']}/{S['count']}件確定・途中経過）"), "status=実績 の actual_jpy 合計。全行が実績になった時点で確定"],
        ]),
        "",
        (f"> ⚠️ 金額が未入力の費目が {len(S['no_amount'])} 件あり、総費用予測に含まれていません: " + "、".join(f"{r['id']} {r['item']}" for r in S["no_amount"]) + "\n" if S["no_amount"] else ""),
        "**区分別の内訳（標準）**: " + " ／ ".join(f"{k} {yen(S['by_status'].get(k, 0))}" for k in EXPENSE_STATUS),
    ]
    return "\n".join(lines)


def gen_budget_by_cat(S):
    rows = []
    for c, v in S["by_cat"].items():
        rows.append([c, yen(v["low"]), yen(v["forecast"]), yen(v["high"]), yen(v["paid"]), yen(v["forecast"] - v["paid"])])
    rows.append(["**合計**", f"**{yen(S['forecast']['low'])}**", f"**{yen(S['forecast']['std'])}**", f"**{yen(S['forecast']['high'])}**", f"**{yen(S['paid'])}**", f"**{yen(S['remaining'])}**"])
    return md_table(["費目", "低予算", "標準", "余裕", "支払済み", "今後必要(標準)"], rows)


def gen_budget_by_month(S):
    rows = [[MONTHS[m], yen(v["forecast"]), yen(v["paid"])] for m, v in S["by_month"].items()]
    return ("期間をまたぐ費用（保険・固定費・授業料など）は利用期間の日数で月に按分しています。\n\n"
            + md_table(["月", "費用予測(標準)", "うち支払済み"], rows))


def gen_budget_by_country(S):
    rows = sorted(S["by_country"].items(), key=lambda x: -x[1])
    return md_table(["国・地域", "費用予測(標準)"], [[k, yen(v)] for k, v in rows])


def gen_budget_detail(rows):
    out = []
    for c in CATEGORIES:
        rs = [r for r in rows if r["category"] == c]
        if not rs:
            continue
        out.append(f"#### {c}\n")
        out.append(md_table(
            ["ID", "内容・支払先", "期間", "支払予定日", "区分", "現地通貨(標準)", "見積(低/標準/余裕)", "支払済み", "今後必要", "実費", "根拠"],
            [[r["id"], f"{r['item']}（{r['payee']}）" if r["payee"] else r["item"],
              f"{r['period_start']}〜{r['period_end']}" if r["period_start"] else "—",
              r["due_date"] or "—", r["status"],
              f"{r['currency']} {num(r['std_local']):,.0f}" if r["currency"] != "JPY" and num(r["std_local"]) is not None else "—",
              f"{yen(r['est']['low'])} / {yen(r['est']['std'])} / {yen(r['est']['high'])}",
              yen(r["paid"]) if r["paid"] else "—", yen(r["remaining"]), yen(r["actual"]),
              " ".join(md_link(s) for s in (r["source"], r["evidence"]) if s) or "—"] for r in rs]))
        notes = [f"- {r['id']}: {r['note']}" for r in rs if r["note"]]
        if notes:
            out.append("\n" + "\n".join(notes))
        out.append("")
    return "\n".join(out)


def gen_fx(fx):
    return md_table(["通貨", "1単位あたり円", "レート日付", "出典"],
                    [[k, f"{v['rate']:g}", v["date"], md_link(v["source"]) if v["source"] else "—"] for k, v in fx.items() if k != "JPY"])


def gen_tasks(tasks, group_field="phase"):
    groups = OrderedDict()
    for t in sorted(tasks, key=lambda t: (t["deadline"] or "9999")):
        groups.setdefault(t[group_field], []).append(t)
    out = []
    for g, ts in groups.items():
        out.append(f"### {g}\n")
        out.append(md_table(["ID", "", "タスク", "期限", "進捗", "担当", "費用目安", "次のアクション", "根拠", "Issue"],
                            [[t["id"], "✅" if t["status"] in ("完了", "不要") else ("⚠️" if t["status"] == "要確認" else "⬜"),
                              t["task"], t["deadline"] or "—", t["status"], t["owner"] or "本人", t["cost_note"] or "—", t["next_action"] or "—",
                              md_link(t["source"]) if t["source"].startswith("http") else "—",
                              f"[#{t['issue'].rsplit('/', 1)[-1]}]({t['issue']})" if t["issue"] else "—"] for t in ts]))
        out.append("")
    return "\n".join(out)


def task_progress(tasks):
    done = sum(1 for t in tasks if t["status"] in ("完了", "不要"))
    return done, len(tasks)


def next_tasks(tasks, n=8):
    open_ = [t for t in tasks if t["status"] not in ("完了", "不要", "保留")]
    return sorted(open_, key=lambda t: (t["deadline"] or "9999", t["priority"] or "9"))[:n]


def gen_next_tasks(tasks):
    return md_table(["期限", "タスク", "進捗", "次のアクション"],
                    [[t["deadline"] or "—", t["task"], t["status"], t["next_action"]] for t in next_tasks(tasks)])


def gen_timeline(timeline):
    return md_table(["期間", "区分", "予定", "場所", "状態", "メモ"],
                    [[f"{r['start']}〜{r['end']}" if r["end"] and r["end"] != r["start"] else r["start"], r["phase"], r["title"], r["place"], r["status"], r["note"]] for r in timeline])


def gen_articles(articles):
    groups = OrderedDict()
    for a in articles:
        groups.setdefault(a["series"], []).append(a)
    out = []
    for g, as_ in groups.items():
        out.append(f"### {g}\n")
        out.append(md_table(["ID", "記事タイトル案", "状態", "使う資料", "必要な体験記録", "下書き"],
                            [[a["id"], a["title"], a["status"], a["materials"], a["needs"], a["draft"] or "—"] for a in as_]))
        out.append("")
    counts = defaultdict(int)
    for a in articles:
        counts[a["status"]] += 1
    return "状態の集計: " + " ／ ".join(f"{s} {counts.get(s, 0)}" for s in ARTICLE_STATUS) + "\n\n" + "\n".join(out)


def gen_unconfirmed(rows, tasks):
    items = [f"- 費用 {r['id']}: {r['item']}（{'金額未入力・集計に含まれていない' if r['no_amount'] else '暫定 ' + yen(r['forecast']['std'])}）" for r in rows if r["status"] == "未確認"]
    items += [f"- タスク {t['id']}: {t['task']}（{t['next_action']}）" for t in tasks if t["status"] == "要確認"]
    return "\n".join(items) if items else "なし"


def gen_problems(problems):
    return "\n".join(f"- ⚠️ {p}" for p in problems) if problems else "- 問題は見つかりませんでした"


def apply_auto(text, blocks):
    for name, content in blocks.items():
        pat = re.compile(rf"(<!-- AUTO:{name} -->)(.*?)(<!-- /AUTO:{name} -->)", re.S)
        text = pat.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", text)
    return text


# ---------------------------------------------------------------- HTML 生成
def esc(s):
    return html.escape(str(s))


def build_html(S, rows, tasks, articles, timeline, fx, problems):
    done, total = task_progress(tasks)
    fc = S["forecast"]
    cap = S["budget_cap"]
    ideal = S["budget_ideal"]
    data = {
        "months": [{"key": m, "label": MONTHS[m], "forecast": round(v["forecast"]), "paid": round(v["paid"])} for m, v in S["by_month"].items()],
        "cats": [{"label": c, "forecast": round(v["forecast"]), "paid": round(v["paid"]), "low": round(v["low"]), "high": round(v["high"])} for c, v in S["by_cat"].items()],
    }

    def tile(label, value, sub=""):
        return f'<div class="tile"><div class="tile-label">{esc(label)}</div><div class="tile-value">{esc(value)}</div><div class="tile-sub">{esc(sub)}</div></div>'

    gap_text = "未入力" if S["gap"] is None else ("余剰 " if S["gap"] >= 0 else "不足 ") + man(abs(S["gap"]))
    tiles = "".join([
        tile("6か月の総費用予測（標準）", man(fc["std"]), f"低予算 {man(fc['low'])} ／ 余裕 {man(fc['high'])}" + (f"｜金額未入力 {len(S['no_amount'])}件は含まず" if S["no_amount"] else "")),
        tile("支払済み", man(S["paid"]), yen(S["paid"])),
        tile("今後必要な支払額", man(S["remaining"]), "総費用予測 − 支払済み"),
        tile("利用可能資金", man(S["available"]) if S["available"] is not None else "未入力", "data/funds.csv に入力"),
        tile("資金の不足・余剰", gap_text, "利用可能資金 − 今後必要額"),
        tile("理想250万円まで", man(S["vs_ideal"]["std"]), "マイナスは超過"),
        tile("上限300万円まで", man(S["vs_cap"]["std"]), "マイナスは超過"),
        tile("実費総額", man(S["actual"]) if S["actual_count"] else "まだなし", f"実績 {S['actual_count']}/{S['count']}件"),
    ])

    # 予算バー（標準予測を 上限300万 に対して表示）
    scale = max(cap, fc["high"]) * 1.02
    def pct(v):
        return f"{max(v, 0) / scale * 100:.2f}%"
    budget_bar = f"""
<div class="bbar" role="img" aria-label="費用予測と予算の比較">
  <div class="bbar-track">
    <div class="bbar-range" style="left:{pct(fc['low'])};width:calc({pct(fc['high'])} - {pct(fc['low'])})" title="低予算〜余裕の幅 {man(fc['low'])}〜{man(fc['high'])}"></div>
    <div class="bbar-paid" style="width:{pct(S['paid'])}" title="支払済み {yen(S['paid'])}"></div>
    <div class="bbar-std" style="left:{pct(fc['std'])}" title="標準予測 {yen(fc['std'])}"></div>
    <div class="bbar-line" style="left:{pct(ideal)}"><span>理想 {man(ideal)}</span></div>
    <div class="bbar-line cap" style="left:{pct(cap)}"><span>上限 {man(cap)}</span></div>
  </div>
  <div class="legend">
    <span><i class="sw sw-paid"></i>支払済み {man(S['paid'])}</span>
    <span><i class="sw sw-std"></i>標準予測 {man(fc['std'])}</span>
    <span><i class="sw sw-range"></i>低予算〜余裕 {man(fc['low'])}〜{man(fc['high'])}</span>
  </div>
</div>"""

    nt = "".join(
        f'<li><span class="due">{esc(t["deadline"] or "期限未定")}</span><span class="pill p-{esc(t["status"])}">{esc(t["status"])}</span>'
        f'<b>{esc(t["task"])}</b><span class="na">→ {esc(t["next_action"])}</span></li>' for t in next_tasks(tasks, 10))

    phases = OrderedDict()
    for t in tasks:
        phases.setdefault(t["phase"], [0, 0])
        phases[t["phase"]][1] += 1
        if t["status"] in ("完了", "不要"):
            phases[t["phase"]][0] += 1
    phase_rows = "".join(
        f'<div class="prow"><span class="plabel">{esc(p)}</span><span class="ptrack"><span style="width:{d / n * 100:.0f}%"></span></span><span class="pnum">{d}/{n}</span></div>'
        for p, (d, n) in phases.items())

    tl = "".join(
        f'<li class="tl-{esc(r["status"])}"><div class="tl-date">{esc(r["start"][5:].replace("-", "/"))}{("〜" + esc(r["end"][5:].replace("-", "/"))) if r["end"] and r["end"] != r["start"] else ""}</div>'
        f'<div class="tl-body"><b>{esc(r["title"])}</b> <span class="pill p-{esc(r["status"])}">{esc(r["status"])}</span><div class="muted">{esc(r["place"])}　{esc(r["note"])}</div></div></li>'
        for r in timeline)

    unc = [r for r in rows if r["status"] == "未確認"]
    unc_html = "".join(f'<li><b>{esc(r["item"])}</b> <span class="muted">{esc(r["category"])}・{"金額未入力（集計外）" if r["no_amount"] else "暫定 " + yen(r["forecast"]["std"])}</span></li>' for r in unc)
    unc_tasks = "".join(f'<li><b>{esc(t["task"])}</b> <span class="muted">{esc(t["next_action"])}</span></li>' for t in tasks if t["status"] == "要確認")

    exp_rows = "".join(
        f'<tr data-st="{esc(r["status"])}"><td>{esc(r["id"])}</td><td>{esc(r["item"])}<div class="muted">{esc(r["payee"])}</div></td><td>{esc(r["category"])}</td><td>{esc(r["country"])}</td>'
        f'<td><span class="pill p-{esc(r["status"])}">{esc(r["status"])}</span></td><td class="n">{yen(r["est"]["low"])}</td><td class="n">{"未入力" if r["no_amount"] else yen(r["forecast"]["std"])}</td><td class="n">{yen(r["est"]["high"])}</td>'
        f'<td class="n">{yen(r["paid"]) if r["paid"] else "—"}</td><td class="n">{yen(r["actual"])}</td>'
        f'<td>{"".join(f"<a href={chr(34)}{esc(s)}{chr(34)} target=_blank rel=noopener>出典</a> " if s.startswith("http") else esc(s) + " " for s in (r["source"], r["evidence"]) if s) or "—"}</td></tr>'
        for r in rows)

    art_counts = defaultdict(int)
    for a in articles:
        art_counts[a["status"]] += 1
    art_html = "".join(
        f'<li><span class="pill p-{esc(a["status"])}">{esc(a["status"])}</span> <b>{esc(a["title"])}</b><div class="muted">{esc(a["series"])}｜資料: {esc(a["materials"])}</div></li>'
        for a in articles)
    art_summary = " ／ ".join(f"{s} {art_counts.get(s, 0)}" for s in ARTICLE_STATUS)

    docs = [("README.md", "全体概要"), ("docs/01-timeline.md", "スケジュール"), ("docs/02-budget.md", "総費用"),
            ("docs/03-preparation.md", "準備ToDo"), ("research/visa-and-immigration.md", "ビザ・再入国"),
            ("research/baguio-diving.md", "バギオ発ダイビング"), ("research/capetown-diving.md", "ケープタウン発ダイビング"),
            ("research/baguio-sightseeing.md", "バギオ観光"), ("research/capetown-sightseeing.md", "ケープタウン観光"),
            ("research/food-and-living.md", "食費・生活"), ("research/winter-clothing.md", "冬服"),
            ("research/safety-and-health.md", "治安・健康"), ("research/philippines-pines.md", "PINES・フィリピン"),
            ("research/africa-trip.md", "5月アフリカ周遊"), ("research/second-school.md", "2校目（ケープタウン）"),
            ("research/sources.md", "出典・調査ログ"), ("blog/article-ideas.md", "記事候補"), ("blog/experience-log.md", "体験・実費ログ"),
            ("data/expenses.csv", "費用CSV"), ("data/tasks.csv", "タスクCSV")]
    docs_html = "".join(f'<a class="doc" href="{esc(p)}">{esc(t)}<span>{esc(p)}</span></a>' for p, t in docs)

    prob_html = "".join(f"<li>{esc(p)}</li>" for p in problems) or "<li>問題なし</li>"
    fx_html = "、".join(f"1 {k} = {v['rate']:g}円（{v['date']}）" for k, v in fx.items() if k != "JPY")

    return fill(HTML_TEMPLATE,
        updated=today().isoformat(), tiles=tiles, budget_bar=budget_bar, next_tasks=nt, phase_rows=phase_rows,
        done=done, total=total, done_pct=f"{done / total * 100:.0f}" if total else "0",
        timeline=tl, unc=unc_html or "<li>なし</li>", unc_tasks=unc_tasks or "<li>なし</li>", unc_count=len(unc),
        exp_rows=exp_rows, articles=art_html, art_summary=art_summary, docs=docs_html,
        problems=prob_html, problem_count=len(problems), fx=esc(fx_html),
        data=json.dumps(data, ensure_ascii=False),
    )


def fill(template, **kw):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(kw[m.group(1)]), template)


HTML_TEMPLATE = (Path(__file__).resolve().parent / "dashboard_template.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------- main
TARGETS = {
    "budget": ROOT / "docs" / "02-budget.md",
    "prep": ROOT / "docs" / "03-preparation.md",
    "timeline": ROOT / "docs" / "01-timeline.md",
    "articles": ROOT / "blog" / "article-ideas.md",
    "readme": ROOT / "README.md",
    "html": ROOT / "index.html",
}


def render_all(S, rows, tasks, articles, timeline, fx, problems):
    """生成物 {path: text} を返す（書き込みはしない）"""
    out = {}
    done, total = task_progress(tasks)
    blocks = {
        "budget": {"summary": gen_budget_summary(S), "by_category": gen_budget_by_cat(S), "by_month": gen_budget_by_month(S),
                   "by_country": gen_budget_by_country(S), "detail": gen_budget_detail(rows), "fx": gen_fx(fx)},
        "prep": {"tasks": gen_tasks(tasks)},
        "timeline": {"timeline": gen_timeline(timeline), "by_month": gen_budget_by_month(S)},
        "articles": {"articles": gen_articles(articles)},
        "readme": {
            "status": "\n".join([
                f"集計基準日: {today().isoformat()}（data/meta.csv）",
                "",
                md_table(["項目", "現状"], [
                    ["準備タスク", f"{done}/{total} 完了"],
                    ["総費用予測（標準）", f"{yen(S['forecast']['std'])}（低予算 {yen(S['forecast']['low'])} ／ 余裕 {yen(S['forecast']['high'])}）"],
                    ["金額未入力の費目", f"{len(S['no_amount'])} 件（総額に含まれない）"],
                    ["支払済み（証憑確認済み）", yen(S["paid_verified"])],
                    ["支払済み（証憑未確認・暫定）", yen(S["paid"] - S["paid_verified"])],
                    ["今後必要な支払額（標準）", yen(S["remaining"])],
                    ["利用可能資金", yen(S["available"], "未入力")],
                    ["上限300万円までの残り（標準）", yen(S["vs_cap"]["std"])],
                    ["記事候補", f"{len(articles)} 件"],
                ]),
            ]),
            "next": gen_next_tasks(tasks),
            "unconfirmed": gen_unconfirmed(rows, tasks),
            "problems": gen_problems(problems),
        },
    }
    for key, b in blocks.items():
        out[TARGETS[key]] = apply_auto(TARGETS[key].read_text(encoding="utf-8"), b)
    out[TARGETS["html"]] = build_html(S, rows, tasks, articles, timeline, fx, problems)
    return out


def main():
    check_only = "--check" in sys.argv
    problems = []
    for r in read_csv("meta.csv"):
        _META[r["key"]] = r["value"]
    fx = load_fx()
    expenses = read_csv("expenses.csv")
    tasks = read_csv("tasks.csv")
    articles = read_csv("articles.csv")
    timeline = read_csv("timeline.csv")
    funds = read_csv("funds.csv")
    validate(expenses, tasks, articles, timeline, problems)
    rows = compute(expenses, fx, problems)
    S = summarize(rows, funds)

    print(f"総費用予測  低予算 {yen(S['forecast']['low'])} / 標準 {yen(S['forecast']['std'])} / 余裕 {yen(S['forecast']['high'])}")
    print(f"支払済み {yen(S['paid'])}（うち証憑確認済み {yen(S['paid_verified'])}）  今後必要 {yen(S['remaining'])}  利用可能資金 {yen(S['available'], '未入力')}")
    print(f"金額未入力 {len(S['no_amount'])} 件  タスク {task_progress(tasks)[0]}/{task_progress(tasks)[1]} 完了  記事候補 {len(articles)} 件")
    print(f"検証: {len(problems)} 件の指摘")
    for p in problems:
        print("  -", p)
    outputs = render_all(S, rows, tasks, articles, timeline, fx, problems)
    if check_only:
        stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if p.read_text(encoding="utf-8") != text]
        if stale:
            print("生成物が CSV と一致しません。`python3 scripts/build.py` を実行してコミットしてください: " + ", ".join(stale))
        return 1 if (problems or stale) else 0
    for p, text in outputs.items():
        p.write_text(text, encoding="utf-8", newline="\n")
    print("更新しました: " + ", ".join(str(p.relative_to(ROOT)) for p in outputs))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
