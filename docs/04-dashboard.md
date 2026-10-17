# ダッシュボードの見方と更新方法

`index.html` は追加ライブラリ不要の静的HTML。ローカルではブラウザの `file://` 直開きだとCSV読み込みがブロックされる場合があるため、リポジトリのルートで以下を起動する。

```sh
python3 scripts/validate_data.py
python3 -m http.server 8000
```

続いて http://localhost:8000/ をブラウザで開く。GitHub Pages等の静的ホスティングに配置した場合も同様に使える（**GitHub Pages公開は未設定**）。

## 更新
- `data/expenses.csv` の1費用につき1行追加。通貨がJPY以外の場合 `fx_jpy_per_unit` がない費用は円集計に含まれない。
- 表示する「登録済み支出の参考小計」は各行の**実費→全額見積→支払額**の優先順位で1回のみ取り込む。支払額自体は別枠で集計。二重加算を避ける。
- **これは入力済み分の参考小計であり6か月総額ではない**。CSVが完成しても、上限からの差額計算には国内費・予備費・未計上の支出がないかを確認する。
- `data/tasks.csv` の状態は `not_started` / `in_progress` / `blocked` / `done`。

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
リポジトリは公開状態。実費CSVには個人が特定される情報、領収書原本、宿泊先住所などを書かない。個人管理向けの証憑は暗号化された非公開保管先で管理する。

関連：[#7](https://github.com/Rikkyhub/studying-abroad/issues/7)
