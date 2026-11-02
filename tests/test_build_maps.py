"""ルート地図（maps/*.html）の生成・データ整合・オフライン性のテスト。"""
import csv
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_maps as bm

MAPS = [REPO / "maps" / "world-map.html", REPO / "maps" / "africa-map.html"]


def rows(name):
    with (REPO / "data" / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


class GeometryTests(unittest.TestCase):
    def test_topojson_decodes(self):
        for name, minimum in (("countries-110m.json", 150), ("countries-50m.json", 200)):
            countries = bm.load_topo(name)
            self.assertGreaterEqual(len(countries), minimum)
            self.assertTrue(all(c["polys"] and c["polys"][0][0] for c in countries))

    def test_paths_within_viewbox_and_not_empty(self):
        geo = {"world": bm.load_topo("countries-110m.json"), "africa": bm.load_topo("countries-50m.json")}
        for kind in ("world", "africa"):
            text = (REPO / "maps" / f"{kind}-map.html").read_text(encoding="utf-8")
            w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', text).groups())
            land = re.search(r'<g class="land">(.*?)</g>', text, re.S).group(1)
            ds = re.findall(r' d="([^"]+)"', land)
            self.assertGreater(len(ds), 40 if kind == "world" else 25)
            for d in ds:
                for x, y in re.findall(r"[ML]\s*(-?[\d.]+)\s+(-?[\d.]+)", d):
                    # 図の外へはみ出す国（ロシア等）は枠でクリップされる。極端な値（折り返しの破綻）だけを検出する
                    self.assertTrue(-w <= float(x) <= 2 * w and -h <= float(y) <= 2 * h, (kind, x, y))
        self.assertTrue(geo["world"])

    def test_antimeridian_countries_have_no_wrap_spans(self):
        """Russia / Fiji: 折り返しで経度が360度飛ばず、図法上で連続した多角形になる"""
        for c in bm.load_topo("countries-110m.json"):
            if c["name"] in ("Russia", "Fiji"):
                for poly in c["polys"]:
                    for ring in poly:
                        lons = [p[0] for p in bm.unwrap(ring)]
                        steps = [abs(b - a) for a, b in zip(lons, lons[1:])]
                        self.assertLess(max(steps), 90, c["name"])

    def test_page_size_reasonable(self):
        for p in MAPS:
            self.assertLess(p.stat().st_size, 400 * 1024, p.name)


class MathTests(unittest.TestCase):
    def test_great_circle_distance(self):
        d = bm.haversine(14.5086, 121.0194, -1.3192, 36.9278)  # MNL-NBO、約9,400km
        self.assertAlmostEqual(d, 9409, delta=9409 * 0.01)
        self.assertAlmostEqual(bm.haversine(40.6413, -73.7781, 51.47, -0.4543), 5540, delta=55)  # JFK-LHR

    def test_great_circle_points_are_continuous_across_antimeridian(self):
        pts = bm.gc_points(35.5, 139.8, 37.6, -122.4, 40)  # 東京-サンフランシスコ（太平洋を東へ）
        lons = [p[1] for p in pts]
        self.assertTrue(all(abs(b - a) < 20 for a, b in zip(lons, lons[1:])))

    def test_manila_to_africa_goes_west_on_world_map(self):
        pts = bm.gc_points(14.5, 121.0, -1.3, 36.9, 40)
        self.assertTrue(all(b[1] <= a[1] + 1e-6 for a, b in zip(pts, pts[1:])))


class RouteDataTests(unittest.TestCase):
    def setUp(self):
        self.points = {r["id"]: r for r in rows("route_points.csv")}
        self.legs = rows("routes.csv")

    def test_legs_reference_points_and_are_contiguous(self):
        by = {}
        for r in self.legs:
            self.assertIn(r["from_point"], self.points)
            self.assertIn(r["to_point"], self.points)
            by.setdefault(r["route_id"], []).append(r)
        self.assertEqual(sorted(by), ["A", "B", "C", "D", "E", "F"])
        for rid, legs in by.items():
            legs.sort(key=lambda r: int(r["seq"]))
            self.assertEqual([int(r["seq"]) for r in legs], list(range(1, len(legs) + 1)), rid)
            for a, b in zip(legs, legs[1:]):
                self.assertEqual(a["to_point"], b["from_point"], f"{rid}-{b['seq']}")

    def test_routes_start_in_manila_and_end_as_researched(self):
        ends = {"A": "CPT", "B": "CPT", "C": "JNB", "D": "TNR", "E": "CPT", "F": "CPT"}  # Dは「マダガスカルのみB/Eで扱う」。南アには繋げない
        for rid, end in ends.items():
            legs = sorted((r for r in self.legs if r["route_id"] == rid), key=lambda r: int(r["seq"]))
            self.assertEqual(legs[0]["from_point"], "MNL")
            self.assertEqual(legs[-1]["to_point"], end)
        for rid in "ABCEF":
            last = [r for r in self.legs if r["route_id"] == rid][-1]
            self.assertEqual(self.points[last["to_point"]]["country"], "南アフリカ")

    def test_ethiopia_is_transit_only(self):
        for r in self.legs:
            if "ADD" in (r["from_point"], r["to_point"]):
                self.assertEqual(r["status"], "空港乗継のみ", r)

    def test_coordinates_sane_for_known_airports(self):
        expect = {"MNL": (14.5, 121.0), "NBO": (-1.3, 36.9), "JNB": (-26.1, 28.2), "CPT": (-34.0, 18.6),
                  "ADD": (9.0, 38.8), "TNR": (-18.8, 47.5), "DAR": (-6.9, 39.2), "LUN": (-15.3, 28.5)}
        for pid, (lat, lon) in expect.items():
            p = self.points[pid]
            self.assertAlmostEqual(float(p["lat"]), lat, delta=0.15, msg=pid)
            self.assertAlmostEqual(float(p["lon"]), lon, delta=0.15, msg=pid)


class RouteFTests(unittest.TestCase):
    def setUp(self):
        self.points = {r["id"]: r for r in rows("route_points.csv")}
        self.legs = sorted((r for r in rows("routes.csv") if r["route_id"] == "F"), key=lambda r: int(r["seq"]))

    def test_order_matches_research_s2(self):
        order = [self.legs[0]["from_point"]] + [r["to_point"] for r in self.legs]
        self.assertEqual(order, ["MNL", "KUL", "JNB", "MLILWANE", "JNB", "VICFALLS", "LIVINGSTONE", "CHOBE", "MAUN", "CPT"])

    def test_countries_and_end(self):
        countries = {self.points[p]["country"] for r in self.legs for p in (r["from_point"], r["to_point"])}
        for c in ("エスワティニ", "ジンバブエ", "ザンビア", "ボツワナ", "南アフリカ"):
            self.assertIn(c, countries)
        self.assertEqual(self.points[self.legs[-1]["to_point"]]["country"], "南アフリカ")

    def test_new_point_coordinates(self):
        expect = {"MAUN": (-19.97, 23.43), "MLILWANE": (-26.47, 31.16), "LIVINGSTONE": (-17.85, 25.87), "CHOBE": (-17.83, 25.16)}
        for pid, (lat, lon) in expect.items():
            self.assertAlmostEqual(float(self.points[pid]["lat"]), lat, delta=0.1, msg=pid)
            self.assertAlmostEqual(float(self.points[pid]["lon"]), lon, delta=0.1, msg=pid)

    def test_great_circle_sanity(self):
        def d(r):
            a, b = self.points[r["from_point"]], self.points[r["to_point"]]
            return bm.haversine(float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"]))
        km = {(r["from_point"], r["to_point"]): d(r) for r in self.legs}
        self.assertAlmostEqual(km[("JNB", "MLILWANE")], 293, delta=30)  # JNB-ムババーネ付近は約290km（道路は約360km）
        self.assertAlmostEqual(km[("CHOBE", "MAUN")], 302, delta=30)  # 直線約300km（道路は約520km）
        self.assertAlmostEqual(km[("MAUN", "CPT")], 1700, delta=150)

    def test_unverified_legs_are_marked(self):
        self.assertEqual(self.legs[7]["unconfirmed"], "Y")  # カサネ→マウン


class LabelOffsetTests(unittest.TestCase):
    def test_label_columns_valid(self):
        for r in rows("route_points.csv"):
            for pre in ("", "world_"):
                self.assertIn(r[f"{pre}label_anchor"], ("", "s", "e", "m"))

    def test_fixed_offset_label_is_used(self):
        items = [{"id": "X", "x": 100.0, "y": 100.0, "pref": "r", "lv0": "テスト", "lv1": "T", "prio": 1, "fixed": (-8.0, 11.0, "end")}]
        res = bm.place_labels(items, [], 11.0, (0, 0, 500, 500))
        self.assertEqual(res["X"][1:4], ("end", 92.0, 111.0))


class PageTests(unittest.TestCase):
    def test_build_maps_check_is_current(self):
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "build_maps.py"), "--check"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_network_or_external_resources(self):
        for p in MAPS:
            t = p.read_text(encoding="utf-8")
            self.assertNotRegex(t, r"fetch\(|XMLHttpRequest|<script[^>]*\ssrc=|<link[^>]*rel=[\"']?stylesheet|@import|<img|WebSocket|sendBeacon", p.name)
            for url in re.findall(r"https?://[^\s\"'<>)]+", t):
                ok = url.startswith("https://www.google.com/maps/search/?api=1&query=") or \
                    url.startswith(("https://www.naturalearthdata.com/", "https://github.com/topojson/world-atlas"))
                self.assertTrue(ok, f"{p.name}: {url}")

    def test_pages_have_selector_table_credit_and_cross_links(self):
        for p in MAPS:
            t = p.read_text(encoding="utf-8")
            for needle in ('name="rt"', 'id="tbody"', "Natural Earth", "実際の道路経路ではない", "未確認", "africa-route-comparison.html",
                           "prefers-color-scheme:dark", 'data-theme="dark"'):
                self.assertIn(needle, t, f"{p.name}: {needle}")
            self.assertIn("直線距離", t)
            self.assertIn("africa-map.html" if "world" in p.name else "world-map.html", t)

    def test_every_route_leg_is_drawn_on_world_map(self):
        t = (REPO / "maps" / "world-map.html").read_text(encoding="utf-8")
        for r in rows("routes.csv"):
            self.assertIn(f'id="leg-{r["route_id"]}-{r["seq"]}"', t)

    def test_maps_listed_in_pages_csv_and_nav(self):
        paths = {r["path"] for r in rows("pages.csv")}
        for rel in ("maps/world-map.html", "maps/africa-map.html"):
            self.assertIn(rel, paths)
        nav = (REPO / "docs" / "02-budget.html").read_text(encoding="utf-8")
        for rel in ("../maps/world-map.html", "../maps/africa-map.html"):
            self.assertIn(rel, nav)
        self.assertIn("ルート地図", nav)
        africa = (REPO / "areas" / "africa.md").read_text(encoding="utf-8")
        for rel in ("../maps/world-map.html", "../maps/africa-map.html"):
            self.assertIn(rel, africa)

    def test_maps_use_shared_template_and_have_no_csv_links(self):
        for p in MAPS:
            t = p.read_text(encoding="utf-8")
            self.assertIn('class="bar"', t)
            self.assertIn("font:16px/1.8", t)
            self.assertNotIn("border-left", t)
            self.assertNotRegex(re.sub(r"<!--.*?-->|<script.*?</script>", "", t, flags=re.S), r"\.csv")
            self.assertNotIn("区間データ", t)


if __name__ == "__main__":
    unittest.main()
