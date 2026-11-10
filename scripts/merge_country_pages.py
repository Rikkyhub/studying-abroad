# -*- coding: utf-8 -*-
"""国別ページ（countries/<slug>.md）に、深掘り調査（research/country-<slug>.md）を統合する一度きりの移行スクリプト。

方針（1国1ページ）:
- 先頭は今の国別ページの「概要・地図・主な観光地・食べ物・ビザ・安全・行き方」を残す。
- 続けて『旅程の目安』の節に、深掘りの章（結論・日数・モデルコース・季節・接続・費用・評価）を載せる。
- ビザ・安全は、同じ節の中に『詳細：…』として深掘りの内容を足す（節を二重にしない。情報は消さない）。
- 未確認・出典・調査ログは1節ずつにまとめ、深掘り側は『詳細（旧深掘り調査）』として続ける。
- 深掘り側の見出しの章番号（「## 3. 」など）は外し、見出しを1段下げる。
使い方: py scripts/merge_country_pages.py <slug> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEEP_SEPARATE = ("入国", "制度", "安全", "未確認", "出典", "検索ログ", "調査ログ")
TAIL_KEYS = ("未確認", "出典", "調査ログ")


def split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    parts = re.split(r"(?m)^## ", text)
    secs = []
    for p in parts[1:]:
        title, _, body = p.partition("\n")
        secs.append((title.strip(), body))
    return parts[0], secs


def strip_num(t: str) -> str:
    return re.sub(r"^[0-9０-９]+(?:-[0-9]+)?[.．、]?\s*", "", t).strip()


def demote(body: str) -> str:
    return re.sub(r"(?m)^(#{3,5}) ", lambda m: "#" + m.group(1) + " ", body)


def has(t: str, keys) -> bool:
    return any(k in t for k in keys)


def merge(slug: str) -> str:
    a = (ROOT / "countries" / f"{slug}.md").read_text(encoding="utf-8")
    bp = ROOT / "research" / f"country-{slug}.md"
    if not bp.exists():
        return a
    b = bp.read_text(encoding="utf-8")
    ahead, asecs = split_sections(a)
    _, bsecs = split_sections(b)
    plan, extra = [], []
    for title, body in bsecs:
        t = strip_num(title)
        (extra if has(t, KEEP_SEPARATE) else plan).append((t, body))

    front = [(t, bd) for t, bd in asecs if not has(t, TAIL_KEYS)]
    tail = [(t, bd) for t, bd in asecs if has(t, TAIL_KEYS)]

    merged = []
    for t, bd in front:
        keys = ("入国", "制度") if has(t, ("ビザ", "入国")) else (("安全",) if has(t, ("安全",)) else ())
        for et, eb in [(x, y) for x, y in extra if keys and has(x, keys)]:
            bd = bd.rstrip("\n") + f"\n\n### 詳細：{et}\n" + demote(eb).rstrip("\n")
        merged.append((t, bd))

    tail_out = []
    for key, title in (("未確認", "未確認事項"), ("出典", "出典一覧"), ("ログ", "調査ログ")):
        a_part = [bd for t, bd in tail if (key in t) or (key == "ログ" and "調査ログ" in t)]
        b_part = [bd for t, bd in extra if (key in t) or (key == "ログ" and has(t, ("検索ログ", "調査ログ")))]
        if a_part or b_part:
            body = "\n\n".join(x.rstrip("\n") for x in a_part)
            if b_part:
                body += ("\n\n" if body else "") + "### 詳細（旧深掘り調査）\n" + "\n\n".join(demote(x).rstrip("\n") for x in b_part)
            tail_out.append((title, body))

    out = [ahead.rstrip("\n"), ""]
    for t, bd in merged:
        out += [f"## {t}", bd.rstrip("\n"), ""]
    if plan:
        out += ["## 旅程の目安（日数・モデルコース・季節・費用・評価）", "",
                "> 日数・モデルコース・季節・費用・評価をまとめた節です（旧『深掘り調査』を統合）。数値は推計を含み、2027年の確定値ではありません。", ""]
        for t, bd in plan:
            out += [f"### {t}", demote(bd).rstrip("\n"), ""]
    for t, bd in tail_out:
        out += [f"## {t}", bd.rstrip("\n"), ""]
    return "\n".join(out).rstrip("\n") + "\n"


def main() -> int:
    for slug in [x for x in sys.argv[1:] if not x.startswith("--")]:
        text = merge(slug)
        (ROOT / "countries" / f"{slug}.md").write_text(text, encoding="utf-8", newline="\n")
        print(slug, len(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
