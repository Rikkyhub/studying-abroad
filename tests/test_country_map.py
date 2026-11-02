"""アフリカ国別地図（maps/africa-countries.html）と国別ページの整合・決定性のテスト。"""
import csv
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_country_map as cm  # noqa: E402

PAGE = REPO / "maps" / "africa-countries.html"
REQUIRED = ["概要", "主な観光地", "おすすめの食べ物", "ビザ・入国（日本国籍）", "安全・健康", "行き方・移動", "未確認事項", "出典一覧", "調査ログ"]


def countries():
    with (REPO / "data" / "countries.csv").open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


class CountryPageTests(unittest.TestCase):
    def test_every_country_has_a_page_with_required_sections(self):
        for c in countries():
            md = REPO / "countries" / f"{c['slug']}.md"
            self.assertTrue(md.is_file(), c["slug"])
            heads = re.findall(r"^## (.+)$", md.read_text(encoding="utf-8"), re.M)
            for need in REQUIRED:
                self.assertTrue(any(h.startswith(need) for h in heads), f"{c['slug']}: {need}")

    def test_iso_numeric_ids_exist_in_geo_data(self):
        ids = {g["id"] for g in cm.bm.load_topo("countries-50m.json")}
        for c in countries():
            self.assertIn(c["iso_numeric"], ids, c["slug"])

    def test_groups_and_short_names_valid(self):
        for c in countries():
            self.assertIn(c["group"], cm.GROUP_NAMES, c["slug"])
            self.assertTrue(c["short"], c["slug"])

    def test_pages_have_no_personal_identifiers(self):
        pat = re.compile(r"[A-Z]{1,2}\d{7}\b|予約番号|パスポート番号|[\w.+-]+@[\w-]+\.[\w.]+")
        for c in countries():
            text = (REPO / "countries" / f"{c['slug']}.md").read_text(encoding="utf-8")
            self.assertIsNone(pat.search(text), c["slug"])


class MapPageTests(unittest.TestCase):
    def test_every_country_with_a_page_is_a_link(self):
        t = PAGE.read_text(encoding="utf-8")
        for c in countries():
            self.assertIn(f'href="../countries/{c["slug"]}.html"', t, c["slug"])

    def test_all_link_targets_exist(self):
        t = PAGE.read_text(encoding="utf-8")
        for href in re.findall(r'href="\.\./countries/([a-z-]+)\.html"', t):
            self.assertTrue((REPO / "countries" / f"{href}.html").is_file(), href)

    def test_no_network_or_external_resources(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertNotRegex(t, r"fetch\(|XMLHttpRequest|<script[^>]*\ssrc=|<link[^>]*rel=[\"']?stylesheet|@import|<img|WebSocket|sendBeacon")
        for url in re.findall(r"https?://[^\s\"'<>)]+", t):
            self.assertTrue(url.startswith(("https://www.naturalearthdata.com/", "https://github.com/topojson/world-atlas")), url)

    def test_keyboard_and_screen_reader_access(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertIn('role="group"', t)
        self.assertEqual(len(re.findall(r'<a class="cn[^"]*" href=', t)), len(countries()))
        self.assertIn("aria-label", t)

    def test_output_does_not_depend_on_hash_seed(self):
        """set の反復順など、実行ごとに変わる要素が出力に入っていないこと（CIとローカルで差が出る原因になる）"""
        outs = set()
        for seed in ("0", "1", "2", "3"):
            r = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, r'%s'); import build_country_map as m; sys.stdout.buffer.write(m.build().encode('utf-8'))" % (REPO / "scripts")],
                               env=dict(os.environ, PYTHONHASHSEED=seed), capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
            outs.add(r.stdout)
        self.assertEqual(len(outs), 1)

    def test_check_is_current(self):
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "build_country_map.py"), "--check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
