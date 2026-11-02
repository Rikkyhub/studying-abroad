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
                for h in ("費用の見積", "資料", "場所と地図", "通貨と円換算"):
                    self.assertIn(h, md, f"{k}: {h}")

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
        # AF-05: 標準・余裕は未計上のまま。行の標準・余裕の円セルが「未計上」
        md = read("areas/africa.md")
        line = next(ln for ln in md.splitlines() if ln.startswith("| ソドワナ"))
        cells = [c.strip() for c in line.strip("|").split("|")]
        self.assertEqual(cells[-2:], ["未計上", "未計上"])
        self.assertNotRegex(cells[-3], r"^¥0$")
        # 金額未入力の行は全シナリオ「未計上」
        line = next(ln for ln in read("areas/africa.md").splitlines() if "ツアー外の食費" in ln and ln.startswith("|"))
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
        self.assertRegex(css, r"font:16px/1\.8")
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

    def test_wide_tables_have_column_widths_on_index(self):
        self.assertIn("<colgroup>", read("index.html"))


if __name__ == "__main__":
    unittest.main()
