# -*- coding: utf-8 -*-
"""世界地図・アフリカ地図（ルート概念図）を生成する。標準ライブラリのみ。

使い方（リポジトリのルートで実行）:
    py scripts/build_maps.py           maps/world-map.html と maps/africa-map.html を再生成
    py scripts/build_maps.py --check   生成物が最新でなければ失敗（CI用）

- 入力: data/route_points.csv, data/routes.csv, data/geo/countries-110m.json, countries-50m.json
  （Natural Earth のパブリックドメインの国境データ。world-atlas 2.0.2 の TopoJSON。ネットワークは使わない）
- 出力: 外部ライブラリ・タイル・フォント・fetch を使わない単独のHTML（file:// で開ける）。
- 航空は大圏（最短）経路の曲線。陸路は点を結ぶ直線で、実際の道路経路ではない。
"""
from __future__ import annotations

import csv
import html
import json
import math
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_html import BASE_CSS, bar, nav as site_nav  # noqa: E402  共通テンプレート

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GEO = DATA / "geo"
OUT_DIR = ROOT / "maps"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query="
EARTH_R = 6371.0088

# 経路色（Okabe-Ito 系の色覚多様性に配慮した配色）+ 形で区別するバッジ（色だけに頼らない）
ROUTE_COLORS = {
    "A": ("#0072B2", "#56B4E9"),
    "B": ("#B84A00", "#FF9A5C"),
    "C": ("#007A5A", "#3DCCA0"),
    "D": ("#A5498A", "#E7A6CE"),
    "E": ("#8A6D00", "#F2C94C"),
    "F": ("#3B3B3B", "#D9D9D9"),
}
BADGE_SHAPE = {"A": "circle", "B": "square", "C": "diamond", "D": "triangle", "E": "hexagon", "F": "pentagon"}
ROUTE_SHORT = {"A": "ナイロビ起点", "B": "ADD乗継→マダガスカル", "C": "陸路主体", "D": "島めぐり", "E": "ケニア→マダガスカル", "F": "S2 南部アフリカ周遊"}
# 行き先として色を付ける国（ISO 3166-1 numeric）
VISIT = {"404", "834", "450", "894", "716", "072", "710", "480", "690", "608", "748"}
CAUTION = "231"  # エチオピア
MODE_JA = {"flight": "航空", "overland": "陸路（直線で例示）", "ferry": "船", "sea": "海路"}


# ---------------------------------------------------------------- geometry
def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    dp = p2 - p1
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R * math.asin(min(1.0, math.sqrt(a)))


def gc_points(lat1, lon1, lat2, lon2, n):
    """大圏上の n+1 点（lat, lon）。経度は連続になるよう展開する（境界をまたいでも飛ばない）"""
    def vec(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    a, b = vec(lat1, lon1), vec(lat2, lon2)
    dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b))))
    om = math.acos(dot)
    out, prev = [], None
    for i in range(n + 1):
        t = i / n
        if om < 1e-9:
            v = a
        else:
            s = math.sin(om)
            k1, k2 = math.sin((1 - t) * om) / s, math.sin(t * om) / s
            v = tuple(k1 * x + k2 * y for x, y in zip(a, b))
        lat = math.degrees(math.atan2(v[2], math.hypot(v[0], v[1])))
        lon = math.degrees(math.atan2(v[1], v[0]))
        if prev is not None:
            while lon - prev > 180:
                lon -= 360
            while lon - prev < -180:
                lon += 360
        prev = lon
        out.append((lat, lon))
    return out


def load_topo(name):
    d = json.loads((GEO / name).read_text(encoding="utf-8"))
    sx, sy = d["transform"]["scale"]
    tx, ty = d["transform"]["translate"]
    arcs = []
    for a in d["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def arc(i):
        return arcs[i] if i >= 0 else arcs[~i][::-1]

    def ring(idx):
        pts = []
        for i in idx:
            seg = arc(i)
            pts.extend(seg if not pts else seg[1:])
        return pts

    countries = []
    for g in d["objects"]["countries"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        out = [[ring(r) for r in poly] for poly in polys]
        countries.append({"id": g.get("id") or "", "name": g["properties"]["name"], "polys": out})
    return countries


def unwrap(ring):
    out = [ring[0]]
    for lon, lat in ring[1:]:
        p = out[-1][0]
        while lon - p > 180:
            lon -= 360
        while lon - p < -180:
            lon += 360
        out.append((lon, lat))
    return out


def simplify(pts, tol):
    """Douglas-Peucker（反復版）。閉じた環でも端点は残す"""
    n = len(pts)
    if n < 4:
        return pts
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    t2 = tol * tol
    while stack:
        i, j = stack.pop()
        x1, y1 = pts[i]
        x2, y2 = pts[j]
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        best, k = -1.0, -1
        for m in range(i + 1, j):
            px, py = pts[m]
            if L == 0:
                d = (px - x1) ** 2 + (py - y1) ** 2
            else:
                t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L))
                d = (px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2
            if d > best:
                best, k = d, m
        if best > t2:
            keep[k] = True
            stack.append((i, k))
            stack.append((k, j))
    return [p for p, f in zip(pts, keep) if f]


def f1(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def poly_d(points, close=True):
    d = "M" + f1(points[0][0]) + " " + f1(points[0][1])
    prev = points[0]
    for x, y in points[1:]:
        d += "L" + f1(x) + " " + f1(y)
    return d + ("Z" if close else "")


class NaturalEarth:
    """Natural Earth 図法（Šavrič ほか 2015 の多項式）。lon0 を中央経線にする"""
    name = "natural-earth"

    def __init__(self, lon0=0.0, lat_n=84.0, lat_s=-58.0, width=1000.0, pad=6.0):
        self.lon0, self.lat_n, self.lat_s = lon0, lat_n, lat_s
        xmax = self._raw(180.0, 0.0)[0]
        self.scale = (width - 2 * pad) / (2 * xmax)
        self.xmax, self.pad = xmax, pad
        self.ytop = self._raw(0.0, lat_n)[1]
        ybot = self._raw(0.0, lat_s)[1]
        self.width = width
        self.height = (self.ytop - ybot) * self.scale + 2 * pad

    @staticmethod
    def _raw(lam_deg, lat_deg):
        lam, phi = math.radians(lam_deg), math.radians(lat_deg)
        p2 = phi * phi
        p4 = p2 * p2
        x = lam * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
        y = phi * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
        return x, y

    def xy(self, lon, lat, shift=0.0):
        x, y = self._raw(lon - self.lon0 + shift, lat)
        return (x * self.scale + self.width / 2, (self.ytop - y) * self.scale + self.pad)

    def rel(self, lon):
        """中央経線からの相対経度を [-180,180) に畳む"""
        return (lon - self.lon0 + 180) % 360 - 180

    def outline(self):
        pts = []
        lat = self.lat_n
        while lat > self.lat_s:
            pts.append(self.xy(self.lon0 - 180, lat))
            lat -= 2
        pts.append(self.xy(self.lon0 - 180, self.lat_s))
        pts.append(self.xy(self.lon0 + 180, self.lat_s))
        lat = self.lat_s
        while lat < self.lat_n:
            pts.append(self.xy(self.lon0 + 180, lat))
            lat += 2
        pts.append(self.xy(self.lon0 + 180, self.lat_n))
        return pts

    shifts = (-360.0, 0.0, 360.0)

    def in_view(self, x, y, m=0):
        return -m <= x <= self.width + m and -m <= y <= self.height + m


class Laea:
    """ランベルト正積方位図法（アフリカ中心）。範囲は緯度経度の枠の投影から決める"""
    name = "laea"
    shifts = (0.0,)

    def __init__(self, lon0, lat0, window, width=1000.0, pad=6.0):
        self.lon0, self.lat0 = lon0, lat0
        self.p1 = math.radians(lat0)
        lonmin, lonmax, latmin, latmax = window
        raw = []
        for i in range(0, 41):
            t = i / 40
            for lat in (latmin, latmax):
                raw.append(self._raw(lonmin + (lonmax - lonmin) * t, lat))
            for lon in (lonmin, lonmax):
                raw.append(self._raw(lon, latmin + (latmax - latmin) * t))
        xs, ys = [p[0] for p in raw], [p[1] for p in raw]
        self.x0, self.x1, self.y0, self.y1 = min(xs), max(xs), min(ys), max(ys)
        self.scale = (width - 2 * pad) / (self.x1 - self.x0)
        self.pad, self.width = pad, width
        self.height = (self.y1 - self.y0) * self.scale + 2 * pad
        self.window = window

    def _raw(self, lon, lat):
        phi, dl = math.radians(lat), math.radians(lon - self.lon0)
        c = math.sin(self.p1) * math.sin(phi) + math.cos(self.p1) * math.cos(phi) * math.cos(dl)
        k = math.sqrt(2 / max(1e-9, 1 + c))
        return (k * math.cos(phi) * math.sin(dl), k * (math.cos(self.p1) * math.sin(phi) - math.sin(self.p1) * math.cos(phi) * math.cos(dl)))

    def cosc(self, lon, lat):
        phi, dl = math.radians(lat), math.radians(lon - self.lon0)
        return math.sin(self.p1) * math.sin(phi) + math.cos(self.p1) * math.cos(phi) * math.cos(dl)

    def xy(self, lon, lat, shift=0.0):
        x, y = self._raw(lon + shift, lat)
        return ((x - self.x0) * self.scale + self.pad, (self.y1 - y) * self.scale + self.pad)

    def rel(self, lon):
        return (lon - self.lon0 + 180) % 360 - 180

    def in_view(self, x, y, m=0):
        return -m <= x <= self.width + m and -m <= y <= self.height + m


def ring_paths(proj, countries, tol, skip=(), only_near=None):
    """国ごとの SVG path（d 文字列）。{id: (name, d)}。穴は同じ path に入れ evenodd で描く"""
    out = {}
    for c in countries:
        if c["id"] in skip:
            continue
        parts = []
        for poly in c["polys"]:
            rings = [unwrap(r) for r in poly if len(r) >= 4]
            if not rings:
                continue
            outer = rings[0]
            ref = sum(p[0] for p in outer) / len(outer)
            fixed = []
            for r in rings:
                m = sum(p[0] for p in r) / len(r)
                k = round((ref - m) / 360)
                fixed.append([(lon + 360 * k, lat) for lon, lat in r])
            lo = min(p[0] for r in fixed[:1] for p in r)
            hi = max(p[0] for r in fixed[:1] for p in r)
            for sh in proj.shifts:
                if proj.name == "natural-earth":
                    a, b = lo - proj.lon0 + sh, hi - proj.lon0 + sh
                    if b < -180 + 0.01 or a > 180 - 0.01:
                        continue
                sub = []
                visible = False
                for r in fixed:
                    if proj.name == "laea" and any(proj.cosc(lon, lat) < -0.97 for lon, lat in r):
                        sub = []
                        visible = False
                        break
                    pts = [proj.xy(lon, lat, sh) for lon, lat in r]
                    if any(proj.in_view(x, y, 40) for x, y in pts) or r is fixed[0] and bbox_hits(pts, proj):
                        visible = True
                    sp = simplify(pts, tol)
                    if len(sp) >= 3:
                        sub.append(sp)
                if visible and sub:
                    parts.append("".join(poly_d(s) for s in sub))
        if parts:
            out[c["id"] or c["name"]] = (c["name"], "".join(parts))
    return out


def bbox_hits(pts, proj):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return not (max(xs) < 0 or min(xs) > proj.width or max(ys) < 0 or min(ys) > proj.height)


def region_polygon(proj, lonmin, lonmax, latmin, latmax):
    pts = []
    n = 12
    for i in range(n + 1):
        pts.append(proj.xy(lonmin + (lonmax - lonmin) * i / n, latmax))
    for i in range(n + 1):
        pts.append(proj.xy(lonmax, latmax + (latmin - latmax) * i / n))
    for i in range(n + 1):
        pts.append(proj.xy(lonmax - (lonmax - lonmin) * i / n, latmin))
    for i in range(n + 1):
        pts.append(proj.xy(lonmin, latmin + (latmax - latmin) * i / n))
    return poly_d(pts)


def graticule(proj, lon_step, lat_step, lonrange, latrange):
    d = []
    lon = lonrange[0]
    while lon <= lonrange[1] + 1e-9:
        pts = [proj.xy(lon, lat) for lat in frange(latrange[0], latrange[1], 3)]
        d.append(poly_d(pts, False))
        lon += lon_step
    lat = latrange[0] if (latrange[0] % lat_step == 0) else math.ceil(latrange[0] / lat_step) * lat_step
    while lat <= latrange[1] + 1e-9:
        pts = [proj.xy(lo, lat) for lo in frange(lonrange[0], lonrange[1], 3)]
        d.append(poly_d(pts, False))
        lat += lat_step
    return "".join(d)


def frange(a, b, step):
    v = a
    while v < b:
        yield v
        v += step
    yield b


# ---------------------------------------------------------------- data
def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_model():
    points = {r["id"]: r for r in read_csv("route_points.csv")}
    legs = []
    for r in read_csv("routes.csv"):
        legs.append(r)
    for r in legs:
        r["seq"] = int(r["seq"])
    routes = {}
    for r in legs:
        routes.setdefault(r["route_id"], {"name": r["route_name_ja"], "legs": []})["legs"].append(r)
    for rid in routes:
        routes[rid]["legs"].sort(key=lambda r: r["seq"])
    for r in legs:
        a, b = points[r["from_point"]], points[r["to_point"]]
        r["km"] = haversine(float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"]))
    for rid, rt in routes.items():
        rt["km"] = sum(l["km"] for l in rt["legs"])
    return points, routes


def maps_link(q):
    return MAPS_URL + quote(q, safe="")


def km_text(km):
    return f"約{int(round(km / 10.0) * 10):,}km"


# ---------------------------------------------------------------- per-map building
def text_w(s, fs):
    return sum(fs * (1.0 if ord(ch) > 0x2E80 else 0.58) for ch in s)


def label_for(p, level):
    code = p["iata_or_code"]
    prov = p["provisional"] == "Y"
    if level == 0:
        t = p["name_ja"] + (" " + code if code else "")
        return t + ("（仮）" if prov else "")
    return (code or p["name_ja"]) + ("*" if prov else "")


def place_labels(items, obstacles, fs, bounds):
    """items: [{id, x, y, pref, lv0, lv1, prio}]。重ならない位置を貪欲に選ぶ。置けないものは None"""
    placed = []
    result = {}
    order = ["r", "l", "t", "b", "tr", "tl", "br", "bl"]

    def rect(x, y, w, pos, g=6.5):
        h = fs
        if pos == "r":
            return (x + g, y - h / 2, x + g + w, y + h / 2), "start", x + g, y + fs * 0.35
        if pos == "l":
            return (x - g - w, y - h / 2, x - g, y + h / 2), "end", x - g, y + fs * 0.35
        if pos == "t":
            return (x - w / 2, y - g - h, x + w / 2, y - g), "middle", x, y - g - 2
        if pos == "b":
            return (x - w / 2, y + g, x + w / 2, y + g + h), "middle", x, y + g + fs * 0.9
        if pos == "tr":
            return (x + 3, y - g - h, x + 3 + w, y - g), "start", x + 3, y - g - 2
        if pos == "tl":
            return (x - 3 - w, y - g - h, x - 3, y - g), "end", x - 3, y - g - 2
        if pos == "br":
            return (x + 3, y + g, x + 3 + w, y + g + h), "start", x + 3, y + g + fs * 0.9
        return (x - 3 - w, y + g, x - 3, y + g + h), "end", x - 3, y + g + fs * 0.9

    def hit(r, others):
        for o in others:
            if r[0] < o[2] and r[2] > o[0] and r[1] < o[3] and r[3] > o[1]:
                return True
        return False

    # CSV で位置を直接指定したラベル（label_dx/dy/anchor）は先に確定し、他のラベルが避ける
    for it in items:
        fx = it.get("fixed")
        if not fx:
            continue
        dx, dy, anchor = fx
        txt = it["lv0"]
        w = text_w(txt, fs) + 2
        tx, ty = it["x"] + dx, it["y"] + dy
        x0 = tx if anchor == "start" else tx - w if anchor == "end" else tx - w / 2
        r = (x0, ty - fs * 0.85, x0 + w, ty + fs * 0.25)
        placed.append(r)
        result[it["id"]] = (txt, anchor, tx, ty, r, 0)
    for it in sorted(items, key=lambda i: i["prio"]):
        if it.get("fixed"):
            continue
        done = None
        for level, txt in ((0, it["lv0"]), (1, it["lv1"])):
            w = text_w(txt, fs) + 2
            prefs = [it["pref"]] if it["pref"] in order else []
            for pos in prefs + [o for o in order if o != it["pref"]]:
                r, anchor, tx, ty = rect(it["x"], it["y"], w, pos)
                if r[0] < bounds[0] or r[2] > bounds[2] or r[1] < bounds[1] or r[3] > bounds[3]:
                    continue
                if hit(r, placed) or hit(r, obstacles):
                    continue
                done = (txt, anchor, tx, ty, r, level)
                break
            if done:
                break
        if done:
            placed.append(done[4])
            result[it["id"]] = done
    return result


def perp_offset(pts, off):
    """折れ線を中央ほど大きく法線方向へずらす（同じ区間を通る複数ルートを見分けるため）"""
    n = len(pts)
    if off == 0 or n < 3:
        return pts
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        k = off * math.sin(math.pi * i / (n - 1))
        out.append((x - dy / L * k, y + dx / L * k))
    return out


def arc_at(pts, frac):
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    goal, acc = sum(seg) * frac, 0.0
    for i, sg in enumerate(seg):
        if acc + sg >= goal:
            t = (goal - acc) / sg if sg else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t)
        acc += sg
    return pts[-1]


def badge_svg(shape, x, y, letter):
    r = 7.2
    if shape == "circle":
        g = f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}"/>'
    elif shape == "square":
        g = f'<rect x="{f1(x - r + 0.6)}" y="{f1(y - r + 0.6)}" width="{f1(2 * r - 1.2)}" height="{f1(2 * r - 1.2)}"/>'
    elif shape == "diamond":
        g = f'<path d="M{f1(x)} {f1(y - r - 1.5)}L{f1(x + r + 1.5)} {f1(y)}L{f1(x)} {f1(y + r + 1.5)}L{f1(x - r - 1.5)} {f1(y)}Z"/>'
    elif shape == "triangle":
        g = f'<path d="M{f1(x)} {f1(y - r - 1.5)}L{f1(x + r + 1.8)} {f1(y + r)}L{f1(x - r - 1.8)} {f1(y + r)}Z"/>'
    elif shape == "pentagon":
        pts = [(x + (r + 1.4) * math.cos(math.radians(-90 + 72 * k)), y + (r + 1.4) * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
        g = f'<path d="{poly_d(pts)}"/>'
    else:
        pts = [(x + (r + 1) * math.cos(math.radians(60 * k)), y + (r + 1) * math.sin(math.radians(60 * k))) for k in range(6)]
        g = f'<path d="{poly_d(pts)}"/>'
    ty = y + 3.2 + (1.6 if shape == "triangle" else 0)
    return g + f'<text x="{f1(x)}" y="{f1(ty)}" text-anchor="middle" class="bl">{letter}</text>'


def build_map(kind, points, routes, world_geo, africa_geo):
    world = kind == "world"
    if world:
        proj = NaturalEarth(lon0=10.0, lat_s=-56.0)
        paths = ring_paths(proj, world_geo, 0.35, skip=("010",))
        fs, key = 11.0, "world_pos"
    else:
        proj = Laea(25.0, 2.0, (-19.0, 64.0, -36.0, 35.0))
        paths = ring_paths(proj, africa_geo, 0.45, skip=("010",))
        fs, key = 12.0, "africa_pos"
    W, H = proj.width, proj.height

    # 経路の描画
    leg_svgs, obstacles, tags, leg_data = [], [], [], []
    rank = {rid: i for i, rid in enumerate(sorted(routes))}
    pt_xy = {}
    for pid, p in points.items():
        lat, lon = float(p["lat"]), float(p["lon"])
        if world:
            x, y = proj.xy(proj.rel(lon) + proj.lon0, lat)
        else:
            x, y = proj.xy(lon, lat)
        pt_xy[pid] = (x, y)
    used_in = {pid: set() for pid in points}
    for rid, rt in routes.items():
        for l in rt["legs"]:
            used_in[l["from_point"]].add(rid)
            used_in[l["to_point"]].add(rid)

    shared = {}
    for rid in sorted(routes):
        for l in routes[rid]["legs"]:
            shared.setdefault(frozenset((l["from_point"], l["to_point"])), []).append(rid)
    for rid in sorted(routes):
        for l in routes[rid]["legs"]:
            a, b = points[l["from_point"]], points[l["to_point"]]
            la1, lo1, la2, lo2 = float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"])
            n = 56 if l["mode"] == "flight" else 12
            gc = gc_points(la1, lo1, la2, lo2, n)
            off = (rank[rid] - 2) * 3.2
            subpaths, mid_candidates = [], []
            for sh in proj.shifts:
                pts = [proj.xy(lon, lat, sh) for lat, lon in gc]
                if world:
                    xs = [p[0] for p in pts]
                    if max(xs) < -20 or min(xs) > W + 20:
                        continue
                pts = perp_offset(pts, off)
                if not any(proj.in_view(x, y, 30) for x, y in pts):
                    continue
                subpaths.append(poly_d(pts, False))
                tot = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
                mid_candidates.append((None, tot, pts))
            if not subpaths:
                leg_data.append({"id": f"{rid}-{l['seq']}", "drawn": False})
                continue
            share = shared[frozenset((l["from_point"], l["to_point"]))]
            frac = 0.5 + (share.index(rid) - (len(share) - 1) / 2) * 0.17 if len(share) > 1 else 0.5
            mid_candidates = [(arc_at(pp, frac), tt, pp) for _, tt, pp in mid_candidates]
            vis = [m for m in mid_candidates if 8 <= m[0][0] <= W - 8 and 8 <= m[0][1] <= H - 8]
            mid, tot, pts = (vis or mid_candidates)[0]
            chord = math.hypot(pt_xy[l["to_point"]][0] - pt_xy[l["from_point"]][0], pt_xy[l["to_point"]][1] - pt_xy[l["from_point"]][1])
            show_badge = bool(vis) and (tot >= (46 if world else 40))
            lid = f"{rid}-{l['seq']}"
            d = "".join(subpaths)
            cls = f"leg r-{rid} m-{l['mode']}" + (" unc" if l["unconfirmed"] == "Y" else "") + (" tr" if l["status"] == "空港乗継のみ" else "")
            title = f"{rid} {a['name_ja']}→{b['name_ja']}（{MODE_JA[l['mode']]}、{km_text(l['km'])}）"
            g = [f'<g class="{cls}" id="leg-{lid}" data-leg="{lid}" data-route="{rid}" tabindex="0" role="button" aria-label="{html.escape(title)}">',
                 f'<title>{html.escape(title)}</title>',
                 f'<path class="hit" d="{d}"/><path class="ln" d="{d}"/>']
            if show_badge:
                g.append(f'<g class="badge">{badge_svg(BADGE_SHAPE[rid], mid[0], mid[1], rid)}</g>')
                if l["unconfirmed"] == "Y":
                    g.append(f'<text class="uncl" x="{f1(mid[0] + 10)}" y="{f1(mid[1] + 3.5)}">未確認</text>')
                obstacles.append((mid[0] - 9, mid[1] - 9, mid[0] + 9, mid[1] + 9))
            g.append("</g>")
            leg_svgs.append("".join(g))
            leg_data.append({"id": lid, "drawn": True})
            # 図の外へ出る端点（アフリカ地図）に方面タグ
            if not world:
                for end, other in (("from_point", "to_point"), ("to_point", "from_point")):
                    px, py = pt_xy[l[end]]
                    if not proj.in_view(px, py, 0):
                        pp = points[l[end]]
                        base = pts if end == "to_point" else pts
                        inside = [q for q in pts if proj.in_view(q[0], q[1], -14)]
                        if inside:
                            q = inside[-1] if end == "to_point" else inside[0]
                            tags.append((rid, q, pp["name_ja"] + ("（仮）" if pp["provisional"] == "Y" else "") + "方面"))
                            tw = text_w(tags[-1][2], 10.5) + 4
                            obstacles.append((min(W - 4, q[0] + 5) - tw, q[1] - 17, min(W - 4, q[0] + 5), q[1] - 3))

    # 点のマーカーとラベル
    items, markers = [], []
    for pid, p in points.items():
        x, y = pt_xy[pid]
        if not (proj.in_view(x, y, -2)):
            continue
        if not used_in[pid] and pid != "BAGUIO":
            continue
        obstacles.append((x - 5, y - 5, x + 5, y + 5))
    for pid, p in points.items():
        x, y = pt_xy[pid]
        if not proj.in_view(x, y, -2) or (not used_in[pid] and pid != "BAGUIO"):
            continue
        pref = p[key]
        if pref not in ("none", "dot"):
            prio = 0 if pid in ("MNL", "CPT", "JNB") else 1 if p["kind"] == "airport" else 2
            it = {"id": pid, "x": x, "y": y, "pref": pref, "lv0": label_for(p, 0), "lv1": label_for(p, 1), "prio": prio}
            pre = "world_label_" if world else "label_"
            if p.get(pre + "dx", "") != "" or p.get(pre + "dy", "") != "":
                it["fixed"] = (float(p.get(pre + "dx") or 0), float(p.get(pre + "dy") or 0),
                               {"s": "start", "e": "end", "m": "middle"}.get(p.get(pre + "anchor") or "s"))
            items.append(it)
    labels = place_labels(items, obstacles, fs, (2, 2, W - 2, H - 2))
    for pid, p in points.items():
        x, y = pt_xy[pid]
        if not proj.in_view(x, y, -2) or (not used_in[pid] and pid != "BAGUIO"):
            continue
        routes_used = "".join(sorted(used_in[pid]))
        cls = "pt"
        if pid == "MNL":
            cls += " start"
        if pid in ("CPT",):
            cls += " end"
        if p["provisional"] == "Y":
            cls += " prov"
        if p["kind"] == "city" or p["kind"] == "park" or p["kind"] == "border":
            cls += " minor"
        title = p["name_ja"] + (f"（{p['iata_or_code']}）" if p["iata_or_code"] else "")
        g = [f'<g class="{cls}" id="pt-{pid}" data-pt="{pid}" data-routes="{routes_used}" tabindex="0" role="button" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>']
        if pid == "MNL":
            g.append(f'<circle class="ring" cx="{f1(x)}" cy="{f1(y)}" r="8.5"/>')
        if pid == "CPT":
            g.append(f'<circle class="ring" cx="{f1(x)}" cy="{f1(y)}" r="8.5"/>')
        g.append(f'<circle class="dot" cx="{f1(x)}" cy="{f1(y)}" r="{4.2 if pid in ("MNL", "CPT") else 3.4}"/>')
        g.append(f'<circle class="hitc" cx="{f1(x)}" cy="{f1(y)}" r="11"/>')
        lab = labels.get(pid)
        if lab:
            txt, anchor, tx, ty, r, level = lab
            minor = "" if pid in ("MNL", "CPT", "JNB", "NBO", "ADD", "TNR") else " minor"
            extra = ""
            g.append(f'<text class="lb{minor}" x="{f1(tx)}" y="{f1(ty)}" text-anchor="{anchor}">{html.escape(txt)}</text>')
        g.append("</g>")
        markers.append("".join(g))
    # 出発・終点の注記
    notes = []
    for pid, word in (("MNL", "出発"), ("CPT", "終点（南ア）")):
        if pid in pt_xy and proj.in_view(*pt_xy[pid], -2):
            x, y = pt_xy[pid]
            lab = labels.get(pid)
            notes.append((pid, word))

    # 方面タグ（重なりを避けて縦にずらす）
    tag_svgs = []
    seen = {}
    tag_rects = []
    for rid, q, txt in sorted(tags, key=lambda t: (t[2], t[0])):
        k = txt
        seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1:
            continue
        x, y = q
        tx, ty = min(W - 4, x + 5), y - 5
        tw = text_w(txt, 10.5) + 4
        for _ in range(12):  # 他の方面タグと重なるなら下へずらす
            r = (tx - tw, ty - 12, tx, ty + 3)
            if not any(r[0] < o[2] and r[2] > o[0] and r[1] < o[3] and r[3] > o[1] for o in tag_rects):
                break
            ty += 18
        tag_rects.append((tx - tw, ty - 12, tx, ty + 3))
        tag_svgs.append(f'<text class="tag" x="{f1(tx)}" y="{f1(ty)}" text-anchor="end">{html.escape(txt)}</text>')

    # エチオピア警戒
    eth = paths.get(CAUTION)
    caution = ""
    if eth:
        north = region_polygon(proj, 30.0, 50.0, 10.0, 18.5)
        caution = (f'<clipPath id="ethclip"><path d="{eth[1]}"/></clipPath>'
                   f'<g class="caution" clip-path="url(#ethclip)"><path d="{eth[1]}" class="ctint"/><path d="{north}" fill="url(#hatch)"/></g>')

    # 国
    land = []
    for cid, (name, d) in paths.items():
        cls = "co" + (" visit" if cid in VISIT else "")
        land.append(f'<path class="{cls}" d="{d}"><title>{html.escape(name)}</title></path>')

    if world:
        grat = graticule(proj, 30, 30, (-180, 180), (-60, 60)) + graticule(proj, 360, 90, (-180, 180), (-58, 84)).replace("", "")
        outline = poly_d(proj.outline())
    else:
        lo0, lo1, la0, la1 = proj.window
        grat = graticule(proj, 10, 10, (-30, 70), (-40, 40))
        outline = f"M0 0H{f1(W)}V{f1(H)}H0Z"
    clip_id = "mapclip"
    sea = f'<clipPath id="{clip_id}"><path d="{outline}"/></clipPath>'
    defs = (f'<defs>{sea}<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="6" height="6" fill="none"/><line x1="0" y1="0" x2="0" y2="6" class="hatchln"/></pattern></defs>')
    fx = [pt_xy[k][0] for k in pt_xy if used_in[k] and proj.in_view(*pt_xy[k], 0)]
    fy = [pt_xy[k][1] for k in pt_xy if used_in[k] and proj.in_view(*pt_xy[k], 0)]
    fw = max(max(fx) - min(fx) + 240, (max(fy) - min(fy) + 80) * W / H)
    fw = min(W, max(fw, W * 0.42))
    fh = fw * H / W
    fcx, fcy = (min(fx) + max(fx)) / 2, (min(fy) + max(fy)) / 2
    f0x = max(0.0, min(W - fw, fcx - fw / 2))
    f0y = max(0.0, min(H - fh, fcy - fh / 2))
    focus = f"{f1(f0x)} {f1(f0y)} {f1(fw)} {f1(fh)}"
    svg = (f'<svg id="map" data-focus="{focus}" viewBox="0 0 {f1(W)} {f1(H)}" role="group" aria-label="{"世界" if world else "アフリカ"}地図：候補ルート" data-w="{f1(W)}" data-h="{f1(H)}">'
           f'{defs}<g clip-path="url(#{clip_id})">'
           f'<path class="sea" d="{outline}"/>'
           f'<path class="grat" d="{grat}"/>'
           f'<g class="land">{"".join(land)}</g>{caution}'
           f'<g class="legs">{"".join(leg_svgs)}</g>'
           f'<g class="tags">{"".join(tag_svgs)}</g>'
           f'</g><path class="frame" d="{outline}"/>'
           f'<g class="pts">{"".join(markers)}</g>'
           f'</svg>')

    # 出発・終点バッジのテキストは地点注記として別途HTMLの凡例で説明する
    return svg, labels


# ---------------------------------------------------------------- page
MAP_VARS = """:root{--sea:#e6eef3;--land:#f4f1e8;--visit:#e3e8c9;--border:#b9b4a4;--grat:#cdd8df;--pt:#1d2227;--caution:#b3261e;--cautionbg:#f1d9d6;
--rA:#0072B2;--rB:#B84A00;--rC:#007A5A;--rD:#A5498A;--rE:#8A6D00;--rF:#3B3B3B}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--sea:#1a2530;--land:#2b2f2c;--visit:#3b4328;--border:#59605a;--grat:#2a3844;--pt:#e3e6e8;--caution:#ff8a80;--cautionbg:#4a2523;
--rA:#56B4E9;--rB:#FF9A5C;--rC:#3DCCA0;--rD:#E7A6CE;--rE:#F2C94C;--rF:#D9D9D9}}
:root[data-theme="dark"]{--sea:#1a2530;--land:#2b2f2c;--visit:#3b4328;--border:#59605a;--grat:#2a3844;--pt:#e3e6e8;--caution:#ff8a80;--cautionbg:#4a2523;
--rA:#56B4E9;--rB:#FF9A5C;--rC:#3DCCA0;--rD:#E7A6CE;--rE:#F2C94C;--rF:#D9D9D9}
"""

# 共通テンプレート（scripts/build_html.py の BASE_CSS：固定ナビ・16px・行間1.8・色トークン）の上に、地図固有の規則だけを足す
CSS = BASE_CSS + MAP_VARS + """.switch{display:flex;flex-wrap:wrap;gap:6px 16px;margin:10px 0;padding:6px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:.95em}
fieldset{border:0;margin:14px 0 6px;padding:0;min-width:0}
legend{font-weight:700;padding:0;margin-bottom:4px}
.sel{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:2px 16px}
.sel label{display:flex;gap:8px;align-items:flex-start;padding:6px 4px;min-height:44px;cursor:pointer}
.sel input{margin-top:6px;flex:none}
.sel .tot{color:var(--muted);font-size:.9em;display:block}
.mapbox{position:relative;margin:10px 0;border:1px solid var(--line)}
svg#map{display:block;width:100%;height:auto;background:var(--sea);touch-action:pan-y;user-select:none;-webkit-user-select:none;font-family:var(--sans)}
svg#map.zoomed{touch-action:none;cursor:grab}
.zoom{position:absolute;right:8px;top:8px;display:flex;gap:4px}
.zoom button{font:inherit;min-width:44px;min-height:44px;padding:0 10px;background:var(--bg);color:var(--ink);border:1px solid var(--line);cursor:pointer}
.sea{fill:var(--sea)} .frame{fill:none;stroke:var(--border);stroke-width:1}
.grat{fill:none;stroke:var(--grat);stroke-width:.6}
.co{fill:var(--land);stroke:var(--border);stroke-width:.5;fill-rule:evenodd;stroke-linejoin:round}
.co.visit{fill:var(--visit)}
.ctint{fill:var(--cautionbg);stroke:var(--caution);stroke-width:.8}
.hatchln{stroke:var(--caution);stroke-width:1.1}
.leg{--c:var(--rA);cursor:pointer;transition:opacity .15s}
.leg.r-A{--c:var(--rA)} .leg.r-B{--c:var(--rB)} .leg.r-C{--c:var(--rC)} .leg.r-D{--c:var(--rD)} .leg.r-E{--c:var(--rE)} .leg.r-F{--c:var(--rF)}
.leg .ln{fill:none;stroke:var(--c);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;pointer-events:none}
.leg .hit{fill:none;stroke:transparent;stroke-width:14}
.leg.m-overland .ln{stroke-width:2.8}
.leg.m-ferry .ln,.leg.m-sea .ln{stroke-dasharray:9 5}
.leg.unc .ln{stroke-dasharray:.1 5.2;stroke-width:2.6}
.leg.m-overland.unc .ln{stroke-width:3}
.leg.tr .ln{stroke-dasharray:7 4 1.5 4}
.leg.r-F:not(.unc):not(.tr) .ln{stroke-dasharray:14 3 3 3}
.leg .badge path,.leg .badge circle,.leg .badge rect{fill:var(--c);stroke:var(--bg);stroke-width:1.2}
.leg .bl{font-size:9.5px;font-weight:700;fill:var(--bg);pointer-events:none}
.leg .uncl{display:none;font-size:10px;fill:var(--ink);paint-order:stroke;stroke:var(--sea);stroke-width:3px;pointer-events:none}
svg#map.solo .leg .uncl{display:inline}
.leg:hover .ln,.leg:focus .ln,.leg.on .ln{stroke-width:4}
.leg:focus{outline:none} .leg:focus-visible .ln{stroke:var(--ink);stroke-width:4.5}
.leg.off,.pt.off{opacity:.1;pointer-events:none}
.pt{cursor:pointer;transition:opacity .15s} .pt:focus{outline:none}
.pt .dot{fill:var(--pt);stroke:var(--sea);stroke-width:1.2}
.pt.prov .dot{fill:var(--sea);stroke:var(--pt);stroke-width:1.6}
.pt .ring{fill:none;stroke:var(--pt);stroke-width:1.6}
.pt.start .ring{stroke-dasharray:none} .pt.end .ring{stroke-dasharray:3 2}
.pt .hitc{fill:transparent}
.pt:focus-visible .dot,.pt:hover .dot{stroke:var(--link);stroke-width:2.4}
.lb{font-size:calc(11px * var(--ts,1));fill:var(--ink);paint-order:stroke;stroke:var(--sea);stroke-width:3.2px;stroke-linejoin:round;pointer-events:none}
.tag{font-size:calc(10.5px * var(--ts,1));fill:var(--muted);paint-order:stroke;stroke:var(--sea);stroke-width:3px}
svg#map.lo .lb.minor{display:none}
#detail{margin:8px 0;padding:10px 14px;border:1px solid var(--line);border-radius:4px;background:var(--th);min-height:5.5em;font-size:.95em}
#detail h3{margin:0 0 4px;font-size:1rem} #detail dl{margin:4px 0;display:grid;grid-template-columns:7em 1fr;gap:2px 10px} #detail dt{color:var(--muted)} #detail dd{margin:0;overflow-wrap:anywhere}
.scroll table{min-width:560px} th{white-space:nowrap}
tr.row{cursor:pointer} tr.row:hover td,tr.row.on td{background:var(--hl)}
tr:last-child td{border-bottom:0}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:6px 18px;margin:8px 0;font-size:.93em}
.legend div{display:flex;gap:8px;align-items:center}
.legend svg{flex:none;width:54px;height:16px;overflow:visible}
.lgl{fill:none;stroke:var(--ink);stroke-width:2.4;stroke-linecap:round}
.cautionnote{border:1px solid var(--caution);border-radius:4px;background:var(--cautionbg);padding:8px 12px;margin:12px 0;font-size:.93em}
.rb{display:inline-block;min-width:1.6em;padding:0 5px;margin-right:4px;font-weight:700;text-align:center;color:var(--bg);background:var(--c,var(--ink))}
.rb.A{--c:var(--rA)} .rb.B{--c:var(--rB)} .rb.C{--c:var(--rC)} .rb.D{--c:var(--rD)} .rb.E{--c:var(--rE)} .rb.F{--c:var(--rF)}
@media(max-width:480px){#detail dl{grid-template-columns:5.5em 1fr}}
"""

JS = r"""(function(){
var D=JSON.parse(document.getElementById('map-data').textContent);
var svg=document.getElementById('map'),detail=document.getElementById('detail'),body=document.getElementById('tbody'),head=document.getElementById('thead');
var W=+svg.dataset.w,H=+svg.dataset.h,vb={x:0,y:0,w:W,h:H},sel='all',legs={},pts={};
D.legs.forEach(function(l){legs[l.id]=l});D.points.forEach(function(p){pts[p.id]=p});
function el(t,txt,cls){var e=document.createElement(t);if(txt!=null)e.textContent=txt;if(cls)e.className=cls;return e}
function link(txt,url){var a=el('a',txt);a.href=url;a.target='_blank';a.rel='noopener';return a}
function row(dl,k,v){dl.appendChild(el('dt',k));var dd=el('dd');if(typeof v==='string')dd.textContent=v;else dd.appendChild(v);dl.appendChild(dd)}
function showLeg(id){var l=legs[id];if(!l)return;detail.textContent='';detail.appendChild(el('h3',l.route+'-'+l.seq+'　'+l.from+' → '+l.to));
var dl=el('dl');row(dl,'手段',l.mode);row(dl,'直線距離（参考）',l.km+'（大圏距離。実際の飛行・走行距離ではない）');row(dl,'状態',l.status+(l.unc?'／未確認':''));row(dl,'備考',l.note);
var s=el('span');s.appendChild(link(l.from+'（Google マップ）',l.url_from));s.appendChild(document.createTextNode('　'));s.appendChild(link(l.to+'（Google マップ）',l.url_to));row(dl,'地図',s);detail.appendChild(dl);
mark(id)}
function showPt(id){var p=pts[id];if(!p)return;detail.textContent='';detail.appendChild(el('h3',p.name+(p.code?'（'+p.code+'）':'')));var dl=el('dl');row(dl,'国',p.country);row(dl,'備考',p.note);row(dl,'使うルート',p.routes||'なし');row(dl,'地図',link('Google マップで開く',p.url));detail.appendChild(dl)}
function mark(id){svg.querySelectorAll('.leg.on').forEach(function(e){e.classList.remove('on')});var g=document.getElementById('leg-'+id);if(g)g.classList.add('on');
body.querySelectorAll('tr.on').forEach(function(e){e.classList.remove('on')});var r=document.getElementById('row-'+id);if(r)r.classList.add('on')}
function tbl(){head.textContent='';body.textContent='';var tr=el('tr');
if(sel==='all'){['ルート','直線距離の合計（参考）','区間数','未確認の区間'].forEach(function(h,i){tr.appendChild(el('th',h,i==1?'n':''))});head.appendChild(tr);
D.routes.forEach(function(r){var t=el('tr',null,'row');t.tabIndex=0;var c=el('td');c.appendChild(el('span',r.id,'rb '+r.id));c.appendChild(document.createTextNode(r.name));t.appendChild(c);t.appendChild(el('td',r.km,'n'));t.appendChild(el('td',String(r.n),'n'));t.appendChild(el('td',String(r.unc),'n'));
var go=function(){pick(r.id)};t.addEventListener('click',go);t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}});body.appendChild(t)});return}
['区間','手段','直線距離','状態','地図'].forEach(function(h,i){tr.appendChild(el('th',h,i==2?'n':''))});head.appendChild(tr);
D.legs.filter(function(l){return l.route===sel}).forEach(function(l){var t=el('tr',null,'row');t.id='row-'+l.id;t.tabIndex=0;t.appendChild(el('td',l.seq+'. '+l.from+' → '+l.to));t.appendChild(el('td',l.mode));t.appendChild(el('td',l.km,'n'));t.appendChild(el('td',l.status+(l.unc?'（未確認）':'')));
var c=el('td');c.appendChild(link(l.to,l.url_to));t.appendChild(c);
var go=function(){showLeg(l.id)};t.addEventListener('click',function(e){if(e.target.tagName!=='A')go()});t.addEventListener('keydown',function(e){if(e.key==='Enter'){go()}});body.appendChild(t)})}
function pick(id){var r=document.querySelector('input[name=rt][value='+id+']');if(r){r.checked=true}apply(id)}
function apply(v){sel=v;svg.classList.toggle('solo',v!=='all');
svg.querySelectorAll('.leg').forEach(function(g){g.classList.toggle('off',v!=='all'&&g.dataset.route!==v)});
svg.querySelectorAll('.pt').forEach(function(g){var r=g.dataset.routes||'';g.classList.toggle('off',v!=='all'&&r.indexOf(v)<0&&g.dataset.pt!=='MNL'&&g.dataset.pt!=='BAGUIO')});
tbl();detail.textContent='';detail.appendChild(el('p',v==='all'?'線または地点を選ぶ（ホバー・タップ・Tabキー）と、区間の詳細を表示します。':'ルート'+v+'：線・表の行を選ぶと区間の詳細を表示します。'))}
document.querySelectorAll('input[name=rt]').forEach(function(r){r.addEventListener('change',function(){apply(r.value)})});
svg.querySelectorAll('.leg').forEach(function(g){var id=g.dataset.leg;g.addEventListener('mouseenter',function(){showLeg(id)});g.addEventListener('focus',function(){showLeg(id)});g.addEventListener('click',function(){showLeg(id)});g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();showLeg(id)}})});
svg.querySelectorAll('.pt').forEach(function(g){var id=g.dataset.pt;['mouseenter','focus','click'].forEach(function(ev){g.addEventListener(ev,function(){showPt(id)})})});
function setVB(){svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);var px=svg.getBoundingClientRect().width||W,sc=px/vb.w;
svg.classList.toggle('lo',sc<0.62);svg.classList.toggle('zoomed',vb.w<W-1);svg.style.setProperty('--ts',Math.max(1,Math.min(1.6,0.62/sc)).toFixed(2))}
function zoom(f){var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2,w=Math.max(W/10,Math.min(W,vb.w/f)),h=w*H/W;vb.w=w;vb.h=h;vb.x=cx-w/2;vb.y=cy-h/2;clamp();setVB()}
function clamp(){vb.x=Math.max(0,Math.min(W-vb.w,vb.x));vb.y=Math.max(0,Math.min(H-vb.h,vb.y))}
document.getElementById('zin').addEventListener('click',function(){zoom(1.6)});document.getElementById('zout').addEventListener('click',function(){zoom(1/1.6)});document.getElementById('zrs').addEventListener('click',function(){vb={x:0,y:0,w:W,h:H};setVB()});
var drag=null;svg.addEventListener('pointerdown',function(e){if(vb.w>=W-1||e.target.closest('.leg,.pt'))return;drag={x:e.clientX,y:e.clientY,vx:vb.x,vy:vb.y};svg.setPointerCapture(e.pointerId)});
svg.addEventListener('pointermove',function(e){if(!drag)return;var k=vb.w/svg.getBoundingClientRect().width;vb.x=drag.vx-(e.clientX-drag.x)*k;vb.y=drag.vy-(e.clientY-drag.y)*k;clamp();setVB()});
svg.addEventListener('pointerup',function(){drag=null});svg.addEventListener('pointercancel',function(){drag=null});
window.addEventListener('resize',setVB);
if(svg.getBoundingClientRect().width<640&&svg.dataset.focus){var f=svg.dataset.focus.split(' ').map(Number);vb={x:f[0],y:f[1],w:f[2],h:f[3]}}
setVB();apply('all');var hm=/^#route-([A-Z])$/.exec(location.hash);if(hm&&document.querySelector('input[name=rt][value='+hm[1]+']'))pick(hm[1]);
})();"""


def legend_html():
    def ln(cls, extra=""):
        return f'<svg viewBox="0 0 54 16" aria-hidden="true"><path class="lgl" d="M2 8H52" {extra}/></svg>'
    items = [
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><path class="lgl" d="M2 13Q27 -6 52 13"/></svg>', "航空：大圏（最短）経路の曲線"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><path class="lgl" d="M2 8H52" style="stroke-width:3.2"/></svg>', "陸路：点を結ぶ直線。実際の道路経路ではない"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><path class="lgl" d="M2 8H52" style="stroke-dasharray:.1 5.2;stroke-width:3"/></svg>', "点線：区間または乗継地が未確認（「未確認」と表示）"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><path class="lgl" d="M2 8H52" style="stroke-dasharray:7 4 1.5 4"/></svg>', "一点鎖線：エチオピアは空港乗継のみ（市内滞在・北部は対象外）"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><circle cx="27" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="27" cy="8" r="3.6" fill="currentColor"/></svg>', "二重丸：出発地（マニラ。バギオからの国内移動は描かない）／破線の二重丸：終点（ケープタウン）"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><circle cx="27" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>', "白抜きの丸と「（仮）」「*」：乗継地は未確認で、資料の例示から仮置きした空港"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><rect x="2" y="2" width="50" height="12" fill="var(--cautionbg)" stroke="var(--caution)"/><path d="M8 14L20 2M18 14L30 2M28 14L40 2M38 14L50 2" stroke="var(--caution)" stroke-width="1"/></svg>', "斜線の赤系：エチオピア（北部は渡航を避ける勧告。概略の範囲で行政区界ではない）"),
        ('<svg viewBox="0 0 54 16" aria-hidden="true"><rect x="2" y="2" width="50" height="12" fill="var(--visit)" stroke="var(--border)"/></svg>', "薄い緑：候補ルートの行き先の国"),
    ]
    return '<div class="legend">' + "".join(f"<div>{i}<span>{t}</span></div>" for i, t in items) + "</div>" + \
        '<p class="muted">ルートは色と、区間の中央のバッジの形・文字（A 丸／B 四角／C ひし形／D 三角／E 六角形／F 五角形）で区別します。同じ区間を通るルートは少しずらして描いています。</p>'


def build_page(kind, points, routes, world_geo, africa_geo):
    world = kind == "world"
    svg, labels = build_map(kind, points, routes, world_geo, africa_geo)
    title = "世界地図：候補ルート" if world else "アフリカ地図：候補ルート"
    data_legs, data_routes, data_pts = [], [], []
    for rid in sorted(routes):
        rt = routes[rid]
        data_routes.append({"id": rid, "name": rt["name"], "km": km_text(rt["km"]), "n": len(rt["legs"]),
                            "unc": sum(1 for l in rt["legs"] if l["unconfirmed"] == "Y")})
        for l in rt["legs"]:
            a, b = points[l["from_point"]], points[l["to_point"]]
            data_legs.append({"id": f"{rid}-{l['seq']}", "route": rid, "seq": l["seq"], "from": a["name_ja"], "to": b["name_ja"],
                              "mode": MODE_JA[l["mode"]], "km": km_text(l["km"]), "status": l["status"], "unc": l["unconfirmed"] == "Y",
                              "note": l["note"], "url_from": maps_link(a["maps_query"]), "url_to": maps_link(b["maps_query"])})
    used = {}
    for rid in routes:
        for l in routes[rid]["legs"]:
            for e in (l["from_point"], l["to_point"]):
                used.setdefault(e, set()).add(rid)
    for pid, p in points.items():
        data_pts.append({"id": pid, "name": p["name_ja"], "code": p["iata_or_code"], "country": p["country"], "note": p["note"],
                         "routes": " ".join(sorted(used.get(pid, ()))), "url": maps_link(p["maps_query"])})
    data = json.dumps({"legs": data_legs, "routes": data_routes, "points": data_pts}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    radios = ['<label><input type="radio" name="rt" value="all" checked><span>すべて<span class="tot">全ルートを重ねて表示</span></span></label>']
    for rid in sorted(routes):
        rt = routes[rid]
        radios.append(f'<label><input type="radio" name="rt" value="{rid}"><span><span class="rb {rid}">{rid}</span>{html.escape(rt["name"])}'
                      f'<span class="tot">直線距離の合計 {km_text(rt["km"])}（参考）</span></span></label>')
    other = ("africa-map.html", "アフリカ地図") if world else ("world-map.html", "世界地図")
    here = "世界地図" if world else "アフリカ地図"
    off_note = ("" if world else '<p class="muted">アジア発の区間は図の外（東）にあります。線が図の端から入る所に「○○方面」と表示し、区間の一覧は下の表で確認できます。</p>')
    zoom_note = "地図は拡大・縮小ボタンで拡大でき、拡大中はドラッグで移動できます。"
    caution = ('<div class="cautionnote"><strong>エチオピア（斜線部）：</strong>英国FCDO（2026-10-16更新）はティグライ・アムハラ・ガンベラ全域への渡航を避けるよう勧告。'
               '外務省も北部の一部にレベル3〜4の危険情報を出し、2026-09-26にスポット情報を発出。アディスアベバは<strong>空港乗継のみ</strong>で、'
               '北部は観光対象外としています（<a href="../research/africa-route-comparison.html#4-最新の危険情報確認日-2026-10-17">比較資料 第4章</a>）。斜線は北部の概略で、実際の区域ではありません。</div>')
    page = f"""<!doctype html>
<!-- generated by scripts/build_maps.py from data/route_points.csv, data/routes.csv, data/geo/*.json; do not edit -->
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜2027 留学・アフリカ周遊</title>
<style>
{CSS}</style></head><body>
{bar("../", "maps/" + ("world-map" if world else "africa-map") + ".html")}
<main class="wrap page">
<p class="crumb"><a href="../index.html">トップ</a> ／ ルート地図</p>
<h1>{title}</h1>
<p class="lead">候補ルートの概念図。実際の経路・運賃・入国条件は <a href="../research/africa-route-comparison.html">research/africa-route-comparison.html</a> を参照。2027年の運航は未確認。</p>
<nav class="switch" aria-label="地図とページの移動"><span aria-current="page"><strong>{here}</strong></span><a href="{other[0]}">{other[1]}</a><a href="../research/africa-route-comparison.html">ルート比較資料</a><a href="../areas/africa.html">アフリカ周遊のページ</a></nav>
<fieldset><legend>表示するルート</legend><div class="sel">{"".join(radios)}</div></fieldset>
<p class="muted">直線距離の合計は大圏（地球上の最短距離）の足し算で、<strong>実際の飛行・走行距離ではありません</strong>。区間の運賃・ダイヤは未確認のものを含みます。{zoom_note}</p>
<div class="mapbox">{svg}<div class="zoom"><button type="button" id="zin" aria-label="拡大">＋</button><button type="button" id="zout" aria-label="縮小">－</button><button type="button" id="zrs" aria-label="全体表示">全体</button></div></div>
{off_note}
<div id="detail" role="status" aria-live="polite"></div>
{caution}
<h2>選んだルートの区間</h2>
<div class="scroll"><table><thead id="thead"></thead><tbody id="tbody"></tbody></table></div>
<h2>凡例</h2>
{legend_html()}
<p class="note">個人の予約・日程・支払いは含みません。公開されている空港・都市・公園の位置と、資料に載っている一般的なルート案だけを描いた概念図です。陸路は実際の道路経路ではなく、点を直線で結んだ例示です。</p>
<footer><nav class="all" id="all-pages" aria-label="全ページ">{site_nav(ROOT, ROOT / "maps" / ("world-map.html" if world else "africa-map.html"))}</nav><p>地図データ：<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（パブリックドメイン）を <a href="https://github.com/topojson/world-atlas" target="_blank" rel="noopener">world-atlas</a> 2.0.2（ISC）経由で使用し、{"図法はNatural Earth図法" if world else "図法はランベルト正積方位図法"}で描画。このページは <code>scripts/build_maps.py</code> が内部データから自動生成します（手で編集しない）。外部の通信は行いません。</p></footer>
</main>
<script type="application/json" id="map-data">{data}</script>
<script>
{JS}
</script>
</body></html>
"""
    return page


def outputs():
    points, routes = load_model()
    world_geo = load_topo("countries-110m.json")
    africa_geo = load_topo("countries-50m.json")
    return {OUT_DIR / "world-map.html": build_page("world", points, routes, world_geo, africa_geo),
            OUT_DIR / "africa-map.html": build_page("africa", points, routes, world_geo, africa_geo)}


def main() -> int:
    out = outputs()
    if "--check" in sys.argv:
        stale = [p.relative_to(ROOT).as_posix() for p, t in out.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            print("地図HTMLが古いです。`py scripts/build_maps.py` を実行してコミットしてください: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"PASS: {len(out)} map pages are current")
        return 0
    OUT_DIR.mkdir(exist_ok=True)
    for p, t in out.items():
        p.write_text(t, encoding="utf-8", newline="\n")
        print(f"{p.relative_to(ROOT).as_posix()}: {len(t.encode('utf-8')) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
