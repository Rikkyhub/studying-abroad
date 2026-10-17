# HTML・Word への変換（Markdown が正本）

このリポジトリの内容の正本は Markdown（`research/`・`docs/`・`blog/`）です。HTML と Word（.docx）は、Python スクリプトで Markdown から自動生成する派生物です。直接編集せず、必ず Markdown を直してから再生成してください。

## 使い方

リポジトリのルートで実行します（Windows は `py`、他は `python3`）。追加インストールは不要で、標準ライブラリだけで動きます。

| コマンド | 内容 |
|---|---|
| `py scripts/export.py html` | 全 Markdown と `data/*.csv` から HTML を再生成 |
| `py scripts/export.py docx` | `research/`・`docs/`・`blog/` の全 Markdown を `exports/` に Word 出力 |
| `py scripts/export.py docx docs/02-budget.md` | 指定した Markdown だけを Word 出力 |
| `py scripts/export.py all` | HTML と Word の両方 |
| `py scripts/export.py docx --out C:\temp\out` | 出力先を変更（既定は `exports/`） |

個別に実行する場合は `py scripts/build_all.py`（集計の AUTO ブロック → HTML。`--check` で最新かを確認）と `py scripts/export_docx.py` を使います。HTML だけなら `py scripts/build_html.py` ですが、AUTO ブロックを更新していないと古い内容が HTML に出るため、通常は `build_all.py` を使います。

## コミットするもの・しないもの

- HTML: 生成物ですがコミットします（GitHub Pages 等でそのまま読めるようにするため）。`py scripts/build_all.py --check` が Markdown/CSV との不一致を検出します。
- Word（.docx）: コミットしません。`exports/` は `.gitignore` 済みで、必要なときに手元で生成します。
- 公開データの扱いは [公開データと非公開データの分離](05-public-data-policy.md) に従います。個人の支払い・資産・契約情報は Markdown に書かないため、変換結果にも含まれません。

## 対応している記法

見出し、段落、太字・斜体・インラインコード、リンク、箇条書きと番号付きリスト（入れ子可・チェックボックス）、表（ヘッダ行と罫線）、引用、コードブロック、区切り線。

Word では日本語フォントに游ゴシック（Yu Gothic）を指定します。外部リンクはハイパーリンクになり、リポジトリ内の相対リンクは「文字（参照先パス）」の表記になります。

## 制限事項

- 画像、脚注、HTML タグ（`<br>` を除く）、入れ子の引用、表内の改行は未対応です。
- 目次・ページ番号・ヘッダ／フッタは付きません。
- 表の列幅は均等割りです。列数の多い表は Word 上で調整してください。
- Word（または LibreOffice）での表示確認は手動です。自動テスト（`tests/test_export_docx.py`）は zip 構造・XML の整合性・見出し／表／リスト・日本語と特殊文字（`& < >`）の保持を検証します。
