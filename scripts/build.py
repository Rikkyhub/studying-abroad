# -*- coding: utf-8 -*-
"""
集計・ダッシュボード生成スクリプト（studying-abroad）

使い方（リポジトリのルートで実行）:
    python3 scripts/build.py           集計して生成物を更新
    python3 scripts/build.py --check   検証のみ。生成物が CSV と一致しなければ失敗（CI用）

- data/*.csv（正本）を読み込み、以下を再生成する。
    * Markdown の <!-- AUTO:名前 --> 〜 <!-- /AUTO:名前 --> の間だけ
    * index.html（全体を再生成）
- CSV 自体は一切書き換えない。
- 公開用の匿名モデル: 個人の支払い・実費・資金は扱わない。総額は見積（低/標準/余裕）の合計のみ。
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
EXPENSE_STATUS = ["見積", "未確認"]  # 公開CSVでは「確定」「実績」を使わない
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
    """各行の見積を円に換算する。金額のない行は 0 ではなく None（金額未入力）として扱う。"""
    out = []
    for r in expenses:
        cur = r["currency"] or "JPY"
        rate = fx.get(cur, {}).get("rate")
        if rate is None:
            problems.append(f"{r['id']}: 通貨 {cur} の為替レートが data/fx.csv にありません")
            rate = 0
        raw = {s: num(r[f"{s}_local"]) for s in SCENARIOS}
        no_amount = all(v is None for v in raw.values())
        est = {s: None if raw[s] is None else raw[s] * rate for s in SCENARIOS}
        if not no_amount:
            if est["std"] is None:
                est["std"] = est["low"] if est["low"] is not None else est["high"]
            if est["low"] is None:
                est["low"] = est["std"]
            if est["high"] is None:
                est["high"] = est["std"]
        out.append({**r, "rate": rate, "est": est, "no_amount": no_amount, "alloc": allocate(r)})
    return out


def _z():
    return {s: 0.0 for s in SCENARIOS}


def summarize(rows, funds):
    """見積の合計だけを集計する。支払い・実費・資金・残額の概念は持たない。
    - total: 金額のある全行（見積＋未確認）の合計。各行は1回だけ加算（二重計上なし）
    - by_status: 見積 / 未確認 の内訳（合計すると total に一致）
    - 金額未入力の行は 0 円として扱わず no_amount に列挙する
    """
    S = {"count": len(rows)}
    priced = [r for r in rows if not r["no_amount"]]
    S["total"] = {s: sum(r["est"][s] for r in priced) for s in SCENARIOS}
    S["by_status"] = OrderedDict((k, _z()) for k in EXPENSE_STATUS)
    S["status_count"] = OrderedDict((k, 0) for k in EXPENSE_STATUS)
    for r in rows:
        S["status_count"][r["status"]] = S["status_count"].get(r["status"], 0) + 1
    for r in priced:
        b = S["by_status"].setdefault(r["status"], _z())
        for s in SCENARIOS:
            b[s] += r["est"][s]
    S["no_amount"] = [r for r in rows if r["no_amount"]]
    S["unverified"] = [r for r in rows if r["status"] == "未確認"]
    S["by_cat"] = OrderedDict((c, _z()) for c in CATEGORIES)
    S["by_month"] = OrderedDict((m, {"見積": 0.0, "未確認": 0.0}) for m in MONTHS)
    S["by_country"] = defaultdict(float)
    for r in priced:
        c = S["by_cat"][r["category"]]
        for s in SCENARIOS:
            c[s] += r["est"][s]
        S["by_country"][r["country"] or "共通"] += r["est"]["std"]
        for m, ratio in r["alloc"].items():
            S["by_month"][m][r["status"]] += r["est"]["std"] * ratio
    budget = {r["id"]: num(r["amount_jpy"]) for r in funds if r["type"] == "予算"}
    S["budget_ideal"] = budget.get("budget_ideal")
    S["budget_cap"] = budget.get("budget_cap")
    S["budget_africa"] = budget.get("budget_africa")
    S["africa_total"] = sum(r["est"]["std"] for r in priced if r["id"].startswith("AF-"))
    # 予算目標との差（予算 − 見積合計）。マイナスは超過。支払いや資金の残高ではない
    S["vs_ideal"] = {s: S["budget_ideal"] - S["total"][s] for s in SCENARIOS}
    S["vs_cap"] = {s: S["budget_cap"] - S["total"][s] for s in SCENARIOS}
    return S


# ---------------------------------------------------------------- 検証
PRIVATE_PATTERNS = [re.compile(p) for p in (r"[\w.+-]+@[\w-]+\.[\w.]+", r"\b\d{9,}\b")]


def validate(expenses, tasks, articles, timeline, problems, funds=()):
    ids = defaultdict(int)
    for r in expenses:
        ids[r["id"]] += 1
        if r["category"] not in CATEGORIES:
            problems.append(f"{r['id']}: 費目「{r['category']}」が定義外です")
        if r["status"] not in EXPENSE_STATUS:
            problems.append(f"{r['id']}: 区分「{r['status']}」は {'/'.join(EXPENSE_STATUS)} のいずれかにしてください（公開CSVに確定・実績は使わない）")
        has_amount = any(r[f"{s}_local"] for s in SCENARIOS)
        if r["status"] == "見積" and not r["source"].startswith("http"):
            problems.append(f"{r['id']}: 区分が見積なのに出典URL（source）が空です。出典がなければ「未確認」にしてください")
        if r["status"] == "見積" and not has_amount:
            problems.append(f"{r['id']}: 区分が見積なのに金額が未入力です。金額がなければ「未確認」にしてください")
        for k in ("period_start", "period_end", "due_date", "collected_on", "recheck_by"):
            try:
                date(r[k])
            except ValueError:
                problems.append(f"{r['id']}: {k}「{r[k]}」は YYYY-MM-DD 形式にしてください")
        for k in ("low_local", "std_local", "high_local"):
            try:
                v = num(r[k])
                if v is not None and v < 0:
                    problems.append(f"{r['id']}: {k} は0以上にしてください")
            except ValueError:
                problems.append(f"{r['id']}: {k}「{r[k]}」が数値ではありません")
        if r["issue"] and not r["issue"].startswith("https://github.com/Rikkyhub/studying-abroad/issues/"):
            problems.append(f"{r['id']}: issue 列は Issue の URL にしてください")
    for r in funds:
        if r["type"] != "予算":
            problems.append(f"{r['id']}: funds.csv は予算目標（type=予算）だけを置く公開用モデルです")
    for r in tasks:
        ids[r["id"]] += 1
        if r["priority"] not in ("1", "2", "3", "4"):
            problems.append(f"{r['id']}: 優先度は 1〜4（1が最優先）にしてください")
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
    for name, rs in (("expenses", expenses), ("tasks", tasks), ("articles", articles), ("timeline", timeline)):
        for r in rs:
            for col, v in r.items():
                if col in ("source", "issue") or v.startswith("http"):
                    continue
                if any(p.search(v) for p in PRIVATE_PATTERNS):
                    problems.append(f"{name} {r.get('id', '')}:{col}: 番号・メール等の個人情報らしき値があります（公開リポジトリ）")


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


def fmt3(d):
    return f"低予算 {yen(d['low'])} ／ 標準 {yen(d['std'])} ／ 余裕 {yen(d['high'])}"


def gen_budget_summary(S):
    t = S["total"]
    na = S["no_amount"]
    lines = [
        f"集計日: {today().isoformat()}（`python3 scripts/build.py` で再計算）。**公開用の匿名モデル**で、個人の支払い・実費・資金は含みません。",
        "",
        md_table(["指標", "標準", "低予算 ／ 余裕", "説明"], [
            ["見積合計（金額入力済みの全行）", yen(t["std"]), f"{yen(t['low'])} ／ {yen(t['high'])}", "各行を1回だけ加算。金額未入力の行は含まない"],
            ["うち 見積（出典あり）", yen(S["by_status"]["見積"]["std"]), f"{yen(S['by_status']['見積']['low'])} ／ {yen(S['by_status']['見積']['high'])}", f"{S['status_count']['見積']} 件"],
            ["うち 未確認（出典なし・推定）", yen(S["by_status"]["未確認"]["std"]), f"{yen(S['by_status']['未確認']['low'])} ／ {yen(S['by_status']['未確認']['high'])}", f"{S['status_count']['未確認']} 件（金額未入力を含む）。費用として加算するだけで、何からも差し引かない"],
            ["金額未入力", f"{len(na)} 件", "—", "0円ではない。見積合計は下限の目安で、6か月総額は未完成"],
            ["目標250万円との差", yen(S["vs_ideal"]["std"]), f"{yen(S['vs_ideal']['low'])} ／ {yen(S['vs_ideal']['high'])}", "予算目標 − 見積合計（マイナス＝超過）"],
            ["上限300万円との差", yen(S["vs_cap"]["std"]), f"{yen(S['vs_cap']['low'])} ／ {yen(S['vs_cap']['high'])}", "予算目標 − 見積合計（マイナス＝超過）"],
            ["5月アフリカ周遊（AF-行）", yen(S["africa_total"]), "—", f"配分目標 {yen(S['budget_africa'])}（総予算の内数）"],
        ]),
        "",
        ("**金額未入力（0円扱いしない）**: " + "、".join(f"{r['id']} {r['item']}" for r in na) if na else "金額未入力の行はありません。"),
    ]
    return "\n".join(lines)


def gen_budget_by_cat(S):
    rows = [[c, yen(v["low"]), yen(v["std"]), yen(v["high"])] for c, v in S["by_cat"].items()]
    t = S["total"]
    rows.append(["**合計**", f"**{yen(t['low'])}**", f"**{yen(t['std'])}**", f"**{yen(t['high'])}**"])
    return md_table(["費目", "低予算", "標準", "余裕"], rows) + "\n\n金額未入力の行は含みません（0円ではありません）。"


def gen_budget_by_month(S):
    rows = [[MONTHS[m], yen(v["見積"] + v["未確認"]), yen(v["見積"]), yen(v["未確認"])] for m, v in S["by_month"].items()]
    return ("期間をまたぐ費用（保険・授業料など）は利用期間の日数で月に按分しています（標準プラン・金額入力済みの行のみ）。\n\n"
            + md_table(["月", "見積合計(標準)", "うち見積", "うち未確認"], rows))


def gen_budget_by_country(S):
    rows = sorted(S["by_country"].items(), key=lambda x: (-x[1], x[0]))
    return md_table(["国・地域", "見積合計(標準)"], [[k, yen(v)] for k, v in rows])


def amount_cell(r, s):
    return "金額未入力" if r["no_amount"] else yen(r["est"][s])


def gen_budget_detail(rows):
    out = []
    for c in CATEGORIES:
        rs = [r for r in rows if r["category"] == c]
        if not rs:
            continue
        out.append(f"#### {c}\n")
        out.append(md_table(
            ["ID", "内容", "期間", "区分", "現地通貨(標準)", "低予算", "標準", "余裕", "出典"],
            [[r["id"], f"{r['item']}（{r['payee']}）" if r["payee"] and r["payee"] != "—" else r["item"],
              f"{r['period_start']}〜{r['period_end']}" if r["period_start"] else "—",
              r["status"],
              f"{r['currency']} {num(r['std_local']):,.0f}" if r["currency"] != "JPY" and num(r["std_local"]) is not None else "—",
              amount_cell(r, "low"), amount_cell(r, "std"), amount_cell(r, "high"),
              md_link(r["source"]) if r["source"] else "—"] for r in rs]))
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
    items = [f"- 費用 {r['id']}: {r['item']}（{'金額未入力・見積合計に含まれていない（0円ではない）' if r['no_amount'] else '推定 ' + yen(r['est']['std']) + '・出典なし'}）" for r in rows if r["status"] == "未確認"]
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
    t = S["total"]
    cap = S["budget_cap"]
    ideal = S["budget_ideal"]
    est_std, unv_std = S["by_status"]["見積"]["std"], S["by_status"]["未確認"]["std"]
    data = {
        "months": [{"key": m, "label": MONTHS[m], "est": round(v["見積"]), "unv": round(v["未確認"])} for m, v in S["by_month"].items()],
        "cats": [{"label": c, "std": round(v["std"]), "low": round(v["low"]), "high": round(v["high"])} for c, v in S["by_cat"].items()],
    }

    def tile(label, value, sub=""):
        return f'<div class="tile"><div class="tile-label">{esc(label)}</div><div class="tile-value">{esc(value)}</div><div class="tile-sub">{esc(sub)}</div></div>'

    tiles = "".join([
        tile("見積合計（標準）", man(t["std"]), f"低予算 {man(t['low'])} ／ 余裕 {man(t['high'])}"),
        tile("うち 見積（出典あり）", man(est_std), f"{S['status_count']['見積']}件"),
        tile("うち 未確認（推定）", man(unv_std), f"{S['status_count']['未確認']}件・差し引きには使わない"),
        tile("金額未入力", f"{len(S['no_amount'])}件", "0円ではない・合計に含まない"),
        tile("目標250万円との差", man(S["vs_ideal"]["std"]), "予算目標 − 見積合計（マイナスは超過）"),
        tile("上限300万円との差", man(S["vs_cap"]["std"]), "予算目標 − 見積合計（マイナスは超過）"),
        tile("5月アフリカ周遊", man(S["africa_total"]), f"配分目標 {man(S['budget_africa'])}"),
        tile("準備タスク", f"{done}/{total}", "完了・不要の件数"),
    ])

    scale = max(cap, t["high"]) * 1.02

    def pct(v):
        return f"{max(v, 0) / scale * 100:.2f}%"
    budget_bar = f"""
<div class="bbar" role="img" aria-label="見積合計と予算目標の比較">
  <div class="bbar-track">
    <div class="bbar-range" style="left:{pct(t['low'])};width:calc({pct(t['high'])} - {pct(t['low'])})" title="低予算〜余裕 {man(t['low'])}〜{man(t['high'])}"></div>
    <div class="bbar-est" style="width:{pct(est_std)}" title="見積（出典あり） {yen(est_std)}"></div>
    <div class="bbar-unv" style="left:{pct(est_std)};width:{pct(unv_std)}" title="未確認（推定） {yen(unv_std)}"></div>
    <div class="bbar-std" style="left:{pct(t['std'])}" title="見積合計（標準） {yen(t['std'])}"></div>
    <div class="bbar-line" style="left:{pct(ideal)}"><span>目標 {man(ideal)}</span></div>
    <div class="bbar-line cap" style="left:{pct(cap)}"><span>上限 {man(cap)}</span></div>
  </div>
  <div class="legend">
    <span><i class="sw sw-est"></i>見積（出典あり） {man(est_std)}</span>
    <span><i class="sw sw-unv"></i>未確認（推定） {man(unv_std)}</span>
    <span><i class="sw sw-std"></i>見積合計（標準） {man(t['std'])}</span>
    <span><i class="sw sw-range"></i>低予算〜余裕 {man(t['low'])}〜{man(t['high'])}</span>
  </div>
</div>"""

    nt = "".join(
        f'<li><span class="due">{esc(x["deadline"] or "期限未定")}</span><span class="pill p-{esc(x["status"])}">{esc(x["status"])}</span>'
        f'<b>{esc(x["task"])}</b><span class="na">→ {esc(x["next_action"])}</span></li>' for x in next_tasks(tasks, 10))

    phases = OrderedDict()
    for x in tasks:
        phases.setdefault(x["phase"], [0, 0])
        phases[x["phase"]][1] += 1
        if x["status"] in ("完了", "不要"):
            phases[x["phase"]][0] += 1
    phase_rows = "".join(
        f'<div class="prow"><span class="plabel">{esc(p)}</span><span class="ptrack"><span style="width:{d / n * 100:.0f}%"></span></span><span class="pnum">{d}/{n}</span></div>'
        for p, (d, n) in phases.items())

    tl = "".join(
        f'<li><div class="tl-date">{esc(r["start"][5:].replace("-", "/"))}{("〜" + esc(r["end"][5:].replace("-", "/"))) if r["end"] and r["end"] != r["start"] else ""}</div>'
        f'<div class="tl-body"><b>{esc(r["title"])}</b> <span class="pill p-{esc(r["status"])}">{esc(r["status"])}</span><div class="muted">{esc(r["place"])}　{esc(r["note"])}</div></div></li>'
        for r in timeline)

    unc = S["unverified"]
    unc_html = "".join(f'<li><b>{esc(r["item"])}</b> <span class="muted">{esc(r["category"])}・{"金額未入力（0円ではない・合計外）" if r["no_amount"] else "推定 " + yen(r["est"]["std"]) + "（出典なし）"}</span></li>' for r in unc)
    unc_tasks = "".join(f'<li><b>{esc(x["task"])}</b> <span class="muted">{esc(x["next_action"])}</span></li>' for x in tasks if x["status"] == "要確認")

    def src(r):
        s = r["source"]
        return f'<a href="{esc(s)}" target="_blank" rel="noopener">出典</a>' if s.startswith("http") else "—"

    def cell(r, s):
        return "金額未入力" if r["no_amount"] else yen(r["est"][s])
    exp_rows = "".join(
        f'<tr data-st="{esc(r["status"])}"><td>{esc(r["id"])}</td><td>{esc(r["item"])}<div class="muted">{esc(r["payee"])}</div></td><td>{esc(r["category"])}</td><td>{esc(r["country"])}</td>'
        f'<td><span class="pill p-{esc(r["status"])}">{esc(r["status"])}</span></td><td class="n">{cell(r, "low")}</td><td class="n">{cell(r, "std")}</td><td class="n">{cell(r, "high")}</td>'
        f'<td>{src(r)}</td></tr>'
        for r in rows)

    art_counts = defaultdict(int)
    for a in articles:
        art_counts[a["status"]] += 1
    art_html = "".join(
        f'<li><span class="pill p-{esc(a["status"])}">{esc(a["status"])}</span> <b>{esc(a["title"])}</b><div class="muted">{esc(a["series"])}｜資料: {esc(a["materials"])}</div></li>'
        for a in articles)
    art_summary = " ／ ".join(f"{s} {art_counts.get(s, 0)}" for s in ARTICLE_STATUS)

    docs = [("README.md", "全体概要"), ("docs/01-timeline.md", "スケジュール"), ("docs/02-budget.md", "予算モデル"),
            ("docs/03-preparation.md", "準備ToDo"), ("docs/05-public-data-policy.md", "公開データ方針"),
            ("docs/06-predeparture-roadmap.md", "出発前ロードマップ"), ("research/visa-and-immigration.md", "ビザ・再入国"),
            ("research/baguio-diving.md", "バギオ発ダイビング"), ("research/capetown-diving.md", "ケープタウン発ダイビング"),
            ("research/baguio-sightseeing.md", "バギオ観光"), ("research/capetown-sightseeing.md", "ケープタウン観光"),
            ("research/food-and-living.md", "食費・生活"), ("research/winter-clothing.md", "冬服"),
            ("research/safety-and-health.md", "治安・健康"), ("research/philippines-pines.md", "PINES・フィリピン"),
            ("research/africa-trip.md", "5月アフリカ周遊"), ("research/second-school.md", "2校目（ケープタウン）"),
            ("research/sources.md", "出典・調査ログ"), ("blog/article-ideas.md", "記事候補"), ("blog/experience-log.md", "体験ログ"),
            ("data/expenses.csv", "費用CSV"), ("data/tasks.csv", "タスクCSV")]
    docs_html = "".join(f'<a class="doc" href="{esc(p)}">{esc(x)}<span>{esc(p)}</span></a>' for p, x in docs)

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
                    ["見積合計（標準）", f"{yen(S['total']['std'])}（{fmt3(S['total'])}）"],
                    ["うち 見積（出典あり）", f"{yen(S['by_status']['見積']['std'])}（{S['status_count']['見積']} 件）"],
                    ["うち 未確認（出典なし・推定）", f"{yen(S['by_status']['未確認']['std'])}（{S['status_count']['未確認']} 件）"],
                    ["金額未入力の費目", f"{len(S['no_amount'])} 件（0円ではない・合計に含まれない）"],
                    ["上限300万円との差（標準）", f"{yen(S['vs_cap']['std'])}（予算目標 − 見積合計）"],
                    ["記事候補", f"{len(articles)} 件"],
                ]),
            ]),
            "next": gen_next_tasks(tasks),
            "unconfirmed": gen_unconfirmed(rows, tasks),
            "problems": gen_problems(problems),
        },
    }
    for key, b in blocks.items():
        out[TARGETS[key]] = apply_auto(TARGETS[key].read_text(encoding="utf-8").replace("\r\n", "\n"), b)
    out[TARGETS["html"]] = build_html(S, rows, tasks, articles, timeline, fx, problems)
    return out


def main():
    check_only = "--check" in sys.argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    problems = []
    for r in read_csv("meta.csv"):
        _META[r["key"]] = r["value"]
    fx = load_fx()
    expenses = read_csv("expenses.csv")
    tasks = read_csv("tasks.csv")
    articles = read_csv("articles.csv")
    timeline = read_csv("timeline.csv")
    funds = read_csv("funds.csv")
    validate(expenses, tasks, articles, timeline, problems, funds)
    rows = compute(expenses, fx, problems)
    S = summarize(rows, funds)

    print(f"見積合計  {fmt3(S['total'])}")
    print(f"うち見積 {yen(S['by_status']['見積']['std'])}  うち未確認 {yen(S['by_status']['未確認']['std'])}（標準）")
    print(f"金額未入力 {len(S['no_amount'])} 件  タスク {task_progress(tasks)[0]}/{task_progress(tasks)[1]} 完了  記事候補 {len(articles)} 件")
    print(f"検証: {len(problems)} 件の指摘")
    for p in problems:
        print("  -", p)
    outputs = render_all(S, rows, tasks, articles, timeline, fx, problems)
    if check_only:
        stale = [str(p.relative_to(ROOT)) for p, text in outputs.items()
                 if p.read_text(encoding="utf-8").replace("\r\n", "\n") != text]
        if stale:
            print("生成物が CSV と一致しません。`python3 scripts/build.py` を実行してコミットしてください: " + ", ".join(stale))
        return 1 if (problems or stale) else 0
    for p, text in outputs.items():
        p.write_text(text, encoding="utf-8", newline="\n")
    print("更新しました: " + ", ".join(str(p.relative_to(ROOT)) for p in outputs))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
