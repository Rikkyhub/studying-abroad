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
        self.assertIn('<td class="n" data-label="b">2</td>', body)  # data-label は携帯幅のカード表示で列名を出すため

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
        for k in ("baguio", "africa", "africa-aug", "capetown", "common"):
            self.assertIn(f'href="areas/{k}.html"', self.index)
        import re
        self.assertLessEqual(len(re.findall(r"<table>", self.index)), 3)  # 地域・通貨・資料
        self.assertLess(len(self.index), 66000)  # 全ページ一覧（国別・8月ページ）の増加に合わせて調整（#58）。カルーセル・折りたたみ用のCSS/JS分を加味。トップは / で開くため軽さを保つ

    def test_tables_have_headers(self):
        import re
        for t in re.findall(r"<table>.*?</table>", self.index, re.S):
            self.assertIn("<thead><tr><th", t)

    def test_top_page_sections_in_order(self):
        import re
        heads = re.findall(r"<h2 id=\"[^\"]+\">(.*?)</h2>", self.index)
        # 旅の路線（時間順の駅）は h2 ではなく kicker の見出しで、予算の前に置く。旅程と地域別の重複は路線に統合した
        self.assertEqual(heads, ["予算の全体像", "いま何をするか（詳しく）", "通貨と円換算", "資料一覧"])
        # 4つの区間の比較（横並び）が、最初の h2（予算）より前にある＝最初の画面に入る
        self.assertLess(self.index.index('class="region-compare"'), self.index.index('<h2 id="budget">'))

    def test_budget_cards_are_model_and_never_zero_for_unpriced(self):
        import re
        sec = self.index.split('<h2 id="budget">')[1].split("<h2 id=")[0]
        # 8月は金額なしで「未計上」と出る
        for label in ("目標総予算", "上限予算", "見積合計（標準）", "フィリピン（バギオ）", "アフリカ周遊（5月）",
                      "南アフリカ（ケープタウン）", "アフリカ周遊（8月）", "飛行機代"):
            self.assertIn(label, sec)
        self.assertIn("モデル", sec)
        self.assertIn("実費ではありません", sec)
        self.assertIn("未計上", sec)
        self.assertNotIn("¥0", sec)
        self.assertNotIn("0円</", sec)

    def test_timeline_cards_one_per_period_with_area_link(self):
        import csv
        import re
        sec = self.index.split('id="plan"')[1].split('<h2 id="budget">')[0]
        import re as _re
        with (ROOT / "data" / "timeline.csv").open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        # 各期間が1つの列（a.region-col）で、地域ページへのリンクになっている
        self.assertEqual(len(re.findall(r'<a class="region-col [^"]*" href="areas/', sec)), len(rows))
        for r in rows:
            self.assertIn(r["period"], sec)
        self.assertIn("モデル", sec)

    def test_first_screen_has_compare_and_budget_strip(self):
        import re
        head = self.index.split('<h2 id="budget">')[0]
        hero = re.search(r'<section class="hero-a">(.*?)</section>', head, re.S).group(1)
        self.assertLess(len(re.sub(r"<[^>]+>", "", hero)), 200)  # ヒーローは短く（最初の画面に比較が入る）
        self.assertEqual(len(re.findall(r'class="region-col ', head)), 4)
        self.assertIn('class="strip"', head)  # 予算の1行の帯
        for col in re.findall(r'<a class="region-col .*?</a>', head, re.S):
            self.assertIn("いまやること", col)
            self.assertRegex(col, r"¥[\d,]+|未計上")

    def test_currency_cards(self):
        sec = self.index.split('<h2 id="fx">')[1].split("<h2 id=")[0]
        for c in ("PHP", "ZAR", "USD"):
            self.assertIn(f"（{c}）", sec)
        self.assertIn("1万円＝", sec)
        self.assertIn('id="fx-calc"', sec)

    def test_link_cards_do_not_nest_links(self):
        import re
        for m in re.findall(r'<a class="(?:card link[^"]*|region-col [^"]*)".*?</a>', self.index, re.S):
            self.assertEqual(m.count("<a "), 1, m[:80])

    def test_floating_card_css(self):
        import re
        style = re.search(r"<style>(.*?)</style>", self.index, re.S).group(1)
        self.assertNotIn("border-left", style)
        self.assertNotIn("border-left", self.index)
        self.assertNotIn("gradient", style)
        self.assertRegex(style, r"transition:transform \.\d+s ease,box-shadow \.\d+s ease")
        self.assertRegex(style, r"@media \(hover:hover\)\{\.card:hover\{transform:translateY\(-\d+px\);box-shadow:var\(--shadow-up\)")
        self.assertRegex(style, r"--shadow:0 10px 30px rgba\(0,0,0,\.\d+\)")
        self.assertRegex(style, r"@media \(prefers-reduced-motion:reduce\)\{\.card\{transition:none\}\.card:hover\{transform:none\}\}")
        self.assertIn("a.card:focus-visible", style)
        self.assertRegex(style, r"gap:2[4-9]px|gap:[3-9]\d px|gap:2[4-9]px")
        self.assertIn("minmax(240px,1fr)", style)

    def test_no_csv_links_on_top_page(self):
        import re
        self.assertNotRegex(self.index, r"""(href|src)=["'][^"']*\.csv""")

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


class NavTests(unittest.TestCase):
    """全ページ共通の上部ナビ：ホーム・地域4つ・費用が横並びで、ほかの入口は「ほか」から開く"""

    MAIN = ("ホーム", "バギオ", "アフリカ5月", "ケープタウン", "アフリカ8月", "費用")

    def test_main_links_on_every_kind_of_page(self):
        for rel in ("index.html", "areas/africa.html", "countries/kenya.html", "research/sources.html",
                    "docs/02-budget.html", "maps/route-map.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            nav = text.split('<nav class="menu"')[1].split("</nav>")[0]
            for label in self.MAIN:
                self.assertIn(f">{label}</a>", nav, f"{rel}: {label}")
            self.assertIn("<summary>ほか</summary>", nav, rel)

    def test_current_page_is_marked(self):
        text = (ROOT / "areas/capetown.html").read_text(encoding="utf-8")
        nav = text.split('<nav class="menu"')[1].split("</nav>")[0]
        self.assertRegex(nav, r'href="[^"]*areas/capetown\.html" aria-current="page">ケープタウン</a>')

    def test_more_menu_reaches_every_group(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        more = text.split('<details class="more-nav')[1].split("</details>")[0]
        for label in ("国別ページ（アフリカ）", "現地調査・比較の資料", "Q&amp;A（確認待ち）", "世界地図", "ルート地図", "ルート作成", "日程プランナー", "全ページ一覧"):
            self.assertIn(label, more, label)


class FontSizeAndHomeMapTests(unittest.TestCase):
    """文字サイズのボタン（小・中・大）と、トップの中心に置くルート地図"""

    def test_font_size_buttons_on_every_page_kind(self):
        for rel in ("index.html", "areas/africa.html", "countries/kenya.html", "docs/02-budget.html",
                    "maps/route-map.html", "maps/world-map.html", "maps/africa-countries.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            for v in ("0.9", "1", "1.15"):
                self.assertIn(f'data-fs="{v}"', text, f"{rel}: {v}")
            self.assertIn('var K="site-fs"', text, rel)  # 保存・復元（localStorage は try/catch の中）
            self.assertIn("try{", text.split('var K="site-fs"')[1][:600], rel)

    def test_home_has_route_map_before_budget(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        i_map = text.index('class="home-map"')
        self.assertLess(i_map, text.index('<h2 id="budget">'))
        self.assertEqual(text.count('class="m"'), 1)  # 地図のSVGは1つ（5月の案G）
        self.assertIn('href="maps/route-map.html"', text)
        self.assertEqual(text.count('class="mini '), 4)  # 区間カードは4つ（地図の左右に2つずつ）


if __name__ == "__main__":
    unittest.main()
