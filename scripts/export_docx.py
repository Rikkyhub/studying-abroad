# -*- coding: utf-8 -*-
"""Markdown を Word（.docx）に変換する。標準ライブラリのみ（zipfile + 手組みOOXML）。

使い方（リポジトリのルートで実行）:
    py scripts/export_docx.py                    research/ docs/ blog/ の全 .md
    py scripts/export_docx.py docs/02-budget.md  指定ファイルだけ
    py scripts/export_docx.py --out DIR          出力先（既定 exports/）

- 正本は Markdown。.docx は生成物（exports/ は .gitignore 済み・コミットしない）。
- 対応: 見出し・段落・太字/斜体/インラインコード・リンク（ハイパーリンク）・
  箇条書き/番号付き（入れ子）・表（ヘッダ行・罫線）・引用・コードブロック・区切り線。
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = ["areas", "research", "countries", "docs", "blog"]
JP_FONT = "Yu Gothic"
MONO_FONT = "Consolas"
PAGE_W = 11906 - 2 * 1134  # A4 幅 - 左右余白(twips)


def sources(root: Path = ROOT) -> list[Path]:
    out: list[Path] = []
    for d in SOURCE_DIRS:
        out += sorted((root / d).glob("*.md"))
    return out


def x(text: str) -> str:
    # XML に使えない制御文字は除去してからエスケープ
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return escape(text)


# ---------------------------------------------------------------- inline
TOKEN = re.compile(
    r"`(?P<code>[^`]+)`"
    r"|\[(?P<label>[^\]]+)\]\((?P<href>[^)\s]+)\)"
    r"|\*\*(?P<bold>.+?)\*\*"
    r"|(?<![\w*])\*(?P<ital>[^*\s][^*]*?)\*(?![\w*])"
    r"|(?P<url>https?://[^\s|）)<>、。]+)"
    r"|(?P<br><br\s*/?>)"
)


class Doc:
    def __init__(self) -> None:
        self.rels: list[str] = []  # hyperlink targets

    def link_id(self, href: str) -> str:
        if href not in self.rels:
            self.rels.append(href)
        return f"rIdL{self.rels.index(href) + 1}"

    def run(self, text: str, bold=False, ital=False, code=False, link=False, size=None) -> str:
        if not text:
            return ""
        rpr = ""
        if code:
            rpr += f'<w:rFonts w:ascii="{MONO_FONT}" w:hAnsi="{MONO_FONT}" w:eastAsia="{JP_FONT}"/>'
            rpr += '<w:shd w:val="clear" w:color="auto" w:fill="EEF2F3"/>'
        if bold:
            rpr += "<w:b/>"
        if ital:
            rpr += "<w:i/>"
        if link:
            rpr += '<w:color w:val="0C6174"/><w:u w:val="single"/>'
        if size:
            rpr += f'<w:sz w:val="{size}"/>'
        parts = text.split("\n")
        body = '<w:br/>'.join(f'<w:t xml:space="preserve">{x(p)}</w:t>' for p in parts)
        return f"<w:r><w:rPr>{rpr}</w:rPr>{body}</w:r>"

    def inline(self, text: str, bold=False, ital=False, size=None) -> str:
        out: list[str] = []
        pos = 0
        for m in TOKEN.finditer(text):
            out.append(self.run(text[pos:m.start()], bold, ital, size=size))
            pos = m.end()
            if m.group("code") is not None:
                out.append(self.run(m.group("code"), bold, ital, code=True, size=size))
            elif m.group("label") is not None:
                href = m.group("href")
                inner = self.run(m.group("label"), bold, ital, link=True, size=size)
                if re.match(r"^https?:", href):
                    out.append(f'<w:hyperlink r:id="{self.link_id(href)}">{inner}</w:hyperlink>')
                else:  # リポジトリ内相対リンクは文字 + 参照先
                    out.append(inner + self.run(f"（{href}）", bold, ital, size=size))
            elif m.group("bold") is not None:
                out.append(self.inline(m.group("bold"), True, ital, size))
            elif m.group("ital") is not None:
                out.append(self.inline(m.group("ital"), bold, True, size))
            elif m.group("url") is not None:
                u = m.group("url")
                out.append(f'<w:hyperlink r:id="{self.link_id(u)}">{self.run(u, bold, ital, link=True, size=size)}</w:hyperlink>')
            else:
                out.append("<w:r><w:br/></w:r>")
        out.append(self.run(text[pos:], bold, ital, size=size))
        return "".join(out)

    # ------------------------------------------------------------ blocks
    def para(self, inner: str, style: str | None = None, ppr: str = "") -> str:
        st = f'<w:pStyle w:val="{style}"/>' if style else ""
        return f"<w:p><w:pPr>{st}{ppr}</w:pPr>{inner}</w:p>"

    def table(self, rows: list[list[str]], aligns: list[str]) -> str:
        ncol = max(len(r) for r in rows)
        w = PAGE_W // ncol
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for _ in range(ncol))
        trs = []
        for ri, row in enumerate(rows):
            row = row + [""] * (ncol - len(row))
            tcs = []
            for ci, cell in enumerate(row):
                shade = '<w:shd w:val="clear" w:color="auto" w:fill="EFF4F5"/>' if ri == 0 else ""
                jc = {"r": "right", "c": "center"}.get(aligns[ci] if ci < len(aligns) else "", "left")
                p = self.para(self.inline(cell, bold=(ri == 0), size=18), ppr=f'<w:spacing w:before="20" w:after="20"/><w:jc w:val="{jc}"/>')
                tcs.append(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shade}</w:tcPr>{p}</w:tc>')
            trpr = "<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>" if ri == 0 else "<w:trPr><w:cantSplit/></w:trPr>"
            trs.append(f"<w:tr>{trpr}{''.join(tcs)}</w:tr>")
        borders = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="9FB3B9"/>'
                          for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        pr = (f'<w:tblPr><w:tblW w:w="{PAGE_W}" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>'
              '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>')
        return f"<w:tbl>{pr}<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>" + self.para("", ppr='<w:spacing w:after="0"/>')


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$", line)) and "-" in line


def convert(md: str) -> tuple[str, str, Doc]:
    """Markdown -> (title, body_xml, Doc)"""
    d = Doc()
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    title = ""
    para: list[str] = []
    i = 0

    def flush():
        if para:
            out.append(d.para(d.inline("\n".join(para))))
            para.clear()

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            for ln in buf or [""]:
                out.append(d.para(d.run(ln.replace("\t", "    "), code=True, size=18), "Code"))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and not title:
                title = re.sub(r"[`*]", "", text)
            out.append(d.para(d.inline(text), f"Heading{level}"))
            i += 1; continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            flush()
            out.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="9FB3B9"/></w:pBdr></w:pPr></w:p>')
            i += 1; continue
        if s.startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            flush()
            head = split_row(s)
            aligns = []
            for c in split_row(lines[i + 1]):
                aligns.append("c" if c.startswith(":") and c.endswith(":") else "r" if c.endswith(":") else "l")
            rows = [head]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i])); i += 1
            out.append(d.table(rows, aligns))
            continue
        if s.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip())); i += 1
            out.append(d.para(d.inline("\n".join(buf)), "Quote"))
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
            flush()
            items = []
            while i < len(lines):
                lm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if lm:
                    items.append([len(lm.group(1).replace("\t", "    ")), lm.group(2), lm.group(3)])
                elif lines[i].startswith("  ") and lines[i].strip() and items:
                    items[-1][2] += " " + lines[i].strip()
                else:
                    break
                i += 1
            stack: list[int] = []
            counters: dict[int, int] = {}
            for ind, mark, text in items:
                while stack and ind < stack[-1]:
                    counters.pop(stack.pop(), None)
                if not stack or ind > stack[-1]:
                    stack.append(ind)
                depth = len(stack) - 1
                if mark[0].isdigit():
                    counters[ind] = counters.get(ind, 0) + 1
                    label = f"{counters[ind]}."
                else:
                    counters.pop(ind, None)
                    label = "•" if depth % 2 == 0 else "◦"
                cm = re.match(r"^\[( |x|X)\]\s+(.*)$", text)
                if cm:
                    label = "☑" if cm.group(1) != " " else "☐"
                    text = cm.group(2)
                left = 360 * (depth + 1)
                ppr = f'<w:ind w:left="{left}" w:hanging="300"/><w:spacing w:before="20" w:after="20"/>'
                out.append(d.para(d.run(label + "\t") + d.inline(text), None,
                                  f'<w:tabs><w:tab w:val="left" w:pos="{left}"/></w:tabs>' + ppr))
            continue
        para.append(s)
        i += 1
    flush()
    return title, "".join(out), d


# ---------------------------------------------------------------- package
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def styles_xml() -> str:
    fonts = f'<w:rFonts w:ascii="{JP_FONT}" w:hAnsi="{JP_FONT}" w:eastAsia="{JP_FONT}" w:cs="{JP_FONT}"/>'

    def heading(n: int, size: int, before: int) -> str:
        return (f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}"/><w:basedOn w:val="Normal"/>'
                f'<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="{before}" w:after="80"/>'
                f'<w:outlineLvl w:val="{n - 1}"/></w:pPr><w:rPr><w:b/><w:color w:val="153948"/><w:sz w:val="{size}"/></w:rPr></w:style>')

    h = "".join(heading(n, s, b) for n, s, b in [(1, 40, 240), (2, 32, 320), (3, 28, 240), (4, 24, 200), (5, 22, 160), (6, 22, 160)])
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>'
            f'<w:docDefaults><w:rPrDefault><w:rPr>{fonts}<w:sz w:val="21"/><w:lang w:val="en-US" w:eastAsia="ja-JP"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
            + h +
            '<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="B77A24"/></w:pBdr>'
            '<w:shd w:val="clear" w:color="auto" w:fill="FFFAF1"/><w:ind w:left="240"/></w:pPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/>'
            '<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="EEF2F3"/><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:style>'
            '</w:styles>')


def build_docx(md: str, dest: Path, fallback_title: str = "") -> str:
    title, body, d = convert(md)
    title = title or fallback_title
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{body}{sect}</w:body></w:document>'
    rel_items = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for n, href in enumerate(d.rels, 1):
        rel_items.append(f'<Relationship Id="rIdL{n}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                         f'Target="{escape(href, {chr(34): "&quot;"})}" TargetMode="External"/>')
    parts = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '</Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>',
        "docProps/core.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + x(title) + '</dc:title></cp:coreProperties>',
        "word/document.xml": document,
        "word/styles.xml": styles_xml(),
        "word/_rels/document.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rel_items) + "</Relationships>",
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():  # [Content_Types].xml を先頭に
            z.writestr(name, data.encode("utf-8"))
    return title


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Markdown を .docx に変換（標準ライブラリのみ）")
    ap.add_argument("paths", nargs="*", help="変換する .md（省略時は research/ docs/ blog/ 全部）")
    ap.add_argument("--out", default="exports", help="出力先ディレクトリ（既定 exports/）")
    args = ap.parse_args(argv)
    files = [Path(p) for p in args.paths] or sources()
    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    n = 0
    for f in files:
        f = f if f.is_absolute() else (Path.cwd() / f)
        if not f.exists():
            print(f"見つかりません: {f}", file=sys.stderr)
            return 1
        try:
            rel = f.resolve().relative_to(ROOT)
            dest = out_dir / rel.with_suffix(".docx")
        except ValueError:
            dest = out_dir / f.with_suffix(".docx").name
        build_docx(f.read_text(encoding="utf-8"), dest, f.stem)
        n += 1
        print(f"  {dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest}")
    print(f"{n} 件の .docx を出力しました: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
