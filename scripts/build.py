# -*- coding: utf-8 -*-
"""
集計スクリプト（README・docs の AUTO ブロック担当）（studying-abroad）

使い方（リポジトリのルートで実行）:
    python3 scripts/build.py           集計して生成物を更新
    python3 scripts/build.py --check   検証のみ。生成物が CSV と一致しなければ失敗（CI用）

- data/*.csv（正本）を読み込み、以下を再生成する。
    * Markdown の <!-- AUTO:名前 --> 〜 <!-- /AUTO:名前 --> の間だけ
- index.html と data/*.html / docs/*.html は scripts/build_html.py の担当。両方を実行するには scripts/build_all.py を使う。
- CSV 自体は一切書き換えない。
- 公開用の匿名モデル: 個人の支払い・実費・資金は扱わない。総額は見積（低/標準/余裕）の合計のみ。
- 標準ライブラリのみ使用。
"""
import csv
import datetime as dt
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import areas  # noqa: E402  地域別ページの AUTO ブロック

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
DEADLINE_KINDS = ["公式期限", "学校・機関の個別期限", "推奨目安", "要確認"]
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
    """data/fx.csv（currency,name_ja,unit,region,jpy_per_unit,rate_date,rate_kind,source）から読む。空欄のレートは None（0扱いしない）"""
    fx = {"JPY": {"rate": 1.0, "date": "", "source": "", "kind": ""}}
    for r in read_csv("fx.csv"):
        fx[r["currency"]] = {"rate": num(r["jpy_per_unit"]), "date": r["rate_date"], "source": r["source"], "kind": r.get("rate_kind", "")}
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
            problems.append(f"{r['id']}: 通貨 {cur} の為替レートが data/fx.csv にありません（または空欄）")
            rate = None
        raw = {s: num(r[f"{s}_local"]) for s in SCENARIOS}
        if rate is None:  # レート不明は0円ではなく金額未入力扱い（problems に報告済み）
            raw = {s: None for s in SCENARIOS}
        no_amount = all(v is None for v in raw.values())
        est = {s: None if raw[s] is None else raw[s] * rate for s in SCENARIOS}
        # 標準だけが入力された行は低予算・余裕にも同額を使う（簡略入力）。
        # 低予算または余裕だけが入力され標準が空の行は、標準を「未計上」とする（0円にも他シナリオの額にもしない）。
        if est["std"] is not None:
            if est["low"] is None:
                est["low"] = est["std"]
            if est["high"] is None:
                est["high"] = est["std"]
        unpriced = [] if no_amount else [s for s in SCENARIOS if est[s] is None]
        out.append({**r, "rate": rate or 0, "est": est, "no_amount": no_amount, "unpriced": unpriced, "alloc": allocate(r)})
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
    S["total"] = {s: sum(r["est"][s] for r in priced if r["est"][s] is not None) for s in SCENARIOS}
    # 一部のシナリオだけ金額が入っている行（空欄＝未計上。0円ではなく、そのシナリオの合計に含まれない）
    S["partial"] = [r for r in priced if r["unpriced"]]
    S["by_status"] = OrderedDict((k, _z()) for k in EXPENSE_STATUS)
    S["status_count"] = OrderedDict((k, 0) for k in EXPENSE_STATUS)
    for r in rows:
        S["status_count"][r["status"]] = S["status_count"].get(r["status"], 0) + 1
    for r in priced:
        b = S["by_status"].setdefault(r["status"], _z())
        for s in SCENARIOS:
            b[s] += r["est"][s] or 0.0
    S["no_amount"] = [r for r in rows if r["no_amount"]]
    S["unverified"] = [r for r in rows if r["status"] == "未確認"]
    S["by_cat"] = OrderedDict((c, _z()) for c in CATEGORIES)
    S["by_month"] = OrderedDict((m, {"見積": 0.0, "未確認": 0.0}) for m in MONTHS)
    S["by_country"] = defaultdict(float)
    for r in priced:
        c = S["by_cat"][r["category"]]
        for s in SCENARIOS:
            c[s] += r["est"][s] or 0.0
        S["by_country"][r["country"] or "共通"] += r["est"]["std"] or 0.0
        for m, ratio in r["alloc"].items():
            S["by_month"][m][r["status"]] += (r["est"]["std"] or 0.0) * ratio
    budget = {r["id"]: num(r["amount_jpy"]) for r in funds if r["type"] == "予算"}
    S["budget_ideal"] = budget.get("budget_ideal")
    S["budget_cap"] = budget.get("budget_cap")
    S["budget_africa"] = budget.get("budget_africa")
    S["africa_total"] = sum(r["est"]["std"] or 0.0 for r in priced if r["id"].startswith("AF-"))
    # 予算目標との差（予算 − 見積合計）。マイナスは超過。支払いや資金の残高ではない
    S["vs_ideal"] = {s: S["budget_ideal"] - S["total"][s] for s in SCENARIOS}
    S["vs_cap"] = {s: S["budget_cap"] - S["total"][s] for s in SCENARIOS}
    return S


# ---------------------------------------------------------------- 検証
PRIVATE_PATTERNS = [re.compile(p) for p in (r"[\w.+-]+@[\w-]+\.[\w.]+", r"\b\d{9,}\b")]


def suspicious_zero(r):
    """low が非ゼロなのに std/high が明示的に 0 の行は「未計上」を 0円と書いた疑い。未計上は空欄にする"""
    out = []
    low = num(r.get("low_local")) if not _bad(r.get("low_local")) else None
    if low:
        for s in ("std", "high"):
            raw = (r.get(f"{s}_local") or "").strip()
            if raw != "" and not _bad(raw) and num(raw) == 0:
                out.append(f"{r['id']}: {s}_local が 0 ですが low_local は非ゼロです。0円は「不要」を意味します。金額が未計上なら空欄にしてください（0は未計上ではない）")
    return out


def _bad(s):
    try:
        num(s)
        return False
    except ValueError:
        return True


def validate(expenses, tasks, articles, timeline, problems, funds=()):
    ids = defaultdict(int)
    for r in expenses:
        ids[r["id"]] += 1
        if r["category"] not in CATEGORIES:
            problems.append(f"{r['id']}: 費目「{r['category']}」が定義外です")
        if r["status"] not in EXPENSE_STATUS:
            problems.append(f"{r['id']}: 区分「{r['status']}」は {'/'.join(EXPENSE_STATUS)} のいずれかにしてください（公開CSVに確定・実績は使わない）")
        has_amount = any(r[f"{s}_local"] for s in SCENARIOS)
        problems.extend(suspicious_zero(r))
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
        if r["deadline_kind"] not in DEADLINE_KINDS:
            problems.append(f"{r['id']}: 期限の種類「{r['deadline_kind']}」は {'/'.join(DEADLINE_KINDS)} のいずれかにしてください")
        if not r["deadline_note"]:
            problems.append(f"{r['id']}: deadline_note（相対期限・要確認の文言）が空です")
        elif re.search(r"\d{4}-\d{2}-\d{2}|\d{4}年\d{1,2}月\d{1,2}日", r["deadline_note"]):
            problems.append(f"{r['id']}: deadline_note に暦日を書かないでください（公開は「出発90日前（推奨目安）」等の相対表記）")
        try:
            int(r["lead_days"])
        except ValueError:
            problems.append(f"{r['id']}: lead_days は整数（並び替え用。出発の何日前か。負は出発後）にしてください")
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
        f"集計日: {today().isoformat()}（`py scripts/build_all.py` で再計算）。**公開用の匿名モデル**で、個人の支払い・実費・資金は含みません。",
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
        "",
        ("**一部シナリオが未計上（空欄＝未計上。0円ではなく、該当シナリオの合計に含まれない）**: "
         + "、".join(f"{r['id']} {r['item']}（{'・'.join(SCENARIOS[s] for s in r['unpriced'])}）" for r in S["partial"])
         if S["partial"] else "一部シナリオだけ未計上の行はありません。"),
        "",
        "金額は公開価格表などからの**匿名の見積**です。実際の支払額・個人の実績ではありません。",
    ]
    return "\n".join(lines)


def gen_budget_by_cat(S):
    rows = [[c, yen(v["low"]), yen(v["std"]), yen(v["high"])] for c, v in S["by_cat"].items()]
    t = S["total"]
    rows.append(["**合計**", f"**{yen(t['low'])}**", f"**{yen(t['std'])}**", f"**{yen(t['high'])}**"])
    return md_table(["費目", "低予算", "標準", "余裕"], rows) + "\n\n金額は公開価格表などからの匿名の見積です。金額未入力の行・未計上のシナリオは含みません（0円ではありません）。"


def gen_budget_by_month(S):
    rows = [[MONTHS[m], yen(v["見積"] + v["未確認"]), yen(v["見積"]), yen(v["未確認"])] for m, v in S["by_month"].items()]
    return ("期間をまたぐ費用（保険・授業料など）は利用期間の日数で月に按分しています（標準プラン・金額入力済みの行のみ。公開価格表からの匿名の見積）。\n\n"
            + md_table(["月", "見積合計(標準)", "うち見積", "うち未確認"], rows))


def gen_budget_by_country(S):
    rows = sorted(S["by_country"].items(), key=lambda x: (-x[1], x[0]))
    return md_table(["国・地域", "見積合計(標準)"], [[k, yen(v)] for k, v in rows])


def amount_cell(r, s):
    if r["no_amount"]:
        return "金額未入力"
    return "未計上" if r["est"][s] is None else yen(r["est"][s])


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
    return md_table(["通貨", "1単位あたり円", "レート日付", "種別", "出典"],
                    [[k, f"{v['rate']:g}" if v["rate"] else "未確認", v["date"] or "—", v.get("kind") or "—", md_link(v["source"]) if v["source"] else "—"]
                     for k, v in fx.items() if k != "JPY"])


def gen_tasks(tasks, group_field="phase"):
    groups = OrderedDict()
    for t in sorted(tasks, key=task_sort_key):
        groups.setdefault(t[group_field], []).append(t)
    out = []
    for g, ts in groups.items():
        out.append(f"### {g}\n")
        out.append(md_table(["ID", "", "タスク", "期限（目安）", "期限の種類", "進捗", "担当", "費用目安", "次のアクション", "根拠", "Issue"],
                            [[t["id"], "✅" if t["status"] in ("完了", "不要") else ("⚠️" if t["status"] == "要確認" else "⬜"),
                              t["task"], t["deadline_note"] or "—", t["deadline_kind"], t["status"], t["owner"] or "本人", t["cost_note"] or "—", t["next_action"] or "—",
                              md_link(t["source"]) if t["source"].startswith("http") else "—",
                              f"[#{t['issue'].rsplit('/', 1)[-1]}]({t['issue']})" if t["issue"] else "—"] for t in ts]))
        out.append("")
    return "\n".join(out)


def task_sort_key(t):
    """並び替え: 出発の何日前か（lead_days）が大きい順＝早く着手するものが先。同値は優先度、ID"""
    try:
        lead = int(t["lead_days"])
    except (KeyError, ValueError):
        lead = -9999
    return (-lead, t["priority"] or "9", t["id"])


def task_progress(tasks):
    done = sum(1 for t in tasks if t["status"] in ("完了", "不要"))
    return done, len(tasks)


def next_tasks(tasks, n=8):
    open_ = [t for t in tasks if t["status"] not in ("完了", "不要", "保留")]
    return sorted(open_, key=task_sort_key)[:n]


def gen_next_tasks(tasks):
    return md_table(["期限（目安）", "種類", "タスク", "進捗", "次のアクション"],
                    [[t["deadline_note"] or "—", t["deadline_kind"], t["task"], t["status"], t["next_action"]] for t in next_tasks(tasks)])


def gen_timeline(timeline):
    rows = sorted(timeline, key=lambda r: (int(r["sort"] or 0), r["id"]))
    return md_table(["期間", "内容", "状態", "概要"], [[r["period"], r["title"], r["status"], r["summary"]] for r in rows])


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
    items += [f"- 費用 {r['id']}: {r['item']}（{'・'.join(SCENARIOS[s] for s in r['unpriced'])}は未計上＝空欄。0円ではない）" for r in rows if r.get("unpriced")]
    items += [f"- タスク {t['id']}: {t['task']}（{t['next_action']}）" for t in tasks if t["status"] == "要確認"]
    return "\n".join(items) if items else "なし"


def gen_problems(problems):
    return "\n".join(f"- ⚠️ {p}" for p in problems) if problems else "- 問題は見つかりませんでした"


def apply_auto(text, blocks):
    for name, content in blocks.items():
        pat = re.compile(rf"(<!-- AUTO:{name} -->)(.*?)(<!-- /AUTO:{name} -->)", re.S)
        text = pat.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", text)
    return text


# ---------------------------------------------------------------- main
TARGETS = {
    "budget": ROOT / "docs" / "02-budget.md",
    "prep": ROOT / "docs" / "03-preparation.md",
    "timeline": ROOT / "docs" / "01-timeline.md",
    "articles": ROOT / "blog" / "article-ideas.md",
    "readme": ROOT / "README.md",
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
    # 地域別ページ（areas/*.md）。手書きの導入文はそのまま、AUTO ブロックだけを作り直す
    pages, places, fx_records = read_csv("pages.csv"), read_csv("places.csv"), read_csv("fx.csv")
    for region in areas.REGION_LABEL:
        path = ROOT / areas.REGION_FILE[region]
        if not path.exists():
            continue
        b = areas.all_blocks(region, rows=rows, tasks=tasks, timeline=timeline, pages=pages, places=places,
                             fx_records=fx_records, root=ROOT)
        out[path] = apply_auto(path.read_text(encoding="utf-8").replace("\r\n", "\n"), b)
    return out


def load_model():
    """CSV を読み込み (S, rows, tasks, articles, timeline, fx, problems, funds) を返す。build_html.py もこれを使う"""
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
    return S, rows, tasks, articles, timeline, fx, problems, funds


def main():
    check_only = "--check" in sys.argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    S, rows, tasks, articles, timeline, fx, problems, funds = load_model()

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
