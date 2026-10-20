# -*- coding: utf-8 -*-
"""生成物をまとめて更新する入口。使い方:  py scripts/build_all.py [--check]

順序（この順でないと docs の HTML が AUTO ブロックの更新前の内容になる）:
  1. scripts/build.py       data/*.csv -> README.md・docs/*.md・blog/*.md の AUTO ブロック（集計）
  2. scripts/build_html.py  Markdown/CSV -> *.html、index.html（ダッシュボード）
  3. scripts/build_maps.py  data/route_points.csv・routes.csv・data/geo -> maps/*.html（世界地図・アフリカ地図）
  4. scripts/build_single.py 上の生成物を連結 -> all.html（全ページを1枚にした閲覧用。Vercel などの静的ホスティング用）

--check は書き込まず、どれかの生成物が CSV/Markdown と一致しなければ失敗する（CI 用）。
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["build.py", "build_html.py", "build_maps.py", "build_single.py"]


def main(argv=None):
    extra = [a for a in (argv if argv is not None else sys.argv[1:]) if a == "--check"]
    rc = 0
    for step in STEPS:
        print(f"== {step} {' '.join(extra)}".rstrip(), flush=True)
        r = subprocess.run([sys.executable, str(HERE / step), *extra])
        if r.returncode:
            rc = r.returncode
            if not extra:
                break
    return rc


if __name__ == "__main__":
    sys.exit(main())
