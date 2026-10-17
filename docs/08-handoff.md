# AI・別PC向け 引き継ぎ手順書

別のAI（Claude Code、Codex等）や別のPCで作業を引き継ぐための手順。要点は [AGENTS.md](../AGENTS.md)、ここはその詳細版。

## 1. セットアップ
```
git clone https://github.com/Rikkyhub/studying-abroad.git
cd studying-abroad
gh auth login        # アカウント: Rikkyhub
```
- Python 3.12（Windowsは `py`、Linux/macOSは `python3`）。追加パッケージは不要。
- 改行はLF。Windowsでは `git config core.autocrlf input` を推奨。

## 2. 最初の15分チェックリスト
1. [ ] `AGENTS.md` を読む
2. [ ] `README.md` を読む（計画の概要、お金の管理原則）
3. [ ] `docs/05-public-data-policy.md` を読む（**必須**）
4. [ ] `git fetch origin && git log --oneline -10`
5. [ ] `gh issue view 1` / `7` / `16`、`gh pr list`（未マージPRと重複しないか確認）
6. [ ] `data/tasks.csv` を眺め、状態が `not_started` / `in_progress` / `blocked` のものを把握
7. [ ] 検証コマンドを一度流して現状がgreenか確認

## 3. 次の作業の見つけ方
- `gh issue list`：優先度 P0 → P1 の順。Issueの受け入れ条件を読む。
- `gh pr list`：同じIssueのPRが既にあれば、それを置き換えるのか補うのかを確認（「main基準の置き換え版」PRが存在する）。
- `data/tasks.csv`：`priority`、`due_date`、`issue_url` から着手候補を探す。
- 迷ったらユーザーに確認する。予約・購入・外部送信は必ず事前承認。

## 4. 調査タスクの流れ（research）
1. 最新mainから `research/<issue>-<slug>` ブランチを作る。
2. 既存の `research/*.md` と `research/sources.md` を読み、重複と矛盾を避ける。
3. 公式情報から調べる。各情報に URL・確認日・適用年度・通貨・対象人数・含まれる内容を付ける。
4. 未確認は「未確認」と書く。2026年の情報を2027年として書かない。
5. 末尾に検索ログを書く（テンプレートは `.claude/skills/studying-abroad-research/template.md`）。
6. 個人情報が入っていないか見直す。
7. 検証コマンドを流し、PRを出す（第6節）。

## 5. データ(CSV)変更タスクの流れ
1. `feat/<issue>-<slug>` ブランチを作る。
2. `data/tasks.csv` / `data/expenses.csv` を編集。費用は**調査価格・匿名モデル**のみ。金額は `low_local`/`std_local`/`high_local`（見積）で、区分は `見積`（出典あり）か `未確認`。
3. 禁止列(`paid_jpy`, `evidence`, `receipt` 等)や個人の支払い値を入れない。`py scripts/check_public_data.py` で確認。
4. `py scripts/build_all.py` で再生成し、`py scripts/validate_data.py`、`py -m unittest discover -s tests`。
5. ダッシュボード(`index.html`)は静的HTMLなので、ブラウザで直接開いて確認する（`file://` で表示できる）。

## 6. HTML・DOCXの再生成
- 正本はMarkdown/CSV。HTMLなどの生成物は手で直さない。
- `py scripts/build_all.py`（`build.py` → `build_html.py` の順）。CIは `py scripts/build_all.py --check` で最新かを確認する。
- Word出力は `py scripts/export_docx.py`（[07-export.md](07-export.md)）。コミットしない。
- 生成物の差分も目視でプライバシー確認する。

## 7. PRの出し方
1. `git status` で意図したファイルだけか確認。
2. `git add <ファイル>`（`-A` は避ける）→ `git commit`（メッセージ末尾に共著行がある環境の指示に従う）。
3. `git push -u origin <branch>`（mainには絶対にpushしない）。
4. `gh pr create --base main`。本文は `変更内容` / `調査根拠` / `公開データの確認` / `残課題` / `検証結果`。テンプレートは `.claude/skills/studying-abroad-pr/SKILL.md`。
5. **マージしない**。人間のレビューを待つ。

## 8. 完了の定義
- Issueの受け入れ条件を満たす（満たせない点は「残課題」に明記）。
- 検証コマンドが全て通る。CIがgreen。
- 公開データの確認(#16)を目視で実施し、PR本文に書いた。
- 出典・確認日・未確認の区別・検索ログが揃っている。

## 9. やってはいけないこと
- mainへの直接push、force-push、rebase、自動マージ、PRのマージ。
- 個人の支払い・資産・パスポート・予約番号・勤務先内部情報のコミット（Issue・PR本文・画像も同様）。
- ユーザー承認なしの予約・購入・支払い・外部送信。
- 生成HTMLの手編集。出典のない数値の記載。履歴の書き換え。

## 10. FAQ・過去の落とし穴
- **Q. なぜ `paid_jpy` や `evidence` 列が禁止？** 公開repoに本人の実際の支払い額・証憑が載る事故(#16)があったため。公開CSVは「調査価格・モデル」だけ。`scripts/check_public_data.py` が列名を検査するが、値の文脈は目視確認が必要。履歴に残った情報は通常のコミットでは消えない。
- **Q. 実際の支払額や残高、個別の期限はどこで管理する？** 非公開のNotionで管理する（本人確認済みの方針）。公開リポジトリには置かず、公開側は「公式の一般料金・匿名モデルの試算・一般的な期限の目安」だけにする。Notionは本人が管理するので、AIは値の提供を本人に依頼し、公開の場（コミット・Issue・PR本文・画像）へ転記しない。ドキュメントには「非公開Notion」と書くだけで、URLやページIDは載せない。確認できていない支払いを、支払済みとして集計に入れない。
- **Q. Windowsでファイルが壊れた。** bashのheredocでPythonコードや `\n` を含む文字列を書くと改行が化ける。ファイル作成・編集はEdit/Writeツールで。Pythonは `py`。
- **Q. サブエージェントが止まった/出力がない。** 長時間の作業では途中状態をWIPコミットして残す。再開時はブランチの `git log` と差分から続きを判断し、重複作業を避ける。
- **Q. 同じIssueに複数PRがある。** 古いPRは旧mainが基準。「main基準の置き換え版」が出ている場合はそちらを優先し、古いPRの扱いはユーザーに確認する。
- **Q. mainに無いファイルを参照してよい？** 未マージPRのファイルに依存しない。参照するなら「ある場合」と断る。

## 11. skillsの使い方
`.claude/skills/` にリポジトリ専用skillsをgit管理している。
| skill | 用途 |
|---|---|
| `studying-abroad-onboarding` | 最初に何を読むか |
| `studying-abroad-research` | 調査レポートの手順と品質基準（`template.md` つき） |
| `studying-abroad-pr` | ブランチ・PR本文・マージ前プライバシー確認・CI |

- Claude Code：`.claude/skills` を自動認識する。
- 他のAI/ツール：自動認識されない場合、`AGENTS.md` と各 `SKILL.md` を直接読み込ませる。
- `.claude/worktrees/` と `settings.local.json` は `.gitignore` 済み（ローカル状態）。
