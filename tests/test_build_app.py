"""app.html（準備タスクのアプリ風画面）と app/tokens.json の整合性チェック。"""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_app as BA  # noqa: E402

TEXT = BA.build()
TOK = json.loads((BA.ROOT / "app" / "tokens.json").read_text(encoding="utf-8"))


def lum(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class AppTests(unittest.TestCase):
    def test_every_task_is_embedded_without_maintainer_fields(self):
        data = json.loads(re.search(r'id="app-data">(.*?)</script>', TEXT, re.S).group(1).replace("<\/", "</"))
        self.assertEqual(len(data["tasks"]), len(BA.load_tasks()))
        for t in data["tasks"]:
            self.assertNotIn("issue", t)

    def test_no_external_requests(self):
        self.assertEqual(re.findall(r"<script[^>]+src=|<link[^>]+href=\"https?:|@import|fetch\(|XMLHttpRequest", TEXT), [])

    def test_tokens_have_light_and_dark_with_same_keys(self):
        self.assertEqual(set(TOK["color"]["light"]), set(TOK["color"]["dark"]))

    def test_text_contrast_meets_wcag_aa(self):
        for mode in ("light", "dark"):
            c = TOK["color"][mode]
            pairs = [("ink", "bg"), ("ink", "surface"), ("inkMuted", "surface"), ("inkMuted", "bg"), ("brandInk", "brand"),
                     ("p1", "p1Soft"), ("p2", "p2Soft"), ("p3", "p3Soft"), ("warn", "warnSoft"), ("brand", "brandSoft")]
            for fg, bg in pairs:
                self.assertGreaterEqual(ratio(c[fg], c[bg]), 4.5, f"{mode}: {fg} on {bg} = {ratio(c[fg], c[bg]):.2f}")

    def test_touch_target_is_at_least_44(self):
        self.assertGreaterEqual(TOK["touchTarget"], 44)

    def test_no_personal_progress_is_sent_anywhere(self):
        self.assertIn("localStorage", TEXT)
        self.assertNotRegex(TEXT, r"navigator\.sendBeacon|\.send\(")


if __name__ == "__main__":
    unittest.main()
