# -*- coding: utf-8 -*-
"""旅のデザイナー（docs/14-trip-designer.html）の部品を作る。

地図（陸地の形）と、行き先の候補（都市の名前・緯度経度・国）と、既存の案（SA8-6・5月の案G など）を JSON にして、
ページに埋め込む。入力はブラウザの中だけに保存され、公開されるのは説明文と、既存の案（匿名モデル）だけ。
使い方は scripts/build_html.py が呼ぶ（単体では実行しない）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import build_maps as bm

ROOT = Path(__file__).resolve().parents[1]

# 地図の範囲（経度・緯度）。日本〜アフリカ〜南米が入る
WINDOW = (-100.0, 150.0, -45.0, 45.0)

# 候補の地点（id, 名前, 国, 緯度, 経度）。route_points.csv のほかに、南米の都市と日本を足す
EXTRA_POINTS = [
    ("GRU", "サンパウロ", "ブラジル", -23.4356, -46.4731), ("IGU", "イグアス", "ブラジル", -25.5963, -54.4872),
    ("LIM", "リマ", "ペルー", -12.0219, -77.1143), ("CUZ", "クスコ", "ペルー", -13.5357, -71.9388),
    ("MAPI", "マチュピチュ", "ペルー", -13.1631, -72.5450), ("PEM", "タンボパタ（アマゾン）", "ペルー", -12.6136, -69.2286),
    ("IQT", "イキトス（アマゾン）", "ペルー", -3.7848, -73.3088), ("ICA", "ワカチナ", "ペルー", -14.0875, -75.7626),
    ("PUNO", "プーノ", "ペルー", -15.8402, -70.0219), ("LPB", "ラパス", "ボリビア", -16.5133, -68.1922),
    ("UYU", "ウユニ", "ボリビア", -20.4463, -66.8484), ("GYE", "グアヤキル", "エクアドル", -2.1574, -79.8837),
    ("GPS", "ガラパゴス", "エクアドル", -0.4538, -90.2659), ("EZE", "ブエノスアイレス", "アルゼンチン", -34.8222, -58.5358),
    ("ASU", "アスンシオン", "パラグアイ", -25.2400, -57.5200), ("TYO", "東京（日本）", "日本", 35.7720, 140.3929),
    ("VALLE", "聖なる谷", "ペルー", -13.3333, -72.0833), ("AGUAS", "アグアスカリエンテス", "ペルー", -13.1547, -72.5258),
]

# 既存の案（日付つきの旅程）。areas/southamerica-aug.md の SA8-6 と、areas/africa.md の案G（5月）と同じ内容。
# 各行：(地点id, 泊数, 移動の種類 fly|move|none, やること)。出発日は start。
PRESETS = [
    {"id": "SA8-6", "name": "8月 南米 SA8-6（イグアス→ウユニ→ペルー）", "start": "2027-08-01", "stops": [
        ["CPT", 1, "fly", "ケープタウン発 8/1（サンパウロ乗継・機内泊）"],
        ["IGU", 2, "fly", "イグアス 8/2〜8/3：ブラジル側・アルゼンチン側"],
        ["GRU", 1, "fly", "8/4 イグアス発 → 乗継（機内泊）→ 8/5 ラパス着"],
        ["LPB", 1, "fly", "ラパス 8/5：高地順応（標高約3,600m）"],
        ["UYU", 3, "fly", "ウユニ 8/6〜8/8：2泊3日のツアー"],
        ["LPB", 1, "fly", "ラパス 8/9"],
        ["CUZ", 1, "fly", "クスコ 8/10：高地順応を続ける"],
        ["VALLE", 2, "move", "聖なる谷 8/11〜8/12（予備日を含む）"],
        ["AGUAS", 1, "move", "アグアスカリエンテス 8/13（列車・予備の入場日）"],
        ["MAPI", 1, "move", "マチュピチュ村 8/14（入場・仮の第一候補）"],
        ["CUZ", 1, "move", "クスコ 8/15（列車で戻る・予備の入場日）"],
        ["PEM", 2, "fly", "アマゾン（タンボパタ）8/16〜8/17"],
        ["LIM", 4, "fly", "リマ 8/18〜8/21：ダイビング（8/20）・予備日"],
        ["TYO", 0, "fly", "リマ発 8/22 → 東京（乗継）"]]},
    {"id": "SA8-5", "name": "8月 南米 SA8-5（イグアス→ペルー・ウユニなし）", "start": "2027-08-01", "stops": [
        ["CPT", 1, "fly", "ケープタウン発 8/1（サンパウロ乗継・機内泊）"],
        ["IGU", 3, "fly", "イグアス 8/2〜8/4：予備日を含む"],
        ["GRU", 1, "fly", "8/5 イグアス発 → 乗継（機内泊）→ 8/6 クスコ着"],
        ["CUZ", 1, "fly", "クスコ 8/6：高地順応（標高約3,400m）"],
        ["VALLE", 1, "move", "聖なる谷 8/7"],
        ["CUZ", 1, "move", "クスコ 8/8：予備日"],
        ["PEM", 3, "fly", "アマゾン（タンボパタ）8/9〜8/11"],
        ["CUZ", 1, "fly", "クスコ 8/12"],
        ["AGUAS", 1, "move", "アグアスカリエンテス 8/13（列車・予備の入場日）"],
        ["MAPI", 1, "move", "マチュピチュ村 8/14（入場・仮の第一候補）"],
        ["CUZ", 1, "move", "クスコ 8/15（列車で戻る・予備の入場日）"],
        ["LIM", 1, "fly", "リマ 8/16"],
        ["ICA", 1, "move", "ワカチナ 8/17（任意・サンドボード）"],
        ["LIM", 4, "move", "リマ 8/18〜8/21：ダイビング（8/20）・予備日"],
        ["TYO", 0, "fly", "リマ発 8/22 → 東京（乗継）"]]},
    {"id": "G", "name": "5月 アフリカ 案G（モーリシャス→マダガスカル→滝周辺3か国）", "start": "2027-05-03", "stops": [
        ["NRT", 0, "fly", "東京発（ムンバイ乗継）"], ["MRU", 3, "fly", "モーリシャス：島内観光"], ["TNR", 13, "fly", "マダガスカル：東部・西部"],
        ["MRU", 2, "fly", "モーリシャスへ戻る（待機）"], ["JNB", 2, "fly", "ヨハネスブルグ（接続の余裕）"], ["VICFALLS", 8, "fly", "滝周辺3か国"],
        ["CPT", 3, "fly", "ケープタウン：学校前の準備"]]},
]


def geo_json() -> str:
    """陸地の外周（簡略化。経度・緯度を小数1桁に丸めた点列）。範囲の外の国は省く"""
    geo = bm.load_topo("countries-110m.json")
    lonmin, lonmax, latmin, latmax = WINDOW
    out = []
    for c in geo:
        for poly in c["polys"]:
            ring = poly[0]
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            if max(xs) < lonmin or min(xs) > lonmax or max(ys) < latmin or min(ys) > latmax:
                continue
            if len(ring) < 4:
                continue
            step = 2 if len(ring) > 60 else 1
            pts = [[round(x, 1), round(y, 1)] for x, y in ring[::step]]
            out.append(pts)
    return json.dumps(out, separators=(",", ":"))


def points_json() -> str:
    """行き先の候補（route_points.csv の地点＋南米・日本）"""
    seen, out = set(), []
    for r in bm.read_csv("route_points.csv"):
        if r["id"] in seen or not r["name_ja"]:
            continue
        seen.add(r["id"])
        out.append([r["id"], r["name_ja"], r["country"], round(float(r["lat"]), 3), round(float(r["lon"]), 3)])
    for pid, name, country, lat, lon in EXTRA_POINTS:
        if pid not in seen:
            seen.add(pid)
            out.append([pid, name, country, lat, lon])
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))


def presets_json() -> str:
    return json.dumps(PRESETS, ensure_ascii=False, separators=(",", ":"))


def designer_html() -> str:
    """ページに埋め込む画面と、動かすスクリプト（外部の通信なし）"""
    tpl = (ROOT / "scripts" / "designer_template.html").read_text(encoding="utf-8")
    return (tpl.replace("@@GEO@@", geo_json()).replace("@@POINTS@@", points_json())
            .replace("@@PRESETS@@", presets_json()).replace("@@WINDOW@@", json.dumps(list(WINDOW))))
