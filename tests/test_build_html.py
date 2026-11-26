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
        self.assertLess(len(self.index), 105000)  # 8月の地域別メニュー追加で100,128文字。5%弱の余裕を認めつつトップの肥大化を監視する

    def test_tables_have_headers(self):
        import re
        for t in re.findall(r"<table>.*?</table>", self.index, re.S):
            self.assertIn("<thead><tr><th", t)

    def test_top_page_sections_in_order(self):
        import re
        heads = re.findall(r"<h2 id=\"[^\"]+\">(.*?)</h2>", self.index)
        # 旅の路線（時間順の駅）は h2 ではなく kicker の見出しで、予算の前に置く。旅程と地域別の重複は路線に統合した
        self.assertEqual(heads, ["予算の全体像", "いま何をするか（詳しく）", "通貨と円換算", "資料一覧"])
        # 地図と4つの区間のカードが、最初の h2（予算）より前にある＝最初の画面に入る
        self.assertLess(self.index.index('class="home-map"'), self.index.index('<h2 id="budget">'))

    def test_budget_overview_uses_the_shared_period_by_kind_table(self):
        import re
        sec = self.index.split('<h2 id="budget">')[1].split("<h2 id=")[0]
        # 行＝時期、列＝費目の1枚の表（費用ページの概要と同じ分け方）
        for label in ("時期", "航空券・長距離移動", "宿泊", "食費・日用品", "現地交通", "観光・ツアー", "授業料・ビザ", "保険・医療・通信", "合計",
                      "2〜4月 バギオ", "5月 アフリカ周遊", "6〜7月 ケープタウン", "8月 周遊"):
            self.assertIn(label, sec, label)
        self.assertIn("モデル", sec)
        self.assertIn("実費ではありません", sec)
        self.assertNotIn("¥0", sec)
        self.assertNotIn("0円</", sec)

    def test_overview_rows_and_columns_add_up_to_the_same_total(self):
        import re
        sec = self.index.split('<h2 id="budget">')[1].split("<h2 id=")[0]
        rows = re.findall(r"<tr>(.*?)</tr>", sec.split("<tbody>")[1], re.S)
        nums = [[int(x.replace(",", "")) for x in re.findall(r"¥([\d,]+)", r)] for r in rows]
        grand = nums[-1][-1]
        self.assertEqual(sum(r[-1] for r in nums[:-1]), grand)  # 行（時期）の合計＝全体
        self.assertEqual(sum(nums[-1][:-1]), grand)  # 列（費目）の合計＝全体

    def test_budget_page_starts_with_the_same_overview(self):
        text = (ROOT / "docs" / "02-budget.html").read_text(encoding="utf-8")
        body = text.split("<article")[1]
        top = body.split("内訳を切り替えて見る</h2>")[0]
        self.assertIn("費用の概要", top)
        for label in ("航空券・長距離移動", "授業料・ビザ", "2〜4月 バギオ", "8月 周遊"):
            self.assertIn(label, top, label)

    def test_area_pages_use_the_shared_cost_kinds(self):
        for k in ("baguio", "africa", "capetown", "southamerica-aug"):
            md = (ROOT / "areas" / f"{k}.md").read_text(encoding="utf-8")
            self.assertIn("ホーム以外のすべてのページと同じ、7つの費目の分け方", md, k)
            self.assertNotIn("交通費（飛行機以外）", md, k)  # 古い6区分の名前

    def test_timeline_cards_one_per_period_with_area_link(self):
        import csv
        import re
        sec = self.index.split('id="plan"')[1].split('<h2 id="budget">')[0]
        import re as _re
        with (ROOT / "data" / "timeline.csv").open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        # 各期間が1つのカード（a.mini）で、地域ページへのリンクになっている
        self.assertEqual(len(re.findall(r'<a class="seg [^"]*" href="areas/', sec)), len(rows))
        for r in rows:
            self.assertIn(r["period"], sec)
        self.assertIn("モデル", sec)

    def test_first_screen_has_compare_and_budget_strip(self):
        import re
        head = self.index.split('<h2 id="budget">')[0]
        top = re.search(r'<div class="home-top">(.*?)</div>', head, re.S).group(1)
        self.assertLess(len(re.sub(r"<[^>]+>", "", top)), 200)  # 見出し行は短く（最初の画面に地図と旅の流れが入る）
        self.assertIn('class="home-body"', head)  # 左=地図、右=旅の流れ・予算・やること の2領域
        self.assertIn('class="home-map"', head)  # 左：ルート地図
        self.assertEqual(len(re.findall(r'<a class="seg ', head)), 4)  # 右：旅の流れ（時間順の4区間）
        self.assertIn('class="strip"', head)  # 右下：いま何をするか（費用の金額は出さない）
        # ホームの最初の画面には、費用の金額を出さない（費用ページの概要を見る）
        first_screen = re.sub(r"<svg.*?</svg>", "", head, flags=re.S)
        self.assertNotRegex(first_screen, r"¥[\d,]{4,}")
        self.assertIn('href="docs/02-budget.html"', head)  # 費用ページへの入口は残す

    def test_currency_cards(self):
        sec = self.index.split('<h2 id="fx">')[1].split("<h2 id=")[0]
        for c in ("PHP", "ZAR", "USD"):
            self.assertIn(f"（{c}）", sec)
        self.assertIn("1万円＝", sec)
        self.assertIn('id="fx-calc"', sec)

    def test_link_cards_do_not_nest_links(self):
        import re
        for m in re.findall(r'<a class="(?:card link[^"]*|seg [^"]*)".*?</a>', self.index, re.S):
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

    MAIN = ("ホーム", "バギオ", "アフリカ5月", "ケープタウン", "アフリカ", "南米", "費用")  # アフリカ・南米は「8月」の開閉メニューの中

    def test_main_links_on_every_kind_of_page(self):
        for rel in ("index.html", "areas/africa.html", "countries/kenya.html", "research/sources.html",
                    "docs/02-budget.html", "maps/route-map.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            nav = text.split('<nav class="menu"')[1].split("</nav>")[0]
            for label in self.MAIN:
                self.assertIn(f">{label}</a>", nav, f"{rel}: {label}")
            for menu in ("8月", "国別", "地図", "ツール", "資料"):
                self.assertIn(f"<summary>{menu}</summary>", nav, rel)

    def test_current_page_is_marked(self):
        text = (ROOT / "areas/capetown.html").read_text(encoding="utf-8")
        nav = text.split('<nav class="menu"')[1].split("</nav>")[0]
        self.assertRegex(nav, r'href="[^"]*areas/capetown\.html" aria-current="page">ケープタウン</a>')

    def test_menus_reach_every_country_and_tool(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = text.split('<nav class="menu"')[1].split("</nav>")[0]
        for label in ("南アフリカ", "ケニア", "ルワンダ", "アフリカ各国の比較", "Q&amp;A（確認待ち）", "世界地図", "ルート地図",
                      "ルート作成", "日程プランナー", "全ページ一覧"):
            self.assertIn(label, nav, label)
        self.assertNotIn("<summary>ほか</summary>", nav)


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
        self.assertEqual(text.count('class="seg '), 4)  # 右に旅の流れ（区間4つ）


class AuditFixTests(unittest.TestCase):
    """Playwright の点検で見つかった不具合の再発防止。"""

    def test_route_builder_does_not_call_planner_only_function(self):
        import build_html
        self.assertNotIn("paintCmp", build_html.ROUTE_SCRIPT)

    def test_mobile_header_wraps_menu_and_tables_scroll(self):
        from site_css import COMPONENTS
        self.assertIn("@media(max-width:600px)", COMPONENTS)
        self.assertIn("nav.menu{order:3;flex:1 1 100%", COMPONENTS)
        self.assertIn(".scroll{overflow-x:auto;border:0", COMPONENTS)
        self.assertNotIn(".scroll{overflow-x:visible", COMPONENTS)

    def test_home_legend_lists_only_drawn_line_types(self):
        import re
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        legend = re.search(r'<span class="legend">(.*?)</span>', text).group(1)
        for k in re.findall(r'<i class="tr (\w+)"></i>', legend):
            self.assertIn(f'class="ln tr {k}"', text)

    def test_home_map_shows_trip_to_and_from_japan(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        svg = text.split('<figure class="home-map">')[1].split("</figure>")[0]
        for word in ("東京", "マニラ・バギオ", "モーリシャス", "ケープタウン", "2月 行き", "5/4 日本発", "帰国"):
            self.assertIn(word, svg, word)

    def test_country_map_puts_list_beside_map(self):
        text = (ROOT / "maps" / "africa-countries.html").read_text(encoding="utf-8")
        self.assertIn('<div class="cm-grid">', text)
        self.assertLess(text.index('class="mapbox"'), text.index('class="cm-right"'))

    def test_country_tabs_use_short_labels_and_side_starts_with_summary(self):
        import re
        text = (ROOT / "countries" / "namibia.html").read_text(encoding="utf-8")
        labels = re.findall(r'role="tab"[^>]*>([^<]*)<', text)
        self.assertIn("旅程の目安", labels)
        self.assertFalse(any("）（" in x for x in labels))
        side = re.search(r'<aside class="pane-side">(.*?)</aside>', text, re.S).group(1)
        self.assertLess(side.index("概要"), side.index("side-meta"))

    def test_app_page_links_back_home(self):
        self.assertIn('href="index.html"', (ROOT / "app.html").read_text(encoding="utf-8"))

    def test_reader_pages_do_not_mention_issue_numbers(self):
        import re
        keep = {"docs/05-public-data-policy.html", "docs/07-export.html", "docs/08-handoff.html", "docs/09-issue-map.html"}
        for p in [ROOT / "index.html", ROOT / "app.html", *ROOT.glob("areas/*.html"), *ROOT.glob("countries/*.html"),
                  *ROOT.glob("maps/*.html"), *ROOT.glob("research/*.html"), *ROOT.glob("docs/*.html")]:
            rel = p.relative_to(ROOT).as_posix()
            if rel in keep:
                continue
            self.assertIsNone(re.search(r"Issue\s*#\d", p.read_text(encoding="utf-8")), rel)

    def test_reader_clean_keeps_js_parentheses(self):
        from build_html import reader_clean
        self.assertEqual(reader_clean("function(){a()}"), "function(){a()}")
        self.assertEqual(reader_clean("比較（Issue #137）です"), "比較です")
        self.assertEqual(reader_clean("資料（2026-10-26閲覧、Issue #66）"), "資料（2026-10-26閲覧）")


class TripDesignerTests(unittest.TestCase):
    """旅のデザイナー（docs/14-trip-designer.html）：ブラウザの中だけで動く入力画面"""

    def setUp(self):
        self.text = (ROOT / "docs" / "14-trip-designer.html").read_text(encoding="utf-8")

    def test_page_has_map_calendar_inputs_and_presets(self):
        for key in ('data-designer', 'id="dz-svg"', 'id="dz-preset"', 'id="dz-start"', 'id="dz-undo"', 'id="dz-zoom"'):
            self.assertIn(key, self.text, key)
        for pid in ("SA8-6", "SA8-5"):
            self.assertIn(f'"id":"{pid}"', self.text, pid)

    def test_input_stays_in_the_browser_only(self):
        # 入力は localStorage だけ。外部への送信（fetch・XMLHttpRequest・sendBeacon）は使わない
        self.assertIn("localStorage", self.text)
        for bad in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket"):
            self.assertNotIn(bad, self.text, bad)

    def test_designer_is_in_the_tools_menu(self):
        nav = (ROOT / "index.html").read_text(encoding="utf-8").split('<nav class="menu"')[1].split("</nav>")[0]
        self.assertIn("旅のデザイナー", nav)

    def test_sa8_6_nights_end_on_aug_22(self):
        import re, datetime as dt
        m = re.search(r'\{"id":"SA8-6".*?"stops":(\[\[.*?\]\])\}', self.text, re.S)
        import json
        stops = json.loads(m.group(1))
        end = dt.date(2027, 8, 1) + dt.timedelta(days=sum(int(x[1]) for x in stops))
        self.assertEqual(end, dt.date(2027, 8, 22))


if __name__ == "__main__":
    unittest.main()
