"""サイト全体の整合性テスト: 生成物の冪等性、公開ページの語句監査、ページ一覧・ナビ・日付粒度。"""
import csv
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

# 個人の支払い・資産を連想させる語。説明文（否定・方針の説明）の中だけに現れてよい
FORBIDDEN = re.compile(r"paid_jpy|actual|evidence|預貯金|残高|70万|700,?000|支払済み|支払い済み|本人申告|賞与")
# 説明文とみなす言い回し。この語を含む段落・セルだけ許可する
EXPLANATORY = ("ではありません", "ではない", "しません", "含めません", "みなさ", "ありません", "禁止", "作らない", "置かない",
               "書かない", "載せない", "非公開", "Notion", "公開しない", "入れない", "出さない", "扱わない", "含まれません",
               "事故", "残高証明")  # 残高証明＝南ア入国・就学ビザの一般的な必要書類（公式の要件の説明）


def visible_lines(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S)
    # ブロック要素の境界でだけ分け、インライン要素（code・strong・a）は同じ行にまとめる
    text = re.sub(r"</?(p|li|td|th|tr|h[1-6]|div|ul|ol|table|blockquote|pre|footer|article|aside|nav|details|summary|br)\b[^>]*>", "\n", text)
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", ln)).strip() for ln in text.split("\n") if ln.strip()]


def pages():
    out = [REPO / "index.html"]
    for d in ("areas", "docs", "research", "blog"):
        out += sorted((REPO / d).glob("*.html"))
    return out


class GeneratedFilesTests(unittest.TestCase):
    def test_build_all_twice_has_no_diff(self):
        """build.py と build_html.py が同じファイルを別の内容で書き換えない（2回実行しても差分なし）"""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "repo"
            shutil.copytree(REPO, work, ignore=shutil.ignore_patterns(".git", "__pycache__", ".claude", "exports"))

            def snapshot():
                return {p.relative_to(work).as_posix(): p.read_bytes() for p in work.rglob("*") if p.is_file() and "__pycache__" not in p.parts}

            def run(*args):
                return subprocess.run([sys.executable, str(work / "scripts" / "build_all.py"), *args], cwd=work,
                                      capture_output=True, text=True, encoding="utf-8", errors="replace")

            self.assertEqual(run().returncode, 0)
            first = snapshot()
            self.assertEqual(run().returncode, 0)
            second = snapshot()
            self.assertEqual([k for k in first if first[k] != second.get(k)], [])
            self.assertEqual(run("--check").returncode, 0)
            # 作業コピーが現在のリポジトリのコミット済み状態と一致している（生成し忘れがない）
            changed = [k for k, v in first.items() if (REPO / k).exists() and (REPO / k).read_bytes() != v]
            self.assertEqual(changed, [], "生成物が最新でない: py scripts/build_all.py を実行してください")

    def test_build_py_does_not_write_index_html(self):
        import build
        self.assertNotIn("html", build.TARGETS)
        self.assertFalse((REPO / "scripts" / "dashboard_template.html").exists())


class PublicPageAuditTests(unittest.TestCase):
    def test_no_payment_or_asset_terms_outside_explanations(self):
        bad = []
        for p in pages():
            for line in visible_lines(p):
                if FORBIDDEN.search(line) and not any(w in line for w in EXPLANATORY):
                    bad.append(f"{p.relative_to(REPO).as_posix()}: {line[:100]}")
        self.assertEqual(bad, [])

    def test_area_cost_has_no_paid_or_remaining(self):
        for k in ("baguio", "africa", "capetown", "common"):
            text = (REPO / "areas" / f"{k}.md").read_text(encoding="utf-8")
            for word in ("支払済", "実績", "不足", "利用可能資金"):
                self.assertNotIn(word, text.replace("実際の支払額ではありません", ""))

    def test_no_day_level_dates_pinned_to_the_person(self):
        pat = re.compile(r"\b(2/6|2/8|4/30|5/31|7/23|5/30|7/24|2027-0[2-8]-\d\d)\b")
        for rel in ("index.html", "areas/baguio.md", "areas/africa.md", "areas/capetown.md", "data/timeline.csv", "docs/01-timeline.md", "README.md"):
            text = (REPO / rel).read_text(encoding="utf-8")
            if rel == "README.md":  # 準備タスクの期限（一般的な締切）は AUTO ブロックの外の記述だけを見る
                text = re.sub(r"<!-- AUTO:.*?<!-- /AUTO:\w+ -->", "", text, flags=re.S)
            self.assertIsNone(pat.search(text), f"{rel}: 日単位の日付が残っている")


class PageListTests(unittest.TestCase):
    # pages.csv に載せないページ（理由つき）
    EXCLUDED = {
        "docs/09-issue-map.md": "pages.csv から生成する保守者向けの対応表",
        "blog/README.md": "なし",
    }

    def test_every_page_is_listed_or_excluded(self):
        with (REPO / "data" / "pages.csv").open(encoding="utf-8", newline="") as f:
            listed = {r["path"] for r in csv.DictReader(f)}
        missing = []
        for d in ("areas", "research", "docs", "blog"):
            for md in sorted((REPO / d).glob("*.md")):
                rel = md.relative_to(REPO).as_posix()
                if rel not in self.EXCLUDED and rel[:-3] + ".html" not in listed:
                    missing.append(rel)
        self.assertEqual(missing, [], "data/pages.csv に行を追加するか EXCLUDED に理由を書く")

    def test_pages_csv_paths_exist(self):
        with (REPO / "data" / "pages.csv").open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                self.assertTrue((REPO / r["path"]).is_file(), r["path"])

    def test_nav_includes_new_pages(self):
        html = (REPO / "docs" / "02-budget.html").read_text(encoding="utf-8")
        for name in ("research/africa-route-comparison.html", "docs/07-export.html", "docs/08-handoff.html"):
            self.assertIn(name, html)
        issue_map = (REPO / "docs" / "09-issue-map.html")
        self.assertTrue(issue_map.exists())
        self.assertIn("09-issue-map.html", (REPO / "docs" / "02-budget.html").read_text(encoding="utf-8"))

    def test_timeline_is_month_granular(self):
        with (REPO / "data" / "timeline.csv").open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                self.assertRegex(r["period"], r"^\d{4}年\d{1,2}月|^\d{4}年\d{1,2}〜\d{1,2}月$")


class FxSchemaTests(unittest.TestCase):
    def test_build_reads_dashboard_fx_schema(self):
        import build
        fx = build.load_fx()
        for cur in ("PHP", "ZAR", "USD"):
            self.assertGreater(fx[cur]["rate"], 0)
            self.assertTrue(fx[cur]["date"])
            self.assertTrue(fx[cur]["source"].startswith("http"))

    def test_missing_rate_is_reported_not_zero(self):
        import build
        r = {k: "" for k in ("id", "category", "country", "phase", "item", "payee", "period_start", "period_end", "due_date",
                             "status", "currency", "low_local", "std_local", "high_local", "source", "collected_on",
                             "recheck_by", "issue", "note")}
        r.update(id="X", category="予備費", status="見積", currency="EUR", std_local="100", source="https://example.com")
        problems = []
        rows = build.compute([r], {"JPY": {"rate": 1.0}}, problems)
        self.assertTrue(any("EUR" in p for p in problems))
        self.assertTrue(rows[0]["no_amount"])
        self.assertIsNone(rows[0]["est"]["std"])


if __name__ == "__main__":
    unittest.main()
