"""集計ロジックの単体テスト。Run: python3 -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build  # noqa: E402

BASE = {k: "" for k in ["id", "category", "country", "phase", "item", "payee", "period_start", "period_end", "due_date", "status",
                        "currency", "low_local", "std_local", "high_local", "paid_jpy", "paid_date", "actual_local", "actual_fx",
                        "actual_jpy", "source", "evidence", "collected_on", "recheck_by", "issue", "note"]}
FX = {"JPY": {"rate": 1.0}, "USD": {"rate": 150.0}}
FUNDS = [{"id": "budget_ideal", "type": "予算", "amount_jpy": "2500000"},
         {"id": "budget_cap", "type": "予算", "amount_jpy": "3000000"},
         {"id": "fund_savings", "type": "資金", "amount_jpy": ""}]


def row(**kw):
    r = dict(BASE, category="予備費", status="見積", source="https://example.com", currency="JPY")
    r.update(kw)
    return r


def run(rows, funds=FUNDS):
    problems = []
    computed = build.compute(rows, FX, problems)
    return build.summarize(computed, funds), computed, problems


class TotalsTest(unittest.TestCase):
    def test_paid_is_not_double_counted(self):
        S, _, _ = run([row(id="A", std_local="1000", paid_jpy="400")])
        self.assertEqual(S["forecast"]["std"], 1000)
        self.assertEqual(S["paid"], 400)
        self.assertEqual(S["remaining"], 600)

    def test_paid_above_estimate_uses_paid(self):
        S, _, _ = run([row(id="A", std_local="1000", paid_jpy="1500")])
        self.assertEqual(S["forecast"]["std"], 1500)
        self.assertEqual(S["remaining"], 0)

    def test_actual_overrides_estimate(self):
        S, _, _ = run([row(id="A", std_local="1000", low_local="500", high_local="2000", actual_jpy="1200", status="実績", evidence="private:x")])
        self.assertEqual(S["forecast"], {"low": 1200, "std": 1200, "high": 1200})
        self.assertEqual(S["actual"], 1200)

    def test_currency_conversion(self):
        S, _, _ = run([row(id="A", currency="USD", std_local="10")])
        self.assertEqual(S["forecast"]["std"], 1500)

    def test_missing_amount_is_not_zero_but_flagged(self):
        S, _, _ = run([row(id="A", status="未確認", source="")])
        self.assertEqual(S["forecast"]["std"], 0)
        self.assertEqual(len(S["no_amount"]), 1)

    def test_scenario_fallback(self):
        S, _, _ = run([row(id="A", std_local="100")])
        self.assertEqual(S["forecast"], {"low": 100, "std": 100, "high": 100})

    def test_unverified_paid_is_separated(self):
        S, _, _ = run([row(id="A", std_local="1000", paid_jpy="700", status="未確認"),
                       row(id="B", std_local="500", paid_jpy="500", status="確定", evidence="private:receipt")])
        self.assertEqual(S["paid"], 1200)
        self.assertEqual(S["paid_verified"], 500)

    def test_budget_remaining(self):
        S, _, _ = run([row(id="A", std_local="2600000")])
        self.assertEqual(S["vs_ideal"]["std"], -100000)
        self.assertEqual(S["vs_cap"]["std"], 400000)
        self.assertIsNone(S["available"])
        self.assertIsNone(S["gap"])

    def test_month_allocation_by_days(self):
        _, computed, _ = run([row(id="A", std_local="100", period_start="2027-02-27", period_end="2027-03-03")])  # 2/27,2/28 と 3/1〜3/3（2027年は平年）
        alloc = computed[0]["alloc"]
        self.assertAlmostEqual(alloc["2027-02"], 0.4)
        self.assertAlmostEqual(alloc["2027-03"], 0.6)


class ValidationTest(unittest.TestCase):
    def validate(self, rows):
        problems = []
        build.validate(rows, [], [], [], problems)
        return problems

    def test_paid_without_evidence_must_be_unconfirmed(self):
        p = self.validate([row(id="A", std_local="1", paid_jpy="1", status="確定")])
        self.assertTrue(any("証憑" in x for x in p))

    def test_estimate_requires_source(self):
        p = self.validate([row(id="A", std_local="1", source="")])
        self.assertTrue(any("根拠" in x for x in p))

    def test_duplicate_id(self):
        p = self.validate([row(id="A", std_local="1"), row(id="A", std_local="1")])
        self.assertTrue(any("一意" in x for x in p))

    def test_private_number_in_evidence(self):
        p = self.validate([row(id="A", std_local="1", evidence="booking 12345678")])
        self.assertTrue(any("個人情報" in x for x in p))


class RepoDataTest(unittest.TestCase):
    def test_repository_data_is_consistent(self):
        """実データで検証エラーがなく、生成物が CSV と一致していること"""
        import subprocess
        r = subprocess.run([sys.executable, str(Path(build.__file__)), "--check"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
