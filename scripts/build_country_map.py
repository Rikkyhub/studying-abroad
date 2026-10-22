# -*- coding: utf-8 -*-
"""アフリカの国別リンク地図（maps/africa-countries.html）を生成する。標準ライブラリのみ。

使い方（リポジトリのルートで実行）:
    py scripts/build_country_map.py           生成
    py scripts/build_country_map.py --check   生成物が最新でなければ失敗（CI用）

- 入力: data/countries.csv（国の一覧・ページ・一言）、data/geo/countries-50m.json（国境。Natural Earth）
- 出力: 外部通信なしの単独HTML。地図の国をクリック（タップ・Enter）すると、その国のページ（countries/<slug>.html）へ移動する。
- 国ページがまだ無い国は、リンクにせず「準備中」と表示する（壊れたリンクを作らない）。
- 地図の描画関数（投影・国境の変換）は scripts/build_maps.py を再利用する。
"""
from __future__ import annotations

import csv
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_maps as bm  # noqa: E402
from build_html import BASE_CSS, bar, nav as site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "maps" / "africa-countries.html"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query="

# 国ごとの代表点（地図上のラベル位置）。緯度経度で与え、同じ投影で描く
LABEL_POS = {
    "710": (24.5, -29.5), "426": (28.2, -29.6), "748": (31.5, -26.55), "508": (35.0, -17.5), "450": (46.8, -19.5),
    "516": (17.2, -22.0), "072": (24.0, -21.8), "716": (29.8, -19.0), "894": (27.8, -14.2),
    "404": (37.8, 0.6), "834": (34.8, -6.3), "231": (39.5, 8.8),
}
# 小さくてラベルを置けない国は、引き出し線なしで色と一覧で示す
SMALL = {"426", "748"}


def load_countries() -> list[dict]:
    with (ROOT / "data" / "countries.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["sort"] = int(r["sort"] or 0)
    return sorted(rows, key=lambda r: (r["sort"], r["slug"]))


def page_exists(slug: str) -> bool:
    return (ROOT / "countries" / f"{slug}.md").is_file()


CSS = BASE_CSS + """
:root{--sea:#e6eef3;--land:#f4f1e8;--border:#b9b4a4;--grat:#cdd8df;--k1:#d9e6f2;--k1s:#0072B2;--k2:#f3e3d3;--k2s:#B84A00;--k3:#d8eee5;--k3s:#007A5A;--k4:#efdcea;--k4s:#A5498A;--soon:#ececec}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--k1:#1f3a50;--k1s:#56B4E9;--k2:#4a3321;--k2s:#FF9A5C;--k3:#1f4033;--k3s:#3DCCA0;--k4:#452c3d;--k4s:#E7A6CE;--soon:#34383a}}
:root[data-theme="dark"]{--sea:#1a2530;--land:#2b2f2c;--border:#59605a;--grat:#2a3844;--k1:#1f3a50;--k1s:#56B4E9;--k2:#4a3321;--k2s:#FF9A5C;--k3:#1f4033;--k3s:#3DCCA0;--k4:#452c3d;--k4s:#E7A6CE;--soon:#34383a}
.mapbox{position:relative;margin:10px 0;border:1px solid var(--line)}
svg#cmap{display:block;width:100%;height:auto;background:var(--sea);font-family:var(--sans)}
.sea{fill:var(--sea)} .grat{fill:none;stroke:var(--grat);stroke-width:.6} .frame{fill:none;stroke:var(--border);stroke-width:1}
.co{fill:var(--land);stroke:var(--border);stroke-width:.5;fill-rule:evenodd;stroke-linejoin:round}
a.cn{cursor:pointer;outline:none}
a.cn .co{stroke-width:.9}
a.cn.g1 .co{fill:var(--k1);stroke:var(--k1s)} a.cn.g2 .co{fill:var(--k2);stroke:var(--k2s)} a.cn.g3 .co{fill:var(--k3);stroke:var(--k3s)} a.cn.g4 .co{fill:var(--k4);stroke:var(--k4s)}
a.cn.soon .co{fill:var(--soon);stroke:var(--border);stroke-dasharray:3 2}
a.cn:hover .co,a.cn:focus-visible .co{stroke-width:3;stroke:var(--ink)}
a.cn:focus-visible{outline:none}
.lb{font-size:calc(12.5px * var(--ts,1));font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--sea);stroke-width:3.4px;stroke-linejoin:round;pointer-events:none;text-anchor:middle}
.lb .short{display:none}
svg#cmap.narrow .lb .full{display:none}
svg#cmap.narrow .lb .short{display:inline}
.lb.sub{font-size:calc(10px * var(--ts,1));font-weight:400;fill:var(--muted)}
.switch{display:flex;flex-wrap:wrap;gap:6px 16px;margin:10px 0;padding:6px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:.95em}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px;margin:10px 0}
.cc{display:block;border:1px solid var(--line);border-left:6px solid var(--s,var(--line));padding:10px 12px;text-decoration:none;color:var(--ink);background:var(--bg);min-height:44px}
.cc:hover,.cc:focus-visible{background:var(--hl)}
.cc b{display:block;font-size:1.02rem}
.cc span{display:block;color:var(--muted);font-size:.9em}
.cc.soon{border-left-style:dashed;color:var(--muted)}
.cc .k{font-size:.8em;font-weight:700;color:var(--s,var(--muted))}
.lg{display:flex;flex-wrap:wrap;gap:6px 18px;margin:8px 0;font-size:.93em}
.lg i{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-2px;border:2px solid var(--s);background:var(--f)}
.g1{--s:var(--k1s);--f:var(--k1)} .g2{--s:var(--k2s);--f:var(--k2)} .g3{--s:var(--k3s);--f:var(--k3)} .g4{--s:var(--k4s);--f:var(--k4)}
"""

GROUP_NAMES = {
    "g1": "南部アフリカ（南ア・周辺の小国）",
    "g2": "ビクトリアの滝・大河周辺（ザンビア・ジンバブエ・ボツワナ・ナミビア）",
    "g3": "インド洋側（モザンビーク・マダガスカル）",
    "g4": "東アフリカ（ケニア・タンザニア・エチオピア乗継）",
}


def build() -> str:
    countries = load_countries()
    geo = bm.load_topo("countries-50m.json")
    proj = bm.Laea(25.0, 2.0, (-19.0, 64.0, -36.0, 35.0))
    paths = bm.ring_paths(proj, geo, 0.45, skip=("010",))
    by_id = {c["iso_numeric"]: c for c in countries}

    land, labels = [], []
    for cid, (name, d) in paths.items():
        c = by_id.get(cid)
        if not c:
            land.append(f'<path class="co" d="{d}"><title>{html.escape(name)}</title></path>')
            continue
        live = page_exists(c["slug"])
        cls = f'cn {c["group"]}' + ("" if live else " soon")
        tip = f'{c["name_ja"]}：{c["summary"]}' + ("" if live else "（ページ準備中）")
        inner = f'<path class="co" d="{d}"/><title>{html.escape(tip)}</title>'
        if live:
            land.append(f'<a class="{cls}" href="../countries/{c["slug"]}.html" aria-label="{html.escape(c["name_ja"])}のページへ">{inner}</a>')
        else:
            land.append(f'<g class="{cls}" aria-label="{html.escape(c["name_ja"])}（ページ準備中）">{inner}</g>')
    for cid, c in by_id.items():
        if cid in SMALL or cid not in LABEL_POS:
            continue
        lon, lat = LABEL_POS[cid]
        x, y = proj.xy(lon, lat)
        labels.append(f'<text class="lb" x="{bm.f1(x)}" y="{bm.f1(y)}"><tspan class="full">{html.escape(c["name_ja"])}</tspan><tspan class="short">{html.escape(c["short"])}</tspan></text>')
    # 小国は図の外側に引き出さず、ラベルを近くに小さく置く
    for cid in sorted(SMALL):
        c = by_id.get(cid)
        if not c:
            continue
        lon, lat = LABEL_POS[cid]
        x, y = proj.xy(lon, lat)
        labels.append(f'<text class="lb sub" x="{bm.f1(x)}" y="{bm.f1(y)}"><tspan class="full">{html.escape(c["name_ja"])}</tspan><tspan class="short">{html.escape(c["short"])}</tspan></text>')

    W, H = proj.width, proj.height
    grat = bm.graticule(proj, 10, 10, (-30, 70), (-40, 40))
    outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
    svg = (f'<svg id="cmap" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" style="--ts:1" role="group" aria-label="アフリカの国別リンク地図">'
           f'<defs><clipPath id="cl"><path d="{outline}"/></clipPath></defs><g clip-path="url(#cl)">'
           f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/>'
           f'<g class="land">{"".join(land)}</g><g class="lbs">{"".join(labels)}</g></g><path class="frame" d="{outline}"/></svg>')

    cards = []
    for c in countries:
        live = page_exists(c["slug"])
        inner = f'<span class="k">{html.escape(GROUP_NAMES[c["group"]].split("（")[0])}</span><b>{html.escape(c["name_ja"])}</b><span>{html.escape(c["summary"])}</span>'
        if live:
            cards.append(f'<a class="cc {c["group"]}" href="../countries/{c["slug"]}.html">{inner}</a>')
        else:
            cards.append(f'<div class="cc soon {c["group"]}">{inner}<span>ページ準備中</span></div>')
    legend = "".join(f'<span class="{g}"><i></i>{html.escape(n)}</span>' for g, n in GROUP_NAMES.items())

    return f"""<!doctype html>
<!-- generated by scripts/build_country_map.py from data/countries.csv, data/geo/countries-50m.json; do not edit -->
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>アフリカ国別地図｜2027 留学・アフリカ周遊</title>
<style>
{CSS}</style></head><body>
{bar("../", "maps/africa-countries.html")}
<main class="wrap page">
<p class="crumb"><a href="../index.html">トップ</a> ／ ルート地図</p>
<h1>アフリカ国別地図</h1>
<p class="lead">色のついた国を押す（クリック・タップ・Tabキーで選んでEnter）と、その国の観光地・おすすめの食べ物・ビザ・安全・行き方のページに移動します。旅程の候補になった国だけを色分けしています。</p>
<nav class="switch" aria-label="地図とページの移動"><a href="africa-map.html">候補ルートのアフリカ地図</a><a href="world-map.html">世界地図</a><a href="../research/africa-route-comparison.html">ルート比較資料</a><a href="../areas/africa.html">アフリカ周遊のページ</a></nav>
<div class="mapbox">{svg}</div>
<div class="lg" aria-label="色の凡例">{legend}</div>
<p class="muted">破線で灰色の国は、ページを準備中です。国境線は概念図としての表示で、各国の公式な主張を表すものではありません。小さな国（レソト・エスワティニ）は地図上で押しにくいので、下の一覧からも移動できます。</p>
<h2>国の一覧</h2>
<div class="cards">{"".join(cards)}</div>
<p class="note">各国ページの内容は、政府・観光局・国立公園など公式の情報を優先し、出典・確認日・未確認事項を記載しています。料金は取得できた年度のもので、2027年の確定料金ではありません。個人の予約・日程・支払いは含みません。</p>
<footer><nav class="all" id="all-pages" aria-label="全ページ">{site_nav(ROOT, ROOT / "maps" / "africa-countries.html")}</nav><p>地図データ：<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（パブリックドメイン）を <a href="https://github.com/topojson/world-atlas" target="_blank" rel="noopener">world-atlas</a> 2.0.2（ISC）経由で使用し、ランベルト正積方位図法で描画。このページは <code>scripts/build_country_map.py</code> が自動生成します（手で編集しない）。外部の通信は行いません。</p></footer>
</main>
<script>
(function(){{var s=document.getElementById('cmap');function f(){{var w=s.getBoundingClientRect().width||1000;s.style.setProperty('--ts',Math.max(1,Math.min(1.9,1000/w*0.62)).toFixed(2));s.classList.toggle('narrow',w<640)}}f();addEventListener('resize',f)}})();
</script>
</body></html>
"""


def main() -> int:
    text = build()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("国別地図HTMLが古いです。`py scripts/build_country_map.py` を実行してコミットしてください", file=sys.stderr)
            return 1
        print("PASS: country map is current")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT).as_posix()}: {len(text.encode('utf-8')) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
