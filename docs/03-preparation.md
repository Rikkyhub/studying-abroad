# 出発前・現地・帰国の準備チェック

一般的な準備チェックリスト（地域ごとの確認事項は [バギオ](../areas/baguio.md)・[アフリカ周遊](../areas/africa.md)・[ケープタウン](../areas/capetown.md)・[共通](../areas/common.md)）。下の AUTO ブロックは `py scripts/build_all.py`（内部で build.py）が生成する。ここには判断の順序と、公的情報の調査結果を記載する。公開用の匿名モデルで、個別の雇用条件・契約・支払い・提出状況は書かない。

## 先に確定すべきもの
- [ ] 語学学校の入寮・修了・退寮日を学校の最新案内で確認
- [ ] 勤務先の休職制度、無給期間の税・社会保険料の扱い、住居と荷物保管
- [ ] 南アフリカの**8週間の英語コース**で必要な滞在資格を学校・在日南アフリカ大使館に確認
- [ ] **5月南アフリカ初入国案**と**6月初入国案**をビザ/再入国ルールで検証
- [ ] フィリピンへの入国時に必要な出国用航空券（正式な予約を用意する）
- [ ] フィリピンの観光滞在延長・SSP等が学校代行かどうかと最終料金
- [ ] アフリカ周遊国のビザ、黄熱病の接種証明条件、国をまたぐ移動の現実性

## タスク一覧（自動）

期限は暦日ではなく出発日などを基準にした相対的な目安です。期限の種類は「公式期限」（制度上の期限）／「学校・機関の個別期限」（各機関の案内に従う）／「推奨目安」（このモデルの提案）／「要確認」。

<!-- AUTO:tasks -->
### 住居・荷物

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-H01 | ⬜ | 賃貸契約の解約予告期間・退去費用を確認（該当する場合） | 出発90日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 契約による | 賃貸借契約書で解約予告期間・違約金・更新料を確認（民法617条の法定は3か月だが契約の特約が優先される例が多い。research/prep-priority1-tasks.md §4） | [出典](https://laws.e-gov.go.jp/law/129AC0000000089) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-H02 | ⬜ | 住居を残す場合と退去する場合の費用を比較（該当する場合） | 出発60日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 家賃6か月分 vs 退去＋保管＋再契約費 | 一般的な維持/退去比較式と6・8か月3箱保管モデルはdocs/02-budget.md §5-1に反映済み。本人の契約条件・実家保管可否・箱数・2027年料金を非公開で確認して実額比較する | [出典](https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000020.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-H06 | ⚠️ | 住民票：国外転出届（海外転出届）が必要かを住民登録のある自治体に確認 | 出発60日前（推奨目安）。届出の要否・時期は自治体の案内による | 推奨目安 | 要確認 | 本人 | — | 滞在期間・日本の生活の本拠・住居の扱いを整理し、住民登録のある市区町村に照会する | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-H03 | ⬜ | 荷物の保管先を決定（実家・トランクルーム・宅配型収納） | 出発30日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 宅配型収納 1箱 約320〜330円/月 | 実家保管（0円モデル）と宅配型を比較。6か月・3箱の単純モデル：minikura 9060円／サマリーポケット 9240円（送料込み・追加条件除外）。2027年の公式料金と箱数を確認 | [出典](https://minikura.com/lineup/nophotobox.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-H04 | ⬜ | 電気・ガス・水道・ネットの解約／休止 | 出発14日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 解約金・撤去費・最終請求は契約先ごとに未確認（JPY） | 代表3事業者の2026年停止手順は研究正本に整理済み。契約先・使用最終日・ガス立会い・ネット撤去/返却・違約金・2027年条件を公式約款で確認後に本人が申込（research/prep-priority2-tasks.md T-H04） | [出典](https://home.tokyo-gas.co.jp/gas_power/procedure/moving/index.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-H05 | ⬜ | 郵便転送届（e転居）・重要書類の受取先を決める | 出発14日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 無料 | 郵便転送の一般制度と4段階の実行手順を既存研究に整理済み。国内受取先とゆうID確認後に転居届を提出し転送不要の差出人へ個別住所変更する。2027年の各社手続を確認（research/prep-priority2-tasks.md §3） | [出典](https://www.post.japanpost.jp/service/receive/relocation/) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### 保険・医療

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-I02 | ⬜ | トラベルクリニック受診・予防接種計画（A型・B型肝炎・破傷風・腸チフス・狂犬病） | 出発90日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 2026-06東京医大税込: 国産A型3回47,850円/輸入A型2回26,400円/B型3回19,800円（ワクチン代のみ・診察料別） | 一般的な接種回数・2026年料金の比較は研究正本に反映。実際の接種歴・製剤選択・短縮可否を渡航外来で相談し予約・接種を本人が行う（research/prep-priority1-tasks.md §2） | [出典](https://hospinfo.tokyo-med.ac.jp/shinryo/tokou/cost.html) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |
| T-I03 | ⬜ | 黄熱ワクチンの要否判断（経由地・訪問国次第） | 出発45日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 検疫所17680円は過去資料の参考額（2027年料金未確認） | research/prep-priority2-tasks.md §1の3ルート比較で黄熱リスク国への実入国とリスク国空港12時間超の乗継を区別。便・国境・訪問順を決めた後に各国当局と航空会社へ2027年要件を照会し渡航外来で接種判断 | [出典](https://www.gov.za/news/media-statements/health-reviews-yellow-fever-requirements-03-feb-2015) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |
| T-I01 | ⬜ | 海外旅行保険（約180日・アジア＋アフリカ）の見積・加入 | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 約180日・複数国の正式見積は未取得（H.S.損保の1年間の参考保険料を6か月に転用しない） | H.S.損保FIT留学32日以上とt@biho留学31日超で同一期間・国・観光混在の正式見積と潜水事故（減圧症・再圧治療・搬送）の約款を照合。加入は本人判断 | [出典](https://www.hs-sonpo.co.jp/store/abroad.php / https://tabiho.jp/tb/) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |
| T-I04 | ⬜ | マラリア予防薬の相談（クルーガー・チョベ・ビクトリア滝方面に行く場合） | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | 自由診療 | Kruger・Chobe・OkavangoのCDC公式リスク地域比較はresearch/prep-priority2-tasks.md §1 T-I04に反映済み。2027年の訪問地点・宿泊環境・流行情報を確認し、トラベルクリニックで予防内服の要否・製剤・服用期間・費用を相談する | [出典](https://www.cdc.gov/yellow-book/hcp/africa-middle-east/south-africa.html) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |
| T-I05 | ⬜ | 歯科検診・常備薬・処方薬（英文処方箋） | 出発14日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 歯科予約 | — | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |
| T-I06 | ✅ | 協会けんぽ海外療養費の一般制度・申請様式を調査 | 出発14日前（推奨目安） | 推奨目安 | 完了 | 本人 | — | 協会けんぽの電子申請・紙申請と様式A/B/Cを一次確認済み。本人の加入健保が別なら当該健保へ申請先・様式・海外申請可否を照会（research/prep-priority2-tasks.md §2） | [出典](https://www.kyoukaikenpo.or.jp/application_form/benefit/003/) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |

### パスポート・ビザ

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-P01 | ⬜ | 訪問国別の旅券残存期間と未使用査証欄を確認 | 出発90日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 更新時 電子申請8900円／窓口9300円 | パスポートの有効期限と空白ページを確認（フィリピンは滞在予定期間＋6か月以上、南アは未使用2ページ以上＋出国予定の30日後まで。research/prep-priority1-tasks.md §1） | [出典](https://www.anzen.mofa.go.jp/m/mbimmigration_122.html) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T-P02 | ⬜ | フィリピン eTravel 登録 | 到着前72時間以内（到着日未定のため日付なし） | 公式期限 | 未着手 | 本人 | 無料 | フィリピン到着前72時間以内に公式サイトで無料登録する（登録QRを搭乗時に提示できるようにする） | [出典](https://etravel.gov.ph/) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T-P05 | ⬜ | 周遊国のビザ要否・費用を確定 | 周遊開始60日前（推奨目安） | 推奨目安 | 進行中 | 本人 | ナミビア査証NAD1600＋3%（2025年3月公式。2027年未確定） | エスワティニ・レソトの日本旅券短期査証免除は各政府公館の公式一覧で確認済み（research/visa-and-immigration.md §2-3）。2027年の適用・国境運用とナミビアNgomaでの査証・決済、他国の最新条件を入管・在日公館へ照合 | [出典](https://www.gov.sz/index.php?id=314 / https://www.lesothoemb-usa.gov.ls/visa/ / https://www.na.emb-japan.go.jp/itpr_ja/11_000001_00805.html) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |

### 留学先手続き

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-S01 | ⬜ | 留学先学校の入学案内・現地費用の2027年版を確認 | 学校の案内に従う（要確認）。目安は出発90日前 | 学校・機関の個別期限 | 未着手 | 本人 | — | エージェント／学校に2027年版の現地費用を確認（公開PDFは2026年10月〜版のみで2027年2月入学分は未確認。research/prep-priority1-tasks.md §5） | [出典](https://philschools.jp/pricelist/pines.pdf) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-S02 | ⬜ | 2校目（南ア）の学校・期間を比較して選ぶ | 第2校の開始90日前（推奨目安） | 推奨目安 | 進行中 | 本人 | research/second-school.md 参照 | UCT ELC・GHS・IHの公式比較モデルを確認済み。IHの2026料金は2026-10-31で有効期限終了。2027年の授業料・コース開講・入学条件・宿泊・語学就学資格を各学校と在日公館に正式確認してから選定 | [出典](https://ihcapetown.com/wp-content/uploads/2026/01/2026-English-USD-Pricelist.pdf) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-S03 | ⬜ | 2校目の宿泊（ホームステイ等）を手配 | 第2校の開始60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | research/second-school.md 参照 | 学校決定後に申込 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### 休職・会社

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-W01 | ⚠️ | 休職・長期休暇制度を利用する場合の規定・承認手続きを確認（該当する場合） | 出発90日前（推奨目安）。社内規定の期限があればそちらを優先 | 推奨目安 | 要確認 | 本人 | — | 就業規則と必要書類を確認（内容は公開しない） | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-W02 | ⬜ | 休職する場合の社会保険料（本人負担分）の支払方法を確認（該当する場合） | 出発60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 月額は標準報酬月額による | 本人負担分の払い方（立替・振込・復職後天引き等）を勤務先の規定で確認。公式FAQは「無給でも事業主に納付義務」とするのみで集め方は未記載（research/prep-priority1-tasks.md §3） | [出典](https://www.tokyokoukenpo.or.jp/asp/faq/faq.asp?articleid=5154) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-W03 | ⬜ | 住民税の扱い（特別徴収継続・立替か普通徴収切替か）を確認（該当する場合） | 出発60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 滞在期間に応じた月数分（モデル） | 特別徴収・普通徴収の扱いを勤務先・住所地の自治体で確認（休職者を普通徴収にできる区分がある自治体の例あり：世田谷区。自治体ごとに異なる。research/prep-priority1-tasks.md §3） | [出典](https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-W04 | ⬜ | 休職前後の休暇・復職手続きの規定を確認（該当する場合） | 出発60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 就業規則を確認（個別の日付・処遇は公開しない） | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-W05 | ⬜ | 休職中の海外渡航・緊急連絡体制の規定を確認（該当する場合） | 出発60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 就業規則を確認 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-W06 | ⬜ | 業務の引継ぎ計画（該当する場合） | 出発14日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 引継ぎ範囲を決める | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### 出発前

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T003 | ⬜ | 留学先学校に就学許可（SSP）・滞在延長の手続き範囲と費用を確認 | 出発90日前（推奨目安）。学校・代行業者の個別期限があればそちらを優先 | 推奨目安 | 未着手 | 本人 | — | 学校にSSPオンライン申請の代行可否・滞在延長の別申請・必要書類・2027年費用を確認 | [出典](https://immigration.gov.ph/services/special-study-permit/) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T004 | ⬜ | 南ア留学先の候補校と南ア大使館に8週間語学就学の必要資格を確認 | 出発90日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 在日南ア大使館・UCT ELC に問い合わせ文案を送る | [出典](https://dirco.gov.za/japan/immigration-visa-info/) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T005 | ⬜ | 南ア入国時期ごとの再入国条件を確認 | 出発90日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | T004と同じ問い合わせで回答を得る | [出典](https://dirco.gov.za/japan/frequently-asked-questions/) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T007 | ✅ | 休職制度・税社保・住居と国内固定費の一般的な確認項目を整理 | 出発60日前（推奨目安） | 推奨目安 | 完了 | 本人 | — | T-W02・T-W03・T-H01〜T-H06 に分割して管理 | [出典](https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20120524.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T002 | ⬜ | フィリピン入国用の有効な出国航空券を確保 | 出発30日前まで（推奨目安）。入国時に提示を求められる場合がある | 推奨目安 | 未着手 | 本人 | — | research/visa-and-immigration.md の推奨案を見て、5月のマニラ発便を先に買うか判断 | [出典](https://tokyo.philembassy.net/en/consular-section/services/visa/visa-free-entry-for-temporary-visits/) | [#2](https://github.com/Rikkyhub/studying-abroad/issues/2) |
| T011 | ⬜ | 外務省危険情報と旅行保険・医療連絡先を確認 | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | — | 外務省の渡航先別危険情報と保険の補償・医療連絡先を渡航前に再確認。バギオ市CDRRMOの緊急911（24時間）・運用連絡先は2026-10-24公式確認済み。学校・病院・保険会社の24時間窓口は未確認（research/safety-and-health.md） | [出典](https://www.anzen.mofa.go.jp/) | [#8](https://github.com/Rikkyhub/studying-abroad/issues/8) |

### 航空券

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-F01 | ⬜ | 日本→マニラ（往路）を購入 | 出発45日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 片道 約2.2〜6.5万円（KAYAK参考） | 便を比較して購入 | [出典](https://www.kayak.com/flight-routes/Tokyo-TYO/Manila-Ninoy-Aquino-Intl-MNL) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-F02 | ⬜ | マニラ→南部アフリカ（周遊開始時）を購入 | 該当便の出発60日前（推奨目安） | 推奨目安 | 未着手 | 本人 | research/africa-trip.md 参照 | ルート案を決めて購入 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-F03 | ⬜ | ケープタウン→日本（帰国便）を購入 | 帰国便の出発90日前（推奨目安） | 推奨目安 | 未着手 | 本人 | research/second-school.md 参照 | 2校目の終了日確定後に購入 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### お金・通信

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-M05 | ⬜ | ふるさと納税・年末調整・確定申告の要否を確認 | 要確認（制度上の時期は国税庁の案内で確認） | 要確認 | 進行中 | 本人 | — | 国税庁の一般条件はresearch/prep-priority2-tasks.md §2で確認済み。勤務先の年末調整対象と源泉徴収票・本人の所得区分・寄附先件数・確定申告予定を非公開で確認し個別要否を判断 | [出典](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-M01 | ⬜ | 海外用クレジットカード2枚以上・デビットカードの準備 | 出発30日前（推奨目安） | 推奨目安 | 未着手 | 本人 | 年会費による | ブランド（Visa/Master）を分けて用意 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-M02 | ⬜ | 日本の携帯番号の維持方法を決める（povo0円・ahamo等） | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | povo基本料0円はトッピング別。ahamo 2026-12改定予定は月3135円から・6か月18810円（40GB以下の仮定・追加費用別） | 研究比較は着手済み。ahamo海外データ対応は南ア・レソト等のみ（2026掲載）で周遊国全域ではない。日本番号維持と現地データを分けて比較し2027年の対応国・端末・MNP条件を公式再確認して本人が選択（research/prep-priority2-tasks.md §3） | [出典](https://ahamo.com/new-ahamo/) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### 計画

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T008 | ⬜ | 2都市の週末ダイビング交通と見積を取得 | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | — | 両都市の公式ダイビング商品比較は既存研究に整理済み。潜水後に高地へ戻る場合はDAN Europe・PADIの一般的な24時間待機目安を参考に海沿い1泊を優先。2027年のショップ見積・交通運賃・帰路最高標高・個別安全確認を取得 | [出典](https://www.daneurope.org/en/faq-medical/surface-interval-diving-1000m-altitude/) | [#3](https://github.com/Rikkyhub/studying-abroad/issues/3) |
| T009 | ⬜ | 2都市の観光・雨天代替案を検証 | 出発30日前（推奨目安） | 推奨目安 | 進行中 | 本人 | — | 両都市の研究§5に日帰り・1泊2日・雨天代替モデルあり。未確認の公式交通運賃・催行条件・2027年料金を追加検証してから日程に配置 | — | [#4](https://github.com/Rikkyhub/studying-abroad/issues/4) |
| T010 | ⬜ | ケープタウンの食材価格と衣類実売価格を確認 | 第2校の開始90日前（推奨目安） | 推奨目安 | 進行中 | 本人 | — | 2026年オンライン表示価格と冬服の店舗候補は既存研究に整理済み。2027年の店頭実売価格・在庫・購入時期を渡航前に再照合。水道水は市の水質情報と宿泊先設備を確認（research/food-and-living.md §3） | — | [#5](https://github.com/Rikkyhub/studying-abroad/issues/5) |

### 渡航中

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-T01 | ⬜ | 外務省 たびレジ登録（フィリピン・アフリカ各国） | 出発7日前（推奨目安） | 推奨目安 | 未着手 | 本人 | たびレジ無料（在留届の費用は未確認） | 国ごとの住所・居所と滞在日数を判定。3か月未満はたびレジ・3か月以上は在留届の対象を確認。ORRネットは到着90日前からオンライン提出可（公式FAQ参照） | [出典](https://www.ezairyu.mofa.go.jp/RRnet/faq.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-T02 | ⬜ | 5月の周遊ルート確定・宿・ツアー予約 | 周遊開始60日前（推奨目安） | 推奨目安 | 進行中 | 本人 | research/africa-trip.md 参照 | 既存A/B/Cとmain統合済み3ルート比較を同じ出発地・日数で再照合。モザンビーク渡航前ETAとKAZAの国境制限を反映し、2027年5月の実際の乗継便・費用・宿泊・催行条件を公式事業者で確認してから本人が最終選択 | [出典](https://www.mozambiquehighcommission.org.uk/visa-section.html) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-T03 | ⬜ | 渡航中の経費は非公開で記録し、公開用の見積を更新 | 渡航中は随時（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 個人の支払記録は公開repoに書かない | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

### 帰国・復職

| ID |  | タスク | 期限（目安） | 期限の種類 | 進捗 | 担当 | 費用目安 | 次のアクション | 根拠 | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| T-R01 | ⬜ | 帰国後の住居・荷物の受け取り | 帰国30日前（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 帰国前に手配 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-R02 | ⬜ | 復職手続き・休職中の社会保険料等の精算（休職した場合） | 帰国後（時期は勤務先等の規定による。要確認） | 要確認 | 未着手 | 本人 | — | 勤務先の規定を確認 | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-R03 | ⬜ | 海外療養費の申請（使った場合） | 帰国後30日以内（推奨目安）。請求の時効は制度で確認 | 推奨目安 | 未着手 | 本人 | — | 領収書と翻訳文を準備（様式A〜Cは担当医の記入・署名が必要。research/prep-priority2-tasks.md §2） | [出典](https://www.kyoukaikenpo.or.jp/benefit/overseas_medical_expenses/) | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |
| T-R04 | ⬜ | 見積モデルの振り返り・ブログ記事化 | 帰国後（推奨目安） | 推奨目安 | 未着手 | 本人 | — | 公開する場合は匿名化した概算のみ使う | — | [#7](https://github.com/Rikkyhub/studying-abroad/issues/7) |

<!-- /AUTO:tasks -->

## 後続作業
- [ ] 航空券/保険/通信とパスポート残存期間・白紙ページの確認
- [ ] ダイビング保険・経験条件・現地用フルレンタル・寒冷水域対策
- [ ] 食費/スーパー/冬服の予算化
- [ ] フィリピンと南アフリカの安全/医療連絡先、緊急時の連絡方法
- [ ] 週末活動の候補を日付と学校スケジュールに配置
- [ ] 体験をブログ用ログへ記録（領収書・個人の支払いは非公開で管理し、公開repoに入れない）

公的情報の確認日は記録すること。制度や2027年料金は直前に再確認する。

## 手続きの要点（公的情報の調査結果・2026-10-16 調査）

> **◎＝個人・会社・自治体の事情で変わる**ので、必ず本人が勤務先・自治体に確認すること。

### 1. 休職中の社会保険料（健康保険・厚生年金）

| 事実 | 出典 | 個別 |
|---|---|---|
| 休職中も在籍していれば被保険者資格は続き、無給でも保険料（本人負担分）が発生する | [東京都情報サービス産業健保 FAQ](https://www.tokyokoukenpo.or.jp/asp/faq/faq.asp?articleid=5154)、[埼玉県 労働相談](https://www.pref.saitama.lg.jp/a0816/rodo/912-2009-1207-184.html) | ○ |
| 本人負担分の払い方（会社の立替と復職後の天引き、毎月振込など）に公的な決まりはない | 同上 | ◎ 会社規定 |
| 雇用保険料は賃金に対してかかるので、無給なら原則発生しない | 埼玉県 労働相談 | ○ |
| 厚生年金は標準報酬月額×18.3%（労使折半で本人9.15%） | [日本年金機構](https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20150515-01.html) | － |
| 4〜6月に報酬がない場合は**従前の標準報酬月額**で定時決定される。2027年4〜6月が無給なら、休職前の等級が続く見込み | [日本年金機構](https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20120524.html) | ○ |
| 協会けんぽ東京（R8年度）: 健康保険9.85%、子ども・子育て支援金0.23%、40〜64歳は介護保険1.62%（いずれも労使合計） | [協会けんぽ](https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf) | ◎ 加入健保 |
| 在籍中なので、国民健康保険・国民年金への切替は不要 | [日本年金機構](https://www.nenkin.go.jp/service/yougo/tagyo/dai2hihokensha.html) | － |

**目安の計算式（本人負担・月額）**: 標準報酬月額 ×（9.15%＋健康保険料率の半分＋支援金率の半分〔＋介護保険料率の半分〕）。6か月分を CM-09 に入力します。

### 2. 住民税

| 事実 | 出典 | 個別 |
|---|---|---|
| 1月1日時点の住所地で前年所得に課税される。給与からの天引き（特別徴収）と、本人納付（普通徴収）がある | [総務省 個人住民税](https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html)、[東京都主税局](https://www.tax.metro.tokyo.lg.jp/kazei/kojin_ju.html) | － |
| 休職で給与から引けなくなる場合、勤務先が異動届を出して普通徴収に切り替えることがある | 自治体の案内例：[千葉市](https://www.city.chiba.jp/shimin/shimin/kusei/tensyutsu_kokugai.html) ほか各市区町村 | ◎ 勤務先・自治体 |
| 国外転出届（海外転出届）が必要かは、日本での生活の本拠・住居の扱いと自治体の運用による。一律の免除や不要の基準があるとは言えない | 自治体の案内例（規則は自治体ごとに異なる）：[千葉市](https://www.city.chiba.jp/shimin/shimin/kusei/tensyutsu_kokugai.html)。住民登録のある市区町村に確認する | ◎ 自治体 |
| 転出届の有無が国民健康保険・年金・住民税に与える影響は、個別の条件（住民登録・加入区分・所得）で変わるため、ここでは判断しない | 住民登録のある自治体・加入している保険者に確認する | ◎ 自治体・保険者 |

### 3. 所得税・年末調整

- 在籍していれば、通常は会社で年末調整されます（[国税庁 No.2665](https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2665.htm)）。
- 休職で年収が下がり源泉徴収税額が多すぎた場合は、還付申告ができます（[国税庁 No.2030](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2030.htm)）。

### 4. 海外療養費（健康保険）

- 海外でかかった医療費の一部が、日本での保険診療の額を基準に戻ってきます。治療目的の渡航は対象外です（[協会けんぽ](https://www.kyoukaikenpo.or.jp/benefit/overseas_medical_expenses/)）。
- 必要書類: 申請書、診療内容明細書、領収明細書、領収書の原本、翻訳文、渡航期間がわかる書類。時効は支払いの翌日から2年です。
- **海外旅行保険の代わりにはなりません**（日本の基準額までしか戻らず、救援費用も対象外）。

### 5. 在留届・たびレジ

- 外国に**3か月以上**滞在する場合は在留届が義務です（[旅券法16条](https://laws.e-gov.go.jp/api/1/lawdata/326AC0000000267)、[ORRネット](https://www.ezairyu.mofa.go.jp/)）。
- 3か月未満なら、たびレジ（任意）に登録します（[たびレジ](https://www.ezairyu.mofa.go.jp/tabireg/index.html)）。
- フィリピンの滞在日数が3か月の境界に近い場合は、在留届・たびレジの対象を外務省の案内で確認します。南アは約8週間＋5月分です。

### 6. パスポート

| 条件 | 内容 | 出典 |
|---|---|---|
| 南アフリカ | 出国予定日から30日以上の残存期間。空白の査証欄2ページ以上 | [外務省](https://www.anzen.mofa.go.jp/m/mbimmigration_122.html) |
| フィリピン | 滞在日数＋6か月以上を強く推奨 | [外務省](https://www.anzen.mofa.go.jp/m/mbimmigration_013.html) |
| モザンビーク／ボツワナ | 残存180日以上／6か月以上 | [africa-trip.md](../research/africa-trip.md) |
| 手数料（2026-07-01〜） | 10年用（18歳以上は10年用のみ）: 電子申請8,900円／窓口9,300円。交付まで約2週間〜1か月 | [東京都](https://www.seikatubunka.metro.tokyo.lg.jp/passport/documents/0000000432) |

**判断基準**: 帰国予定（2027年7月下旬）＋6か月 ＝ **2028年1月下旬以降まで有効**で、空白ページが10ページ程度あるか。

### 7. 予防接種

| 対象 | 推奨（FORTH） |
|---|---|
| フィリピン | A型肝炎・B型肝炎・破傷風・ポリオ・腸チフス（＋狂犬病・日本脳炎は条件付き）（[FORTH](https://www.forth.go.jp/destinations/country/philippines.html)） |
| 南部アフリカ | A型肝炎・B型肝炎・破傷風・腸チフス（＋狂犬病）。クルーガー・オカバンゴ・チョベ・ナミビア北部はマラリアのリスクあり（[FORTH](https://www.forth.go.jp/destinations/country/s_africa.html)） |
| ザンビア・ジンバブエ・モザンビーク | 上記に加え髄膜炎など（[FORTH](https://www.forth.go.jp/destinations/country/e_africa.html)） |
| 黄熱 | 原則は経路しだい。東京検疫所は収入印紙17,680円で、証明書は接種10日後から生涯有効（[東京検疫所](https://www.forth.go.jp/keneki/tokyo/abroad/yellow-fever-vaccination/index.html)） |
| 費用の例 | 東京医大病院: 初診3,201円、A型肝炎15,950円、B型肝炎6,600円、破傷風4,400円、狂犬病16,500円、腸チフス9,900円（1回あたり、[料金表](https://hospinfo.tokyo-med.ac.jp/shinryo/tokou/cost.html)） |

A型・B型肝炎と狂犬病は複数回の接種が必要です。**2026年11月中にトラベルクリニックを受診**すると、2月の出発に間に合います（T-I02）。

### 8. 海外旅行保険

| 事実 | 出典 |
|---|---|
| 損保ジャパン off!・エイチ・エス損保 たびともは**最長31日**で、6か月には使えない | [損保ジャパン FAQ](https://faq.sompo-japan.jp/off/faq_detail.html?id=50136)、[HS損保](https://www.hs-sonpo.co.jp/travel/) |
| クレジットカード付帯保険は90日までのものが多い | [HS損保](https://www.hs-sonpo.co.jp/travel/useful/creditcard-travelers-usage.php) |
| 東京海上日動 長期海外旅行保険（6か月・治療救援無制限）の代理店掲載例: 約17.9万円〜35.2万円（年齢による） | [代理店掲載（2023年資料）](https://www.travel-hoken.net/comp/price_set.html)、[公式シミュレーション](https://www.tmn-hoken.jp/study/simulation.html) |
| t@biho の留学プラン（1年）の例: 韓国15.4万円、北米21.5万円 | [t@biho](https://tabiho.jp/merit-studyabroad/index.html)（6か月・アジア＋アフリカは見積が必要） |

### 9. 荷物保管・携帯電話

| サービス | 料金 | 出典 |
|---|---|---|
| サマリーポケット | 1箱330円／月〜（取り出し送料880円〜、最低保管期間あり） | [公式](https://pocket.sumally.com/) |
| minikura | 1箱320円／月〜 | [公式](https://minikura.com/) |
| povo2.0 | 基本料0円。180日以内に有料トッピングを買わないと利用停止 | [公式](https://povo.jp/) |
| ahamo | 30GBまで海外で追加料金なし。ただし海外で使い始めてから15日を過ぎると速度制限。2026-12-01に料金改定 | [公式](https://ahamo.com/services/roaming-data/index.html) |

### A04：退去・荷物整理・固定費の公開比較モデル（2026-10-29確認）

- **退去前**：契約書の解約予告期間・違約金・原状回復特約を確認する。国土交通省のガイドラインは一般基準であり、個別契約の金額や解約日を確定するものではない。[国土交通省・原状回復ガイドライン](https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000020.html)
- **退去時**：通常損耗・経年変化と故意・過失等による損傷を区別し、入退去時の写真・精算明細を確認する。通常損耗を無条件で借主負担としない（契約の有効性は個別確認）。
- **国内の受取先**：日本郵便の転居届による対象郵便物の転送は無料、届出日から1年間。登録まで3〜7営業日、e転居は本人確認済みゆうIDが必要。差出人への住所変更とは別の手続。[日本郵便・転居転送](https://www.post.japanpost.jp/service/receive/relocation/)
- **比較式（実額未入力）**：住居維持案＝留守中の家賃・共益費＋維持する固定費。退去案＝契約に基づく解約関連費＋引越・保管・再契約費。荷物量、運搬距離、実際の保管先を同じ条件で比較する。保管・通信・公共料金の実売は各事業者で再取得し、未確認金額を0円として埋めない。
- **未確認・次の取得先**：契約書・管理会社の精算条件、保管/引越事業者の2027年見積、各固定費の契約先。本人の解約・申込・支払は未実施。

## 勤務先・自治体に確認すること（一般的な確認項目）

個別の回答・日付・処遇は公開リポジトリに書かない。

**勤務先（休職する場合）**
1. 勤務先の休職制度と承認手続き（T-W01）
2. 社会保険料の本人負担分の払い方と期限（T-W02）
3. 住民税の特別徴収・普通徴収の扱い（T-W03）
4. 休職前後の休暇・復職手続き・年末調整の規定（T-W04）
5. 休職中の渡航に関する規定と緊急連絡体制（T-W05）
6. 加入している健保の種類と、海外療養費の申請窓口

**自治体・関係機関**
1. 国外転出届が必要か（生活の本拠・住居の扱いによる。T-H06）
2. 普通徴収になった場合の納付方法
3. 南アでの8週間の語学留学がビザなしで可能か：駐日南アフリカ大使館（T004）
4. フィリピン滞在が3か月の境界に近い場合に在留届が必要か：外務省

## 持ち物リスト（準備中に更新）

| 区分 | 物 | 状態 |
|---|---|---|
| 書類 | パスポート（残存期間・空白ページ）、パスポートのコピー、証明写真、eTravel、航空券の控え、保険証券（英文）、予防接種証明（イエローカード）、学校の入学許可書、国際キャッシュカード・クレジットカード2枚以上 | 未着手 |
| 健康 | 常備薬、英文の処方箋、虫よけ（DEET）、日焼け止め、マスク | 未着手 |
| 衣類 | バギオ（朝晩涼しい）とケープタウン（6〜7月は冬で雨が多い）向けの防寒着、サファリ用の長袖・地味な色の服 | 未着手 |
| 電子機器 | 変換プラグ（フィリピンはA型、南アはM型など）、モバイルバッテリー、SIMフリーのスマートフォン | 未着手 |
| ダイビング | （任意）Cカード、ログブック、マスク | 未着手 |

※ 南アのプラグ形状などは出発前に再確認すること（未調査）。
