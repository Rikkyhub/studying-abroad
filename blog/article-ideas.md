# ブログの将来記事・調査の再利用

**実際の経験と準備中の調査を分ける**。記事候補は公開原稿ではない。[Issue #7](https://github.com/Rikkyhub/studying-abroad/issues/7)。

## 初期の記事案（2026-10-16、下の一覧に統合済み）

| 記事案 | 段階 | 必要な材料 |
|---|---|---|
| 休職制度を使って6か月留学・旅行する準備 | 調査/準備中 | 一般的な手続きと公開料金 |
| 6か月の費用モデル：出発前見積と見直し | 調査/準備中 | 費用CSV（見積）・為替レート |
| バギオの語学学校12週間のモデル：授業・食事・週末 | 未体験 | 現地写真・公開されている授業時間・費用 |
| バギオから土日で行けるダイビング | 調査/準備中 | ショップ回答/バス時刻/体験後の記録 |
| アフリカ1か月周遊：国・経路・費用 | 計画中 | フライト/バス/宿/体験記録 |
| ケープタウンの冬の生活と自炊費 | 調査/準備中 | スーパー実売・レシート・レシピ |
| ケープタウンの冬ダイビング | 調査/準備中 | 冬季ショップ・装備・体験後の写真 |
| ビザと再入国：6か月旅程をどう組んだか | 調査/準備中 | 当局回答と適用制度・日付 |
| 英語力と海外就労準備への影響 | 未体験 | 開始前/途中/終了後の同尺度の記録 |

公開前：名前・私用メール・旅券番号・予約番号・勤務先非公開情報・領収書原本を削除する。第三者の写真等も許諾を確認。

## 記事化のルール

1. **調査で分かった事実と、本人の体験を分けて書く**。
   - 調査した事実は「（2026年10月時点の公式情報）」のように時点と出典を書く。
   - 体験は [experience-log.md](experience-log.md) に記録したことだけを使う。
2. **体験談・感想・口コミ・写真を作らない**。体験していないことは「予定」「調べた情報」と書く。
3. **公開前に次のものを消す**: 本名、会社名・部署、社内の制度や手続きの詳細、予約番号、住所、パスポート番号、ホームステイ先の情報、他の人が写った写真（許可がない場合）。
4. 費用の記事は各地域ページの費用の見積を使い、「見積」と明記する。個人の支払額を載せるかは本人が別途判断し、公開リポジトリには書かない。
5. 料金・制度は変わるので、記事にも「情報の時点」を書く。

## 記事候補一覧（自動）

状態：`未着手` → `資料収集中` → `下書き` → `公開可能`（→ `公開済み`）

<!-- AUTO:articles -->
状態の集計: 未着手 0 ／ 資料収集中 9 ／ 下書き 16 ／ 公開可能 0 ／ 公開済み 0

### 留学準備

| ID | 記事タイトル案 | 状態 | 使う資料 | 必要な体験記録 | 下書き |
|---|---|---|---|---|---|
| A01 | 休職制度を使って半年間海外に行く準備（一般的な手続き） | 資料収集中 | docs/03-preparation.md（休職タスク） | 公開可能な一般手続きのみ（勤務先の内部情報は書かない） | — |
| A02 | 留学先にフィリピン（バギオ）を検討するときの比較ポイント | 資料収集中 | research/philippines-pines.md | 比較の観点（公開料金・立地・設備）。個人の選択理由は載せない | — |
| A03 | 半年間の予算モデル（目標250万円の内訳） | 資料収集中 | docs/02-budget.md／data/expenses.csv | 公開用の見積モデル（個人の資産・支払いは載せない） | — |
| A04 | 退去・荷物整理・日本に残る固定費の整理 | 下書き | blog/experience-log.md／docs/03-preparation.md／https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000020.html／https://www.post.japanpost.jp/service/receive/relocation/ | 2026-10-31国交省2011年再改訂ガイドラインと日本郵便公式を直接再確認。退去の契約確認・通常損耗と過失の区分・荷物仕分け・国内固定費・郵便転送・証拠表の5節で一般記事下書き完成。日本郵便の無料転送は届出日から1年で登録3〜7営業日。2027年の個別解約期限・運送/保管/処分費・本人の契約/申請は未確認。契約書・管理会社・運送/保管事業者・自治体が次の取得先。未体験・未公開・生成物/CI/main未完了 | blog/experience-log.md |
| A05 | 長期語学留学の準備と手続きチェックリスト（一般論） | 下書き | blog/experience-log.md／docs/03-preparation.md／data/tasks.csv／https://ryugaku.jasso.go.jp/oversea_info/basic/planning.html／https://ryugaku.jasso.go.jp/faq/faq_life.html | 2026-10-31 JASSO公式の2026-04-10更新準備工程と現地生活FAQを直接確認。目的・学校・入国資格・保険・宿泊・資金・安全・渡航後記録の6段階を一般向け下書きに整理。実際に必要だったという体験主張を削除。準備開始の約半年前は目安であり個別期限ではない。2027年の学校規約・査証・保険・料金・予約は未確認。学校最新版募集要項・大使館/入管・保険約款が次の取得先。生成HTML・CI・main未完了 | blog/experience-log.md |
| A06 | 休職中の社会保険料・住民税はいくらかかるか | 資料収集中 | docs/03-preparation.md（税・社会保険） | 制度の一般的な計算式（個人の請求額は載せない） | — |
| A07 | 半年・アジア＋アフリカの海外旅行保険の選び方 | 資料収集中 | docs/03-preparation.md（保険） | 保険の選び方の観点（個別契約の内容は載せない） | — |
| A08 | アフリカ渡航前の予防接種と費用 | 下書き | blog/experience-log.md／research/prep-priority1-tasks.md／https://www.forth.go.jp/keneki/tokyo/abroad/yellow-fever-vaccination/index.html／https://hospinfo.tokyo-med.ac.jp/shinryo/tokou/cost.html／https://www.cdc.gov/yellow-fever/hcp/vaccine/ | 2026-10-31一次資料で黄熱料金2施設・証明書10日・同日接種の一般原則とYellow BookのMMR30日例外を下書き化。2027年料金・本人の接種歴・実経路・接種要否・在庫・医師判断は未確認。未接種・未予約 | blog/experience-log.md |

### 留学生活

| ID | 記事タイトル案 | 状態 | 使う資料 | 必要な体験記録 | 下書き |
|---|---|---|---|---|---|
| A09 | 語学学校の授業コース構成の例（一般論） | 下書き | blog/experience-log.md／research/philippines-pines.md／https://pinesacademy.edu.ph/eng/program_power_esl／https://pinesacademy.edu.ph/eng/program_intensive_esl | 2026-10-31学校公式ページの検索取得本文でPower ESL5の1対1×5とIntensiveの1対1×5＋グループ×2を照合。Intensive公式英語ページのRegular Class(8)と内訳計7の矛盾を明記し2027年の授業数を確約しない。任意選択授業と通常授業を分離した5節・確認表の一般記事下書きを完成。学校ページ直接閲覧は403。2027年の開講・分数・時間割・料金・選択授業・グループ人数・評価は学校回答待ち。未体験・未公開・生成物/CI/main未完了 | blog/experience-log.md |
| A10 | バギオの寮生活・食事・1か月の生活費の目安 | 資料収集中 | research/philippines-pines.md／https://matchingenglish.com/wp-content/uploads/2025/10/PINES-MEAL-OPTIONS.pdf | 2026-10-29学校作成Meal Options資料（2024-08-01以降申込向け）を直接照合。平日食は寮費に含まれ、週末は土曜朝食無料・土曜昼/日曜昼/日曜夜の最大3食を各PHP179で金曜17時までに申請。4週の3食モデルPHP2148、12週PHP6444。日曜朝食PHP100・土曜夕食ありの旧記述は公式資料と不一致。2027年の制度/料金と外食・日用品・生活費総額は未確認。未体験を体験談にしない | — |
| A11 | 12週間の語学留学で英語力はどう変わるか（一般論） | 下書き | blog/experience-log.md／https://support.cambridgeenglish.org/hc/en-gb/articles/202838506-Guided-learning-hours／https://www.coe.int/en/web/common-european-framework-reference-languages | 2026-10-31公式再確認：Cambridge English（2026-10-29更新）はCEFR段階上昇の指導付き学習約200時間を参考値としA2/B1/B2の時間表は初心者からの累積。欧州評議会CEFR Companion Volume 2020は技能別の行動記述を提供。開始前・4/8/12週の同条件別版テストと独自観察表・学習時間区分を含むA11一般記事を既存原稿に完成。2027年の学校時間割・評価・本人の伸びは未確認。12週間での上達保証なし。未体験・未公開・main未統合 | blog/experience-log.md |
| A12 | 語学留学で起きやすい困りごとと対策（一般論） | 下書き | blog/experience-log.md／https://ryugaku.jasso.go.jp/faq/faq_planning.html／https://ryugaku.jasso.go.jp/faq/faq_life.html | 2026-10-31 JASSO一次資料2件を直接再確認。学習目標・寮規則・医療と保険・紛失時の停止連絡・就学資格の誤認を6節と連絡表に整理した一般向けA12記事下書きを既存原稿に完成。2027年の学校固有規則・医療機関・就学許可・保険約款は未確認で学校公式案内・大使館/入管・保険会社が次の取得先。体験談ではなく未公開。生成物/CI/main未完了 | blog/experience-log.md |
| A13 | ケープタウンの語学学校の選び方（比較の観点） | 資料収集中 | research/second-school.md | UCT ELC公式2027年料金表は同一ページで8〜11週Standard週R5 540とR5 120が併記。IH公式2026年Webとパンフレットは個別授業表記が不一致。2027年の有効料金・授業形式・就学資格は学校と当局に要確認。未体験を体験談にしない | — |
| A14 | フィリピンと南アフリカの語学留学の制度・費用の違い（公開情報） | 資料収集中 | research/philippines-pines.md／research/second-school.md／https://e-services.immigration.gov.ph/／https://dirco.gov.za/japan/immigration-visa-info/ | 2026-10-29政府一次確認：比入管eServicesは非学位・1年未満のSSPとVisa Waiver（29日）・観光滞在延長を別サービスとして案内。南ア在日大使館はStudy Visa申請書類・掲載手数料JPY4300を案内する一方、領事業務一覧は対象を大学・航空学校と表記。民間語学学校8週間の就学資格・2027年の料金/申請条件は未確定。学校/大使館/入管へ確認。体験談ではない | — |

### アフリカ旅行

| ID | 記事タイトル案 | 状態 | 使う資料 | 必要な体験記録 | 下書き |
|---|---|---|---|---|---|
| A15 | 1か月で南部アフリカを周遊するモデルルートの例 | 資料収集中 | research/africa-trip.md／https://www.zambiaimmigration.gov.zm/kaza-univisa/／https://www.mozambiquehighcommission.org.uk/visa-section.html | 2026-10-29公式一次確認：30日7か国の一般モデルを研究正本へ追加。KAZAはボツワナ日帰り限定で宿泊不可。モザンビークは査証免除と渡航前ETAを区別。2027年の便・陸路接続・料金・国境運用・南ア就学資格は未確認。体験談ではない | — |
| A16 | 周遊ルートと移動費の目安 | 下書き | research/africa-trip.md／data/expenses.csv／https://www.intercape.co.za/cape-town-to-johannesburg-by-bus/／https://strab.co.za/border-transfers/ | 2026-10-31運営者公式を再確認：Intercape 2026ガイドCape Town→Johannesburgは片道ZAR650から・18〜20時間・Park Station着。STRAB国境送迎はPonta do Ouro ZAR280/人片道・最少2名で車両は国境を越えない。夜行便・1名相乗り・2027年運行/実売・安全な送迎は未確認。一般向けA16記事下書き完成。体験談ではない。生成HTML/CI/mainは未完了 | blog/experience-log.md |
| A17 | サファリツアーの種類と料金の目安 | 下書き | research/africa-trip.md／blog/experience-log.md／https://chobezi.com/chobe-day-trip-2/／https://chobezi.com/two-day-one-night-safari/／https://www.chobesafarilodge.com/faq | 2026-10-31運営者一次資料：Chobeziの3時間ゲームドライブBWP856・3時間ボートBWP856・日帰りセットBWP1384（最少2名）・2日1泊キャンプBWP4546（公園内宿泊料別）。Chobe Safari Lodgeの自社活動参加者BWP190と非居住者自走BWP270は異なる入園区分で他社ツアーに自動加算しない。2027年料金・1名相乗り・入園料包含・実売・国境送迎は未確認。一般記事下書き完成で未体験・未公開。生成物/CI/main未完了 | blog/experience-log.md |
| A18 | 南部アフリカのダイビングの種類と料金の目安 | 下書き | research/africa-trip.md／blog/experience-log.md／https://coraldivers.co.za/wp-content/uploads/2026/09/Coral-2027-Resort-Rates.pdf／https://www.peri-peridivers.com/pdf/peri-peri-divers-price-list-tofo.pdf | 2026-10-31運営者公式PDFを直接確認。Coralの2027-02-01〜2028-01-31料金は5/2〜9/22ローシーズンで2Mile1本ZAR550・5本タンク重量込ZAR2475・フル器材ZAR450/日。器材3日仮定の5本モデルZAR3825は宿・公園料・遠方リーフ・交通等を除く。Peri-Periのトーフは自己器材MZN3400/本・全器材MZN4000/本・Ocean Safari MZN3600でPDF適用年不明。Reef Tax MZN400/場所週・遠方MZN400は別。2027年のPeri-Peri実売・公園料・空席・資格/海況・1名参加・安全な交通は未確認。A18一般向け記事下書き完成で未体験・未公開。生成物/CI/mainは未完了 | blog/experience-log.md |
| A19 | アフリカ周遊中の一般的な安全対策 | 下書き | research/africa-trip.md／blog/experience-log.md／https://www.anzen.mofa.go.jp/info/pcsafetymeasure_122.html／https://www.anzen.mofa.go.jp/info/pchazardspecificinfo_2025T062.html | 2026-10-30外務省一次確認：南アCBDのレベル2とモザンビーク北部のレベル2/3を地域別に区別。乗降場所・日中接続・送迎・緊急連絡先を含む一般向け安全判断記事を既存原稿へ作成。2027年の危険レベル・運行・宿/送迎・保険条件は未確認。未体験・未公開・main未統合 | blog/experience-log.md |
| A20 | 1か月のアフリカ周遊の費用モデルと節約方法 | 下書き | docs/02-budget.md／https://chobezi.com/chobe-game-drive/／https://chobezi.com/chobe-boat-cruise/／https://chobezi.com/chobe-day-trip-2/／https://www.intercape.co.za/cape-town-to-johannesburg-by-bus/ | 2026-10-30運営者一次資料再確認：Chobeziの3時間ドライブとクルーズは各BWP856/人、別売り2商品BWP1712/人。日帰りセットBWP1384/人は最少2名で掲載額差BWP328/人だが同一条件・1名相乗り・入園料包含は未確認。Intercape Cape Town→Johannesburgは2026年案内でZAR650から・18〜20時間。逆方向・2027年料金・日中接続は未確認。予算は未入力と重複計上を区別し体験談にしない | blog/experience-log.md |

### 帰国後

| ID | 記事タイトル案 | 状態 | 使う資料 | 必要な体験記録 | 下書き |
|---|---|---|---|---|---|
| A21 | 半年間の費用モデルの見直しポイント | 下書き | docs/02-budget.md／data/expenses.csv／https://www.boj.or.jp/statistics/market/forex/fxdaily/index.htm／https://www.jcb.jp/rate/jpy.html | 2026-10-30日銀・JCB一次資料を再確認。既存blog/experience-log.mdに見積の費目分解・未確認と部分見積の扱い・為替とカード換算・二重計上防止・生成物検査を含む一般記事下書きを完成。2027年実売・カード請求・本人の実支出は未確認。記事未公開でmain未統合。正式生成HTML・全validator・exact HEAD CIは未完了 | blog/experience-log.md |
| A22 | 見積モデルの初版と更新版の差分の見方 | 下書き | docs/02-budget.md／data/expenses.csv／blog/experience-log.md／https://www.boj.or.jp/statistics/market/forex/fxdaily/index.htm／https://www.jcb.jp/rate/jpy.html | 2026-10-30日銀・JCB公式を直接確認。既存記事原稿にA22の5章構成を完成。PH-08旧PHP9792→PHP6444は入力・範囲訂正で実節約ではない。通貨と版SHA・数量・価格・為替・未入力を分離。2027年価格と本人請求は未確認。正式生成物・CI・main統合は未完了 | blog/experience-log.md |
| A23 | 長期の海外経験を準備するときの一般的な考え方 | 下書き | blog/experience-log.md／https://ryugaku.jasso.go.jp/faq/faq_planning.html／https://ryugaku.jasso.go.jp/faq/faq_life.html | 2026-10-30 JASSO公式FAQ2件を直接再確認。目的→方法→学校/滞在資格/生活条件の確認順をもとに一般向け記事下書きを既存研究正本へ作成。語学学校/大学/ワーキングホリデー/周遊の制度と成果を分離し方法別の確認表を追加。2027年学校条件・査証/就労資格・保険は未確認で学校募集要項・当局・保険約款が次の取得先。未体験/未公開でmain未統合 | blog/experience-log.md |
| A24 | 長期留学の準備で起きやすい失敗と対策（一般論） | 下書き | blog/experience-log.md／https://ryugaku.jasso.go.jp/oversea_info/basic/planning.html／https://ryugaku.jasso.go.jp/oversea_info/basic/agency.html | 2026-10-30 JASSO公式準備工程（2026-04-10更新）と代理店契約注意（2025-07-31更新）を直接再確認。既存blog/experience-log.mdのA24節を六つの想定リスク・具体的な予防策・申込前確認表を含む一般向け記事下書きへ展開。2027年の学校規約・国別就学資格・保険条件は未確認。学校最新版要項・大使館/入管・保険会社約款が次の取得先。実体験ではなく記事未公開。main未統合 | blog/experience-log.md |
| A25 | これから半年間の留学を考える人向けの準備ガイド | 下書き | blog/experience-log.md／https://ryugaku.jasso.go.jp/oversea_info/basic/planning.html／https://ryugaku.jasso.go.jp/faq/faq_life.html | 2026-10-30 JASSO公式準備工程と代理店契約注意を直接再確認。既存blog/experience-log.mdのA25節を一般向け記事本文へ展開し原稿下書きまで完了。体験談ではない。2027年学校契約・査証・保険の個別条件と生成HTML/CIは未確認。 | blog/experience-log.md |

<!-- /AUTO:articles -->

## 下書きのテンプレート

`drafts/` に `A01_休職して半年海外へ.md` のような名前で作ります。

```markdown
---
id: A01
title:
status: 下書き
情報の時点: YYYY-MM-DD
公開前チェック: [ ] 個人情報 [ ] 会社情報 [ ] 予約番号 [ ] 写真の許可 [ ] 調査情報の出典と時点
---

## この記事で分かること

## 調べた情報（出典・時点つき）

## 実際にやったこと（体験）

## 振り返り
```
