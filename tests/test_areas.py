"""地域別ページ（areas/）の生成・表・CSV リンク禁止・見え方に関する回帰テスト。"""
import csv
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import areas  # noqa: E402
import build  # noqa: E402

REGIONS = ("baguio", "africa", "capetown", "common")
# 保守者・AI向けのページ（データファイルへの言及を許す）
MAINTAINER_PAGES = {"AGENTS.md", "CLAUDE.md", "docs/04-dashboard.md", "docs/04-dashboard.html", "docs/05-public-data-policy.md",
                    "docs/05-public-data-policy.html", "docs/08-handoff.md", "docs/08-handoff.html", "docs/09-issue-map.md",
                    "docs/09-issue-map.html", "docs/07-export.md", "docs/07-export.html"}
CSV_LINK = re.compile(r"""(?:\]\(|href=["'])(?!https?:)[^)"']*(?:\.csv\b|data/[a-z_]+\.(?:md|html)|blob/[^)"']*\.csv)""")


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


class AreaPageTests(unittest.TestCase):
    def test_each_area_page_exists_with_expected_sections(self):
        for k in REGIONS:
            md, html = read(f"areas/{k}.md"), read(f"areas/{k}.html")
            for name in ("tasks", "cost", "docs"):
                self.assertIn(f"<!-- AUTO:{name} -->", md, k)
            self.assertIn("<table>", html)
            if k != "common":
                # 旅のしおり型の章立て：要点→やること→費用→住む場所→準備→調査メモ（資料・通貨・地図は調査メモの中）
                for h in ("旅の要点", "今日のやること", "費用の見積", "住む場所・町と地図", "出発前の準備", "調査メモ", "資料の一覧", "通貨と円換算"):
                    self.assertIn(h, md, f"{k}: {h}")
                self.assertLess(md.index("旅の要点"), md.index("今日のやること"), k)
                self.assertLess(md.index("費用の見積"), md.index("調査メモ"), k)

    def test_area_pages_have_sidebar_toc_and_open_key_sections(self):
        # 左の目次（サイドバー）があり、最初に開いている節は「旅の要点」「旅の流れ」だけ（最初の画面に入れる）
        import re
        for k in ("baguio", "africa", "capetown", "africa-aug"):
            html = read(f"areas/{k}.html")
            # 左に要点（pane-side）、右にタブ（pane）の1画面。タブは JS が無くても全節が縦に読める
            self.assertIn('class="doc tabbed"', html, k)
            self.assertIn('<aside class="pane-side">', html, k)
            self.assertIn('role="tablist"', html, k)
            # 最初のタブが開いていて、タブが2つ以上ある。左（pane-side）に「旅の要点」か「概要」がある
            self.assertRegex(html, r'role="tab"[^>]*aria-selected="true"', k)
            self.assertGreaterEqual(len(re.findall(r'role="tab"', html)), 3, k)
            side = html.split('<aside class="pane-side">')[1].split("</aside>")[0]
            self.assertTrue("旅の要点" in side or "概要" in side, k)

    def test_country_pages_tabs_in_reading_order(self):
        # 国別ページ：左に概要・ビザ・安全、右のタブは「旅程の目安」が先頭、その後に観光地・行き方・食べ物
        import re
        for k in ("kenya", "zambia", "madagascar", "rwanda"):
            html = read(f"countries/{k}.html")
            tabs = re.findall(r'role="tab"[^>]*>([^<]*)<', html)
            self.assertTrue(tabs[0].startswith("旅程の目安"), (k, tabs[:3]))
            self.assertLess([i for i, x in enumerate(tabs) if "主な観光地" in x][0], [i for i, x in enumerate(tabs) if "行き方" in x][0], k)
            side = html.split('<aside class="pane-side">')[1].split("</aside>")[0]
            for key in ("概要", "ビザ", "安全"):
                self.assertIn(key, side, f"{k}: {key}")

    def test_pages_without_toc_use_one_column(self):
        # ルート作成・日程プランナーは目次がなく、本文が1列で全幅になる（左の細い列に押し込まれない）
        for rel in ("docs/11-route-builder.html", "docs/13-day-planner.html"):
            html = read(rel)
            self.assertIn('class="doc no-toc"', html, rel)
            self.assertNotIn('<aside class="doc-toc">', html, rel)

    def test_cost_table_has_subtotal_and_caption(self):
        for k in ("baguio", "africa", "capetown"):
            md = read(f"areas/{k}.md")
            self.assertIn("小計", md)
            self.assertIn("公開価格表からの匿名の見積", md)

    def test_unpriced_is_never_zero_yen(self):
        S, rows, *_ = build.load_model()
        for r in rows:
            if r["unpriced"]:
                self.assertIn("未計上", areas.cost_block(rows, areas.PHASE_REGION[r["phase"]]))
        # 金額未入力の行（Issue #77/#80 の新5月案：マダガスカル国内線）は、全シナリオ「未計上」で ¥0 と書かない
        line = next(ln for ln in read("areas/africa.md").splitlines() if "マダガスカル国内線" in ln and ln.startswith("|"))
        self.assertEqual(line.count("未計上"), 3)
        self.assertNotIn("¥0 |", line)

    def test_subtotal_equals_sum_of_converted_rows_no_currency_mixing(self):
        S, rows, *_ = build.load_model()
        for k in ("baguio", "africa", "capetown", "common"):
            t = areas.region_totals(rows, k)
            for s in areas.SCEN:
                want = sum(r["est"][s] for r in rows if areas.PHASE_REGION[r["phase"]] == k and not r["no_amount"] and r["est"][s] is not None)
                self.assertAlmostEqual(t["all"][s] or 0.0, want, places=3)
        # 全地域の小計の合計はビルドの総計と一致（取りこぼし・二重計上なし）
        total = sum((areas.region_totals(rows, k)["all"]["std"] or 0) for k in REGIONS)
        self.assertAlmostEqual(total, S["total"]["std"], places=3)

    def test_every_expense_phase_maps_to_a_region(self):
        with (REPO / "data" / "expenses.csv").open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                self.assertIn(r["phase"], areas.PHASE_REGION, r["id"])

    def test_fx_currencies_per_area(self):
        self.assertIn("PHP", read("areas/baguio.md"))
        self.assertIn("USD", read("areas/baguio.md"))
        self.assertIn("ZAR", read("areas/capetown.md"))
        self.assertIn("ZAR", read("areas/africa.md"))

    def test_africa_map_links_only_when_files_exist(self):
        md = read("areas/africa.md")
        for name in ("world-map", "africa-map"):
            exists = (REPO / "maps" / f"{name}.html").exists()
            self.assertEqual(f"maps/{name}.html" in md, exists, name)

    def test_area_pages_are_in_pages_csv(self):
        with (REPO / "data" / "pages.csv").open(encoding="utf-8-sig", newline="") as f:
            paths = {r["path"] for r in csv.DictReader(f)}
        for k in REGIONS:
            self.assertIn(f"areas/{k}.html", paths)

    def test_tasks_all_have_region(self):
        with (REPO / "data" / "tasks.csv").open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                self.assertTrue(r["region"], r["id"])

    def test_places_have_maps_links_in_area_pages(self):
        for k in ("baguio", "africa", "capetown"):
            self.assertIn("https://www.google.com/maps/search/?api=1&query=", read(f"areas/{k}.md"))


class NoCsvForReadersTests(unittest.TestCase):
    def test_no_csv_links_in_reader_pages(self):
        bad = []
        for p in list(REPO.rglob("*.md")) + list(REPO.rglob("*.html")):
            rel = p.relative_to(REPO).as_posix()
            if rel in MAINTAINER_PAGES or rel.startswith((".claude/", "exports/", ".git/")):
                continue
            text = p.read_text(encoding="utf-8")
            if CSV_LINK.search(text):
                bad.append(rel)
        self.assertEqual(bad, [])

    def test_no_csv_view_wording_or_nav_group(self):
        for p in list(REPO.rglob("*.html")):
            rel = p.relative_to(REPO).as_posix()
            if rel.startswith((".claude/", "exports/")) or rel in MAINTAINER_PAGES:
                continue
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("データ（CSV）", text, rel)
            self.assertNotIn("CSV の表示", text, rel)

    def test_no_csv_view_pages_exist(self):
        self.assertEqual(sorted(p.name for p in (REPO / "data").glob("*.html")), [])
        self.assertEqual(sorted(p.name for p in (REPO / "data").glob("*.md")), [])


class LayoutTemplateTests(unittest.TestCase):
    def test_template_tokens_and_readability(self):
        import build_html
        css = build_html.BASE_CSS
        self.assertIn(':root:not([data-theme="light"])', css)
        self.assertIn(':root[data-theme="dark"]', css)
        self.assertRegex(css, r"font-size:calc\(16px \* var\(--fs,1\)\)")  # 文字サイズは倍率(--fs)で変えられる
        self.assertRegex(css, r"font:1rem/1\.\d+")
        self.assertIn("tabular-nums", css)
        self.assertIn("72ch", css)
        self.assertRegex(css, r"th\{position:sticky")
        for bad in ("gradient", "border-left", "border-inline-start"):
            self.assertNotIn(bad, css)

    def test_generated_pages_share_template(self):
        for rel in ("index.html", "areas/baguio.html", "research/sources.html", "docs/02-budget.html", "blog/article-ideas.html"):
            text = read(rel)
            self.assertIn('class="bar"', text, rel)
            self.assertIn("<style>", text)

    def test_index_docs_are_grouped_cards_not_one_wide_table(self):
        # 資料一覧は分野ごとのカード（62行の1枚表をやめた）。表が残る場合だけ列幅を指定する
        index = read("index.html")
        self.assertIn('class="grid docs-grid"', index)
        if "<table>" in index:
            self.assertIn("<colgroup>", index)


if __name__ == "__main__":
    unittest.main()
