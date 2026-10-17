# -*- coding: utf-8 -*-
"""Markdown（正本）から HTML / Word を生成する入口。

使い方（リポジトリのルートで実行）:
    py scripts/export.py html            AUTO ブロックと HTML を再生成（scripts/build_all.py）
    py scripts/export.py docx [paths...] Word を exports/ に出力
    py scripts/export.py all  [paths...] 両方
    オプション: --out DIR（docx の出力先。既定 exports/）
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_all  # noqa: E402
import export_docx  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", choices=["html", "docx", "all"])
    ap.add_argument("paths", nargs="*", help="docx 対象の .md（省略時は全件）")
    ap.add_argument("--out", default="exports")
    a = ap.parse_args(argv)
    rc = 0
    if a.target in ("html", "all"):
        rc = build_all.main([])  # build.py（AUTO ブロック）→ build_html.py（HTML・index.html）の順
    if rc == 0 and a.target in ("docx", "all"):
        rc = export_docx.main([*a.paths, "--out", a.out])
    return rc


if __name__ == "__main__":
    sys.exit(main())
