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

## 公開に関する注意
リポジトリは公開状態。実費CSVには個人が特定される情報、領収書原本、宿泊先住所などを書かない。個人管理向けの証憑は暗号化された非公開保管先で管理する。

関連：[#7](https://github.com/Rikkyhub/studying-abroad/issues/7)
