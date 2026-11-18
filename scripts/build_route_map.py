# -*- coding: utf-8 -*-
"""案G（35日モデル）の地図 maps/route-map.html を生成する。標準ライブラリのみ。

使い方（リポジトリのルートで実行）:
    py scripts/build_route_map.py           生成
    py scripts/build_route_map.py --check   生成物が最新でなければ失敗（CI用）

- 内容: ①アフリカ全体の経路（Day 番号つき）②マダガスカル拡大図（日数案 現行14日／A／B／C を切り替え）
- 日程は research/may-madagascar-vfa-redesign.md の「Day 1〜Day 35」表と日数案の表に合わせた**仮置き**。確定旅程ではない。
- 国境・投影は scripts/build_maps.py を再利用する（Natural Earth・外部通信なし）。
- 陸路・国内線は点を結ぶ直線で、実際の道路経路ではない。国際線は大圏の曲線。
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_maps as bm  # noqa: E402
from build_html import BASE_CSS, FONT_SIZE_JS, bar, nav as site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "maps" / "route-map.html"

# マダガスカル内の町（route_points.csv にない地点。概略の座標）
LOCAL = {
    "ANDASIBE": ("アンダシベ", -18.94, 48.42),
    "MORONDAVA": ("モロンダバ", -20.28, 44.32),
}

# 全体図の経路。(通し番号の表示, 出発点, 到着点, 種類, 日数の表示)
# 点の ID は data/route_points.csv。Day は 35日表（現行14日案）の日。
MAIN_LEGS = [
    ("BOM", "MRU", "flight", "Day 1〜2"),   # 日本→ムンバイ→モーリシャス（日本側は図の外）
    ("MRU", "TNR", "flight", "Day 6"),
    ("TNR", "MRU", "flight", "Day 19"),
    ("MRU", "JNB", "flight", "Day 21"),
    ("JNB", "VICFALLS", "flight", "Day 23"),
    ("VICFALLS", "LIVINGSTONE", "overland", ""),
    ("LIVINGSTONE", "KASANE", "overland", ""),
    ("KASANE", "VICFALLS", "overland", ""),
    ("VICFALLS", "CPT", "flight", "Day 32"),
]

# 日数案ごとのマダガスカル内の動き（Day は日本発 Day 1 からの通し番号）。
# 出国日以降は共通の内容で、日付だけが前倒しになる。
PLANS = {
    "now": {
        "label": "現行 14日", "stay": 14, "exit": "Day 19 5/21(金)", "total": 35,
        "legs": [("MRU", "TNR", "Day 6", "flight"), ("TNR", "ANDASIBE", "Day 7", "road"), ("ANDASIBE", "TNR", "Day 9", "road"),
                 ("TNR", "MORONDAVA", "Day 10", "domestic"), ("MORONDAVA", "TNR", "Day 16", "domestic"), ("TNR", "MRU", "Day 19", "flight")],
        "note": "余裕重視。首都で2日、西部で予備2日。欠航の予備は計4日。",
    },
    "A": {
        "label": "A 10日", "stay": 10, "exit": "Day 15 5/17(月)", "total": 31,
        "legs": [("MRU", "TNR", "Day 6", "flight"), ("TNR", "ANDASIBE", "Day 7", "road"), ("ANDASIBE", "TNR", "Day 9", "road"),
                 ("TNR", "MORONDAVA", "Day 10", "domestic"), ("MORONDAVA", "TNR", "Day 14", "domestic"), ("TNR", "MRU", "Day 15", "flight")],
        "note": "標準。欠航の予備は1日。",
    },
    "B": {
        "label": "B 7日", "stay": 7, "exit": "Day 12 5/14(金)", "total": 28,
        "legs": [("MRU", "TNR", "Day 6", "flight"), ("TNR", "ANDASIBE", "Day 6", "road"), ("ANDASIBE", "TNR", "Day 7", "road"),
                 ("TNR", "MORONDAVA", "Day 8", "domestic"), ("MORONDAVA", "TNR", "Day 11", "domestic"), ("TNR", "MRU", "Day 12", "flight")],
        "note": "4泊5日＋予備2日。首都に泊まらず直行できれば最短。欠航1回までは吸収できる。",
    },
    "C": {
        "label": "C 5日", "stay": 5, "exit": "Day 10 5/12(水)", "total": 26,
        "legs": [("MRU", "TNR", "Day 6", "flight"), ("TNR", "ANDASIBE", "Day 6", "road"), ("ANDASIBE", "TNR", "Day 7", "road"),
                 ("TNR", "MORONDAVA", "Day 8", "domestic"), ("MORONDAVA", "TNR", "Day 10", "domestic"), ("TNR", "MRU", "Day 10", "flight")],
        "note": "4泊5日のみ。欠航の予備なし。1回の欠航で出国日がずれる。",
    },
}

# ---- カレンダー：日ごとの「国・場所・内容・種別」。正本は research/may-madagascar-vfa-redesign.md の35日表と日数案の日別表
# 種別: fly=空路 / move=昼間の車・国境 / tour=観光・体験 / gap=予備・待機 / base=準備・滞在
KIND_LABEL = {"fly": "移動（空路）", "move": "移動（昼間の車・国境）", "tour": "観光・体験", "gap": "予備・待機", "base": "準備・滞在"}
import datetime as _dt
CAL_START = _dt.date(2027, 5, 3)  # Day 1（仮置き）
WD = "月火水木金土日"


def _mada_days(plan):
    """マダガスカル滞在中の日（Day 6〜出国日）。{Day: (国, 場所, 内容, 種別)}"""
    M = "マダガスカル"
    if plan == "now":
        return {6: (M, "TNR", "到着。首都近郊泊", "fly"), 7: (M, "TNR→Andasibe", "日中の車で東部へ", "move"),
                8: (M, "Andasibe", "インドリ等のキツネザル", "tour"), 9: (M, "Andasibe→TNR", "首都へ戻る", "move"),
                10: (M, "TNR→Morondava", "国内線で西部へ", "fly"),
                11: (M, "Morondava", "バオバブ街道・Kirindy", "tour"), 12: (M, "Morondava", "バオバブ街道・Kirindy", "tour"),
                13: (M, "Morondava", "バオバブ街道・Kirindy", "tour"),
                14: (M, "Morondava", "予備（欠航・雨天）", "gap"), 15: (M, "Morondava", "予備（欠航・雨天）", "gap"),
                16: (M, "Morondava→TNR", "国内線で首都へ", "fly"),
                17: (M, "TNR近郊", "観光・予備", "gap"), 18: (M, "TNR近郊", "予備（国内線遅延）", "gap"),
                19: (M + "→モーリシャス", "TNR→MRU", "マダガスカルを出国", "fly")}
    if plan == "A":
        return {6: (M, "TNR", "到着。首都泊", "fly"), 7: (M, "TNR→Andasibe", "日中の車で東部へ", "move"),
                8: (M, "Andasibe", "インドリ観察", "tour"), 9: (M, "Andasibe→TNR", "首都へ戻る", "move"),
                10: (M, "TNR→Morondava", "国内線で西部へ", "fly"),
                11: (M, "Morondava", "バオバブ街道・Kirindy", "tour"), 12: (M, "Morondava", "バオバブ街道・Kirindy", "tour"),
                13: (M, "Morondava", "予備（欠航・雨天）", "gap"),
                14: (M, "Morondava→TNR", "国内線で首都へ", "fly"), 15: (M + "→モーリシャス", "TNR→MRU", "マダガスカルを出国", "fly")}
    if plan == "B":
        return {6: (M, "MRU→TNR→Andasibe", "到着後そのまま東部へ（日中の車）", "move"),
                7: (M, "Andasibe→TNR", "観察後、首都へ（午後便なら西部へ直行）", "move"),
                8: (M, "TNR→Morondava", "国内線で西部へ。バオバブ夕景", "fly"),
                9: (M, "Morondava", "Kirindy等", "tour"), 10: (M, "Morondava", "バオバブ街道・予備", "tour"),
                11: (M, "Morondava→TNR", "国内線で首都へ（欠航なら翌日）", "fly"), 12: (M + "→モーリシャス", "TNR→MRU", "マダガスカルを出国", "fly")}
    return {6: (M, "MRU→TNR→Andasibe", "到着後そのまま東部へ", "move"),
            7: (M, "Andasibe→TNR", "朝の観察後、首都へ", "move"),
            8: (M, "TNR→Morondava", "国内線で西部へ。バオバブ夕景", "fly"),
            9: (M, "Morondava", "Kirindy等", "tour"),
            10: (M + "→モーリシャス", "Morondava→TNR→MRU", "首都経由でそのまま出国（予備なし）", "fly")}


def calendar_days(plan):
    """Day 1〜最終日の (day, date, 国, 場所, 内容, 種別) の一覧。出国日以降は案で日付だけ前倒しになる"""
    exit_day = {"now": 19, "A": 15, "B": 12, "C": 10}[plan]
    days = {1: ("日本→インド", "東京→Mumbai", "国際線出発", "fly"), 2: ("モーリシャス", "MRU", "到着", "fly"),
            3: ("モーリシャス", "島内", "島内観光", "tour"), 4: ("モーリシャス", "島内", "島内観光", "tour"),
            5: ("モーリシャス", "島内", "島内観光", "tour")}
    days.update(_mada_days(plan))
    tail = [("モーリシャス", "MRU周辺", "再接続・待機（便が合えば削れる）", "gap"),
            ("モーリシャス→南アフリカ", "MRU→JNB", "直行片道", "fly"),
            ("南アフリカ", "JNB", "別切り接続バッファ", "gap"),
            ("南アフリカ→ジンバブエ", "JNB→VFA", "空路", "fly"),
            ("ジンバブエ", "Victoria Falls", "滝の観光", "tour"),
            ("ザンビア", "Livingstone", "昼間の国境移動・反対側の滝", "move"),
            ("ザンビア", "Livingstone", "観光・ツアー", "tour"),
            ("ボツワナ", "Kasane", "昼間の送迎・Kazungula国境", "move"),
            ("ボツワナ", "Kasane／Chobe", "ゲームドライブ・ボート", "tour"),
            ("ボツワナ", "Kasane／Chobe", "ゲームドライブ・ボート", "tour"),
            ("ボツワナ→ジンバブエ", "Kasane→Victoria Falls", "昼間の越境、空港接続", "move"),
            ("ジンバブエ", "Victoria Falls", "空路前の予備日", "gap"),
            ("ジンバブエ→南アフリカ", "VFA→Cape Town", "空路", "fly"),
            ("南アフリカ", "Cape Town", "学校前の準備", "base"), ("南アフリカ", "Cape Town", "学校前の準備", "base"),
            ("南アフリカ", "Cape Town", "学校前の準備", "base")]
    for i, t in enumerate(tail):
        days[exit_day + 1 + i] = t
    return [(n, CAL_START + _dt.timedelta(days=n - 1), *days[n]) for n in sorted(days)]



# ---- 8月の代表案の日別（仮置き）。条件：Day 1 = 2027-08-01(日) ケープタウン発、Day 20 = 8/20(金) 日本着（#137。8/20優先・8/24許容上限の目安）。
# 制約：MPM→NBO は、Kenya Airways公式は直行・水金日だが第三者DBは直行なしで矛盾（2027年8月は未確認。R-68）、CPT↔WDH のバスは水・金・日（Wikivoyage）。
# 滞在配分は research/137-route-redesign-comparison.md と research/africa-august-comparison.md から仮置き。運賃・便は未確認。
AUG_START = _dt.date(2027, 8, 1)
AUG_PLANS = {
    "A0": {"label": "A0 ケニア中心", "note": "CPT→NBO→サファリ→ドーハ→日本。ケニアに長く滞在", "days": [
        ("南アフリカ→ケニア", "CPT→NBO", "空路（経由便の可能性）", "fly"),
        ("ケニア", "ナイロビ", "入国・休息（eTA）", "base"),
        ("ケニア", "ナイロビ→マサイマラ", "昼間の車か小型機で移動", "move"),
        ("ケニア", "マサイマラ", "ゲームドライブ", "tour"), ("ケニア", "マサイマラ", "ゲームドライブ", "tour"),
        ("ケニア", "マサイマラ", "ゲームドライブ（マラ川の渡河期）", "tour"),
        ("ケニア", "マサイマラ→ナイロビ", "戻り", "move"),
        ("ケニア", "ナイロビ", "市内・予備", "gap"),
        ("ケニア", "ナイロビ→ナクル湖", "日中の車", "move"), ("ケニア", "ナクル湖", "サファリ", "tour"),
        ("ケニア", "ナクル湖→ナイロビ", "戻り", "move"),
        ("ケニア", "ナイロビ", "予備", "gap"), ("ケニア", "ナイロビ", "予備", "gap"),
        ("ケニア", "アンボセリ方面", "日帰りまたは1泊", "tour"), ("ケニア", "アンボセリ方面", "サファリ", "tour"),
        ("ケニア", "ナイロビ", "戻り・買い物", "base"), ("ケニア", "ナイロビ", "予備（国際線の前日）", "gap"),
        ("ケニア→カタール", "NBO→DOH", "空路（乗継観光は未確定）", "fly"),
        ("カタール", "ドーハ", "乗継（観光は任意）", "gap"),
        ("カタール→日本", "DOH→東京", "日本着（8/20）", "fly")]},
    "A2": {"label": "A2 ナミビア中心", "note": "CPT→WDH→砂漠→ドーハ→日本。ナミビアに長め", "days": [
        ("南アフリカ→ナミビア", "CPT→WDH", "空路（航空会社は未確認）", "fly"),
        ("ナミビア", "ウィントフック", "入国・休息（査証の確認）", "base"),
        ("ナミビア", "WDH→Sesriem", "乗合シャトル（日中）", "move"),
        ("ナミビア", "Sesriem", "Sossusvlei・Deadvlei（日の出）", "tour"), ("ナミビア", "Sesriem", "Sesriem Canyon・予備", "tour"),
        ("ナミビア", "Sesriem→Swakopmund", "日中の車", "move"),
        ("ナミビア", "Swakopmund", "砂丘・ダイビング候補", "tour"), ("ナミビア", "Swakopmund", "予備", "gap"),
        ("ナミビア", "Swakopmund→Etosha", "日中の車", "move"),
        ("ナミビア", "Etosha", "ゲームドライブ", "tour"), ("ナミビア", "Etosha", "ゲームドライブ", "tour"),
        ("ナミビア", "Etosha", "ゲームドライブ", "tour"),
        ("ナミビア", "Etosha→ウィントフック", "日中の車（予備を含む）", "move"),
        ("ナミビア", "ウィントフック", "予備", "gap"),
        ("ナミビア", "ウィントフック", "買い物・休息", "base"),
        ("ナミビア→南アフリカ", "WDH→JNB", "空路（WDH→ドーハの直行はなく、JNB経由が前提。第三者DB・2027年は未確認）", "fly"),
        ("南アフリカ→カタール", "JNB→DOH", "空路（乗継日。運賃・接続は未確認）", "fly"),
        ("カタール", "ドーハ", "乗継（観光は任意）", "gap"),
        ("カタール→日本", "DOH→東京", "日本着の前日（予備）", "gap"),
        ("日本", "東京", "日本着（8/20）", "fly")]},
    "A4": {"label": "A4 南部3か国→ケニア→ドーハ", "note": "レソト→エスワティニ→モザンビーク→NBO→ドーハ→日本。国境の移動が多い", "days": [
        ("南アフリカ→レソト", "CPT→マセル（MSU）", "空路か国境越え（日中）", "fly"),
        ("レソト", "マセル", "入国・休息", "base"),
        ("レソト", "マセル周辺", "ポニートレッキング・日帰り", "tour"), ("レソト", "マセル周辺", "ハイキング", "tour"),
        ("レソト→南アフリカ", "マセル→JNB方面", "南ア経由で移動（日中）", "move"),
        ("南アフリカ→エスワティニ", "→ムババーネ", "昼間の国境越え", "move"),
        ("エスワティニ", "Mlilwane", "保護区・文化", "tour"), ("エスワティニ", "Mlilwane／Hlane", "保護区", "tour"),
        ("エスワティニ", "Hlane", "保護区", "tour"),
        ("エスワティニ→モザンビーク", "→マプト", "昼間の国境越え（要確認）", "move"),
        ("モザンビーク", "マプト", "入国・市内", "base"),
        ("モザンビーク", "マプト", "予備（Kenya Airways公式の水・金・日便に合わせる想定。直行の実在は未確認）", "gap"),
        ("モザンビーク→ケニア", "MPM→NBO", "金曜13:50発（公式は直行・水金日。第三者DBは直行なしで矛盾・未確認）", "fly"),
        ("ケニア", "ナイロビ", "入国・休息（eTA）", "base"),
        ("ケニア", "ナイロビ周辺", "国立公園（日帰り）", "tour"), ("ケニア", "ナイロビ周辺", "予備", "gap"),
        ("ケニア→カタール", "NBO→DOH", "空路", "fly"),
        ("カタール", "ドーハ", "乗継（観光は任意）", "gap"),
        ("カタール→日本", "DOH→東京", "日本着の前日（予備）", "gap"),
        ("日本", "東京", "日本着（8/20）", "fly")]},
    "A5": {"label": "A5 南部3か国→JNB→ドーハ", "note": "ケニアに行かず、JNB経由でドーハから日本へ。移動が少なく予備が多い", "days": [
        ("南アフリカ→レソト", "CPT→マセル（MSU）", "空路か国境越え（日中）", "fly"),
        ("レソト", "マセル", "入国・休息", "base"),
        ("レソト", "マセル周辺", "ポニートレッキング・日帰り", "tour"), ("レソト", "マセル周辺", "ハイキング", "tour"),
        ("レソト→南アフリカ", "マセル→JNB方面", "南ア経由で移動（日中）", "move"),
        ("南アフリカ→エスワティニ", "→ムババーネ", "昼間の国境越え", "move"),
        ("エスワティニ", "Mlilwane", "保護区・文化", "tour"), ("エスワティニ", "Mlilwane／Hlane", "保護区", "tour"),
        ("エスワティニ", "Hlane", "保護区", "tour"),
        ("エスワティニ→モザンビーク", "→マプト", "昼間の国境越え（要確認）", "move"),
        ("モザンビーク", "マプト", "入国・市内", "base"), ("モザンビーク", "マプト", "海岸・日帰り", "tour"),
        ("モザンビーク", "マプト", "予備", "gap"), ("モザンビーク", "マプト", "予備", "gap"),
        ("モザンビーク→南アフリカ", "マプト→JNB", "空路または昼間のバス", "move"),
        ("南アフリカ", "JNB", "休息・予備", "gap"),
        ("南アフリカ→カタール", "JNB→DOH", "空路", "fly"),
        ("カタール", "ドーハ", "乗継（観光は任意）", "gap"),
        ("カタール→日本", "DOH→東京", "日本着の前日（予備）", "gap"),
        ("日本", "東京", "日本着（8/20）", "fly")]},
}


def aug_calendar_days(key):
    """8月の案の日別。(day, date, 国, 場所, 内容, 種別)。Day 1 = 8/1（日）"""
    return [(i + 1, AUG_START + _dt.timedelta(days=i), *d) for i, d in enumerate(AUG_PLANS[key]["days"])]

def calendar_html(plan, days=None):
    """月ごとの週表（月曜始まり）。1日=1セル。日付・Day番号・国・場所・内容"""
    ds = {d[1]: d for d in (days if days is not None else calendar_days(plan))}
    first, last = min(ds), max(ds)
    out = []
    cur = _dt.date(first.year, first.month, 1)
    while cur <= last:
        nxt = _dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
        rows = []
        wk = cur - _dt.timedelta(days=cur.weekday())
        while wk < nxt and wk <= last:
            cells = []
            has = False
            for i in range(7):
                day = wk + _dt.timedelta(days=i)
                if day.month != cur.month:
                    cells.append('<td class="x"></td>')
                    continue
                e = ds.get(day)
                if e:
                    has = True
                    n, _d, country, place, what, kind = e
                    cells.append(f'<td class="k-{kind}"><span class="dd">{day.day}</span><span class="dn2">Day {n}</span>'
                                 f'<b>{html.escape(country)}</b><span class="pl">{html.escape(place)}</span><span class="wh">{html.escape(what)}</span></td>')
                else:
                    cells.append(f'<td class="off"><span class="dd">{day.day}</span></td>')
            rows.append(("<tr>" if has else '<tr class="blank">') + "".join(cells) + "</tr>")
            wk += _dt.timedelta(days=7)
        out.append(f'<table class="cal"><caption>{cur.year}年{cur.month}月</caption><thead><tr>'
                   + "".join(f"<th>{w}</th>" for w in WD) + f'</tr></thead><tbody>{"".join(rows)}</tbody></table>')
        cur = nxt
    return "".join(out)

MODE_STYLE = {"flight": ("fl", "空路"), "domestic": ("dm", "国内線（直線で例示）"), "road": ("rd", "昼間の車（直線で例示）"), "overland": ("rd", "陸路（直線で例示）")}

CSS = BASE_CSS + """
:root{--sea:#e6eef3;--land:#f4f1e8;--border:#b9b4a4;--grat:#cdd8df;--fl:#9B1D20;--dm:#1B7A8C;--rd:#8A6D00;--pt:#1d2227}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--fl:#F2A1A3;--dm:#9AD9E6;--rd:#F2C94C;--pt:#fbfbfa}}
:root[data-theme="dark"]{--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--fl:#F2A1A3;--dm:#9AD9E6;--rd:#F2C94C;--pt:#fbfbfa}
.zwrap{overflow:auto;margin:6px 0;max-width:100%}
.rwrap{display:grid;grid-template-columns:max-content minmax(200px,1fr);gap:0 16px;align-items:start}
@media (max-width:1100px){.rwrap{grid-template-columns:1fr}}
h1{margin:6px 0!important;font-size:1.35rem!important}.crumb{margin:6px 0!important}h2.mt{margin:6px 0!important;font-size:1.05rem!important}
.mapbox{position:relative;border:1px solid var(--line);width:calc(min(94vw,860px,max(420px,(100vh - 190px) * var(--ar,1.6))) * var(--zf,1))}
.map-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:4px 14px}
.map-sub{margin:0 0 6px!important;font-size:.85rem}
.zoom{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0;padding:0}
.zoom button{font:inherit;min-width:50px;min-height:34px;padding:2px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);cursor:pointer}
.zoom button[aria-pressed=true]{background:var(--link);color:#fff;border-color:var(--link)}
svg.m{display:block;width:100%;height:auto;background:var(--sea);font-family:var(--sans)}
.sea{fill:var(--sea)} .grat{fill:none;stroke:var(--grat);stroke-width:.6} .frame{fill:none;stroke:var(--border);stroke-width:1}
.co{fill:var(--land);stroke:var(--border);stroke-width:.5;fill-rule:evenodd;stroke-linejoin:round}
.co.v{fill:var(--hl);stroke:var(--muted);stroke-width:.8}
.ln{fill:none;stroke-width:2.6;stroke-linecap:round}
.ln.fl{stroke:var(--fl);stroke-dasharray:7 5} .ln.dm{stroke:var(--dm)} .ln.rd{stroke:var(--rd);stroke-width:3}
.pt{fill:var(--bg);stroke:var(--pt);stroke-width:2}
.tx{font-size:calc(12.5px * var(--ts,1));font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--sea);stroke-width:3.4px;stroke-linejoin:round;pointer-events:none}
.tx.big{font-size:calc(15px * var(--ts,1))}
.dn{font-size:calc(11px * var(--ts,1));font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--sea);stroke-width:3px;stroke-linejoin:round;pointer-events:none}
.dn.a{fill:var(--fl)} .dn.b{fill:var(--dm)} .dn.c{fill:var(--rd)}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0}
.tabs button{font:inherit;min-height:38px;padding:4px 16px;border:1px solid var(--line);border-radius:8px 8px 0 0;background:var(--bg);color:var(--ink);cursor:pointer}
.tabs button[aria-selected=true]{background:var(--link);color:#fff;border-color:var(--link);font-weight:700}
.chips[hidden],.mapbox[hidden]{display:none}
.chips{display:flex;flex-wrap:wrap;gap:4px 6px;border-top:2px solid var(--link);padding-top:4px}
.chips label{display:inline-flex;gap:6px;align-items:center;min-height:36px;padding:3px 10px;border:1px solid var(--line);border-radius:18px;background:var(--bg);cursor:pointer}
.chips label:has(input:checked){background:var(--hl);border-color:var(--link);font-weight:700}
.chips input{margin:0}
.rinfo{margin:6px 0;padding:6px 10px;border-left:6px solid var(--link);background:var(--bg);font-size:.92em}.rinfo b{display:block}
.calbox{margin:8px 0}
[data-cpan][hidden],.acal[hidden],.aplan[hidden]{display:none}
table.cal{width:100%;min-width:0;table-layout:fixed;border-collapse:collapse;margin:10px 0}
table.cal caption{text-align:left;font-weight:700;font-size:1.05rem;padding:4px 0}
table.cal th{background:var(--th);border:1px solid var(--line);padding:3px;font-size:.85rem;text-align:center}
table.cal td{border:1px solid var(--line);vertical-align:top;padding:4px 5px;height:96px;font-size:.78rem;line-height:1.35;overflow:hidden}
table.cal tr.blank td{height:30px}
table.cal td.x{background:var(--bg)} table.cal td.off{color:var(--muted)}
table.cal .dd{font-weight:700;font-size:.95rem;margin-right:4px} table.cal .dn2{color:var(--muted);font-size:.72rem}
table.cal b{display:block;font-size:.8rem;margin-top:1px} table.cal .pl{display:block;color:var(--muted)} table.cal .wh{display:block}
table.cal td.k-fly{background:var(--c-fly)} table.cal td.k-move{background:var(--c-move)} table.cal td.k-tour{background:var(--c-tour)}
table.cal td.k-gap{background:var(--c-gap);border-style:dashed} table.cal td.k-base{background:var(--c-base)}
:root{--c-fly:#fbe3e4;--c-move:#fbf0d2;--c-tour:#dff1e6;--c-gap:#eceff1;--c-base:#e3ecf8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--c-fly:#4a2a2c;--c-move:#463c1e;--c-tour:#22402d;--c-gap:#2e3336;--c-base:#25344a}}
:root[data-theme="dark"]{--c-fly:#4a2a2c;--c-move:#463c1e;--c-tour:#22402d;--c-gap:#2e3336;--c-base:#25344a}
.cal-key{display:flex;flex-wrap:wrap;gap:6px 14px;margin:6px 0;font-size:.9rem}
.cal-key i{display:inline-block;width:14px;height:14px;margin-right:5px;vertical-align:-2px;border:1px solid var(--line)}
@media (max-width:700px){table.cal td{height:auto;font-size:.7rem;padding:3px} table.cal .wh,table.cal .pl{display:none}}
.switch{display:flex;flex-wrap:wrap;gap:6px 16px;margin:10px 0;padding:6px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:.95em}
.plans{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.plans button{font:inherit;padding:6px 14px;min-height:44px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);cursor:pointer}
.plans button[aria-pressed=true]{background:var(--link);color:#fff;border-color:var(--link)}
.pinfo{margin:8px 0;padding:10px 12px;border:1px solid var(--line);border-left:6px solid var(--link);background:var(--bg)}
.pinfo b{display:block}
.lg{display:flex;flex-wrap:wrap;gap:6px 18px;margin:8px 0;font-size:.93em}
.lg svg{vertical-align:-3px;margin-right:6px}
.plan{display:none} .plan.on{display:inline}
table.pl{border-collapse:collapse;width:100%;margin:8px 0}
table.pl th,table.pl td{border:1px solid var(--line);padding:5px 8px;text-align:left}
table.pl th{background:var(--th)}
"""


def pt(points, pid):
    """点の (名前, 緯度, 経度)。route_points.csv か LOCAL から"""
    if pid in LOCAL:
        return LOCAL[pid]
    if pid == "KASANE":
        p = points[pid]
    else:
        p = points[pid]
    return (p["name_ja"], float(p["lat"]), float(p["lon"]))


def leg_path(proj, a, b, flight, n=24):
    if flight:
        pts = [proj.xy(lon, lat) for lat, lon in bm.gc_points(a[1], a[2], b[1], b[2], n)]
    else:
        pts = [proj.xy(a[2], a[1]), proj.xy(b[2], b[1])]
    return "M" + "L".join(f"{bm.f1(x)} {bm.f1(y)}" for x, y in pts), pts


def offset_line(pts, off):
    """往復で線が重ならないよう、中点を進行方向と直角にずらした二次曲線にする"""
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    d = (dx * dx + dy * dy) ** 0.5 or 1.0
    mx, my = (x0 + x1) / 2 - dy / d * off, (y0 + y1) / 2 + dx / d * off
    return f"M{bm.f1(x0)} {bm.f1(y0)}Q{bm.f1(mx)} {bm.f1(my)} {bm.f1(x1)} {bm.f1(y1)}", (mx * 0.5 + (x0 + x1) * 0.25, my * 0.5 + (y0 + y1) * 0.25)


def land_svg(proj, geo, visit, tol, extra=""):
    paths = bm.ring_paths(proj, geo, tol, skip=("010",))
    out = []
    for cid, (name, d) in paths.items():
        out.append(f'<path class="co{" v" if cid in visit else ""}" d="{d}"><title>{html.escape(name)}</title></path>')
    return "".join(out)


# 全体図で選べる案。G は Day 番号つき（35日表）。他は routes.csv の区間をそのまま描く（Day なし）
MAY_IDS = ["G", "M0A", "M0B", "M0C", "M1A", "M1B"]
AUG_IDS = ["A0", "A1", "A2", "A3", "A4", "A4X", "A5", "A5X", "A6", "A7", "A8", "A9", "A10", "A11", "A12"]
G_DAYS = {("BOM", "MRU"): "Day 1〜2", ("MRU", "TNR"): "Day 6", ("TNR", "MRU"): "Day 19", ("MRU", "JNB"): "Day 21", ("JNB", "VICFALLS"): "Day 23", ("VICFALLS", "CPT"): "Day 32"}
SHORT = {"G": "G：現行35日", "M0A": "M0-A ナミビアなし・往復", "M0B": "M0-B オープンジョー", "M0C": "M0-C 短縮", "M1A": "M1-A ボツワナ→ナミビア", "M1B": "M1-B マウン入口"}


def short_name(rid, name):
    if rid in SHORT:
        return SHORT[rid]
    n = name.split("：", 1)[1] if "：" in name[:14] else name
    return rid + " " + n.split("（", 1)[0]


def route_svg(proj, points, legs, rid):
    """1案ぶんの線と地点。G だけ Day 番号を付ける。同じ2点の往復は左右にずらす"""
    lines, labels, used = [], [], []
    for l in legs:
        a, b, mode = l["from_point"], l["to_point"], ("flight" if l["mode"] == "flight" else "overland")
        pa, pb = pt(points, a), pt(points, b)
        key = tuple(sorted((a, b)))
        for q in (a, b):
            if q not in used:
                used.append(q)
        d, pts = leg_path(proj, pa, pb, mode == "flight")
        again = sum(1 for m in legs if tuple(sorted((m["from_point"], m["to_point"]))) == key) > 1
        if again:
            d, mid = offset_line(pts, 10)
        else:
            mid = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
        day = G_DAYS.get((a, b), "") if rid == "G" else ""
        cls = MODE_STYLE[mode][0]
        tip = html.escape(pa[0]) + "→" + html.escape(pb[0]) + (("（" + day + "）") if day else "")
        lines.append(f'<path class="ln {cls}" d="{d}"><title>{tip}</title></path>')
        if day:
            dy = -8 if a == "MRU" else 14
            labels.append(f'<text class="dn" x="{bm.f1(mid[0])}" y="{bm.f1(mid[1] + dy)}" text-anchor="middle">{html.escape(day)}</text>')
    if rid == "G":
        _, vla, vlo = pt(points, "VICFALLS")
        vx, vy = proj.xy(vlo, vla)
        labels.append(f'<text class="dn c" x="{bm.f1(vx - 12)}" y="{bm.f1(vy - 34)}" text-anchor="end">Day 24〜31 滝周辺3か国</text>')
    dots, names = [], []
    for pid in used:
        n, lat, lon = pt(points, pid)
        x, y = proj.xy(lon, lat)
        if not proj.in_view(x, y, -4):
            continue
        dots.append(f'<circle class="pt" cx="{bm.f1(x)}" cy="{bm.f1(y)}" r="4.5"/>')
        names.append(f'<text class="tx" x="{bm.f1(x + 8)}" y="{bm.f1(y - 7)}" text-anchor="start">{html.escape(n)}</text>')
    return "".join(lines), "".join(dots), "".join(names), "".join(labels)


def build_africa(points, geo, routes):
    """5月の案（モーリシャス以南）と8月の案（ケープタウン→日本）で、地図の範囲を分けた2枚を作る。切り替えで見える方だけ表示"""
    visit_may = {"480", "450", "710", "716", "894", "072", "516"}
    visit_aug = {"404", "834", "710", "426", "748", "508", "516", "072", "634", "784"}
    out = []
    for kind, ids, win, lon0, lat0, visit in (
            ("may", MAY_IDS, (10.0, 62.0, -37.0, -8.0), 37.0, -22.0, visit_may),
            ("aug", AUG_IDS, (14.0, 62.0, -36.0, 27.0), 38.0, -4.0, visit_aug)):
        proj = bm.Laea(lon0, lat0, win)
        W, H = proj.width, proj.height
        outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
        grat = bm.graticule(proj, 10, 10, (0, 80), (-40, 40))
        groups = []
        for rid in ids:
            if rid not in routes:
                continue
            ln, dt, nm, lb = route_svg(proj, points, routes[rid]["legs"], rid)
            on = rid == "G"
            groups.append(f'<g class="rt{" on" if on else ""}" data-rt="{rid}" style="display:{"inline" if on else "none"}">{ln}{dt}{nm}{lb}</g>')
        hid = "" if kind == "may" else " hidden"
        out.append(f'<div class="mapbox" data-pan="{kind}"{hid}><svg class="m" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" role="img" aria-label="{"5月" if kind == "may" else "8月"}の案の全体図">'
                   f'<defs><clipPath id="c1{kind}"><path d="{outline}"/></clipPath></defs><g clip-path="url(#c1{kind})">'
                   f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/><g>{land_svg(proj, geo, visit, 0.5)}</g>'
                   f'{"".join(groups)}</g><path class="frame" d="{outline}"/></svg></div>')
    return "".join(out)


def africa_may_svg(id_prefix: str = "") -> str:
    """トップページ用：5月の案G だけの地図（SVG1枚。約46KB）。8月の地図やマダガスカル拡大は含めない。
    id_prefix は <clipPath> の id を、ページ内の他の地図と重ねないための接頭辞"""
    points, routes = bm.load_model()
    geo = bm.load_topo("countries-50m.json")
    visit = {"480", "450", "710", "716", "894", "072", "516"}
    proj = bm.Laea(37.0, -22.0, (10.0, 62.0, -37.0, -8.0))
    W, H = proj.width, proj.height
    outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
    grat = bm.graticule(proj, 10, 10, (0, 80), (-40, 40))
    ln, dt, nm, lb = route_svg(proj, points, routes["G"]["legs"], "G")
    cid = f"{id_prefix}c1may"
    return (f'<svg class="m" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" role="img" aria-label="5月の案Gの全体図（モーリシャス以南）">'
            f'<defs><clipPath id="{cid}"><path d="{outline}"/></clipPath></defs><g clip-path="url(#{cid})">'
            f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/><g>{land_svg(proj, geo, visit, 0.5)}</g>'
            f'<g class="rt on" data-rt="G">{ln}{dt}{nm}{lb}</g></g><path class="frame" d="{outline}"/></svg>')


def build_madagascar(points, geo):
    proj = bm.Laea(46.5, -19.0, (42.5, 51.5, -23.5, -15.5), width=700.0)
    W, H = proj.width, proj.height
    outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
    grat = bm.graticule(proj, 2, 2, (40, 54), (-26, -12))
    land = land_svg(proj, geo, {"450"}, 0.2)
    groups = []
    for key, plan in PLANS.items():
        lines, labels = [], []
        for i, (a, b, day, mode) in enumerate(plan["legs"]):
            if "MRU" in (a, b):
                continue
            pa, pb = pt(points, a), pt(points, b)
            d, pts = leg_path(proj, pa, pb, mode == "flight", 16)
            # 同じ2点の往復（TNR↔アンダシベ、TNR↔モロンダバ）は左右にずらす
            back = sum(1 for (a2, b2, _d, _m) in plan["legs"][:i] if {a2, b2} == {a, b})
            if {a, b} != {"MRU", "TNR"}:
                d, mid = offset_line(pts, 16)
            else:
                mid = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
            cls = MODE_STYLE[mode][0]
            lines.append(f'<path class="ln {cls}" d="{d}"><title>{html.escape(pa[0])}→{html.escape(pb[0])}（{day}）</title></path>')
            tcls = "a" if mode == "flight" else ("b" if mode == "domestic" else "c")
            labels.append(f'<text class="dn {tcls}" x="{bm.f1(mid[0])}" y="{bm.f1(mid[1])}" text-anchor="middle">{html.escape(day)}</text>')
        groups.append(f'<g class="plan{" on" if key == "now" else ""}" data-plan="{key}" style="display:{"inline" if key == "now" else "none"}">{"".join(lines)}{"".join(labels)}</g>')
    dots, names = [], []
    for pid, dx, dy, anchor in (("MRU", 0, 0, "start"), ("TNR", 12, -10, "start"), ("ANDASIBE", 12, 0, "start"), ("MORONDAVA", -12, 4, "end")):
        if pid == "MRU":
            continue
        n, lat, lon = pt(points, pid)
        x, y = proj.xy(lon, lat)
        dots.append(f'<circle class="pt" cx="{bm.f1(x)}" cy="{bm.f1(y)}" r="6"/>')
        names.append(f'<text class="tx big" x="{bm.f1(x + dx)}" y="{bm.f1(y + dy)}" text-anchor="{anchor}">{html.escape(n)}</text>')
    # モーリシャスは図の外（東）。首都から北東へ弧を描いて図の端へ出し、方向だけ示す
    tx, ty = proj.xy(47.4788, -18.7969)
    ex, ey = proj.xy(51.5, -16.2)
    cx, cy = (tx + ex) / 2 - 10, (ty + ey) / 2 - 38
    arrow = (f'<path class="ln fl" d="M{bm.f1(tx)} {bm.f1(ty)}Q{bm.f1(cx)} {bm.f1(cy)} {bm.f1(ex)} {bm.f1(ey)}"/>'
             f'<text class="tx" x="{bm.f1(ex - 6)}" y="{bm.f1(ey - 12)}" text-anchor="end">→ モーリシャス（東へ約1,700km）</text>')
    return (f'<svg class="m" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" role="img" aria-label="マダガスカル拡大図。日数案ごとに経路が変わる">'
            f'<defs><clipPath id="c2"><path d="{outline}"/></clipPath></defs><g clip-path="url(#c2)">'
            f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/><g>{land}</g>{"".join(groups)}'
            f'<g>{arrow}</g><g>{"".join(dots)}</g><g>{"".join(names)}</g></g><path class="frame" d="{outline}"/></svg>')


def build() -> str:
    points, routes = bm.load_model()
    geo = bm.load_topo("countries-50m.json")
    africa = build_africa(points, geo, routes)
    mada = build_madagascar(points, geo)

    def chip(rid):
        rt = routes[rid]
        inf = bm.ROUTE_INFO.get(rid)
        tip = rt["name"] + (("｜確認できた費用の小計：" + inf[0]) if inf else "")
        chk = " checked" if rid == "G" else ""
        return (f'<label title="{html.escape(tip)}"><input type="radio" name="rt" value="{rid}"{chk}>'
                f'<span>{html.escape(short_name(rid, rt["name"]))}</span></label>')
    may_n = len([r for r in MAY_IDS if r in routes])
    aug_n = len([r for r in AUG_IDS if r in routes])
    may_chips = "".join(chip(r) for r in MAY_IDS if r in routes)
    aug_chips = "".join(chip(r) for r in AUG_IDS if r in routes)
    rtabs = ('<div class="tabs" role="tablist" aria-label="5月と8月の切替">'
             f'<button type="button" role="tab" data-tab="may" aria-selected="true">5月の案（{may_n}）</button>'
             f'<button type="button" role="tab" data-tab="aug" aria-selected="false">8月の案（{aug_n}）</button></div>'
             f'<div class="chips" data-pan="may">{may_chips}</div><div class="chips" data-pan="aug" hidden>{aug_chips}</div>')
    g_info = ('案Gは35日表（Day 番号つき）。費用は<a href="../research/may-madagascar-vfa-redesign.html">ルート調査</a>と'
              '<a href="../research/africa-budget-fermi.html">フェルミ予算</a>を参照')
    info_parts = []
    for r in MAY_IDS + AUG_IDS:
        if r not in routes:
            continue
        if r in bm.ROUTE_INFO:
            body = "確認できた費用の小計：" + html.escape(bm.ROUTE_INFO[r][0]) + "／主な未確認：" + html.escape(bm.ROUTE_INFO[r][2])
        else:
            body = g_info
        disp = "block" if r == "G" else "none"
        info_parts.append(f'<div class="rinfo" data-rt="{r}" style="display:{disp}"><b>{html.escape(routes[r]["name"])}</b>{body}</div>')
    infos_r = "".join(info_parts)
    btns_cal = "".join(f'<button type="button" data-cplan="{k}" aria-pressed="{"true" if k == "now" else "false"}">{html.escape(p["label"])}</button>' for k, p in PLANS.items())
    cal_key = "".join(f'<span><i style="background:var(--c-{k})"></i>{v}</span>' for k, v in KIND_LABEL.items())
    cal_blocks = "".join(f'<div class="calbox" data-cplan="{k}"{"" if k == "now" else " hidden"}>{calendar_html(k)}</div>' for k in PLANS)
    aug_btns = "".join(f'<button type="button" data-aplan="{k}" aria-pressed="{"true" if i == 0 else "false"}">{html.escape(v["label"])}</button>' for i, (k, v) in enumerate(AUG_PLANS.items()))
    aug_infos = "".join(f'<p class="pinfo aplan" data-aplan="{k}"{"" if i == 0 else " hidden"}><b>{html.escape(v["label"])}</b>{html.escape(v["note"])}</p>' for i, (k, v) in enumerate(AUG_PLANS.items()))
    aug_blocks = "".join(f'<div class="calbox acal" data-aplan="{k}"{"" if i == 0 else " hidden"}>{calendar_html(k, aug_calendar_days(k))}</div>' for i, k in enumerate(AUG_PLANS))
    zbtns = "".join(f'<button type="button" data-z="{z}" aria-pressed="false">{z}%</button>' for z in (70, 100, 125, 150))
    btns = "".join(f'<button type="button" data-plan="{k}" aria-pressed="{"true" if k == "now" else "false"}">{html.escape(p["label"])}</button>' for k, p in PLANS.items())
    infos = "".join(
        f'<div class="pinfo plan{" on" if k == "now" else ""}" data-plan="{k}" style="display:{"block" if k == "now" else "none"}"><b>{html.escape(p["label"])}（マダガスカル滞在{p["stay"]}暦日）</b>'
        f'出国 {html.escape(p["exit"])}／全体 {p["total"]}日。{html.escape(p["note"])}</div>' for k, p in PLANS.items())
    rows = "".join(
        f"<tr><th>{html.escape(p['label'])}</th><td>{html.escape(p['exit'])}</td><td>{p['total']}日</td><td>{html.escape(p['note'])}</td></tr>" for p in PLANS.values())
    legend = ('<div class="lg" aria-label="線の凡例">'
              '<span><svg width="34" height="10"><path d="M0 5H34" class="ln fl" style="stroke:var(--fl);stroke-dasharray:7 5;stroke-width:3;fill:none"/></svg>空路（国際線）</span>'
              '<span><svg width="34" height="10"><path d="M0 5H34" style="stroke:var(--dm);stroke-width:3;fill:none"/></svg>国内線（直線で例示）</span>'
              '<span><svg width="34" height="10"><path d="M0 5H34" style="stroke:var(--rd);stroke-width:3;fill:none"/></svg>昼間の車・陸路（直線で例示）</span></div>')

    return f"""<!doctype html>
<!-- generated by scripts/build_route_map.py from data/route_points.csv, data/geo/countries-50m.json; do not edit -->
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ルート地図（5月・8月）｜2027 留学・アフリカ周遊</title>
<style>
{CSS}</style>{FONT_SIZE_JS}</head><body>
{bar("../", "maps/route-map.html")}
<main class="wrap page">
<p class="crumb"><a href="../index.html">トップ</a> ／ ルート地図</p>
<div class="map-top"><h1>ルート地図（5月・8月の案）</h1>
<div class="zoom" role="group" aria-label="地図の表示サイズ"><span>地図のサイズ：</span>{zbtns}</div></div>
<p class="muted map-sub">5月の案はモーリシャス以南、8月の案はケープタウンから日本までを表示します。</p>
<div class="rsel" role="group" aria-label="表示するルート">{rtabs}</div>
<div class="rwrap"><div class="zwrap">{africa}</div><div class="rside">{infos_r}</div></div>
{legend}
<p class="lead" style="margin-top:14px">モーリシャス→マダガスカル→ビクトリアの滝周辺3か国→ケープタウンの35日モデル。線の横の「Day」は、<a href="../research/may-madagascar-vfa-redesign.html#day-1day-35乗継と国内移動を含む相対日モデル">35日表</a>の日です。Day 1 は 2027年5月3日の仮置きで、確定した日程ではありません。</p>
{bm.map_switch("route-map")}
<h2>2. カレンダー（5月・8月）</h2>
<div class="tabs" role="tablist" aria-label="カレンダーの月"><button type="button" role="tab" data-ctab="may" aria-selected="true">5月の案G</button><button type="button" role="tab" data-ctab="aug" aria-selected="false">8月の案（代表4案）</button></div>
<div data-cpan="may">
<p>日付と曜日、国、移動・観光・予備を月ごとの表にしたものです。マダガスカルの日数案（現行・A・B・C）で切り替わります。Day 1 は2027年5月3日（月）の仮置きで、確定した日程ではありません。</p>
<div class="plans" role="group" aria-label="日数案（カレンダー）">{btns_cal}</div>
<div class="cal-key" aria-label="色の凡例">{cal_key}</div>
{cal_blocks}
</div>
<div data-cpan="aug" hidden>
<p>8月は、ケープタウンの留学終了後に出発し、<b>8/20（金）までの日本着を優先</b>した約20日の案です（<b>8/24を許容の上限</b>とする目安。予約・確定はしていません）。Day 1 は8/1（日）の仮置きで、確定した日程ではありません。MPM→NBO（水・金・日）、WDH↔CPTのバス（水・金・日）など、確認できた曜日の制約には合わせてあります。運賃・便は未確認です。</p>
<div class="plans" role="group" aria-label="8月の案（カレンダー）">{aug_btns}</div>
{aug_infos}
<div class="cal-key" aria-label="色の凡例">{cal_key}</div>
{aug_blocks}
</div>
<h2>3. マダガスカル拡大図（日数案で切り替え）</h2>
<p>アフリカ全体の縮尺では首都・アンダシベ・モロンダバが重なるので、島だけを拡大しています。下のボタンで、日数案ごとの動きと日が切り替わります。</p>
<div class="plans" role="group" aria-label="マダガスカルの日数案">{btns}</div>
{infos}
<div class="zwrap"><div class="mapbox">{mada}</div></div>
{legend}
<h3>日数案の一覧</h3>
<table class="pl"><thead><tr><th>案</th><th>出国</th><th>全体</th><th>欠航の予備など</th></tr></thead><tbody>{rows}</tbody></table>
<p class="muted">経路は点を結んだ概念図で、実際の道路・航路ではありません。空路は大圏の曲線、国内線・陸路は直線です。アンダシベ・モロンダバの座標は概略です。国内線の曜日・時刻・運賃、MRU↔TNRの運航曜日は未確認で、日付は仮置きです。国境線は概念図としての表示で、各国の公式な主張を表すものではありません。往復する区間は、重ならないよう線を左右にずらして描いています。</p>
<footer><nav class="all" id="all-pages" aria-label="全ページ">{site_nav(ROOT, ROOT / "maps" / "route-g.html")}</nav><p>地図データ：<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（パブリックドメイン）を <a href="https://github.com/topojson/world-atlas" target="_blank" rel="noopener">world-atlas</a> 2.0.2（ISC）経由で使用し、ランベルト正積方位図法で描画。このページは <code>scripts/build_route_map.py</code> が自動生成します（手で編集しない）。外部の通信は行いません。</p></footer>
</main>
<script>
(function(){{
var zs=document.querySelectorAll(".zoom button"),KEY="route-g-zoom-v2";
function zoom(z){{var r=document.documentElement.style;r.setProperty("--zf",(z/100).toFixed(2));r.setProperty("--ts",Math.max(1,Math.min(1.5,100/z)).toFixed(2));zs.forEach(function(b){{b.setAttribute("aria-pressed",b.getAttribute("data-z")===String(z)?"true":"false")}});try{{localStorage.setItem(KEY,String(z))}}catch(e){{}}}}
document.querySelectorAll(".mapbox svg").forEach(function(v){{var q=(v.getAttribute("viewBox")||"").split(" ");if(q.length===4&&+q[3])v.parentNode.style.setProperty("--ar",(q[2]/q[3]).toFixed(3))}});
var z0=100;try{{var sv=localStorage.getItem(KEY);if(sv&&[70,100,125,150].indexOf(+sv)>=0)z0=+sv}}catch(e){{}}
zoom(z0);zs.forEach(function(b){{b.addEventListener("click",function(){{zoom(+b.getAttribute("data-z"))}})}});
var rs=document.querySelectorAll('.chips input[name=rt]');
function pickRt(k){{document.querySelectorAll('.rt').forEach(function(g){{g.style.display=g.getAttribute('data-rt')===k?'inline':'none'}});
 document.querySelectorAll('.rinfo').forEach(function(e){{e.style.display=e.getAttribute('data-rt')===k?'block':'none'}});
 rs.forEach(function(r){{r.checked=r.value===k}})}}
rs.forEach(function(r){{r.addEventListener('change',function(){{pickRt(r.value)}})}});
document.querySelectorAll('.tabs button').forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-tab');
 document.querySelectorAll('.tabs button').forEach(function(x){{x.setAttribute('aria-selected',x===b?'true':'false')}});
 document.querySelectorAll('.chips').forEach(function(c){{c.hidden=c.getAttribute('data-pan')!==k}});
 document.querySelectorAll('.mapbox[data-pan]').forEach(function(c){{c.hidden=c.getAttribute('data-pan')!==k}});
 var first=document.querySelector('.chips[data-pan='+k+'] input');if(first){{pickRt(first.value)}}}})}});
var hm=/^#route-([A-Z][A-Z0-9]*)$/.exec(location.hash);
if(hm){{var tr=document.querySelector('.chips input[value="'+hm[1]+'"]');if(tr){{var pn=tr.closest('.chips').getAttribute('data-pan');var tb=document.querySelector('.tabs button[data-tab="'+pn+'"]');if(tb)tb.click();pickRt(hm[1])}}}}
var cbs=document.querySelectorAll('button[data-cplan]');
cbs.forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-cplan');
 cbs.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false')}});
 document.querySelectorAll('.calbox').forEach(function(c){{c.hidden=c.getAttribute('data-cplan')!==k}})}})}});
var cm=/^#cal-(now|A|B|C)$/.exec(location.hash);if(cm){{var cb=document.querySelector('button[data-cplan="'+cm[1]+'"]');if(cb)cb.click()}}
var abs=document.querySelectorAll('button[data-aplan]');
abs.forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-aplan');
 abs.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false')}});
 document.querySelectorAll('.acal,.aplan').forEach(function(c){{c.hidden=c.getAttribute('data-aplan')!==k}})}})}});
document.querySelectorAll('button[data-ctab]').forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-ctab');
 document.querySelectorAll('button[data-ctab]').forEach(function(x){{x.setAttribute('aria-selected',x===b?'true':'false')}});
 document.querySelectorAll('[data-cpan]').forEach(function(c){{c.hidden=c.getAttribute('data-cpan')!==k}})}})}});
var am=/^#cal-(A[0-9]+)$/.exec(location.hash);if(am){{var ab=document.querySelector('button[data-aplan="'+am[1]+'"]');var tb2=document.querySelector('button[data-ctab="aug"]');if(ab&&tb2){{tb2.click();ab.click()}}}}
var bs=document.querySelectorAll(".plans button[data-plan]");
function show(k){{
 bs.forEach(function(b){{b.setAttribute("aria-pressed",b.getAttribute("data-plan")===k?"true":"false")}});
 document.querySelectorAll("[data-plan].plan").forEach(function(e){{e.style.display=e.getAttribute("data-plan")===k?(e.tagName.toLowerCase()==="g"?"inline":"block"):"none"}});
}}
bs.forEach(function(b){{b.addEventListener("click",function(){{show(b.getAttribute("data-plan"));try{{history.replaceState(null,"","#"+b.getAttribute("data-plan"))}}catch(e){{}}}})}});
var h=decodeURIComponent((location.hash||"").slice(1));
if(h&&document.querySelector('.plans button[data-plan="'+h+'"]'))show(h);
}})();
</script>
</body></html>
"""


def main() -> int:
    text = build()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("案Gの地図HTMLが古いです。`py scripts/build_route_map.py` を実行してコミットしてください", file=sys.stderr)
            return 1
        print("PASS: route-map map is current")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT).as_posix()}: {len(text.encode('utf-8')) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
