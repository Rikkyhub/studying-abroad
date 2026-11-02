"""research/southern-africa-countries.md 第0章の再採点表の整合性（日数の検算と、未計上費用の順位付け禁止）。"""
import re
import unittest
from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / "research" / "southern-africa-countries.md"


def table_rows(text, header_start):
    lines = text.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(header_start))
    rows = []
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return rows


def rng(s):
    nums = [int(n) for n in re.findall(r"\d+", s)]
    return (nums[0], nums[-1]) if len(nums) > 1 else (nums[0], nums[0])


class ScenarioRankingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_day_totals_equal_tourist_plus_travel_plus_spare(self):
        rows = table_rows(self.text, "| 案 | 観光日 | 移動日")
        self.assertEqual(len(rows), 6)
        for r in rows:
            tour, spare, total = rng(r[1]), rng(r[3]), rng(r[5])
            # 移動日は「3＋国間」の式の右辺（和）を使う
            tr = rng(r[2].split("＝")[-1])
            self.assertEqual((tour[0] + tr[0] + spare[0], tour[1] + tr[1] + spare[1]), total, r[0])

    def test_uncosted_scenarios_get_no_numeric_transport_rank(self):
        rows = table_rows(self.text, "| 案 | 総交通費（万円） | 状態 | 順位")
        self.assertEqual(len(rows), 6)
        for r in rows:
            if "未計上" in r[2]:
                self.assertEqual(r[3], "比較不能", r[0])
            else:
                self.assertRegex(r[3], r"^\d+$", r[0])

    def test_main_table_marks_uncosted_transport(self):
        rows = table_rows(self.text, "| シナリオ（新方針の構成）")
        for r in rows:
            if "未計上" in r[4]:
                self.assertTrue(r[6].endswith("比較不能"), r[0])
                self.assertNotRegex(r[4], r"^\d")


if __name__ == "__main__":
    unittest.main()
