# AGENTS.md — AI・別PC向けの入口

このファイルは Claude Code / Codex / その他のAIエージェントが最初に読む入口。詳細な手順は [docs/08-handoff.md](docs/08-handoff.md)。

## このリポジトリは何か
2027年2〜7月の海外留学（フィリピン・バギオ → アフリカ周遊 → ケープタウン等）の**準備・費用・調査**を管理する**公開リポジトリ**（Rikkyhub/studying-abroad）。調査資料(`research/`)、計画(`docs/`)、地域別ページ(`areas/`)、静的トップページ(`index.html`)、生成用の内部データ(`data/*.csv`)で構成。国の優劣を比較するサイトではない。

## 最重要：公開リポジトリのプライバシー規則
正本は [docs/05-public-data-policy.md](docs/05-public-data-policy.md)。要約：
- 公開してよい：学校・事業者の一般料金と条件（公式URL・確認日・適用年・通貨つき）、匿名モデルの試算、個人を特定しない調査。
- **コミット禁止**：個人の支払い・請求履歴、資産・所得・税額、パスポート情報、予約番号・識別子、領収書画像、住所・連絡先、勤務先内部資料・契約・申請履歴、他人の情報、限定共有URL。
- `paid_jpy` / `evidence` など個人の支払い・証憑を示す列は `data/expenses.csv` に作らない（Issue #16）。
- **個人の実績は非公開のNotionで管理する**（本人確認済みの方針）。実際の支払額、残高、領収書、個別の期限、予約・契約の状況はNotionにだけ置き、リポジトリには書かない。公開側に残すのは、公式の一般料金・匿名モデルの試算・一般的な期限の目安だけ。ドキュメントでは「非公開Notion」と書くにとどめ、URLやページIDは載せない。Notionの内容をAIが必要とするときは、本人に値の提供を依頼し、公開の場に転記しない。
- 自動検査は補助。CSV・Markdown・生成HTML・PR本文・画像を目視でも確認する。
- 一度pushした情報は履歴に残る。履歴の書き換えは別途承認が必要で、勝手に行わない。

## 読む順序
1. この `AGENTS.md`
2. `README.md`（計画の概要・お金の管理原則）
3. `docs/05-public-data-policy.md`
4. 進行中の作業：Issue #1（全体）・#7（予算・基盤）・#16（プライバシー）と `gh pr list`
5. 必要に応じて `docs/` と `research/`（`docs/08-handoff.md` に手順の詳細）
6. 地域別ページ `areas/*.md`（読者向け）。元データは内部入力 `data/*.csv`（保守者のみ）

## 正本と生成物
| 種別 | 扱い |
|---|---|
| `areas/*.md`, `research/*.md`, `docs/*.md` | **正本**（ここを編集する。読者が見るのはこれらと生成HTML） |
| `data/*.csv` | 生成スクリプトの**内部入力**（読者向けにはリンクしない。費用・タスク・日程・資料・場所・為替。行を足すときは `region` 列も付ける） |
| `index.html` ほかHTML、Markdown内の AUTO ブロック | 閲覧用。生成スクリプトがある場合は手で直さず再生成する |

## 検証コマンド
Windows は `py`、Linux/macOS は `python3`（CIは Python 3.12・追加依存なし）。
```
py scripts/validate_data.py
py scripts/check_public_data.py
py scripts/build_all.py --check    # 生成物（README・docs の AUTO ブロック、全HTML、index.html）が最新か
py scripts/check_links.py
py -m unittest discover -s tests
```
CSV・Markdown を変えたら `py scripts/build_all.py` で再生成して同じコミットに含める（`build.py` が集計の AUTO ブロック、続けて `build_html.py` が HTML と index.html を生成する。生成物は手で編集しない）。Word 出力は `py scripts/export_docx.py`（[docs/07-export.md](docs/07-export.md)）。

## GitHub運用ルール
- ブランチ名：`feat/<issue番号>-<slug>`、調査は `research/<issue番号>-<slug>`、文書は `docs/<slug>`。
- 1 Issue = 1 PR。`main` への直接push、force-push、rebase、自動マージは禁止。**マージは人間のレビュー後**。
- PR本文の節：`変更内容` / `調査根拠` / `公開データの確認` / `残課題` / `検証結果`。
- 予約・購入・支払い・外部への送信（メール、問い合わせ、投稿）は、**ユーザーの明示的な承認なしに行わない**。

## 調査の品質規則
- 公式情報を最優先。各情報に URL・確認日・適用年度・通貨・対象人数・含まれる内容を記す。
- 確認できなかったものは「未確認」と明記し、推測で埋めない。
- 各レポートの末尾に検索ログ（何を検索し何が見つかったか）を残す。
- 2026年のイベント・料金を2027年のものとして書かない。

## Windows の注意
- Python は `py`。bashのheredocで `\n` を含むPythonを書くと壊れるので、ファイル作成はEdit/Writeツールを使う。
- 改行は LF。
- エージェント用ワークツリー(`.claude/worktrees/`)はコミットしない（`.gitignore` 済み）。

## 専用skills（`.claude/skills/`）
`studying-abroad-onboarding` / `studying-abroad-research` / `studying-abroad-pr`。Claude Codeは自動認識。他のAIは各 `SKILL.md` を直接読む。
