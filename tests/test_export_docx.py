"""Checks for the Markdown -> .docx exporter (stdlib only)."""
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from export_docx import ROOT, build_docx, sources  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SAMPLE = """# 題名 & <テスト>

段落に **太字** と `code` と [出典](https://example.com/a?x=1&y=2) と https://example.org/z

## 一覧

- 項目A
  - 子項目 1
- 項目B
1. 手順一
2. 手順二

| 学校 | 費用 |
|---|---:|
| A校 | 100 |
| B校 | 200 |

> 注意: 要確認

---

```
a < b && c > d
```
"""


class DocxTests(unittest.TestCase):
    def build(self, md=SAMPLE):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        dest = Path(d.name) / "sub" / "t.docx"
        build_docx(md, dest)
        return dest

    def doc_root(self, dest):
        with zipfile.ZipFile(dest) as z:
            self.assertIsNone(z.testzip())
            return ET.fromstring(z.read("word/document.xml"))

    def test_required_parts_and_xml_valid(self):
        dest = self.build()
        with zipfile.ZipFile(dest) as z:
            names = z.namelist()
            for n in ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml", "word/_rels/document.xml.rels"]:
                self.assertIn(n, names)
            for n in names:
                ET.fromstring(z.read(n))  # すべて整形式

    def test_structure(self):
        root = self.doc_root(self.build())
        styles = [e.get(W + "val") for e in root.iter(W + "pStyle")]
        self.assertIn("Heading1", styles)
        self.assertIn("Heading2", styles)
        self.assertIn("Quote", styles)
        self.assertEqual(len(list(root.iter(W + "tbl"))), 1)
        self.assertEqual(len(list(root.iter(W + "tr"))), 3)
        self.assertEqual(len(list(root.iter(W + "tblHeader"))), 1)
        self.assertEqual(len(list(root.iter(W + "hyperlink"))), 2)

    def test_japanese_and_special_chars_roundtrip(self):
        root = self.doc_root(self.build())
        text = "".join(t.text or "" for t in root.iter(W + "t"))
        for s in ["題名 & <テスト>", "太字", "学校", "A校", "手順二", "a < b && c > d", "注意: 要確認"]:
            self.assertIn(s, text)

    def test_list_markers(self):
        root = self.doc_root(self.build())
        text = "".join(t.text or "" for t in root.iter(W + "t"))
        self.assertIn("•", text)
        self.assertIn("2.", text)

    def test_hyperlink_relationship_escaped(self):
        dest = self.build()
        with zipfile.ZipFile(dest) as z:
            rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        targets = [r.get("Target") for r in rels]
        self.assertIn("https://example.com/a?x=1&y=2", targets)

    def test_all_repo_markdown_converts(self):
        with tempfile.TemporaryDirectory() as d:
            files = sources()
            self.assertTrue(files)
            for f in files:
                dest = Path(d) / (f.stem + ".docx")
                build_docx(f.read_text(encoding="utf-8"), dest)
                with zipfile.ZipFile(dest) as z:
                    ET.fromstring(z.read("word/document.xml"))


if __name__ == "__main__":
    unittest.main()
