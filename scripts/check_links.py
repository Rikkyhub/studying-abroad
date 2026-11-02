"""Check that relative links in Markdown/HTML point to files that exist. Run: python3 scripts/check_links.py

外部URLは検証しない（ネットワーク不要・CIを安定させるため）。外部URLの確認日は research/sources.md で管理する。
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "private", "receipts", "secrets", "node_modules", "scripts"}  # scripts/ のテンプレートは生成前の相対パス
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HTML_LINK = re.compile(r"""(?:href|src)=["']([^"']+)["']""")


def files():
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".html") and not SKIP_DIRS.intersection(p.relative_to(ROOT).parts):
            yield p


def main():
    errors = []
    checked = 0
    for p in files():
        text = p.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)  # コードブロック内は対象外
        pattern = HTML_LINK if p.suffix == ".html" else MD_LINK
        for target in pattern.findall(text):
            if re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", target) or "${" in target:
                continue
            path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not path:
                continue
            checked += 1
            if not (p.parent / path).resolve().exists():
                errors.append(f"{p.relative_to(ROOT)}: broken link -> {target}")
    for e in errors:
        print("ERROR:", e, file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: {checked} local links OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
