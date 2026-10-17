---
name: studying-abroad-pr
description: studying-abroad でブランチ作成・コミット・PR作成・マージ前確認をするときに使う。PR, プルリク, ブランチ, CI, プライバシー確認, 公開データの確認, pull request, branch, privacy checklist.
---

# ブランチ・PR

## ルール
- ブランチ：`feat/<issue>-<slug>` / `research/<issue>-<slug>` / `docs/<slug>`。最新 `origin/main` から作る。
- 1 Issue = 1 PR。main直push・force-push・rebase・自動マージ禁止。**マージは人間**。
- `git add` は対象ファイルを指定（`-A`を避ける）。

## 検証（CIと同じ。Linuxは python3）
```
py scripts/validate_data.py
py scripts/check_public_data.py
py -m unittest discover -s tests
```
`py scripts/build_all.py` で生成物（AUTO ブロック・HTML・index.html）を再生成して差分を確認。

## マージ前プライバシー確認(#16)
- [ ] 個人の支払い・請求・資産・所得・税額がない
- [ ] パスポート・予約番号・領収書・住所・連絡先がない
- [ ] 勤務先の内部情報・契約・申請履歴がない
- [ ] 禁止列(`paid_jpy`, `evidence` 等)がない
- [ ] CSV・Markdown・生成HTML・画像・PR本文を目視確認した

## PR本文テンプレート
```
## 変更内容
## 調査根拠
## 公開データの確認(#16)
## 残課題
## 検証結果
```
`gh pr create --base main --title "[<種別>] ..."`。Issue番号を `Refs #N` で記載。マージはしない。
