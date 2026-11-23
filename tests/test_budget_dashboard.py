import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
from budget_dashboard import ledger


class DashboardTest(unittest.TestCase):
    def test_seven_month_route(self):
        summary, rows, *_ = build.load_model()
        items = {r["id"]: r for r in ledger(rows)}
        self.assertTrue({"PH-11", "SA8-out", "SA8-return"} <= items.keys())
        self.assertFalse({"SC-08", "PH-12", "AU-01"} & items.keys())
        self.assertEqual(items["SA8-food"]["amount"], 27000)
        self.assertEqual(items["SA8-hotel"]["amount"], 54000)
        self.assertEqual(items["SA8-return"]["amount"], 205000)
        for scenario in build.SCENARIOS:
            plan = ledger(rows, scenario)
            self.assertTrue(all(r["amount"] is not None for r in plan))
            self.assertEqual(sum(r["amount"] for r in plan), summary["total"][scenario])
        self.assertIn("2027-08", items["CM-01"]["months"])
        for r in items.values():
            if r["amount"] is None:
                self.assertTrue(all(x is None for x in r["months"].values()))
            else:
                self.assertEqual(sum(r["months"].values()), r["amount"])
