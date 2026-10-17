---
name: studying-abroad-onboarding
description: studying-abroad リポジトリで作業を始める/引き継ぐとき、何から読むか知りたいときに使う。onboarding, handoff, 引き継ぎ, 最初に読む, 別PC, 新しいAI, 作業開始, start here.
---

# studying-abroad オンボーディング

公開リポジトリ。個人の支払い・資産・パスポート・予約番号・勤務先情報は絶対にコミットしない。

## 読む順序
1. `AGENTS.md`（規則の要約・コマンド）
2. `README.md`
3. `docs/05-public-data-policy.md`（必須）
4. `gh issue view 1 7 16`（1件ずつ）と `gh pr list`
5. 必要に応じて `docs/`、`research/`
6. `data/tasks.csv`、`data/expenses.csv`

## 次にやること
- 詳細手順は `docs/08-handoff.md`（最初の15分チェックリスト、タスクの見つけ方）。
- 調査なら `studying-abroad-research`、PR作成なら `studying-abroad-pr` を使う。
- 検証：`py scripts/validate_data.py` / `py scripts/check_public_data.py`（Linuxは `python3`）。
- 予約・購入・外部送信はユーザー承認が必要。mainへのpush・マージ禁止。
