"""all.html（全ページを1枚にまとめた閲覧用ページ）の整合性チェック。"""
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_single as BS  # noqa: E402

TEXT = BS.build()


class SingleHtmlTests(unittest.TestCase):
    def test_every_page_has_a_section_and_a_toc_link(self):
        for _, rel, _ in BS.pages():
            self.assertIn(f'<section class="pg" id="{BS.sid(rel)}"', TEXT, rel)
            self.assertIn(f'<a href="#{BS.sid(rel)}">', TEXT, rel)

    def test_no_duplicate_ids(self):
        ids = re.findall(r'\bid="([^"]+)"', TEXT)
        self.assertEqual([k for k, v in Counter(ids).items() if v > 1], [])

    def test_in_page_anchors_resolve(self):
        ids = set(re.findall(r'\bid="([^"]+)"', TEXT))
        broken = {h for h in re.findall(r'\bhref="#([^"]+)"', TEXT) if h not in ids}
        self.assertEqual(broken, set())

    def test_page_anchors_in_individual_pages_resolve(self):
        """個別HTMLの `ページ#見出し` リンクが、相手ページに実在する見出し id を指している"""
        root = BS.ROOT
        ids_of = {}
        for _, rel, _ in BS.pages():
            ids_of[rel] = set(re.findall(r'\bid="([^"]+)"', (root / rel).read_text(encoding="utf-8")))
        bad = []
        for _, rel, _ in BS.pages():
            html_text = (root / rel).read_text(encoding="utf-8")
            for href in re.findall(r'\bhref="([^"]+#[^"]+)"', html_text):
                if re.match(r"^[a-z]+:", href):
                    continue
                path, _, frag = href.partition("#")
                target = (Path(rel).parent / path).as_posix() if path else rel
                target = str(Path(target).as_posix())
                parts = []
                for seg in target.split("/"):
                    if seg == "..":
                        parts and parts.pop()
                    elif seg not in ("", "."):
                        parts.append(seg)
                target = "/".join(parts)
                if target in ids_of and frag not in ids_of[target]:
                    bad.append(f"{rel} -> {href}")
        self.assertEqual(bad, [])

    def test_no_relative_page_links_left(self):
        left = [h for h in re.findall(r'\bhref="([^"#][^"]*)"', TEXT) if not re.match(r"^[a-z]+:", h)]
        self.assertEqual(left, ["index.html"])  # サイドバー注記の個別ページ版へのリンクだけ

    def test_map_scripts_find_their_elements(self):
        ids = set(re.findall(r'\bid="([^"]+)"', TEXT))
        for pfx in ("p-maps-world-map", "p-maps-africa-map"):
            for name in ("map-data", "map", "detail", "tbody", "thead", "zin", "zout", "zrs"):
                self.assertIn(f"{pfx}-{name}", ids)

    def test_no_external_scripts(self):
        self.assertEqual(re.findall(r'<script[^>]+src=', TEXT), [])


if __name__ == "__main__":
    unittest.main()
