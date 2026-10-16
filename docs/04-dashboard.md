# ダッシュボードの見方と更新方法

`index.html` は **`scripts/build.py` が CSV から生成する静的HTML**です。データはHTMLに埋め込まれているため、`file://` で直接開いてもスマートフォンでもそのまま表示できます（外部ライブラリ・サーバー不要）。

```sh
python3 scripts/build.py          # CSV → docs/*.md の AUTO ブロック・README・index.html を再生成
python3 scripts/build.py --check  # 生成物が CSV と一致するか検証（CIで実行）
```

## 表示内容
- お金の全体像：総費用予測（低予算/標準/余裕）、支払済み（証憑確認済み/暫定）、今後必要額、利用可能資金、予算250万/300万円との差、実費
- 次にやること・準備の進捗（tasks.csv）
- 月別・費目別の費用グラフ（支払済み/これから）と表
- スケジュール（timeline.csv）・未確定項目・費用明細（区分でフィルタ）・記事候補・データ検証結果

## 数値がずれない仕組み
- 金額は **data/expenses.csv だけ**から計算し、README・docs・index.html の数値はすべて同じ計算結果を埋め込む。
- 手でHTMLやAUTOブロックを編集しても次回の生成で上書きされる。CIの `--check` が古い生成物を検出する。
- 計算ルールは [02-budget.md](02-budget.md) を参照。

## 公開に関する注意
リポジトリは公開状態。CSVには個人が特定される情報、領収書原本、予約番号、宿泊先住所を書かない。`evidence` 列には非公開保管先でのラベル（例 `private:2026-10_PINES_invoice`）だけを書く。`validate_data.py` は番号・メール・電話番号らしき値を検出してエラーにする。

関連：[#7](https://github.com/Rikkyhub/studying-abroad/issues/7)
