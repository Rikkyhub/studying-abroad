# ダッシュボードの見方と更新方法

`index.html` は **CSV から生成する静的HTML**です。データはHTMLに埋め込まれているため、`file://` で直接開いても表示できます（外部ライブラリ・サーバー不要）。

```sh
py scripts/build_all.py          # 生成物をすべて更新（入口はこれ1つ）
py scripts/build_all.py --check  # 生成物が CSV/Markdown と一致するか検証（CIで実行）
```

Linux/macOS では `py` の代わりに `python3` を使います。

## 生成の流れ（2段階・順序固定）
`build_all.py` は次の順で実行します。担当ファイルが重ならないので、何度実行しても同じ結果になります（テストで確認）。

| 順 | スクリプト | 読むもの | 書くもの |
|---|---|---|---|
| 1 | `scripts/build.py` | `data/expenses.csv`・`funds.csv`・`fx.csv`・`tasks.csv`・`timeline.csv`・`articles.csv`・`meta.csv` | `README.md`・`docs/01〜03-*.md`・`blog/article-ideas.md` の `<!-- AUTO:... -->` ブロック（見積集計・月別・費目別・為替・タスク表など）。`index.html` は書かない |
| 2 | `scripts/build_html.py` | 上記のMarkdown（AUTO更新後）と `data/*.csv` | `research/`・`docs/`・`blog/` の `*.html`、`data/*.md|html`（CSVの表示用）、`docs/09-issue-map.*`、`index.html` の AUTO ブロック |

- 順序が逆だと、docs の HTML が AUTO ブロック更新前の内容になります。
- 手で HTML や AUTO ブロックを編集しても次回の生成で上書きされます。CIの `--check` が古い生成物を検出します。
- 計算ルールは [02-budget.md](02-budget.md) を参照。

## 表示内容（index.html）
- 今やること・未確認のこと：優先度1の未完了タスク
- 旅程（`timeline.csv`、月単位）・準備タスク（優先度順の先頭12件）・調査資料・場所と地図
- 通貨と円換算：`fx.csv` の参考レートと電卓
- 予算：`funds.csv` の予算目標（目標・上限・5月アフリカ周遊の内数）と、`build.py` の集計による費用の見積集計（低予算/標準/余裕の合計、見積と未確認の内訳、金額未入力の件数）
- 計画・記録（docs・blog・データのリンク）

支払い・実費・利用可能資金・残額は表示しません。表示する金額はすべて見積で、何かが支払済み・確定であることを意味しません。「未確認」は別枠で表示するだけで、何からも差し引きません。金額未入力の行は0円ではなく件数で示します。

## ダッシュボードを動かすCSV
- `data/expenses.csv`：費用の見積（区分は `見積`＝出典あり／`未確認`）。支払い・実績の列は置かない。期間は月単位のモデル値（月初〜月末）。
- `data/funds.csv`：予算目標のみ（type=予算）。個人の資金・残高は置かない。
- `data/fx.csv`：`currency,name_ja,unit,region,jpy_per_unit,rate_date,rate_kind,source`。`jpy_per_unit` は1単位あたりの円。集計（`build.py`）と換算表・電卓（`build_html.py`）が同じ値を使う。expenses.csv で使う通貨にレートが無い、または空欄だと `build.py` が問題として報告する（0円扱いにしない）。
- `data/pages.csv`：調査資料・計画の表。`refs` 列に根拠にした一次情報のURLを `;` 区切りで最大3件（http/https、資料の出典欄にあるURLだけを使う）。`issue` 列は表には出さず、保守者向けの [Issue対応表](09-issue-map.md) にだけ出る。`research/`・`docs/`・`blog/` の新しいページは、ここに行を足す（除外するページは `tests/test_site_audit.py` の除外リストに理由つきで書く）。
- `data/timeline.csv`：旅程の表（`id,period,title,status,summary,page_ids,sort`）。期間は「2027年2〜4月」のように**月単位**で書き、日単位の日付は書かない（`validate_data.py` が検出）。`page_ids` は pages.csv の `id`。
- `data/tasks.csv`：準備タスク。`issue` は表に出さない（Issue対応表に出る）。
- `data/places.csv`：「場所と地図」の表。公共の施設・名所・ショップだけを `maps_query` で書く（自宅・宿泊先・予約情報は書かない）。リンクは `https://www.google.com/maps/search/?api=1&query=...` に自動変換される。

## 為替レートの更新
1. 公開されている参考レート（現在はMUFGの対顧客外国為替相場の仲値TTM、https://www.murc-kawasesouba.jp/fx/index.php ）を確認する。
2. `data/fx.csv` の `jpy_per_unit`・`rate_date`（YYYY-MM-DD）・`rate_kind`・`source` を更新する。取得できない通貨は `jpy_per_unit` を空にする（表示は「未確認」。推測値は入れない）。
3. `py scripts/build_all.py` で集計・表・電卓を再生成する。
- これは参考レートで、現金両替・ATM・カードのレートには手数料や差額が加わり一致しない。通貨が違う金額の合計は円換算前には出さない。

## 公開に関する注意
リポジトリは公開状態。CSVには個人の支払い・資産・証憑、個人が特定される情報、予約番号、宿泊先住所を書かない（[公開データ方針](05-public-data-policy.md)）。個人の実績は非公開のNotionで管理する。`check_public_data.py` は禁止列・個人資金行を、`validate_data.py` は番号・メール・電話番号らしき値を検出してエラーにする。自動検査は補助で、目視確認も行う。

関連：[#7](https://github.com/Rikkyhub/studying-abroad/issues/7)、[#16](https://github.com/Rikkyhub/studying-abroad/issues/16)
