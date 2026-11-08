# -*- coding: utf-8 -*-
"""Editable Markdown must be the only source for 35-day estimated unit costs."""
import csv
import unittest
from pathlib import Path
from scripts import fermi_budget

ROOT = Path(__file__).resolve().parents[1]


def legacy_expenses():
    with (ROOT / "data" / "expenses.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MarkdownBudgetTest(unittest.TestCase):
    def test_md_quantities_and_unit_prices_reconcile(self):
        entries = fermi_budget.read_assumptions(ROOT)
        nights = sum(x["quantity"] for x in entries if x["unit"] == "泊")
        days = sum(x["quantity"] for x in entries if x["kind"] == "食費")
        self.assertGreater(days, 0)
        self.assertEqual(days - nights, 1, "day/night quantities require a consistent itinerary")
        totals = fermi_budget.aggregate(ROOT)
        self.assertGreater(sum(x[1] for x in totals.values()), 0)
        self.assertEqual(totals["AF-15"][1], sum(
            x["quantity"] * x["prices"][1] for x in entries if x["id"] == "AF-15"))
        for values in totals.values():
            self.assertLessEqual(values[0], values[1])
            self.assertLessEqual(values[1], values[2])

    def test_md_in_memory_overlay_without_editing_csv(self):
        old = legacy_expenses()
        unmodified = [(r["id"], r.get("std_local", "")) for r in old]
        result = fermi_budget.apply_to_expenses([dict(x) for x in old], ROOT)
        self.assertEqual(unmodified, [(r["id"], r.get("std_local", "")) for r in old])
        by_id = {x["id"]: x for x in result}
        totals = fermi_budget.aggregate(ROOT)
        self.assertEqual(set(totals).difference(by_id), set())
        for expense_id, amounts in totals.items():
            self.assertEqual(by_id[expense_id]["status"], "未確認")
            self.assertEqual(by_id[expense_id]["currency"], "JPY")
            self.assertEqual(
                [int(by_id[expense_id][f"{s}_local"]) for s in ("low", "std", "high")], amounts)
        self.assertEqual(by_id["AF-15"]["category"], "寮・ホームステイ・宿泊")
        self.assertEqual(by_id["AF-11"]["category"], "食費・日常生活費")
        self.assertEqual(by_id["AF-20"]["category"], "観光・ツアー・ダイビング")
        self.assertEqual(by_id["AF-22"]["category"], "現地交通費")
        self.assertEqual(by_id["AF-16"]["category"], "航空券・長距離移動")
        self.assertEqual(by_id["AF-19"]["currency"], "USD")
        self.assertEqual(len(result), len(old) + 4)

    def test_reject_double_priced_rows(self):
        old = legacy_expenses()
        source = [dict(x) for x in old]
        for row in source:
            if row["id"] == "AF-11":
                row["std_local"] = "100"
                break
        with self.assertRaisesRegex(ValueError, "double-count"):
            fermi_budget.apply_to_expenses(source, ROOT)


if __name__ == "__main__":
    unittest.main()
