"""Regression checks for the public CSV data gate."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_public_data import check


class PublicDataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()

    def write(self, name, columns, rows):
        with (self.root / "data" / name).open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

    def test_market_estimates_allowed(self):
        self.write("expenses.csv", ["id", "quoted_amount", "paid_amount", "actual_amount"],
                   [{"id": "SAMPLE", "quoted_amount": "120", "paid_amount": "", "actual_amount": ""}])
        self.write("funds.csv", ["id", "type", "name", "amount_jpy"],
                   [{"id": "budget_cap", "type": "予算", "name": "モデル上限", "amount_jpy": "2500000"}])
        self.assertEqual(check(self.root), [])

    def test_nonempty_legacy_payment_rejected_without_value_in_error(self):
        self.write("expenses.csv", ["id", "paid_amount"],
                   [{"id": "SAMPLE", "paid_amount": "987654321"}])
        problems = check(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("paid_amount", problems[0])
        self.assertNotIn("987654321", problems[0])

    def test_new_payment_columns_rejected_even_if_empty(self):
        self.write("expenses.csv", ["id", "paid_jpy", "evidence"], [])
        self.assertEqual(len(check(self.root)), 2)

    def test_personal_funding_row_rejected(self):
        self.write("funds.csv", ["id", "type", "name", "amount_jpy"],
                   [{"id": "fund_savings", "type": "資金", "name": "", "amount_jpy": ""}])
        self.assertEqual(len(check(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
