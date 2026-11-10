# -*- coding: utf-8 -*-
"""国別ページ（countries/<slug>.md）に差し込む「おおよその位置の地図」(SVG) を作る。標準ライブラリのみ。

- 入力: data/country_places.csv（地点の緯度経度・出典URL）、data/geo/countries-50m.json（国境。Natural Earth）、
        data/routes.csv + data/route_points.csv（候補ルートのうち、その国の中で完結する区間）
- 出力: build_html.py が `@@COUNTRY-MAP@@` の位置へ埋め込む HTML 断片（外部通信なし）
- 地図は概念図。国境線は各国の公式な主張を表さない。地点は町・公園の代表点で、入口や空港の位置そのものではない。
  線は2点を結ぶ直線で、実際の道路や航路ではない。
"""
from __future__ import annotations

import csv
import html
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_maps as bm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KIND_JA = {"city": "町", "park": "公園・保護区", "lake": "湖畔", "falls": "滝", "coast": "海岸・島", "site": "見どころ"}
KIND_SHAPE = {"city": "sq", "park": "tri", "lake": "dia", "falls": "dia", "coast": "dia", "site": "circ"}
# 国ごとの投影の枠（余白をつけた緯度経度の範囲）を自動計算するときの余白（度）
PAD = 0.4
WIDTH = 760.0

CSS = """
.cmap{margin:14px 0 8px;max-width:100%}
.cm-box{position:relative;border:1px solid var(--line);background:var(--cm-sea);touch-action:pan-y}
.cm-box.zoomed{touch-action:none;cursor:grab}
.cm-zoom{position:absolute;right:8px;top:8px;display:flex;gap:4px}
.cm-zoom button{font:inherit;min-width:44px;min-height:44px;padding:0 10px;background:var(--bg);color:var(--ink);border:1px solid var(--line);cursor:pointer}
.cm-zoom button:hover,.cm-zoom button:focus-visible{background:var(--hl)}
.cmap details.cm-more{margin:6px 0;border:1px solid var(--line);padding:2px 10px;background:var(--bg)}
.cmap details.cm-more summary{cursor:pointer;min-height:40px;display:flex;align-items:center;font-weight:700}
.cmap .cm-box svg{display:block;width:100%;max-width:100%;height:auto;max-height:min(62vh,640px);min-height:240px;margin:0 auto;background:var(--cm-sea);user-select:none;-webkit-user-select:none}
.cmap .cm-land{fill:var(--cm-land);stroke:var(--cm-border);stroke-width:.6;fill-rule:evenodd;stroke-linejoin:round}
.cmap .cm-me{fill:var(--cm-me);stroke:var(--cm-meb);stroke-width:1.3;fill-rule:evenodd;stroke-linejoin:round}
.cmap .cm-leg{fill:none;stroke:var(--link);stroke-width:2.6;stroke-dasharray:6 4;opacity:.9}
.cmap .pt{fill:var(--cm-pt);stroke:var(--cm-ptb);stroke-width:1.4}
.cmap .pt.city{fill:var(--cm-city)}
.cmap text.cm-t{font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--cm-sea);stroke-width:3.4px;stroke-linejoin:round;font-family:var(--sans)}
.cmap text.cm-n{font-size:calc(10.5px * var(--ts,1));fill:var(--muted);paint-order:stroke;stroke:var(--cm-sea);stroke-width:3px;font-family:var(--sans)}
.cm-key{display:flex;flex-wrap:wrap;gap:6px 18px;margin:8px 0;font-size:.9rem;color:var(--muted)}
.cm-key span{display:inline-flex;align-items:center;gap:6px}
.cmap .cm-key svg{display:inline-block;width:22px;height:14px;min-height:0;max-height:none;flex:none;color:var(--cm-ptb);background:none}
.cm-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:2px 16px;margin:6px 0;padding:0;list-style:none;font-size:.92rem}
.cm-list li{max-width:none}
:root{--cm-sea:#e6eef3;--cm-land:#e9e5d8;--cm-border:#b9b4a4;--cm-me:#fffdf4;--cm-meb:#6f6a5a;--cm-pt:#fff;--cm-ptb:#0a58a8;--cm-city:#0a58a8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--cm-sea:#1a2530;--cm-land:#232724;--cm-border:#59605a;--cm-me:#3d4540;--cm-meb:#aab5ad;--cm-pt:#16181a;--cm-ptb:#7db4ec;--cm-city:#7db4ec}}
:root[data-theme="dark"]{--cm-sea:#1a2530;--cm-land:#232724;--cm-border:#59605a;--cm-me:#3d4540;--cm-meb:#aab5ad;--cm-pt:#16181a;--cm-ptb:#7db4ec;--cm-city:#7db4ec}
"""


ZOOM_JS = """<script>
(function(){
if(window.__cmInit)return;window.__cmInit=1;
document.querySelectorAll('.cm-box').forEach(function(box){
 var svg=box.querySelector('svg'),W=+svg.dataset.w,H=+svg.dataset.h,vb={x:0,y:0,w:W,h:H},drag=null;
 function clamp(){vb.x=Math.max(0,Math.min(W-vb.w,vb.x));vb.y=Math.max(0,Math.min(H-vb.h,vb.y))}
 function set(){svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);box.classList.toggle('zoomed',vb.w<W-1)}
 function zoom(f){var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2,w=Math.max(W/8,Math.min(W,vb.w/f)),h=w*H/W;vb.w=w;vb.h=h;vb.x=cx-w/2;vb.y=cy-h/2;clamp();set()}
 box.querySelectorAll('.cm-zoom button').forEach(function(b){b.addEventListener('click',function(){var z=b.dataset.z;if(z==='in')zoom(1.6);else if(z==='out')zoom(1/1.6);else{vb={x:0,y:0,w:W,h:H};set()}})});
 svg.addEventListener('pointerdown',function(e){if(vb.w>=W-1)return;drag={x:e.clientX,y:e.clientY,vx:vb.x,vy:vb.y};svg.setPointerCapture(e.pointerId)});
 svg.addEventListener('pointermove',function(e){if(!drag)return;var r=svg.getBoundingClientRect(),k=Math.max(vb.w/r.width,vb.h/r.height);vb.x=drag.vx-(e.clientX-drag.x)*k;vb.y=drag.vy-(e.clientY-drag.y)*k;clamp();set()});
 svg.addEventListener('pointerup',function(){drag=null});svg.addEventListener('pointercancel',function(){drag=null});
});
})();
</script>"""


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_places(root: Path = ROOT) -> dict:
    by: dict = {}
    for r in read_csv(root / "data" / "country_places.csv"):
        by.setdefault(r["slug"], []).append(r)
    return by


def load_country_iso(root: Path = ROOT) -> dict:
    return {r["slug"]: r for r in read_csv(root / "data" / "countries.csv")}


def in_country_legs(root: Path, country_ja: str) -> list[dict]:
    """案A〜Hのうち、出発点と到着点がどちらもその国にある区間（国内移動）。重複する区間は1本にする"""
    pts = {r["id"]: r for r in read_csv(root / "data" / "route_points.csv")}
    seen, out = set(), []
    for r in read_csv(root / "data" / "routes.csv"):
        a, b = pts.get(r["from_point"]), pts.get(r["to_point"])
        if not a or not b or a["country"] != country_ja or b["country"] != country_ja:
            continue
        key = (r["from_point"], r["to_point"], r["mode"])
        if key in seen:
            continue
        seen.add(key)
        out.append({"a": a, "b": b, "mode": r["mode"], "routes": [r["route_id"]]})
    # 同じ区間が複数の案に出るときは、案の記号を集める
    merged: dict = {}
    for r in read_csv(root / "data" / "routes.csv"):
        a, b = pts.get(r["from_point"]), pts.get(r["to_point"])
        if a and b and a["country"] == country_ja and b["country"] == country_ja:
            merged.setdefault((r["from_point"], r["to_point"], r["mode"]), []).append(r["route_id"])
    for o in out:
        o["routes"] = merged[(o["a"]["id"], o["b"]["id"], o["mode"])]
    return out


def main_land_box(geo, iso: str):
    """その国の主な領土（点数が最大のポリゴン）の外接枠 (lonmin, lonmax, latmin, latmax)。離島・海外領土で枠が広がりすぎないようにする"""
    best = None
    for c in geo:
        if c["id"] != iso:
            continue
        for poly in c["polys"]:
            ring = poly[0]
            if best is None or len(ring) > len(best):
                best = ring
    if not best:
        return None
    return (min(x for x, _ in best), max(x for x, _ in best), min(y for _, y in best), max(y for _, y in best))


def bounds(points: list[dict], land=None) -> tuple:
    lats = [float(p["lat"]) for p in points]
    lons = [float(p["lon"]) for p in points]
    lo, hi, la, lb = min(lons), max(lons), min(lats), max(lats)
    if land:
        lo, hi, la, lb = min(lo, land[0]), max(hi, land[1]), min(la, land[2]), max(lb, land[3])
    return (lo - PAD, hi + PAD, la - PAD, lb + PAD)


def marker(shape: str, x: float, y: float, cls: str, k: float = 1.0) -> str:
    """記号。k は縮小される分の補正（画面で同じ大きさに見えるようにする）"""
    a, b = 5 * k, 6 * k
    if shape == "sq":
        return f'<rect class="pt {cls}" x="{bm.f1(x - a)}" y="{bm.f1(y - a)}" width="{bm.f1(2 * a)}" height="{bm.f1(2 * a)}"/>'
    if shape == "tri":
        return f'<path class="pt {cls}" d="M{bm.f1(x)} {bm.f1(y - b)}L{bm.f1(x + b)} {bm.f1(y + a)}L{bm.f1(x - b)} {bm.f1(y + a)}Z"/>'
    if shape == "dia":
        return f'<path class="pt {cls}" d="M{bm.f1(x)} {bm.f1(y - b)}L{bm.f1(x + b)} {bm.f1(y)}L{bm.f1(x)} {bm.f1(y + b)}L{bm.f1(x - b)} {bm.f1(y)}Z"/>'
    return f'<circle class="pt {cls}" cx="{bm.f1(x)}" cy="{bm.f1(y)}" r="{bm.f1(a)}"/>'


def render(slug: str, root: Path = ROOT, geo=None) -> str:
    places = load_places(root).get(slug, [])
    cinfo = load_country_iso(root).get(slug)
    if not places or not cinfo:
        return ""
    geo = geo or bm.load_topo("countries-50m.json")
    lonmin, lonmax, latmin, latmax = bounds(places, main_land_box(geo, cinfo["iso_numeric"]))
    lat0, lon0 = (latmin + latmax) / 2, (lonmin + lonmax) / 2
    proj = bm.Laea(lon0, lat0, (lonmin, lonmax, latmin, latmax), width=WIDTH)
    paths = bm.ring_paths(proj, geo, 0.35, skip=("010",))
    iso = cinfo["iso_numeric"]
    land = []
    for cid, (name, d) in paths.items():
        cls = "cm-me" if cid == iso else "cm-land"
        land.append(f'<path class="{cls}" d="{d}"/>')

    shrink = min(1.0, 620.0 / proj.height) if proj.height > 620 else 1.0
    kk = max(1.0, min(2.0, 1.0 / shrink)) if shrink < 1.0 else 1.0
    items, dots = [], []
    for i, p in enumerate(places):
        x, y = proj.xy(float(p["lon"]), float(p["lat"]))
        shape = KIND_SHAPE.get(p["kind"], "circ")
        dots.append(marker(shape, x, y, p["kind"], kk))
        items.append({"id": i, "x": x, "y": y, "pref": "r", "lv0": p["name_ja"], "lv1": p["name_ja"],
                      "prio": 0 if p["kind"] == "city" else 1})
    # 国内の候補ルートの区間（点線）
    legs = []
    for lg in in_country_legs(root, cinfo["name_ja"]):
        ax, ay = proj.xy(float(lg["a"]["lon"]), float(lg["a"]["lat"]))
        bx, by = proj.xy(float(lg["b"]["lon"]), float(lg["b"]["lat"]))
        legs.append(f'<path class="cm-leg" d="M{bm.f1(ax)} {bm.f1(ay)}L{bm.f1(bx)} {bm.f1(by)}"><title>案{"・".join(lg["routes"])}：'
                    f'{html.escape(lg["a"]["name_ja"])}→{html.escape(lg["b"]["name_ja"])}（直線。実際の経路ではない）</title></path>')
    fs = max(14.0, min(26.0, 12.5 / shrink)) if shrink < 1.0 else 14.0  # 画面で約12.5pxになるよう、縮小される分だけ描画サイズを大きくする
    placed = bm.place_labels(items, [], fs, (2, 2, proj.width - 2, proj.height - 2))
    labels = []
    for i, p in enumerate(places):
        r = placed.get(i)
        if not r:
            # 置き場がない点は、枠内に収まる側（右か左）に重なりを許して置く。名前が欠けないことを優先する
            it = items[i]
            w = bm.text_w(p["name_ja"], fs) + 2
            right = it["x"] + 8 * kk + w <= proj.width - 2
            anchor = "start" if right else "end"
            tx = it["x"] + (8 * kk if right else -8 * kk)
            r = (p["name_ja"], anchor, tx, it["y"] + fs * 0.35, None, 0)
        txt, anchor, tx, ty, _rect, _lv = r
        labels.append(f'<text class="cm-t" style="font-size:{fs:.0f}px" x="{bm.f1(tx)}" y="{bm.f1(ty)}" text-anchor="{anchor}">{html.escape(txt)}</text>')

    W, H = proj.width, proj.height
    svg = (f'<svg id="cms-{slug}" data-w="{bm.f1(W)}" data-h="{bm.f1(H)}" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="{html.escape(cinfo["name_ja"])}のおおよその位置の地図。'
           f'町と見どころの位置を示す概念図">'
           f'<g>{"".join(land)}</g><g>{"".join(legs)}</g><g>{"".join(dots)}</g><g>{"".join(labels)}</g></svg>')
    def ico(shape):
        d = {"sq": '<rect x="6" y="2" width="10" height="10" fill="currentColor"/>',
             "tri": '<path d="M11 1L17 13H5Z" fill="none" stroke="currentColor" stroke-width="1.8"/>',
             "dia": '<path d="M11 1L17 7L11 13L5 7Z" fill="none" stroke="currentColor" stroke-width="1.8"/>',
             "circ": '<circle cx="11" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'}[shape]
        return f'<svg viewBox="0 0 22 14" aria-hidden="true">{d}</svg>'
    used = {p["kind"] for p in places}
    key = ('<p class="cm-key">' + "".join(f'<span>{ico(sh)}{lab}</span>' for kind, sh, lab in (
        ("city", "sq", "町"), ("park", "tri", "公園・保護区"), ("lake", "dia", "湖畔・滝・海岸"), ("site", "circ", "見どころ")) if kind in used or (kind == "lake" and used & {"falls", "coast"}))
           + ('<span><svg viewBox="0 0 22 14" aria-hidden="true"><path d="M1 7H21" stroke="var(--link)" stroke-width="2.2" stroke-dasharray="5 3"/></svg>候補ルートの国内区間（直線）</span>' if legs else '')
           + '</p>')
    lis = []
    for p in places:
        q = bm.maps_link(p["name_en"] + " " + cinfo["name_ja"]) if hasattr(bm, "maps_link") else ""
        note = f"（{html.escape(p['note'])}）" if p["note"] else ""
        lis.append(f'<li><a href="{html.escape(q)}" rel="noopener">{html.escape(p["name_ja"])}</a>'
                   f' <span class="muted">{KIND_JA.get(p["kind"], "")}{note}</span></li>')
    note = ('<p class="muted">位置は町・公園の代表点のおおよその値です（出典：各地点の Wikivoyage 記事の座標）。入口・空港の位置そのものではなく、'
            '国境線は概念図で各国の公式な主張を表しません。点線は2点を結ぶ直線で、実際の道路・航路ではありません。</p>')
    box = (f'<div class="cm-box" id="cmb-{slug}">{svg}<div class="cm-zoom" role="group" aria-label="地図の拡大・縮小">'
           f'<button type="button" data-z="in" aria-label="拡大">＋</button><button type="button" data-z="out" aria-label="縮小">－</button>'
           f'<button type="button" data-z="rs" aria-label="全体表示">全体</button></div></div>')
    more = f'<details class="cm-more"><summary>地点の一覧とGoogle Maps（{len(places)}か所）</summary><ul class="cm-list">{"".join(lis)}</ul></details>'
    return f'<div class="cmap">{box}{key}<p class="muted">拡大中はドラッグで動かせます。</p>{more}{note}</div>{ZOOM_JS}'


def main() -> int:
    geo = bm.load_topo("countries-50m.json")
    for slug in sorted(load_places()):
        frag = render(slug, ROOT, geo)
        print(slug, len(frag.encode("utf-8")) // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
