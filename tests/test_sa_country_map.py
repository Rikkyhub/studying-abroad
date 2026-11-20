"""南米国別地図（maps/southamerica-countries.html）と、国別ページ（group=g4）の整合・決定性のテスト。"""
import csv
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_sa_country_map as sm

PAGE = REPO / "maps" / "southamerica-countries.html"


def sa_countries():
    with (REPO / "data" / "countries.csv").open(newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if r["group"] == "g4"]


class SouthAmericaMapTests(unittest.TestCase):
    def test_seven_countries_each_with_a_page(self):
        cs = sa_countries()
        self.assertEqual(sorted(c["slug"] for c in cs),
                         sorted(["peru", "bolivia", "ecuador", "brazil", "argentina", "chile", "mexico"]))
        for c in cs:
            self.assertTrue((REPO / "countries" / f"{c['slug']}.md").is_file(), c["slug"])

    def test_every_country_is_a_link_to_an_existing_page(self):
        t = PAGE.read_text(encoding="utf-8")
        for c in sa_countries():
            self.assertIn(f'href="../countries/{c["slug"]}.html"', t, c["slug"])
        for href in re.findall(r'href="\.\./countries/([a-z-]+)\.html"', t):
            self.assertTrue((REPO / "countries" / f"{href}.html").is_file(), href)

    def test_africa_countries_are_not_drawn_as_links(self):
        """アフリカの国（g1〜g3）は、この地図ではリンクにしない（アフリカ国別地図の役割）"""
        t = PAGE.read_text(encoding="utf-8")
        svg = t[t.index('<svg id="samap"'):t.index("</svg>", t.index('<svg id="samap"'))]  # 地図の本体だけ（上部ナビ・全ページ一覧には各国のリンクがある）
        self.assertNotIn('href="../countries/kenya.html"', svg)
        self.assertNotIn('href="../countries/namibia.html"', svg)
        cards = t[t.index('<div class="cards">'):t.index("</div>", t.index('<div class="cards">'))]
        self.assertNotIn("countries/kenya.html", cards)

    def test_mexico_is_in_a_separate_inset(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="mexbox"', t)
        self.assertIn("メキシコ（別枠）", t)

    def test_no_network_or_external_resources(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertNotRegex(t, r"fetch\(|XMLHttpRequest|<script[^>]*\ssrc=|<link[^>]*rel=[\"']?stylesheet|@import|<img|WebSocket|sendBeacon")
        for url in re.findall(r"https?://[^\s\"'<>)]+", t):
            self.assertTrue(url.startswith(("https://www.naturalearthdata.com/", "https://github.com/topojson/world-atlas")), url)

    def test_keyboard_and_screen_reader_access(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertIn('role="group"', t)
        self.assertEqual(len(re.findall(r'<a class="cn[^"]*" href=', t)), len(sa_countries()))
        self.assertIn("aria-label", t)

    def test_map_page_is_listed_in_map_switch_and_nav(self):
        from build_html import MAP_PAGES
        self.assertIn("southamerica-countries", [n for n, _ in MAP_PAGES])
        self.assertIn('href="southamerica-countries.html"', (REPO / "maps" / "africa-countries.html").read_text(encoding="utf-8"))

    def test_country_pages_link_back_to_the_map(self):
        for c in sa_countries():
            md = (REPO / "countries" / f"{c['slug']}.md").read_text(encoding="utf-8")
            self.assertIn("../maps/southamerica-countries.html", md, c["slug"])

    def test_output_does_not_depend_on_hash_seed(self):
        outs = set()
        for seed in ("0", "1", "2"):
            r = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, r'%s'); import build_sa_country_map as m; sys.stdout.buffer.write(m.build().encode('utf-8'))" % (REPO / "scripts")],
                               env=dict(os.environ, PYTHONHASHSEED=seed), capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
            outs.add(r.stdout)
        self.assertEqual(len(outs), 1)

    def test_check_is_current(self):
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "build_sa_country_map.py"), "--check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
