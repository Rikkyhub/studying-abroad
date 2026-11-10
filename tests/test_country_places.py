import csv
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_maps as bm  # noqa: E402

# 50m の国境は海岸線を粗く丸めるため、海岸の町・島は線の外に数km出ることがある。その許容距離（km）
COAST_TOLERANCE_KM = 30


def _inside(poly, lon, lat):
    c = False
    for ring in poly:
        j = len(ring) - 1
        for i in range(len(ring)):
            xi, yi = ring[i]
            xj, yj = ring[j]
            if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-18) + xi:
                c = not c
            j = i
    return c


def _km_to_border(country, lon, lat):
    best = 1e9
    for poly in country["polys"]:
        for ring in poly:
            for x, y in ring:
                best = min(best, bm.haversine(lat, lon, y, x))
    return best


class CountryPlacesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geo = {c["id"]: c for c in bm.load_topo("countries-50m.json")}
        with (ROOT / "data" / "countries.csv").open(newline="", encoding="utf-8-sig") as f:
            cls.iso = {r["slug"]: r["iso_numeric"] for r in csv.DictReader(f)}
        with (ROOT / "data" / "country_places.csv").open(newline="", encoding="utf-8-sig") as f:
            cls.rows = list(csv.DictReader(f))

    def test_every_point_is_inside_or_next_to_its_country(self):
        for r in self.rows:
            with self.subTest(place=f"{r['slug']}/{r['id']}"):
                self.assertIn(r["slug"], self.iso, "countries.csv にない国")
                c = self.geo[self.iso[r["slug"]]]
                lon, lat = float(r["lon"]), float(r["lat"])
                if any(_inside(p, lon, lat) for p in c["polys"]):
                    continue
                self.assertLessEqual(_km_to_border(c, lon, lat), COAST_TOLERANCE_KM,
                                     "国境の外側に離れすぎ。座標の取り違えの可能性")

    def test_every_point_has_a_public_source(self):
        for r in self.rows:
            with self.subTest(place=f"{r['slug']}/{r['id']}"):
                self.assertTrue(r["source_url"].startswith("https://"))

    def test_country_page_embeds_a_map_for_each_country_with_places(self):
        for slug in sorted({r["slug"] for r in self.rows}):
            with self.subTest(slug=slug):
                html = (ROOT / "countries" / f"{slug}.html").read_text(encoding="utf-8")
                self.assertIn('class="cmap"', html)


if __name__ == "__main__":
    unittest.main()
