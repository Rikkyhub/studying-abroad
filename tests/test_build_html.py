"""Regression checks for the Markdown -> HTML page generator."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_html import INTERNAL_CSV, ROOT, convert, csv_to_markdown, inline, outputs


class InlineTests(unittest.TestCase):
    def test_escapes_html(self):
        self.assertEqual(inline("<script>"), "&lt;script&gt;")

    def test_bold_code_and_links(self):
        out = inline("**注意** `paid` [出典](https://example.com/a)")
        self.assertIn("<strong>注意</strong>", out)
        self.assertIn("<code>paid</code>", out)
        self.assertIn('href="https://example.com/a" target="_blank" rel="noopener"', out)

    def test_repo_md_link_points_to_html(self):
        self.assertIn('href="sources.html"', inline("[出典](sources.md)"))
        self.assertIn('href="../data/expenses.csv"', inline("[CSV](../data/expenses.csv)"))

    def test_bare_url_linked(self):
        self.assertIn('<a href="https://immigration.gov.ph/x"', inline("https://immigration.gov.ph/x"))


class BlockTests(unittest.TestCase):
    def test_table_and_heading(self):
        title, body, toc = convert("# 題\n\n## 表\n\n| a | b |\n|---|---:|\n| 1 | 2 |\n")
        self.assertEqual(title, "題")
        self.assertEqual(toc[0][2], "表")
        self.assertIn('<td class="n">2</td>', body)

    def test_nested_list_and_checkbox(self):
        _, body, _ = convert("- 親\n  - 子\n- [x] 済\n")
        self.assertIn("<ul><li>親<ul><li>子</li></ul></li><li>", body)
        self.assertIn('class="check done"', body)

    def test_comments_removed(self):
        _, body, _ = convert("<!-- AUTO:x -->\n本文\n")
        self.assertNotIn("AUTO", body)


class CsvViewTests(unittest.TestCase):
    def test_csv_becomes_table_without_breaking_on_pipes_or_newlines(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "data").mkdir()
            (root / "data" / "x.csv").write_text('a,b\n"1|2","line1\nline2"\n3\n', encoding="utf-8")
            md = csv_to_markdown(root / "data" / "x.csv", root)
        self.assertIn("| a | b |", md)
        self.assertIn("| 1／2 | line1 line2 |", md)
        self.assertIn("| 3 |  |", md)

    def test_every_csv_has_md_and_html_view(self):
        out = outputs()
        for csv_path in (ROOT / "data").glob("*.csv"):
            if csv_path.name in INTERNAL_CSV:  # 地図の入力データは閲覧ページを作らない
                self.assertNotIn(csv_path.with_suffix(".html"), out)
                continue
            self.assertIn(csv_path.with_suffix(".md"), out)
            self.assertIn(csv_path.with_suffix(".html"), out)


class RepoTests(unittest.TestCase):
    def test_generated_pages_are_current(self):
        for path, text in outputs().items():
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.exists(), "run python3 scripts/build_html.py")
                self.assertEqual(path.read_text(encoding="utf-8"), text, "run python3 scripts/build_html.py")

    def test_no_raw_markdown_left(self):
        for path, text in outputs().items():
            with self.subTest(path=path.name):
                self.assertNotIn("**", text)
                self.assertNotIn("\x00", text)


class IndexTableTests(unittest.TestCase):
    def setUp(self):
        self.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_index_matches_generated(self):
        self.assertEqual(self.index, outputs()[ROOT / "index.html"])

    def test_every_pages_csv_path_exists_and_is_linked(self):
        import csv
        with (ROOT / "data" / "pages.csv").open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(rows)
        for r in rows:
            with self.subTest(id=r["id"]):
                self.assertTrue((ROOT / r["path"]).is_file())
                self.assertIn(f'href="{r["path"]}"', self.index)

    def test_tables_have_headers_and_no_cards(self):
        import re
        tables = re.findall(r"<table>.*?</table>", self.index, re.S)
        self.assertGreaterEqual(len(tables), 5)
        for t in tables:
            self.assertIn("<thead><tr><th", t)
        self.assertNotIn('class="card"', self.index)
        self.assertNotIn('class="links"', self.index)


class DashboardDataTests(unittest.TestCase):
    def setUp(self):
        import csv
        self.index = (ROOT / "index.html").read_text(encoding="utf-8")
        def rd(n):
            with (ROOT / "data" / n).open(newline="", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f))
        self.pages, self.places, self.fx = rd("pages.csv"), rd("places.csv"), rd("fx.csv")

    def test_refs_are_http_urls_and_rendered(self):
        import re
        for r in self.pages:
            for u in filter(None, r["refs"].split(";")):
                with self.subTest(id=r["id"], url=u):
                    self.assertRegex(u, r"^https?://[^\s;]+$")
                    self.assertIn(f'href="{u.replace("&", "&amp;")}"', self.index)

    def test_no_issue_links_in_dashboard_tables(self):
        self.assertNotIn("関連Issue", self.index)
        self.assertNotIn("/issues/", self.index.split("<footer>")[0])
        self.assertIn("docs/09-issue-map.html", self.index)
        self.assertTrue((ROOT / "docs" / "09-issue-map.html").exists())

    def test_map_links_well_formed(self):
        import re
        import html as _h
        urls = [_h.unescape(u) for u in re.findall(r'href="(https://www\.google\.com/maps/search/[^"]*)"', self.index)]
        self.assertGreaterEqual(len(urls), len(self.places))
        for r in self.places:
            self.assertTrue(r["maps_query"].strip())
            from build_html import maps_url
            self.assertIn(maps_url(r["maps_query"]), urls)
        for u in urls:
            self.assertRegex(u, r"^https://www\.google\.com/maps/search/\?api=1&query=[A-Za-z0-9%+_.~-]+$")

    def test_fx_json_matches_csv_and_unknown_shows_unconfirmed(self):
        import json, re
        m = re.search(r'<script type="application/json" id="fx-data">(.*?)</script>', self.index, re.S)
        data = json.loads(m.group(1))
        self.assertEqual([d["code"] for d in data], [r["currency"] for r in self.fx])
        for d, r in zip(data, self.fx):
            self.assertEqual(d["rate"], float(r["jpy_per_unit"]) if r["jpy_per_unit"] else None)
            self.assertRegex(r["currency"], r"^[A-Z]{3}$")
        from build_html import fx_table
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "data").mkdir()
            (root / "data" / "fx.csv").write_text(
                "currency,name_ja,unit,region,jpy_per_unit,rate_date,rate_kind,source\nBWP,プラ,P,ボツワナ,,,,\n",
                encoding="utf-8")
            self.assertIn("未確認", fx_table(root))


if __name__ == "__main__":
    unittest.main()
