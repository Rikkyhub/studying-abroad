"""Regression checks for the Markdown -> HTML page generator."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_html import ROOT, convert, inline, outputs


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

    def test_csv_has_no_reader_pages(self):
        """CSV の閲覧用ページ（data/*.html|md）は作らない"""
        for p in outputs():
            self.assertNotEqual(p.parent.name, "data", p)


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_index_matches_generated(self):
        self.assertEqual(self.index, outputs()[ROOT / "index.html"])

    def test_index_is_short_and_links_every_area(self):
        for k in ("baguio", "africa", "capetown", "common"):
            self.assertIn(f'href="areas/{k}.html"', self.index)
        import re
        self.assertLessEqual(len(re.findall(r"<table>", self.index)), 3)  # 地域・通貨・資料
        self.assertLess(len(self.index), 30000)

    def test_tables_have_headers_and_no_cards(self):
        import re
        for t in re.findall(r"<table>.*?</table>", self.index, re.S):
            self.assertIn("<thead><tr><th", t)
        self.assertNotIn('class="card"', self.index)

    def test_all_pages_csv_non_ops_pages_listed(self):
        import csv
        with (ROOT / "data" / "pages.csv").open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            self.assertTrue((ROOT / r["path"]).is_file(), r["path"])
            if r["area"] not in ("地域別", "運用"):
                self.assertIn(f'href="{r["path"]}"', self.index)

    def test_no_issue_links_in_dashboard_tables(self):
        self.assertNotIn("/issues/", self.index.split("<footer>")[0])
        self.assertIn("docs/09-issue-map.html", self.index)

    def test_fx_json_matches_csv(self):
        import csv, json, re
        with (ROOT / "data" / "fx.csv").open(newline="", encoding="utf-8-sig") as f:
            fx = list(csv.DictReader(f))
        m = re.search(r'<script type="application/json" id="fx-data">(.*?)</script>', self.index, re.S)
        data = json.loads(m.group(1))
        self.assertEqual([d["code"] for d in data], [r["currency"] for r in fx])
        for d, r in zip(data, fx):
            self.assertEqual(d["rate"], float(r["jpy_per_unit"]) if r["jpy_per_unit"] else None)

    def test_unknown_rate_shows_unconfirmed(self):
        import tempfile
        from build_html import fx_summary
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "data").mkdir()
            (root / "data" / "fx.csv").write_text(
                "currency,name_ja,unit,region,jpy_per_unit,rate_date,rate_kind,source\nBWP,プラ,P,ボツワナ,,,,\n",
                encoding="utf-8")
            self.assertIn("未確認", fx_summary(root))


if __name__ == "__main__":
    unittest.main()
