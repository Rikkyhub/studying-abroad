# -*- coding: utf-8 -*-
"""Fermi budget input consistency: quantities x hypothetical JPY unit prices.

Public estimates only. This does not validate that the assumed unit prices are
market rates or that the travel schedule/booking is possible.
"""
import csv
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSUMPTIONS = ROOT / "data" / "fermi_assumptions.csv"
EXPENSES = ROOT / "data" / "expenses.csv"
SCENARIOS = ("low", "std", "high")


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def calculate():
    totals = defaultdict(lambda: dict.fromkeys(SCENARIOS, 0))
    for entry in read_csv(ASSUMPTIONS):
        quantity = int(entry["quantity"])
        if quantity <= 0:
            raise ValueError(f"{entry['expense_id']}: quantity must be positive")
        for scenario in SCENARIOS:
            unit_price = int(entry[f"{scenario}_unit_jpy"])
            if unit_price < 0:
                raise ValueError(f"{entry['expense_id']}: unit price must be nonnegative")
            totals[entry["expense_id"]][scenario] += quantity * unit_price
    return totals


class FermiBudgetTest(unittest.TestCase):
    def test_expense_rows_reconcile_with_quantity_times_unit_price(self):
        totals = calculate()
        expenses = {row["id"]: row for row in read_csv(EXPENSES)}
        self.assertEqual(set(totals).difference(expenses), set())
        for expense_id, scenarios in totals.items():
            expense = expenses[expense_id]
            self.assertEqual(expense["currency"], "JPY", expense_id)
            self.assertEqual(expense["status"], "未確認", expense_id)
            for scenario, expected in scenarios.items():
                with self.subTest(id=expense_id, scenario=scenario):
                    self.assertEqual(int(expense[f"{scenario}_local"]), expected)
        self.assertGreater(sum(v["std"] for v in totals.values()), 0)

    def test_35_days_and_34_nights_are_accounted_for_once(self):
        entries = read_csv(ASSUMPTIONS)
        self.assertEqual(sum(int(r["quantity"]) for r in entries
                             if r["unit"] == "泊"), 34)
        self.assertEqual(sum(int(r["quantity"]) for r in entries
                             if r["cost_kind"] == "食費" and r["unit"] == "日"), 35)

    def test_separate_food_lodging_and_surface_transport(self):
        expenses = {row["id"]: row for row in read_csv(EXPENSES)}
        self.assertEqual(expenses["AF-11"]["category"], "食費・日常生活費")
        self.assertEqual(expenses["AF-15"]["category"], "寮・ホームステイ・宿泊")
        self.assertEqual(expenses["AF-16"]["category"], "航空券・長距離移動")
        self.assertEqual(expenses["AF-22"]["category"], "現地交通費")
        self.assertEqual(sum(1 for x in read_csv(ASSUMPTIONS)
                             if x["expense_id"] == "AF-15"), 1)

    def test_scenarios_are_ordered(self):
        for expense_id, scenarios in calculate().items():
            with self.subTest(id=expense_id):
                self.assertLessEqual(scenarios["low"], scenarios["std"])
                self.assertLessEqual(scenarios["std"], scenarios["high"])


if __name__ == "__main__":
    unittest.main()
