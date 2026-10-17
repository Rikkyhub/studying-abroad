# ダッシュボードの見方と更新方法

`index.html` は **`scripts/build.py` が CSV から生成する静的HTML**です。データはHTMLに埋め込まれているため、`file://` で直接開いても表示できます（外部ライブラリ・サーバー不要）。

```sh
python3 scripts/build.py          # CSV → docs/*.md の AUTO ブロック・README・index.html を再生成
python3 scripts/build.py --check  # 生成物が CSV と一致するか検証（CIで実行）
```

Windows では `python3` の代わりに `py` を使います。

## 表示内容
- お金の全体像（公開用の匿名モデル）：見積合計（低予算/標準/余裕）、うち見積（出典あり）とうち未確認（推定）の内訳、金額未入力の件数、予算目標250万/300万円との差、5月アフリカ周遊の配分
- 次にやること・準備の進捗（tasks.csv）
- 月別（見積/未確認の内訳）・費目別の見積グラフと表
- スケジュール（timeline.csv）・未確認の費目・費用明細（区分でフィルタ）・記事候補・データ検証結果

支払い・実費・利用可能資金・残額の表示はありません。表示する金額はすべて見積で、何かが支払済み・確定であることを意味しません。

## 数値がずれない仕組み
- 金額は **data/expenses.csv だけ**から計算し、README・docs・index.html の数値はすべて同じ計算結果を埋め込む。
- 手でHTMLやAUTOブロックを編集しても次回の生成で上書きされる。CIの `--check` が古い生成物を検出する。
- 計算ルールは [02-budget.md](02-budget.md) を参照。

## ダッシュボードを動かすCSV
`index.html` の表は `py scripts/build_html.py` が次のCSVから埋め込む（CSVを読み込まないので `file://` でも表示できる）。
- `data/pages.csv`：調査資料・計画の表。`refs` 列に根拠にした一次情報のURLを `;` 区切りで最大3件（http/https、資料の出典欄にあるURLだけを使う）。`issue` 列は表には出さず、保守者向けの [Issue対応表](09-issue-map.md) にだけ出る。
- `data/timeline.csv`：旅程の表。`page_ids` は pages.csv の `id`。
- `data/tasks.csv`：準備タスク。`issue_url` は表に出さない（Issue対応表に出る）。
- `data/places.csv`：「場所と地図」の表。公共の施設・名所・ショップだけを `maps_query` で書く（自宅・宿泊先・予約情報は書かない）。リンクは `https://www.google.com/maps/search/?api=1&query=...` に自動変換される。
- `data/fx.csv`：「通貨と円換算」の表と電卓。`jpy_per_unit` は1単位あたりの円。

## 為替レートの更新
1. 公開されている参考レート（現在はMUFGの対顧客外国為替相場の仲値TTM、https://www.murc-kawasesouba.jp/fx/index.php ）を確認する。
2. `data/fx.csv` の `jpy_per_unit`・`rate_date`（YYYY-MM-DD）・`rate_kind`・`source` を更新する。取得できない通貨は `jpy_per_unit` を空にする（表示は「未確認」。推測値は入れない）。
3. `py scripts/build_html.py` で表・電卓のデータを再生成する。
- これは参考レートで、現金両替・ATM・カードのレートには手数料や差額が加わり一致しない。通貨が違う金額の合計は出さない。

## 公開に関する注意
リポジトリは公開状態。CSVには個人の支払い・資産・証憑、個人が特定される情報、予約番号、宿泊先住所を書かない（[公開データ方針](05-public-data-policy.md)）。`check_public_data.py` は禁止列・個人資金行を、`validate_data.py` は番号・メール・電話番号らしき値を検出してエラーにする。自動検査は補助で、目視確認も行う。

関連：[#7](https://github.com/Rikkyhub/studying-abroad/issues/7)、[#16](https://github.com/Rikkyhub/studying-abroad/issues/16)
