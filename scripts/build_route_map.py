# -*- coding: utf-8 -*-
"""案G（35日モデル）の地図 maps/route-g.html を生成する。標準ライブラリのみ。

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
from build_html import BASE_CSS, bar, nav as site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "maps" / "route-g.html"

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
MODE_STYLE = {"flight": ("fl", "空路"), "domestic": ("dm", "国内線（直線で例示）"), "road": ("rd", "昼間の車（直線で例示）"), "overland": ("rd", "陸路（直線で例示）")}

CSS = BASE_CSS + """
:root{--sea:#e6eef3;--land:#f4f1e8;--border:#b9b4a4;--grat:#cdd8df;--fl:#9B1D20;--dm:#1B7A8C;--rd:#8A6D00;--pt:#1d2227}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--fl:#F2A1A3;--dm:#9AD9E6;--rd:#F2C94C;--pt:#fbfbfa}}
:root[data-theme="dark"]{--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--fl:#F2A1A3;--dm:#9AD9E6;--rd:#F2C94C;--pt:#fbfbfa}
.zwrap{overflow:auto;margin:6px 0;max-width:100%}
h1{margin:6px 0!important;font-size:1.35rem!important}.crumb{margin:6px 0!important}h2.mt{margin:6px 0!important;font-size:1.05rem!important}
.mapbox{position:relative;border:1px solid var(--line);width:calc(min(100%,(100vh - 215px) * var(--ar,1.6)) * var(--zf,1))}
.zoom{position:sticky;top:var(--bar,44px);z-index:5;display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0;padding:6px 0;background:var(--bg);border-bottom:1px solid var(--line)}
.zoom button{font:inherit;min-width:56px;min-height:40px;padding:4px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);cursor:pointer}
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


def build_africa(points, geo):
    proj = bm.Laea(37.0, -22.0, (10.0, 66.0, -37.0, -8.0))
    visit = {"480", "450", "710", "716", "894", "072"}
    W, H = proj.width, proj.height
    outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
    grat = bm.graticule(proj, 10, 10, (0, 80), (-40, 0))
    lines, labels = [], []
    seen = {}
    for i, (a, b, mode, day) in enumerate(MAIN_LEGS):
        pa, pb = pt(points, a), pt(points, b)
        cls = MODE_STYLE[mode][0]
        # 同じ区間の往復は曲線を左右にずらす
        key = tuple(sorted((a, b)))
        seen[key] = seen.get(key, 0) + 1
        if a == "BOM":
            continue
        d, pts = leg_path(proj, pa, pb, mode == "flight")
        if seen[key] > 1 or key in {("MRU", "TNR"), ("KASANE", "LIVINGSTONE"), ("KASANE", "VICFALLS")}:
            d, mid = offset_line(pts, 10)
        else:
            mid = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
        lines.append(f'<path class="ln {cls}" d="{d}"><title>{html.escape(pa[0])}→{html.escape(pb[0])}（{day}）</title></path>')
        if day:
            labels.append(f'<text class="dn" x="{bm.f1(mid[0])}" y="{bm.f1(mid[1] + (-8 if a == "MRU" else 14))}" text-anchor="middle">{html.escape(day)}</text>')
    # 日本から（図の外）。ムンバイ方向へ大圏の線を引き、図の端で切る
    _, la, lo = pt(points, "MRU")
    bn, bla, blo = pt(points, "BOM")
    d, _pts = leg_path(proj, ("", la, lo), ("", bla, blo), True)
    lines.append(f'<path class="ln fl" d="{d}"><title>日本→ムンバイ→モーリシャス（Day 1〜2）</title></path>')
    mxx, myy = proj.xy(lo, la)
    labels.append(f'<text class="dn" x="{bm.f1(mxx + 8)}" y="{bm.f1(myy - 34)}" text-anchor="start">日本から Day 1〜2</text>')
    # 滝周辺3か国は線が短く重なるので、日をまとめて1か所に書く
    _, vla, vlo = pt(points, "VICFALLS")
    vx, vy = proj.xy(vlo, vla)
    labels.append(f'<text class="dn c" x="{bm.f1(vx - 12)}" y="{bm.f1(vy - 34)}" text-anchor="end">Day 24〜31 滝周辺3か国</text>')
    dots, names = [], []
    for pid, dx, dy, anchor in (("MRU", 12, 16, "start"), ("TNR", -12, -8, "end"), ("JNB", 12, 4, "start"), ("VICFALLS", -10, -8, "end"),
                                ("CPT", 12, 4, "start")):
        n, lat, lon = pt(points, pid)
        x, y = proj.xy(lon, lat)
        dots.append(f'<circle class="pt" cx="{bm.f1(x)}" cy="{bm.f1(y)}" r="5"/>')
        names.append(f'<text class="tx" x="{bm.f1(x + dx)}" y="{bm.f1(y + dy)}" text-anchor="{anchor}">{html.escape(n)}</text>')
    return (f'<svg class="m" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" role="img" aria-label="案Gの全体経路（アフリカ南部）">'
            f'<defs><clipPath id="c1"><path d="{outline}"/></clipPath></defs><g clip-path="url(#c1)">'
            f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/><g>{land_svg(proj, geo, visit, 0.5)}</g>'
            f'<g>{"".join(lines)}</g><g>{"".join(dots)}</g><g>{"".join(names)}</g><g>{"".join(labels)}</g></g><path class="frame" d="{outline}"/></svg>')


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
    points, _routes = bm.load_model()
    geo = bm.load_topo("countries-50m.json")
    africa = build_africa(points, geo)
    mada = build_madagascar(points, geo)

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
<title>案Gルート地図｜2027 留学・アフリカ周遊</title>
<style>
{CSS}</style></head><body>
{bar("../", "maps/route-g.html")}
<main class="wrap page">
<p class="crumb"><a href="../index.html">トップ</a> ／ ルート地図</p>
<h1>案Gのルート地図（Day 番号つき）</h1>
<div class="zoom" role="group" aria-label="地図の表示サイズ"><span>地図のサイズ：</span>{zbtns}</div>
<h2 class="mt">1. 全体（アフリカ南部）</h2>
<div class="zwrap"><div class="mapbox">{africa}</div></div>
{legend}
<p class="lead" style="margin-top:14px">モーリシャス→マダガスカル→ビクトリアの滝周辺3か国→ケープタウンの35日モデル。線の横の「Day」は、<a href="../research/may-madagascar-vfa-redesign.html#day-1day-35乗継と国内移動を含む相対日モデル">35日表</a>の日です。Day 1 は 2027年5月3日の仮置きで、確定した日程ではありません。</p>
{bm.map_switch("route-g")}
<h2>2. マダガスカル拡大図（日数案で切り替え）</h2>
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
var bs=document.querySelectorAll(".plans button");
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
        print("PASS: route-g map is current")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT).as_posix()}: {len(text.encode('utf-8')) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
