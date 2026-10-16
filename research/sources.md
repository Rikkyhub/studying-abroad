# 一次資料・調査ログ

最終確認：2026-10-17。Issue別の詳細な出典一覧・調査ログは各レポート末尾にある（例：[safety-and-health.md](safety-and-health.md) §8・§9）。公式サイト上の料金でも**2027年価格・空き状況・制度改定を保証しない**。サイトの利用条件・対象者（現地住民限定等）を読む。

| 分野 | 出典 | 確認したこと | 確認日 | 留意事項 |
|---|---|---|---|---|
| PH入国 | https://tokyo.philembassy.net/en/consular-section/services/visa/visa-free-entry-for-temporary-visits/ | 対象国の30日短期査証免除・有効な復路/第三国航空券 | 2026-10-16 | 語学就学・延長は別要件 |
| PH延長 | https://immigration.gov.ph/visas/visa-waiver/ | 30日免除後の初回29日Waiver | 2026-10-16 | 12週を完了する後続手続を学校確認 |
| PH SSP | https://immigration.gov.ph/services/special-study-permit/ | 非学位学習の許可制度 | 2026-10-16 | 公開料金は2014年更新表記で古い |
| PHオンライン | https://e-services.immigration.gov.ph/ | SSP/延長などの手続分類 | 2026-10-16 | 本人/学校の役割未確認 |
| SA東京大使館 | https://dirco.gov.za/japan/frequently-asked-questions/ | 日本旅券・観光/商用90日未満査証免除 | 2026-10-16 | 就学や再入国に一律適用しない |
| SA東京大使館 | https://dirco.gov.za/japan/immigration-visa-info/ | Study Visa、旅券余白、資金/航空・黄熱病案内 | 2026-10-16 | 国籍/在留区分に応じた適用要確認 |
| PHダイビング | https://diveunion.com.ph/ | La Unionのコース料金・海洋保護区料・時期 | 2026-10-16 | フルレンタル/ダイブ本数未確認 |
| ZAダイビング | https://piscesdivers.co.za/reef-and-kelp/ | 2ガイドダイブ＋レンタル、ZAR3600 | 2026-10-16 | 2027価格は不明 |
| ZAダイビング | https://piscesdivers.co.za/wreck-and-reef/ | 2ガイドダイブ＋レンタル、ZAR3200 | 2026-10-16 | 2027価格は不明 |
| ZAダイビング | https://www.diveschoolcapetown.co.za/fun-dives/scuba-shoredives/ | 2ダイブ、レンタル、ZAR2950 | 2026-10-16 | 送迎地域を要確認 |
| ZAダイビング | https://piscesdivers.co.za/guided-shore-dives/ | 水温12〜18°C、運営上の注意書き | 2026-10-16 | アザラシダイブ停止情報の再確認 |
| バギオ観光 | https://visita.baguio.gov.ph/park-tickets/20 | The Mansionの無料入場の掲示 | 2026-10-16 | 2027営業条件は不明 |
| ケープタウン冬 | https://www.capetown.travel/the-best-time-of-year-to-visit-cape-town/ | 冬季気温/降雨日、観光季節感 | 2026-10-16 | 2027予報ではない |
| ケープタウン観光 | https://www.capetown.travel/100-things-to-do-in-winter-in-cape-town/ | 冬季の観光候補・現地住民向け特別料金と区別 | 2026-10-16 | キャンペーンは2026年 |
| ケープタウン治安 | https://www.anzen.mofa.go.jp/od/ryojiMailDetail.html?keyCd=157521 | 在ケープタウン領事事務所の犯罪注意喚起 | 2026-10-16 | 原通知は2025-06-07 |
| 潜水後の標高 | https://world.dan.org/health-medicine/health-resources/diseases-conditions/flying-after-diving/ | DANの標高上昇/減圧症、飛行前水面休息の考え方 | 2026-10-16 | バギオへのバス移動には個別判断が必要 |

### 引き続き調査
- 南アでの8週間語学留学の適切な許可と5〜8月の再入国日数：**大使館からの個別回答なし**。
- バギオ起点の現実的な土日交通便とショップの総額、学校門限。
- スーパー実売の数量・値段、衣料品の店舗と商品価格、観光非居住者料金。
- 外貨換算レート：**未採用**（検証可能な日付/レートが取得できたときに記録）。

公開時には出典リンクを明示し、記事・体験・価格の更新日を残す。

## 調査履歴

| 日付 | Issue | 内容 | 結果 |
|---|---|---|---|
| 2026-10-16 | 初期 | PR #9 の初期調査、およびリポジトリ外で作成したローカル資料（PINES・ケープタウン・アフリカ・日本の手続き） | research/philippines-pines.md・africa-trip.md・second-school.md、docs/03-preparation.md に統合 |
| 2026-10-17 | #7 | UCT ELC 2027年料金表、PINES 料金表 PDF（2026年10月〜版）を再取得して照合 | PH-01 を USD 建ての見積に更新 |
| 2026-10-17 | #8 | 外務省オープンデータ（領事メール全件）、FORTH、CDC、DAN、Eskom、病院・救急・領事の連絡先 | research/safety-and-health.md。緊急番号（10111・10177・021-425-1695・911・143・02-8551-5786）は外務省ページで再確認済み |

## 調査環境の制約（2026-10-17）
- 組み込みの WebSearch ツールは API エラーで使えない。WebFetch と curl で直接取得し、検索には Bing・Brave・DuckDuckGo を curl 経由で利用した（ボット判定で失敗することがある）。
- 403 などでアクセスできなかったサイト（mofa.go.jp 本体の医療情報、在外公館サイト、pinesacademy.com、sanparks.org ほか）は「未確認」として扱っている。
