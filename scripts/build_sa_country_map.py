# -*- coding: utf-8 -*-
"""南米の国別リンク地図（maps/southamerica-countries.html）を生成する。標準ライブラリのみ。

使い方（リポジトリのルートで実行）:
    py scripts/build_sa_country_map.py           生成
    py scripts/build_sa_country_map.py --check   生成物が最新でなければ失敗（CI用）

- 入力: data/countries.csv（group が g4 の国）、data/geo/countries-50m.json（国境。Natural Earth）
- 出力: 外部通信なしの単独HTML。地図の国をクリック（タップ・Enter）すると、その国のページ（countries/<slug>.html）へ移動する。
- 南米の本体（ペルー・ボリビア・エクアドル・ブラジル・アルゼンチン・チリ・パラグアイ）を大きく描き、南米から離れたメキシコは
  右上の小さな枠に別に描く（同じ枠に入れると南米が小さくなるため）。
- アフリカの国別地図（scripts/build_country_map.py）の見た目・投影関数を再利用する。国境線は概念図で、各国の公式な主張を表さない。
"""
from __future__ import annotations

import csv
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_maps as bm  # noqa: E402
import build_country_map as acm  # noqa: E402  アフリカ国別地図（CSS・色・ラベルの作り方を共有）
from build_html import FONT_SIZE_JS, bar, nav as site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "maps" / "southamerica-countries.html"
SA_GROUP = "g4"
MEXICO = "484"

# 南米の本体を描く緯度経度の枠（西端・東端・南端・北端）と、ラベルの位置
SA_WINDOW = (-84.0, -33.0, -56.0, 13.0)
SA_LABEL_POS = {
    "604": (-75.0, -9.5), "068": (-64.5, -17.0), "218": (-78.3, -1.3), "076": (-52.5, -10.0),
    "032": (-65.0, -35.0), "152": (-71.2, -33.0), "600": (-58.2, -23.4),
}
SMALL_SA = {"218", "600"}  # 小さくてラベルを小さめに置く国
MX_WINDOW = (-119.0, -84.0, 13.0, 33.5)
MX_LABEL = (-102.0, 24.0)

EXTRA_CSS = """
svg#samap{display:block;width:100%;height:auto;max-height:calc(100dvh - 222px);background:var(--sea);font-family:var(--sans)}
@media(max-width:1000px){svg#samap{max-height:none}}
svg#samap.narrow .lb .full{display:none}
svg#samap.narrow .lb .short{display:inline}
.cm-note{margin:6px 0;font-size:.86em;color:var(--muted)}
.mexbox{position:absolute;right:8px;top:8px;width:min(34%,230px);border:1px solid var(--line);border-radius:var(--rad);overflow:hidden;background:var(--sea);box-shadow:0 1px 6px rgba(0,0,0,.18)}
.mexbox svg{display:block;width:100%;height:auto}
.mexbox .cap{position:absolute;left:6px;bottom:4px;font-size:.72rem;color:var(--muted);pointer-events:none}
.mapbox{position:relative}
"""


def load_countries() -> list[dict]:
    with (ROOT / "data" / "countries.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["sort"] = int(r["sort"] or 0)
    rows = [r for r in rows if r["group"] == SA_GROUP]
    return sorted(rows, key=lambda r: (r["sort"], r["slug"]))


def page_exists(slug: str) -> bool:
    return (ROOT / "countries" / f"{slug}.md").is_file()


def _land(paths, by_id, only=None) -> list[str]:
    out = []
    for cid, (name, d) in paths.items():
        c = by_id.get(cid)
        if not c:
            if only is None:
                out.append(f'<path class="co" d="{d}"><title>{html.escape(name)}</title></path>')
            continue
        if only is not None and cid not in only:
            continue
        live = page_exists(c["slug"])
        cls = f'cn {c["group"]}' + ("" if live else " soon")
        tip = f'{c["name_ja"]}：{c["summary"]}' + ("" if live else "（ページ準備中）")
        inner = f'<path class="co" d="{d}"/><title>{html.escape(tip)}</title>'
        if live:
            out.append(f'<a class="{cls}" href="../countries/{c["slug"]}.html" aria-label="{html.escape(c["name_ja"])}のページへ">{inner}</a>')
        else:
            out.append(f'<g class="{cls}" aria-label="{html.escape(c["name_ja"])}（ページ準備中）">{inner}</g>')
    return out


def _label(proj, c, lon, lat, sub=False) -> str:
    x, y = proj.xy(lon, lat)
    cls = "lb sub" if sub else "lb"
    return (f'<text class="{cls}" x="{bm.f1(x)}" y="{bm.f1(y)}"><tspan class="full">{html.escape(c["name_ja"])}</tspan>'
            f'<tspan class="short">{html.escape(c["short"])}</tspan></text>')


def _build_raw() -> str:
    countries = load_countries()
    by_id = {c["iso_numeric"]: c for c in countries}
    geo = bm.load_topo("countries-50m.json")

    # 南米の本体
    lonmin, lonmax, latmin, latmax = SA_WINDOW
    proj = bm.Laea((lonmin + lonmax) / 2, (latmin + latmax) / 2, SA_WINDOW)
    paths = bm.ring_paths(proj, geo, 0.45, skip=("010",))
    land = _land(paths, by_id, only=None)
    labels = [_label(proj, by_id[cid], *SA_LABEL_POS[cid], sub=(cid in SMALL_SA)) for cid in SA_LABEL_POS if cid in by_id]
    W, H = proj.width, proj.height
    grat = bm.graticule(proj, 10, 10, (lonmin, lonmax), (latmin, latmax))
    outline = f"M0 0H{bm.f1(W)}V{bm.f1(H)}H0Z"
    svg = (f'<svg id="samap" viewBox="0 0 {bm.f1(W)} {bm.f1(H)}" style="--ts:1" role="group" aria-label="南米の国別リンク地図">'
           f'<defs><clipPath id="sacl"><path d="{outline}"/></clipPath></defs><g clip-path="url(#sacl)">'
           f'<path class="sea" d="{outline}"/><path class="grat" d="{grat}"/>'
           f'<g class="land">{"".join(land)}</g><g class="lbs">{"".join(labels)}</g></g><path class="frame" d="{outline}"/></svg>')

    # メキシコ（別枠）
    mx = by_id.get(MEXICO)
    mex_html = ""
    if mx:
        mlon0, mlon1, mlat0, mlat1 = MX_WINDOW
        mproj = bm.Laea((mlon0 + mlon1) / 2, (mlat0 + mlat1) / 2, MX_WINDOW, width=420.0)
        mpaths = bm.ring_paths(mproj, geo, 0.45, skip=("010",))
        mland = _land(mpaths, by_id, only={MEXICO})
        mland = [f'<path class="co" d="{d}"/>' for cid, (n, d) in mpaths.items() if cid != MEXICO and cid in ("840", "320", "084", "340", "222", "558")] + mland
        mw, mh = mproj.width, mproj.height
        mout = f"M0 0H{bm.f1(mw)}V{bm.f1(mh)}H0Z"
        mex_html = (f'<div class="mexbox"><svg id="samexmap" viewBox="0 0 {bm.f1(mw)} {bm.f1(mh)}" role="group" aria-label="メキシコ（南米から離れているため別枠）">'
                    f'<defs><clipPath id="saclm"><path d="{mout}"/></clipPath></defs><g clip-path="url(#saclm)"><path class="sea" d="{mout}"/>'
                    f'<g class="land">{"".join(mland)}</g><g class="lbs">{_label(mproj, mx, *MX_LABEL)}</g></g><path class="frame" d="{mout}"/></svg>'
                    f'<span class="cap">メキシコ（別枠）</span></div>')

    cards = []
    for c in countries:
        live = page_exists(c["slug"])
        inner = f'<span class="k">{html.escape(acm.GROUP_NAMES[c["group"]].split("（")[0])}</span><b>{html.escape(c["name_ja"])}</b><span>{html.escape(c["summary"])}</span>'
        if live:
            cards.append(f'<a class="cc {c["group"]}" href="../countries/{c["slug"]}.html">{inner}</a>')
        else:
            cards.append(f'<div class="cc soon {c["group"]}">{inner}<span>ページ準備中</span></div>')
    legend = f'<span class="g4"><i></i>南米・メキシコ（色のついた国を押すと国別ページへ）</span>'

    return f"""<!doctype html>
<!-- generated by scripts/build_sa_country_map.py from data/countries.csv, data/geo/countries-50m.json; do not edit -->
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>南米国別地図｜2027 留学・アフリカ周遊</title>
<style>
{acm.CSS}{EXTRA_CSS}</style>{FONT_SIZE_JS}</head><body>
{bar("../", "maps/southamerica-countries.html")}
<main class="wrap page">
<p class="crumb"><a href="../index.html">トップ</a> ／ ルート地図</p>
<div class="page-top"><h1>南米国別地図</h1>
<p class="lead">色のついた国を押す（クリック・タップ・Tabキーで選んでEnter）と、その国の観光地・季節・ビザ・安全・行き方のページに移動します。旅程の決定ではなく、調べた国の入口です。</p></div>
{bm.map_switch("southamerica-countries")}
<div class="cm-grid">
<div class="mapbox">{svg}{mex_html}</div>
<div class="cm-right">
<div class="lg" aria-label="色の凡例">{legend}</div>
<h2>国の一覧</h2>
<div class="cards">{"".join(cards)}</div>
<p class="muted">国境線は概念図としての表示で、各国の公式な主張を表すものではありません。メキシコは南米から離れているため、右上の別枠に描いています。ガラパゴス諸島（エクアドル）は小さいため、この縮尺では描いていません。</p>
<p class="note">各国ページの内容は、調査資料（<a href="../research/south-america-countries-a.html">南米の国別比較（1）</a>・<a href="../research/south-america-countries-b.html">（2）</a>）の転記です。公式の情報は英国外務省・ガラパゴスの公式などに限られ、料金は取得できた年度のもので、2027年の確定料金ではありません。</p>
</div></div>
<footer><nav class="all" id="all-pages" aria-label="全ページ">{site_nav(ROOT, ROOT / "maps" / "southamerica-countries.html")}</nav><p>地図データ：<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（パブリックドメイン）を <a href="https://github.com/topojson/world-atlas" target="_blank" rel="noopener">world-atlas</a> 2.0.2（ISC）経由で使用。このページは <code>scripts/build_sa_country_map.py</code> が内部データから自動生成します（手で編集しない）。外部の通信は行いません。</p></footer>
</main>
<script>
(function(){{var s=document.getElementById('samap');function f(){{var w=s.getBoundingClientRect().width||1000;s.style.setProperty('--ts',Math.max(1,Math.min(1.9,1000/w*0.62)).toFixed(2));s.classList.toggle('narrow',w<640)}}f();addEventListener('resize',f)}})();
</script>
</body></html>
"""


def build() -> str:
    """生成したHTMLから、作業管理用の「Issue #番号」の言及を外す（build_html.reader_clean）"""
    from build_html import reader_clean
    return reader_clean(_build_raw())


def main() -> int:
    text = build()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("南米国別地図HTMLが古いです。`py scripts/build_sa_country_map.py` を実行してコミットしてください", file=sys.stderr)
            return 1
        print("PASS: south america country map is current")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT).as_posix()}: {len(text.encode('utf-8')) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
