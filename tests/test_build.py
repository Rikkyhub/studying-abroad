"""集計ロジックの単体テスト（公開用匿名モデル）。Run: python3 -m unittest discover -s tests -v"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build  # noqa: E402
import check_public_data  # noqa: E402

COLUMNS = ["id", "category", "country", "phase", "item", "payee", "period_start", "period_end", "due_date", "status",
           "currency", "low_local", "std_local", "high_local", "source", "collected_on", "recheck_by", "issue", "note"]
BASE = {k: "" for k in COLUMNS}
FX = {"JPY": {"rate": 1.0}, "USD": {"rate": 150.0}}
FUNDS = [{"id": "budget_ideal", "type": "予算", "amount_jpy": "2500000"},
         {"id": "budget_cap", "type": "予算", "amount_jpy": "3000000"},
         {"id": "budget_africa", "type": "予算", "amount_jpy": "600000"}]


def row(**kw):
    r = dict(BASE, category="予備費", status="見積", source="https://example.com", currency="JPY")
    r.update(kw)
    return r


def run(rows, funds=FUNDS):
    problems = []
    computed = build.compute(rows, FX, problems)
    return build.summarize(computed, funds), computed, problems


class TotalsTest(unittest.TestCase):
    def test_each_row_counted_once(self):
        S, _, _ = run([row(id="A", std_local="1000"), row(id="B", std_local="500")])
        self.assertEqual(S["total"]["std"], 1500)

    def test_no_double_counting_across_breakdowns(self):
        """見積＋未確認の内訳、費目別、月別の合計がすべて総額に一致する"""
        rows = [row(id="A", std_local="1000", low_local="800", high_local="1200", period_start="2027-02-27", period_end="2027-03-03"),
                row(id="B", std_local="300", status="未確認", source="", category="通信費", due_date="2027-05-10")]
        S, _, _ = run(rows)
        self.assertEqual(S["total"]["std"], 1300)
        self.assertEqual(sum(v["std"] for v in S["by_status"].values()), S["total"]["std"])
        for s in ("low", "std", "high"):
            self.assertAlmostEqual(sum(v[s] for v in S["by_cat"].values()), S["total"][s])
        self.assertAlmostEqual(sum(v["見積"] + v["未確認"] for v in S["by_month"].values()), S["total"]["std"])
        self.assertAlmostEqual(sum(S["by_country"].values()), S["total"]["std"])

    def test_unverified_is_added_not_subtracted(self):
        """未確認は費用として別枠で加算されるだけで、予算差・合計を減らさない"""
        S0, _, _ = run([row(id="A", std_local="1000")])
        S1, _, _ = run([row(id="A", std_local="1000"), row(id="U", std_local="700", status="未確認", source="")])
        self.assertEqual(S1["total"]["std"], S0["total"]["std"] + 700)
        self.assertEqual(S1["by_status"]["未確認"]["std"], 700)
        self.assertEqual(S1["by_status"]["見積"]["std"], 1000)
        self.assertEqual(S1["vs_cap"]["std"], S0["vs_cap"]["std"] - 700)

    def test_no_paid_or_funds_concepts(self):
        S, computed, _ = run([row(id="U", std_local="700", status="未確認", source="")])
        for key in ("paid", "paid_verified", "remaining", "available", "gap", "actual", "forecast"):
            self.assertNotIn(key, S)
            self.assertNotIn(key, computed[0])

    def test_missing_amount_is_not_zero(self):
        S, computed, _ = run([row(id="A", std_local="1000"), row(id="M", status="未確認", source="")])
        self.assertTrue(computed[1]["no_amount"])
        self.assertEqual(computed[1]["est"], {"low": None, "std": None, "high": None})
        self.assertEqual([r["id"] for r in S["no_amount"]], ["M"])
        self.assertEqual(S["total"]["std"], 1000)
        self.assertEqual(S["status_count"]["未確認"], 1)

    def test_missing_amount_shown_as_unentered(self):
        S, computed, _ = run([row(id="M", status="未確認", source="", item="生活費")])
        detail = build.gen_budget_detail(computed)
        self.assertIn("金額未入力", detail)
        self.assertNotIn("¥0", detail)
        self.assertIn("M 生活費", build.gen_budget_summary(S))

    def test_currency_conversion(self):
        S, _, _ = run([row(id="A", currency="USD", std_local="10")])
        self.assertEqual(S["total"]["std"], 1500)

    def test_scenario_fallback(self):
        S, _, _ = run([row(id="A", std_local="100")])
        self.assertEqual(S["total"], {"low": 100, "std": 100, "high": 100})

    def test_budget_difference(self):
        S, _, _ = run([row(id="A", std_local="2600000")])
        self.assertEqual(S["vs_ideal"]["std"], -100000)
        self.assertEqual(S["vs_cap"]["std"], 400000)

    def test_month_allocation_by_days(self):
        _, computed, _ = run([row(id="A", std_local="100", period_start="2027-02-27", period_end="2027-03-03")])
        alloc = computed[0]["alloc"]
        self.assertAlmostEqual(alloc["2027-02"], 0.4)
        self.assertAlmostEqual(alloc["2027-03"], 0.6)


class ValidationTest(unittest.TestCase):
    def validate(self, rows, funds=()):
        problems = []
        build.validate(rows, [], [], [], problems, funds)
        return problems

    def test_confirmed_and_actual_status_rejected(self):
        for st in ("確定", "実績"):
            p = self.validate([row(id="A", std_local="1", status=st)])
            self.assertTrue(any("区分" in x for x in p), st)

    def test_estimate_requires_source(self):
        p = self.validate([row(id="A", std_local="1", source="")])
        self.assertTrue(any("出典" in x for x in p))

    def test_estimate_requires_amount(self):
        p = self.validate([row(id="A")])
        self.assertTrue(any("金額" in x for x in p))

    def test_duplicate_id(self):
        p = self.validate([row(id="A", std_local="1"), row(id="A", std_local="1")])
        self.assertTrue(any("一意" in x for x in p))

    def test_private_number_in_note(self):
        p = self.validate([row(id="A", std_local="1", note="booking 123456789")])
        self.assertTrue(any("個人情報" in x for x in p))

    def test_non_budget_fund_row_rejected(self):
        p = self.validate([], funds=[{"id": "x", "type": "資金", "amount_jpy": ""}])
        self.assertTrue(any("funds.csv" in x for x in p))


class RepoDataTest(unittest.TestCase):
    def test_repository_data_is_consistent(self):
        """実データで検証エラーがなく、生成物が CSV と一致していること"""
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "build.py"), "--check"],
                           capture_output=True, text=True, encoding="utf-8", timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_public_csv_passes_public_data_check(self):
        self.assertEqual(check_public_data.check(REPO), [])

    def test_public_csv_has_only_estimate_statuses(self):
        rows = build.read_csv("expenses.csv")
        self.assertTrue(rows)
        self.assertTrue({r["status"] for r in rows} <= {"見積", "未確認"})
        for col in check_public_data.DISALLOWED_EXPENSE_FIELDS:
            self.assertNotIn(col, rows[0])

    def test_rebuild_is_deterministic(self):
        """build を実行した直後に --check が通り、2回実行しても生成物が変わらない"""
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "repo"
            shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            script = dst / "scripts" / "build.py"
            targets = ["README.md", "index.html", "docs/01-timeline.md", "docs/02-budget.md", "docs/03-preparation.md", "blog/article-ideas.md"]
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True, timeout=120)
            first = {t: (dst / t).read_bytes() for t in targets}
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True, timeout=120)
            self.assertEqual(first, {t: (dst / t).read_bytes() for t in targets})
            r = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True, encoding="utf-8", timeout=120)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
