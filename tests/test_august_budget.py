# -*- coding: utf-8 -*-
"""Country budget models are Markdown-first; alternative August routes are exclusive."""
import csv
import tempfile
import unittest
from pathlib import Path
from scripts import august_budget, fermi_budget

ROOT = Path(__file__).resolve().parents[1]


def expenses():
    with (ROOT / "data" / "expenses.csv").open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


class MayAndAugustBudgetTest(unittest.TestCase):
    def test_may_country_entries_preserve_35_days_34_nights_and_total(self):
        rows = fermi_budget.read_assumptions(ROOT)
        self.assertEqual(sum(x["quantity"] for x in rows if x["unit"] == "泊"), 34)
        self.assertEqual(sum(x["quantity"] for x in rows if x["kind"] == "食費"), 35)
        self.assertEqual(sum(x[1] for x in fermi_budget.aggregate(ROOT).values()), 295500)
        for country, expected in (("ジンバブエ", 4), ("ザンビア", 2), ("ボツワナ", 3)):
            self.assertEqual(
                sum(x["quantity"] for x in rows if x["country"] == country and x["unit"] == "泊"),
                expected)
        self.assertIn("ジンバブエ", fermi_budget.render_summary_md(ROOT))
        self.assertIn("国・地域別の内訳", fermi_budget.render_summary_md(ROOT))

    def test_undecided_august_looks_at_each_route_without_adding_to_global_budget(self):
        active, rows, budgets = august_budget.calculate(ROOT)
        self.assertEqual(active, "未定")
        self.assertEqual(set(budgets), {"A", "B", "C", "D", "E"})
        self.assertEqual({case: value["nights"] for case, value in budgets.items()},
                         {"A": 17, "B": 15, "C": 14, "D": 10, "E": 15})
        expected = {"A": 78000, "B": 69000, "C": 64500, "D": 46500, "E": 69000}
        self.assertEqual({case: value["lodging"][1] + value["food"][1]
                          for case, value in budgets.items()}, expected)
        before = expenses()
        after = august_budget.apply_to_expenses([dict(x) for x in before], ROOT)
        self.assertEqual(len(after), len(before))
        self.assertIn("¥78,000", august_budget.render_summary_md(ROOT))
        self.assertIn("未定のため候補の費用は総予算へ一切加算", august_budget.render_summary_md(ROOT))

    def test_only_selected_august_route_adds_lodging_and_food(self):
        source = (ROOT / august_budget.SOURCE).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            target = root / august_budget.SOURCE
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.replace("**予算へ反映する案：未定**",
                                             "**予算へ反映する案：A**", 1), encoding="utf-8")
            active, _, budgets = august_budget.calculate(root)
            self.assertEqual(active, "A")
            base = expenses()
            result = august_budget.apply_to_expenses([dict(x) for x in base], root)
            new = result[len(base):]
            self.assertEqual(len(new), 5)
            self.assertTrue(all(row["phase"] == "アフリカ周遊（8月）" for row in new))
            self.assertTrue(all(row["status"] == "未確認" for row in new))
            self.assertTrue(all(august_budget.SOURCE.as_posix() in row["note"] for row in new))
            self.assertEqual(sum(int(row["std_local"]) for row in new), 78000)
            self.assertEqual(sum(int(row["std_local"]) for row in new),
                             budgets["A"]["lodging"][1] + budgets["A"]["food"][1])
            self.assertEqual(len({x["id"] for x in result}), len(result))
            self.assertFalse(any("ルワンダ" in row["item"] for row in new))

    def test_unknown_route_selection_fails_instead_of_zero_budget(self):
        source = (ROOT / august_budget.SOURCE).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            target = root / august_budget.SOURCE
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.replace("**予算へ反映する案：未定**",
                                             "**予算へ反映する案：UNKNOWN**", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "selected scenario"):
                august_budget.calculate(root)


if __name__ == "__main__":
    unittest.main()
