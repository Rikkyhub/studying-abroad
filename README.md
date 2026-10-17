# studying-abroad — 2027年2〜7月 海外留学・アフリカ周遊

> **目的**：フィリピン留学、5月のアフリカ周遊、6〜7月の第2か国留学を**6か月全体**で管理する。国同士を評価・比較するサイトではない。準備・費用・実体験を蓄積して、後日ブログ記事に利用する。

## 現時点の計画（2026-10-16時点）

| 期間 | 内容 | 状態 |
|---|---|---|
| 2027/02/06〜5月初旬 | バギオ PINES、2/8授業開始、12週間 | 留学先・コース決定。支払証憑と終了日を要確認 |
| 2027/05 | アフリカ周遊、約1か月 | 検討中、予算目安60万円 |
| 2027/06〜07 | ケープタウンを候補とする語学留学8週間 | 未確定。学校、入国・就学条件の確認が必要 |
| 2027/08 | 前後観光・帰国・復職準備 | 仮計画、休職/復職日の承認状況を照合 |

PINESのコース予定：Power ESL5（4週）→ Intensive ESL（8週）。

## お金の管理原則

- **目標250万円、上限300万円**は6か月全体の予算目標で、利用実績ではない。
- 複数通貨の元金額を保持し、円換算はレートと基準日を記載する。
- 予算、見積、請求額、支払実績、現地実費は区別する。
- 交通・宿・保険・手続・日本に残る固定費も含める。
- ブログ原稿と費用の元データは別管理。個人情報・予約番号を公開しない。

公開データには本人の実際の支払い・資産・契約内容は載せず、調査価格とモデル試算だけを掲載する。

## 作業の入口

- [全体Issue #1](https://github.com/Rikkyhub/studying-abroad/issues/1)
- [ビザ・再入国 #2](https://github.com/Rikkyhub/studying-abroad/issues/2)
- [ダイビング #3](https://github.com/Rikkyhub/studying-abroad/issues/3)
- [観光 #4](https://github.com/Rikkyhub/studying-abroad/issues/4)
- [食費・スーパー #5](https://github.com/Rikkyhub/studying-abroad/issues/5)
- [冬服 #6](https://github.com/Rikkyhub/studying-abroad/issues/6)
- [総予算・準備・ブログ記録 #7](https://github.com/Rikkyhub/studying-abroad/issues/7)
- [治安・健康 #8](https://github.com/Rikkyhub/studying-abroad/issues/8)

**重要**：リポジトリの一般公開を前提とする。パスポート情報、宿泊予約番号、領収書画像、勤務先内部資料、住所はコミットしない。

## Webで見られる計画画面

- [ダッシュボード](index.html)：月別計画・入力済み費用小計・準備タスク・調査資料へのリンク。ブラウザで使う場合はリポジトリ内で `python3 -m http.server 8000` を起動して `http://localhost:8000` を開く（GitHub Pagesは**未設定**）。
- [ダッシュボードの更新方法](docs/04-dashboard.md)
- CSVの検証：`python3 scripts/validate_data.py`。GitHub ActionsでもPR時に検証。

現時点の研究資料は完成版ではない。公式で確認できた情報と未確認の候補を区別し、各Issueで継続調査する。

## AI・別PCで作業する場合

[AGENTS.md](AGENTS.md)（入口・規則）→ [docs/08-handoff.md](docs/08-handoff.md)（引き継ぎ手順書）。専用skillsは `.claude/skills/`。
