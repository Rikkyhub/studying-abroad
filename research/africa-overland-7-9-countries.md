# 東アフリカ→南部アフリカ縦断：7か国・9か国・モザンビーク追加の実現性（調査版）

**確認日：2026-10-18 / 想定：2027年5月、日本の一般旅券、一人旅の匿名モデル。** Issue [#44](https://github.com/Rikkyhub/studying-abroad/issues/44)（関連 #1, #2, #7, #8, #16, #23, #38）。

> **調査版であり、予約・購入・確定旅程ではない。** 旅程はすべて相対日数（Day N、**Day 1 = マニラ出発日**）で、実在の日付・予約・支払い・個人情報を含まない（[公開データ方針](../docs/05-public-data-policy.md)）。2027年便は未購入・未検証。比較の土台は [アフリカ周遊ルート比較](africa-route-comparison.md)（#23）と [南部アフリカ各国](southern-africa-countries.md)（#38）。

**ラベル**：**確認済み**（URL・確認日あり）／**推計**（式を併記）／**未確認**（取得できなかった。0円や推測値で埋めない）。2026年の料金を2027年のものとは断定しない。

---

## 1. 結論と判定表

**判定の基準（ゲート）**：Issue の「出発から約27〜30日を実旅行に充てる」を、Day 1 = 出発日なので **ケープタウン（CPT）到着が Day 30 以内**と置く。必要日数は「観光日＋移動日＋予備日」の合計（最小／標準／最大）。標準が30以内なら「収まる」、最小のみ30以内なら「条件付き（予備日と観光を削る）」、最小でも30超なら「収まらない」。

| 案 | 国数 | 必要日数（観光日＋移動日＋予備日＝最小／標準／最大） | 1か月以内でCPT着か | 主なボトルネック | 撤退案 |
|---|---:|---|---|---|---|
| **A7** Kenya→Tanzania→Malawi→Zambia→Zimbabwe→Botswana→South Africa | 7 | 8＋10＋2＝**20** ／ 13＋13＋3＝**29** ／ 19＋15＋3＝**37** | **収まる（標準29。余裕1日）。最大側は超過** | Dar es Salaam→Mbeya→Malawi→Lusaka の連続陸路（運行・接続とも**未確認**）、Kasane→CPT 空路の運賃・便 | Lilongwe→Livingstone（または Victoria Falls）を空路に置換（移動1〜2日短縮の**推計**、運賃は未確認）／Malawi を2日に圧縮 |
| **B9** A7＋Uganda＋Rwanda（Rusumo 経由で Tanzania へ） | 9 | 9＋14＋2＝**25** ／ 16＋17＋3＝**36** ／ 24＋19＋3＝**46** | **標準では収まらない（36）。最小のみ25で可** | Kigali→Rusumo→Mwanza、Mwanza→Mbeya（運行**未確認**）、Mbeya→Malawi | Rwanda を削り Kigali を飛ばす（-4〜5日、8か国）／Kigali→Dar es Salaam 空路（運賃未確認）／Uganda・Rwanda の観光日を各1日へ |
| **A7＋Moz** A7＋Mozambique南部（Ponta do Ouro・Maputo） | 8 | 11＋13＋3＝**27** ／ 17＋15＋4＝**36** ／ 24＋18＋4＝**46** | **標準では収まらない（36）。最小27は観光を最小にしたときのみ** | Kasane→JNB→Kosi Bay（国境 08:00〜17:00）→Ponta の接続、潜水後の待機 | Malawi・Tanzania・Kenya を各1日削る（計-3）＋Ponta 2日（-1）＋予備日-1＋Maputo 0泊（-1）で標準36→**30**（**推計**、全項目が最小側）／または Moz を別旅行へ |
| **B9＋Moz** | 10 | 12＋17＋3＝**32** ／ 20＋19＋4＝**43** ／ 29＋22＋4＝**55** | **最小でも32で収まらない** | 上記すべて | Moz か Uganda・Rwanda のどちらかを外す（B9のまま、または A7＋Moz へ） |

- 日数の内訳（行ごとの最小／標準／最大）は[第7章](#7-日別ルート案day番号候補)に置く。式は `必要日数＝観光日T＋移動日M＋予備日B` で、Day N = CPT 到着日の目安。
- Issue の暫定推定（A7 25〜31、B9 29〜36、A7＋Moz 30〜37、B9＋Moz 34〜42）との違い：本書は最小〜最大の幅が広い（最小が短く最大が長い）。**標準値は A7 29、B9 36 で Issue の帯と整合**。A7＋Moz（標準36）と B9＋Moz（標準43）は Issue の上限（37／42）付近。
- **Kenya 初入国での EATV（USD100）は確認できない**（[第4章](#4-ビザ比較表)）。個別手続きを前提に費用を組む。
- 費用は[第8章](#8-費用モデル)。**60万円に収まるとは主張しない。**

---

## 2. 前提

| 項目 | 前提 |
|---|---|
| モデル | 匿名の一般モデル。旅程は相対日（Day N）。実在の出発日・予約・支払い・勤務・学校契約の情報は含まない |
| 対象外 | 島国（マダガスカル・モーリシャス＝別旅行）、レソト、南アフリカ国内観光（乗継・空港・通過のみ）。ブルンジはルワンダ国境閉鎖を前提に**入れない** |
| 多様性方針（#38） | **同じ種類の大型動物サファリを重ねない**。サファリは Chobe（Kasane）に集約し、他国では「そこでしか得られない体験」（湖・滝・文化・海）を優先する |
| 為替 | リポジトリの為替表の USD＝**158.19円**（MUFG TTM、2026-10-16。出典 [MURC](https://www.murc-kawasesouba.jp/fx/index.php)）。KES・UGX・RWF・TZS・MWK・ZMW・MZN は為替未採用のため円換算は**未確認** |
| 料金の年 | 公式料金の多くは2026年値。2027年5月の料金・運行・制度は再確認が必要 |
| 国境の数え方 | 「国数」に数えるのは、国境で適法に入国許可を受けた国。滞在が短くても手続きは省略しない |

---

## 3. 国別

各国の外務省レベルは、リポジトリ既存調査（#23：2026-10-17、#38：2026-10-18）の値を転記したもので、**今回の外務省サイトは保守ページ（取得失敗）のため再取得できていない**。英国FCDOは gov.uk の公開API（`/api/content/foreign-travel-advice/<国>`）で2026-10-18に取得した「最終更新日」と警告区分（全土ではなく地域指定の警告が多い）。FCDOの入国要件は英国旅券向けで、日本旅券の要件ではない（参考）。

### 3.0 国別サマリ

| 国 | 日本旅券の入国（公式URL） | 最低／推奨日数（**推計**） | 固有体験の候補（**推計**・一般知識） | 外務省（既存調査） | FCDO（2026-10-18取得） |
|---|---|---|---|---|---|
| Kenya | eTA必須。標準 USD30（再入国は EAC 域内可との記載）。+政府提供の旅行医療保険が必須（金額未確認） | 1／2 | [Nairobi](https://www.google.com/maps/search/?api=1&query=Nairobi%20National%20Park) 周辺。**サファリはここで重ねない** | 2025-05-19更新：ソマリア国境等レベル4、ラム郡等レベル3、ナイロビ市の一部レベル2、その他レベル1 | 2026-10-16更新。地域指定の「全面回避」「不要不急回避」警告あり。エボラ関連の入国時スクリーニング記載 |
| Uganda | 査証必須（免除国一覧に日本は見当たらず）。単独査証 USD50。黄熱病証明は2026-10-02付で**不要に** | 1／2 | Kampala・Nile 源流（Jinja）。ゴリラ許可証は料金・可否**未確認** | **未確認** | 2026-10-08更新。警告区分なし。コンゴ民主共和国国境は閉鎖（FCDO記載） |
| Rwanda | 全国籍に到着時査証（2018-01-01以降）。日本の料金は**未確認**（Issue の USD50 は公式ページで再取得できず） | 1／2 | Kigali の追悼施設と街 | **未確認** | 2026-09-04更新。Rusizi 地区に不要不急回避。DRC国境に制限 |
| Tanzania | 査証必要。日本は到着時／オンライン可リストに掲載。通常 USD50（90日） | 1／2（A7はDar es Salaam）。Mbeya 経由 | Swahili 海岸文化（Dar es Salaam）。サファリは重ねない | 2025-11-03更新：キゴマ州西部レベル3、ムトワラ州レベル2、アルーシャ州・ザンジバルを含む沿岸レベル1 | 2026-10-09更新。地域指定の不要不急回避警告。政府提供の旅行保険が必須（金額未確認） |
| Malawi | 査証必要。オンライン USD75（公式料金表）。FCDOは到着時 USD50 と記載。日本固有の扱いは**未確認** | 2／3 | Malawi 湖（水辺・淡水湖の滞在） | **未確認** | 2026-07-03更新。警告区分なし |
| Zambia | **日本は査証免除（免除国一覧 No.76）。** KAZA の対象国にも日本掲載 | 1／1〜2 | Livingstone 側の滝（Mosi-oa-Tunya）、Zambezi 川 | 2026-04-15更新：コンゴ民主共和国・アンゴラ国境地帯レベル2、その他レベル1 | 2026-06-01更新。警告区分なし |
| Zimbabwe | 単独入国 USD30（公式料金表、港でも可）。日本は到着時査証（#38 取得）。複数入国 USD55 の表記も | 2／2 | Victoria Falls のジンバブエ側 | 2024-12-18更新：全土レベル1 | 2026-07-15更新。警告区分なし |
| Botswana | 日本の免除は公式で**未確認**（gov.bw が証明書エラー）。FCDOは英国旅券90日免除 | 1／2 | Chobe の川沿い観察（このモデルのサファリ） | **未確認** | 2026-06-01更新。警告区分なし |
| South Africa（通過） | 日本は90日免除（DHA免除国表）。2026-07-01以降オンライン旅行者申告が必要（FCDO） | 乗継のみ | 対象外（乗継） | 2025-04-28更新：JNB・Pretoria・Durban のCBD周辺レベル2、その他レベル1 | 2026-07-08更新。警告区分なし |
| Mozambique（南部） | ビザ免除＋事前登録（駐日大使館）／ETA対象（政府ポータル）／ETA 5営業日前（FCDO）。**3出典が食い違う**（第4章） | 3／4〜5（Ponta 2〜3＋移動） | Ponta do Ouro のリーフ潜水（動物遭遇は確約しない） | 2025-07-04更新：北部カーボデルガード州等レベル3、**Maputo を含むその他レベル1**（#38転記） | 2026-08-20更新。地域指定の警告あり（南部の区分は今回の取得範囲外＝**未確認**） |
| Eswatini（任意） | 日本の扱いは公式で**未確認**（gov.sz が応答なし）。FCDOは英国旅券30日免除 | 2／3 | 自然保護区と文化体験（#38） | **未確認** | 2025-12-10更新。警告区分なし |

出典（入国要件の原典）：[Kenya 駐日大使館 eTA](https://www.kenyarep-jp.com/en/eta/)／[Kenya eTA 資格画面](https://extern.api.etakenya.go.ke/eligibility)／[Uganda 入管 Tourist Visa](https://immigration.go.ug/services/tourist-visa)／[Uganda 入管 EATV](https://immigration.go.ug/services/east-african-tourist-visa)／[Rwanda 入管 特別枠査証](https://www.migration.gov.rw/our-services/visa-issued-under-special-arrangement)／[Tanzania eVisa ガイドライン](https://visa.immigration.go.tz/guidelines)／[Malawi 入管 料金](https://www.immigration.gov.mw/visa-fees)／[Zambia 免除国](https://www.zambiaimmigration.gov.zm/nationals-who-dont-require-visa/)／[KAZA UNIVISA](https://www.zambiaimmigration.gov.zm/kaza-univisa/)／[Zimbabwe 入管 料金](https://www.zimimmigration.gov.zw/?page_id=6958)／[南アフリカ DHA 免除国](https://www.dha.gov.za/index.php/immigration-services/exempt-countries)（いずれも2026-10-18確認）。

### 3.1 国別の補足（確認できた事実）

- **Kenya**：標準 eTA USD30、通過 USD20、1年複数回 USD300、East African Tourist eTA（USD100）は大使館ページで `TEMPORARILY UNAVAILABLE`、政府画面で `COMING SOON`。駐日大使館ページに「eTA申請者に旅行医療保険が必須」の見出しあり。FCDOは2026-10-05以降、ケニア政府提供の保険が必須と記載（保険料は**未確認**）。
- **Uganda**：公式ページ「Official Notice: Yellow Fever Vaccination Certificate is No Longer Mandatory for Entry into Uganda / October 2, 2026」。EATV と単独（USD50）は同じ入管サイトに掲載。
- **Tanzania**：オンライン申請は通常査証 USD50（最長90日）、複数入国 USD100。FCDOは、居住者以外にタンザニア政府提供の入国旅行保険が必須で、最初の入国口で一度購入すればよいと記載。
- **Malawi**：公式のオンライン料金表は Single Entry USD75、Transit USD50（VISA／Mastercardのみ）。FCDOは到着時の単一入国 USD50 と記載。**50と75は「到着時」と「オンライン」の別料金として併存**し、どちらが日本旅券に適用されるかは公式に未確認。2026年に日本人対象の制度変更があるとの Issue 記載は、公式ページから確認できなかった（**未確認**）。
- **Zimbabwe**：公式料金表は「Ordinary single-entry visa（online）30 USD／（port of entry）30 USD」「Multiple entry visa 55 USD」。
- **Botswana・Eswatini**：公式サイト（gov.bw：証明書エラー、gov.sz：応答なし）に接続できず、日本旅券の要件は**未確認**。

---

## 4. ビザ比較表

為替は USD＝158.19円（MUFG TTM、2026-10-16）。差額は式で示す。

### 4.1 EATV（USD100）vs 個別（Kenya・Uganda・Rwanda）

| 項目 | 内容 | 状態 |
|---|---|---|
| EATV の制度 | Uganda・Rwanda 両政府が USD100・90日・Kenya／Uganda／Rwanda の複数回入国と説明。**発給国が最初の入国国** | **確認済み**（[Uganda](https://immigration.go.ug/services/east-african-tourist-visa)、[Rwanda](https://www.migration.gov.rw/our-services/visa-issued-under-special-arrangement)、2026-10-18） |
| Kenya 発給 | 大使館：`East African Tourist eTA *TEMPORARILY UNAVAILABLE`／政府画面：`East African Tourist eTA COMING SOON` | **確認済み**（[大使館](https://www.kenyarep-jp.com/en/eta/)、[政府画面](https://extern.api.etakenya.go.ke/eligibility)、2026-10-18）。Issue の記載と一致 |
| Kenya 初入国で EATV が通用するか | 公式ページに「Kenya 初入国で Uganda／Rwanda 発給の EATV が使える」とは書かれていない。各国は「発給国が最初の入国国」とのみ記載 | **未確認**。使えると断定しない |
| 個別の合計 | Kenya eTA 30＋Uganda 50＋Rwanda 50＝**USD130**（Rwanda の50は Issue 記載値で、公式料金ページは今回**未取得**） | Kenya・Uganda＝確認済み／Rwanda＝**未確認** |
| 差額 | 130－100＝**USD30＝4,746円**（30×158.19）。EATV が使える場合の理論差額 | 推計（式） |
| 入口を Uganda／Rwanda に変えた場合 | EATV を Uganda または Rwanda で発給し、その国から入る順序にすれば制度上は成立する。ただし Kenya 先頭の本ルート（Nairobi→Kampala）とは順序が変わる。航空運賃の差は**未確認** | **未確認** |
| Kenya の追加費用 | 標準 eTA 申請時に政府提供の旅行医療保険の購入が必要（FCDO）。金額**未確認**。個別でも EATV でも別に発生しうる | 未確認 |
| 購入前の確認先 | Kenya 入国当局（Directorate of Immigration Services）への照会が必要。**本調査では送信していない**（外部送信は承認なしに行わない） | 未達 |

結論：費用計算は**個別USD130**（A7は Kenya のみ USD30、B9は Kenya＋Uganda＋Rwanda）で組み、EATV はあくまで最大USD30の節約余地として扱う。

### 4.2 KAZA UNIVISA vs Zimbabwe 単独＋Zambia 免除（Zimbabwe 入国回数 n 別）

| 項目 | 内容 | 状態 |
|---|---|---|
| KAZA UNIVISA | USD50。12か月のうち30日まで、Zambia・Zimbabwe 滞在中有効。Botswana は **Kazungula 国境経由の日帰りのみ**。対象国に日本掲載 | **確認済み**（[KAZA](https://www.zambiaimmigration.gov.zm/kaza-univisa/)、2026-10-18） |
| KAZA の窓口料金 | 公式料金表で Kaza 50＋手数料 0.5＝**USD50.50** | **確認済み**（[料金表](https://www.zambiaimmigration.gov.zm/for-residents/pricing-page/)、2026-10-18） |
| Zambia | 日本は査証免除（一覧 No.76）。無料 | **確認済み**（[免除国](https://www.zambiaimmigration.gov.zm/nationals-who-dont-require-visa/)、2026-10-18） |
| Zimbabwe 単独 | USD30／入国。複数入国 USD55 の表記も | **確認済み**（[料金表](https://www.zimimmigration.gov.zw/?page_id=6958)、2026-10-18） |

| Zimbabwe 入国回数 n | 個別（Zimbabwe 単独 30×n、Zambia 0） | KAZA（50） | 差額（KAZA－個別） | 有利 |
|---:|---:|---:|---:|---|
| 1 | 30 | 50 | **+20** | 個別（4,746円 vs 7,910円。差 3,164円＝20×158.19） |
| 2 | 60 | 50 | **-10** | KAZA（差 1,582円＝10×158.19） |
| 3 | 90 | 50 | **-40** | KAZA |

- 式：個別＝30n、KAZA＝50（カード手数料込みなら50.50）。**損益分岐は n＝2（30×2＞50）**。複数入国 USD55 を使えば n≧2 でも 55 で、KAZA（50）が5ドル有利。
- A7・B9 の標準ルートは Livingstone（Zambia）→ Victoria Falls 日帰り（Zimbabwe、n＝1）→ Kasane（Botswana）なので**個別（Zimbabwe 30）が有利**。Zimbabwe 側と Zambia 側を2回以上往復する日程なら KAZA が有利。
- **Botswana に泊まる場合、KAZA は Botswana の滞在を賄わない**（日帰りのみ）。Botswana の入国審査は別途必要。

### 4.3 Mozambique：eTA／事前登録の相違

| 出典 | 内容 | 状態 |
|---|---|---|
| [駐日モザンビーク大使館](https://embamoc.jp/visas) | 政令 No.10/2023 により日本を含む29か国は**観光・商用の査証を免除**。30日（延長30日）、複数入国可。旅券残存6か月、往復航空券の写し、宿泊証明を要する。**免除対象者も evisa.gov.mz で出発の48時間前までに事前登録が必要** | **確認済み**（2026-10-18）。ページに事前登録の「停止」注記は**今回の取得本文では見つからなかった** |
| [政府ポータル](https://evisa.gov.mz/Home) | 「新プラットフォームは2026-02-11開始、旧プラットフォームは廃止」。日本は **ETA プログラムの表（30日・Tourist/Business）に掲載**。ETA の料金は同ページに未掲載 | **確認済み**（2026-10-18）。金額は**未確認** |
| [英国FCDO](https://www.gov.uk/foreign-travel-advice/mozambique/entry-requirements)（英国旅券向け） | 渡航前に ETA 必須、**5営業日前までの申請を推奨**、国境で支払い不可、約USD47（査証料37＋処理手数料650 MZN） | **確認済み**（英国旅券。日本旅券の金額は**未確認**） |

差異：大使館は「免除＋48時間前の事前登録」、政府ポータルは「ETA対象」、FCDOは「5営業日前のETA」。**必要な手続き・金額・所要は2027年直前に政府ポータルの実動作か当局へ確認**（「ビザ免除＝手続き0円」とは見なさない）。費用モデルでは英国旅券の約USD47を**仮置き**（日本旅券で同額とは断定しない）。

### 4.4 その他

| 国 | 内容 | 状態 |
|---|---|---|
| Malawi | オンライン Single USD75、Transit USD50（公式料金表）。到着時 USD50（FCDO）。2026年の日本人向け制度変更は公式で見つからず | 公式料金＝確認済み／日本固有の扱い＝**未確認** |
| Tanzania | 通常 USD50（90日）、複数 USD100。日本は到着時／オンライン可の一覧に掲載。EATV の対象外 | **確認済み**（[ガイドライン](https://visa.immigration.go.tz/guidelines)、2026-10-18） |
| South Africa | 日本は90日免除 | **確認済み**（[DHA](https://www.dha.gov.za/index.php/immigration-services/exempt-countries)、2026-10-18） |

---

## 5. 陸路バス所要時間表

**2027年便は未購入・未検証。運行の存在と所要の掲載のみを確認**。取得は各ページ25秒以内のタイムアウトで1回のみ。

| 区間 | 運行会社・URL | 所要時間・運賃・便（掲載） | 確認日 | 状態 |
|---|---|---|---|---|
| Nairobi→Kampala | [Modern Coast](https://moderncoastltd.com/routes/nairobi-to-kampala) | 約12時間、KES 3,500〜5,000、毎日 06:00／10:30／15:00／19:00発 | 2026-10-18 | **確認済み**（Issue と一致） |
| Kampala→Kigali | [Modern Coast](https://moderncoastltd.com/routes) | 9時間、UGX 80,000〜（Kigali→Kampala は RWF 35,000〜）。Issue の「夜発翌朝着」は未再確認 | 2026-10-18 | 所要＝**確認済み**／夜行の詳細＝**未確認**（Trinity Bus は今回再取得せず） |
| Nairobi→Kigali（直通） | [Modern Coast](https://moderncoastltd.com/routes) | 15時間、KES 7,000〜 | 2026-10-18 | **確認済み**（Issue になし。Uganda を飛ばす選択肢） |
| Nairobi→Dar es Salaam | [Modern Coast](https://moderncoastltd.com/routes) | 14時間、KES 4,500〜 | 2026-10-18 | **確認済み**（A7 の入口。便数は未確認） |
| Mwanza→Mbeya | [Premierline](https://premierline.co.tz/bus-tickets/mwanza-to-mbeya) | 取得ページは検索フォームのみ。取得日の便は「No trips found」。Issue の「約19時間、87,000 TZS、特定日の例」は**再現できなかった** | 2026-10-18 | **未確認**（動的検索のため日付指定が必要） |
| Lusaka→Livingstone | [African Bus](https://www.africanbus.com/tickets) | Power Tools 社 03:30発→11:15着（7時間45分）ZMW 300、休運日 Saturday。06:00発（9時間40分）ZMW 300、Rayon 社 07:00発 ZMW 500（同ページの所要「3時間05分」は他社と矛盾し、信頼しない） | 2026-10-18 | **確認済み**（Issue の「約7時間45分／300 ZMW」と一致） |
| Kasane→Maputo | [rome2rio](https://www.rome2rio.com/s/Kasane/Maputo) | HTTP 403 で取得不可。Issue の「約25時間30分」は再確認できない | 2026-10-18 | **未確認**（運行会社直販ではなく交通検索の例） |
| Kigali→Rusumo→Mwanza | 運行会社を特定できず | — | — | **未確認**（直通便の存在を示す公式・運行会社ページを取得できていない） |
| Dar es Salaam→Mbeya | 運行会社を特定できず | — | — | **未確認**（A7 の主要区間） |
| Mbeya→Songwe 国境→Karonga→Mzuzu／Lilongwe→Lusaka | 運行会社を特定できず | — | — | **未確認**（Tanzania→Malawi→Zambia の接続の実証なし） |

結論：**Nairobi–Kampala–Kigali は掲載上つながる。Kigali→Tanzania→Malawi→Zambia は通しの実証がなく、B9 の核心リスク**。夜行を避けると中間泊が必要で、日数に反映した（Mwanza→Mbeya は2日）。

---

## 6. Mozambique ダイビング（南部限定）

### 6.1 Ponta do Ouro のショップ料金（Gozo Azul、2026年公開料金）

出典：[Gozo-Azul Diving](https://gozo-azul.co.za/scuba-diving/)（2026-10-18確認）。「為替変動により表示額は変わりうる」との注記あり。

| 項目 | USD | 備考 |
|---|---:|---|
| リーフダイブ（1〜4本、器材別） | 50／本 | 5〜9本は45、10本以上は40 |
| シャークダイブ | 60／本 | パッケージ対象外（追加料金） |
| フルギア（1〜4本時） | 15／本 | シリンダー8、ウエイト5は別項目。**フルギアにシリンダー・ウエイトが含まれるかは未確認** |
| リーフ税（連続14日） | 10 | |

**Issue の USD140 の再計算**：リーフ2本 50×2＝100、フルギア 15×2＝30、リーフ税 10 → 100＋30＋10＝**USD140**（Issue と一致）。140×158.19＝**22,147円**（Issue の約22,100円と一致）。

- 4本の場合：50×4＋15×4＋10＝**USD270＝42,711円**。
- シリンダー8＋ウエイト5が別料金だった場合の上振れ：2本で＋(8＋5)×2＝USD26 → 140＋26＝166＝26,260円（**推計**。実際の扱いは未確認）。
- 5月の水温・海況・見られる生物、ソロ参加条件、経験条件、送迎の価格は**未確認**。動物遭遇は確約しない。

### 6.2 アクセス（モザンビーク国立公園当局 ANAC）

出典：[ANAC Ponta do Ouro](https://www.anac.gov.mz/en/parques/ponta-do-ouro/)（2026-10-18確認）。

| 項目 | 内容 | 状態 |
|---|---|---|
| Kosi Bay（ANACの表記は Kosy Bay）国境 | Johannesburg から 673 km、Durban から 498 km、**毎日 08:00〜17:00**。JNB→国境は7〜8時間（道路状況による）。閉門の数時間前の到着を計画 | **確認済み** |
| 道路 | 宿泊地周辺の砂道は4WD推奨。国境にレンタカーあり | **確認済み** |
| Maputo から | Katembe 経由で約3時間（フェリーは毎時、Katembe から約110 km の土道、4WD推奨）、Boane 経由で約4時間（約170 km） | **確認済み** |
| 航空 | Kasane→JNB→Maputo の便・運賃 | **未確認** |

### 6.3 潜水後の飛行

出典：[DAN Guidelines for Flying After Diving](https://dan.org/health-medicine/health-resource/health-safety-guidelines/guidelines-for-flying-after-diving/)（2026-10-18確認）。

- 合意勧告は、**ノンデコ潜水1回なら最低12時間、複数日の反復潜水なら最低18時間**。減圧停止を伴う潜水やヘリオックス／トライミックスはこれより大幅に長い。DAN がより単純な「あらゆるレクリエーション潜水後24時間」を提案した経緯が同ページにある。
- Issue の「最低18時間、日程設計は24時間以上」は、**DAN の飛行に関する勧告**として扱う。道路での高所移動（JNB は標高が高い）はこのページの対象外で、機械的に同じ時間を当てはめない（高所移動の目安は**未確認**。保守的に最終潜水から24時間を空けるのは計画上の余裕）。
- 日程への反映：最終潜水を午前に済ませ、Maputo 泊を挟んで翌日以降に空路（Day 表の c27〜c29）。

### 6.4 日数基準と安全

- **日数基準**（**推計**）：Ponta の潜水2〜4日（標準3）＋移動（Kasane→JNB→国境→Ponta 1〜2日、Ponta→Maputo 1日）＋Maputo 0〜1泊＋海況予備1日 → 追加は標準で7日前後（Day 表では A7 の標準29→36）。最低3日（移動1＋潜水2）・推奨4〜5日は成り立たず、**CPT への帰路を含めると+7日**。Issue の「+3〜5日」は帰路と待機を含めると不足の見積り。
- **安全**：Maputo を含む南部はレベル1（外務省 2025-07-04、#38転記）。北部（カーボデルガード州等）レベル3。**北部経由の短絡路を使わない**。FCDOはランド国境の混雑・日没後の強盗に注意（#23記載、本書では再取得せず）。国境越えは昼間のみ、Kosi Bay は17:00閉門。

---

## 7. 日別ルート案（Day番号・候補）

**状態はすべて「候補」。確定ではない。** カレンダー日付は置かない（Day 1 = マニラ出発日）。T＝観光日、M＝移動日、B＝予備日。バスの所要は[第5章](#5-陸路バス所要時間表)。

### 7.1 日数の内訳（行ごとの最小／標準／最大）

| 行 | 区分 | 内容 | 最小 | 標準 | 最大 | A7 | B9 | A7+Moz | B9+Moz |
|---|---|---|---:|---:|---:|:-:|:-:|:-:|:-:|
| c01 | M | MNL→NBO（出発日〜到着日） | 2 | 2 | 2 | ○ | ○ | ○ | ○ |
| c02 | T | Kenya（Nairobi） | 1 | 2 | 3 | ○ | ○ | ○ | ○ |
| c03 | M | Nairobi→Dar es Salaam（バス） | 1 | 1 | 1 | ○ | | ○ | |
| c04 | T | Tanzania（Dar es Salaam） | 1 | 2 | 3 | ○ | | ○ | |
| c05 | M | Dar es Salaam→Mbeya | 1 | 1 | 2 | ○ | | ○ | |
| c06 | T | Mbeya 周辺 | 0 | 1 | 1 | ○ | ○ | ○ | ○ |
| c07 | M | Nairobi→Kampala（バス） | 1 | 1 | 1 | | ○ | | ○ |
| c08 | T | Uganda（Kampala 周辺） | 1 | 2 | 3 | | ○ | | ○ |
| c09 | M | Kampala→Kigali（バス） | 1 | 1 | 1 | | ○ | | ○ |
| c10 | T | Rwanda（Kigali 周辺） | 1 | 2 | 3 | | ○ | | ○ |
| c11 | M | Kigali→Rusumo→Mwanza | 2 | 2 | 3 | | ○ | | ○ |
| c12 | T | Mwanza（ビクトリア湖） | 0 | 1 | 2 | | ○ | | ○ |
| c13 | M | Mwanza→Mbeya（夜行回避で中間泊） | 2 | 2 | 2 | | ○ | | ○ |
| c14 | M | Mbeya→国境→Karonga→Mzuzu | 1 | 2 | 2 | ○ | ○ | ○ | ○ |
| c15 | T | Malawi（湖畔） | 2 | 3 | 4 | ○ | ○ | ○ | ○ |
| c16 | M | Mzuzu→Lilongwe | 1 | 1 | 2 | ○ | ○ | ○ | ○ |
| c17 | M | Lilongwe→Lusaka（陸路2日／空路1日） | 1 | 2 | 2 | ○ | ○ | ○ | ○ |
| c18 | M | Lusaka→Livingstone（バス） | 1 | 1 | 1 | ○ | ○ | ○ | ○ |
| c19 | T | Zambia（Livingstone） | 1 | 1 | 2 | ○ | ○ | ○ | ○ |
| c20 | T | Zimbabwe（Victoria Falls） | 2 | 2 | 3 | ○ | ○ | ○ | ○ |
| c21 | M | Victoria Falls→Kasane（Kazungula） | 1 | 1 | 1 | ○ | ○ | ○ | ○ |
| c22 | T | Botswana（Chobe／Kasane） | 1 | 2 | 3 | ○ | ○ | ○ | ○ |
| c23 | M | Kasane→JNB→CPT（空路・乗継） | 1 | 2 | 2 | ○ | ○ | | |
| c24 | M | Kasane→JNB（空路） | 1 | 1 | 1 | | | ○ | ○ |
| c25 | M | JNB→Kosi Bay 国境→Ponta do Ouro | 1 | 1 | 1 | | | ○ | ○ |
| c26 | T | Ponta do Ouro（潜水） | 2 | 3 | 4 | | | ○ | ○ |
| c27 | M | Ponta→Maputo | 1 | 1 | 1 | | | ○ | ○ |
| c28 | T | Maputo（最終潜水から24時間待機を兼ねる） | 1 | 1 | 1 | | | ○ | ○ |
| c29 | M | Maputo→（JNB 経由）CPT | 1 | 1 | 2 | | | ○ | ○ |
| c30 | B | 予備日 | 2 | 3 | 3 | ○ | ○ | | |
| c31 | B | 予備日（Moz 追加分を含む） | 3 | 4 | 4 | | | ○ | ○ |

| 案 | T（最小／標準／最大） | M | B | 合計（最小／標準／最大） |
|---|---|---|---|---|
| A7 | 8／13／19 | 10／13／15 | 2／3／3 | **20／29／37** |
| B9 | 9／16／24 | 14／17／19 | 2／3／3 | **25／36／46** |
| A7＋Moz | 11／17／24 | 13／15／18 | 3／4／4 | **27／36／46** |
| B9＋Moz | 12／20／29 | 17／19／22 | 3／4／4 | **32／43／55** |

- 日数は**独自の推計**（国別の最低／推奨日数と、バスの掲載所要を日単位に切り上げ、夜間移動と深夜着を避ける前提）。実運行で接続を検証した確定日程ではない。
- オプション Eswatini：+2／+3／+3日（JNB から往復の乗合バス、片道約4時間40分、[TransMagnific](https://transmagnific.com/schedule.php)、#38 で2026-10-18に取得した記載の転記で、今回は再取得していない）。
- 空路区間（c17 の空路置換、c23〜c24、c29）の便・運賃・乗継は**未確認**。

### 7.2 A7（標準29日）

| Day | 場所 | 手段 | 所要 | 国境 | 宿泊地 | 観光 | 状態 |
|---|---|---|---|---|---|---|---|
| 1〜2 | MNL→Nairobi（Kenya） | 航空（乗継あり） | 未確認 | Kenya 入国（eTA） | Nairobi | 到着後は休養 | 候補（航空**未確認**） |
| 3〜4 | Nairobi | 市内 | — | — | Nairobi | 市内・国立公園の一部（サファリは重ねない） | 候補 |
| 5 | Nairobi→Dar es Salaam | Modern Coast 掲載14時間 | 14h（掲載） | Namanga 周辺（名称は一般知識）。Tanzania 入国 | Dar es Salaam | — | 候補。**夜間到着の回避は未確認** |
| 6〜7 | Dar es Salaam | 市内 | — | — | Dar es Salaam | Swahili 海岸文化 | 候補 |
| 8 | Dar es Salaam→Mbeya | 長距離バス | **未確認** | — | Mbeya | — | **未確認区間** |
| 9 | Mbeya | — | — | — | Mbeya | 高地の軽い観光 | 候補 |
| 10〜11 | Mbeya→Songwe 国境→Karonga→Mzuzu | バス／乗合 | **未確認** | Tanzania 出国・Malawi 入国 | Karonga または Mzuzu | — | **未確認区間** |
| 12〜14 | Malawi 湖畔 | 現地 | — | — | 湖畔 | 湖の滞在 | 候補 |
| 15 | Mzuzu→Lilongwe | バス | **未確認** | — | Lilongwe | — | 未確認 |
| 16〜17 | Lilongwe→Lusaka | バス（Mchinji 国境）2日、または空路 | **未確認** | Malawi 出国・Zambia 入国（免除） | 国境近郊→Lusaka | — | **未確認区間** |
| 18 | Lusaka→Livingstone | African Bus 掲載 7h45〜9h40 | 約8〜10h | — | Livingstone | — | 候補（**確認済み**の運行） |
| 19 | Livingstone | 現地 | — | — | Livingstone | Zambia 側の滝 | 候補 |
| 20〜21 | Victoria Falls（Zimbabwe 側） | 橋の国境 | 数時間（未確認） | Zambia 出国・Zimbabwe 入国（USD30） | Victoria Falls | 滝の Zimbabwe 側 | 候補 |
| 22 | Victoria Falls→Kasane | 陸路（Kazungula） | **未確認** | Zimbabwe 出国・Botswana 入国 | Kasane | — | 候補 |
| 23〜24 | Kasane | 現地 | — | — | Kasane | Chobe の川沿い観察 | 候補 |
| 25〜26 | Kasane→JNB→CPT | 空路 | **未確認** | South Africa 入国（免除。オンライン申告） | CPT | 乗継のみ | 候補（運賃は #38 の参考 約60,500円＝Skyscanner参考、**非保証・再取得せず**） |
| 27〜29 | 予備日（途中に分散して使う） | — | — | — | — | — | 余裕1日（Day 30 に対し） |

### 7.3 B9（標準36日）

| Day | 場所 | 手段 | 所要 | 国境 | 宿泊地 | 観光 | 状態 |
|---|---|---|---|---|---|---|---|
| 1〜2 | MNL→Nairobi | 航空 | 未確認 | Kenya 入国 | Nairobi | — | 候補 |
| 3〜4 | Nairobi | — | — | — | Nairobi | 市内 | 候補 |
| 5 | Nairobi→Kampala | Modern Coast 12h | 12h（掲載） | Busia 周辺。Uganda 入国 | Kampala | — | 候補（**確認済み**の運行） |
| 6〜7 | Kampala | — | — | — | Kampala | Nile 源流方面の候補 | 候補 |
| 8 | Kampala→Kigali | Modern Coast 9h | 9h（掲載） | Rwanda 入国 | Kigali | — | 候補（夜行の有無**未確認**） |
| 9〜10 | Kigali | — | — | — | Kigali | 追悼施設・街 | 候補 |
| 11〜12 | Kigali→Rusumo→Mwanza | バス／乗合 | **未確認** | Rwanda 出国・Tanzania 入国（Rusumo） | Rusumo 近郊→Mwanza | — | **未確認区間（核心リスク）** |
| 13 | Mwanza | — | — | — | Mwanza | ビクトリア湖 | 候補 |
| 14〜15 | Mwanza→Mbeya | Premierline 等 | 約19h（Issue記載・再現不可） | — | 中間泊→Mbeya | — | **未確認区間** |
| 16 | Mbeya | — | — | — | Mbeya | — | 候補 |
| 17〜18 | Mbeya→Songwe→Mzuzu | バス／乗合 | **未確認** | Malawi 入国 | Karonga／Mzuzu | — | **未確認区間** |
| 19〜21 | Malawi 湖畔 | — | — | — | 湖畔 | 湖の滞在 | 候補 |
| 22 | Mzuzu→Lilongwe | バス | **未確認** | — | Lilongwe | — | 未確認 |
| 23〜24 | Lilongwe→Lusaka | バス2日／空路 | **未確認** | Zambia 入国 | Lusaka | — | **未確認区間** |
| 25 | Lusaka→Livingstone | African Bus | 約8〜10h | — | Livingstone | — | 候補 |
| 26 | Livingstone | — | — | — | Livingstone | Zambia 側の滝 | 候補 |
| 27〜28 | Victoria Falls | 橋の国境 | 数時間（未確認） | Zimbabwe 入国 | Victoria Falls | Zimbabwe 側の滝 | 候補 |
| 29 | →Kasane | 陸路 | **未確認** | Botswana 入国 | Kasane | — | 候補 |
| 30〜31 | Kasane | — | — | — | Kasane | Chobe | 候補 |
| 32〜33 | Kasane→JNB→CPT | 空路 | **未確認** | South Africa 入国 | CPT | 乗継 | 候補 |
| 34〜36 | 予備日 | — | — | — | — | — | **Day 30 を6日超過** |

### 7.4 A7＋Moz（標準36日）

Day 1〜24 は A7（7.2）と同じ。25日目以降：

| Day | 場所 | 手段 | 所要 | 国境 | 宿泊地 | 観光 | 状態 |
|---|---|---|---|---|---|---|---|
| 25 | Kasane→JNB | 空路 | **未確認** | South Africa 入国 | JNB 近郊 | — | 候補 |
| 26 | JNB→Kosi Bay→Ponta do Ouro | 車（約673km・7〜8h）＋国境（08:00〜17:00）＋砂道4WD | 7〜8h＋国境（ANAC） | South Africa 出国・Mozambique 入国 | Ponta do Ouro | — | 候補。**国境の閉門前に着く計画が必須** |
| 27〜29 | Ponta do Ouro | 現地ボート | — | — | Ponta do Ouro | リーフ潜水（2〜4本） | 候補（料金は第6章） |
| 30 | Ponta→Maputo | 陸路（Katembe経由約3h／Boane経由約4h） | 3〜4h（ANAC） | — | Maputo | — | 候補 |
| 31 | Maputo | — | — | — | Maputo | 最終潜水から24時間の待機（DAN勧告に基づく計画上の余裕） | 候補 |
| 32 | Maputo→JNB→CPT | 空路 | **未確認** | South Africa 入国 | CPT | — | 候補 |
| 33〜36 | 予備日 | — | — | — | — | — | **Day 30 を6日超過** |

---

## 8. 費用モデル

**一人・円。USD＝158.19円（MUFG TTM、2026-10-16）。** 8項目を分け、同じ費用を二重に数えない（宿は1泊＝1回、国境費用はビザ欄だけ、バス運賃は陸路欄だけ、ツアーは潜水・サファリ等の追加体験だけ）。**未確認の項目は0円でなく「未確認」**とし、既知分だけ合算する。**60万円に収まるとは主張しない。**

| 項目 | A7 | B9 | A7＋Moz | 式・根拠 | 状態 |
|---|---|---|---|---|---|
| 航空 | MNL→NBO **未確認**＋Kasane→CPT 約60,500円（#38の参考最安、非保証） | MNL→NBO **未確認**＋同左 | MNL→NBO **未確認**＋Kasane→JNB→Maputo→CPT **未確認** | 運賃は Skyscanner の参考で、このPRでは再取得していない | **未確認**を含む |
| 陸路バス | Nairobi→Dar es Salaam KES 4,500〜、Lusaka→Livingstone ZMW 300〜500、他は未確認 | Nairobi→Kampala KES 3,500〜5,000、Kampala→Kigali UGX 80,000〜、Lusaka→Livingstone ZMW 300〜500、他は未確認 | A7と同じ＋Moz内の送迎**未確認** | 掲載運賃（第5章）。KES・UGX・ZMW の円換算は為替未採用のため**未確認** | **未確認**を含む |
| 宿 | 日数の積み上げ。国別の単価は Kenya・Tanzania・Malawi・Uganda・Rwanda が**未確認**。Zimbabwe 3〜7万円、Zambia 1.8〜4.5万円、Botswana(Chobe) 4〜8万円は#38の「現地費」（宿＋食＋域内移動＋主な観光の合算）の再掲 | 同左＋Uganda・Rwanda・Mwanza **未確認** | A7＋Moz 現地費 3〜8万円（#38の仮置き） | 現地費は宿・食・域内移動・観光を含む合算のため、宿・食・ツアーを別欄に足すと**二重計上**になる | 一部のみ（#38転記） |
| 食 | 上記の現地費に含む（別計上しない） | 同左 | 同左 | 二重計上防止 | — |
| ビザ・入国許可 | Kenya 30＋Tanzania 50＋Malawi 50〜75＋Zimbabwe 30（n＝1）＝USD160〜185＝**25,310〜29,265円** | Kenya 30＋Uganda 50＋Rwanda 50＋Tanzania 50＋Malawi 50〜75＋Zimbabwe 30＝USD260〜285＝**41,129〜45,084円**（EATVが使えれば USD230〜255＝36,384〜40,338円） | A7＋Moz ETA 約USD47（仮置き）＝USD207〜232＝**32,745〜36,700円** | 公式料金（第4章）。Botswana・Eswatini は**未確認**のため含まず。Rwanda の50は Issue 記載で**未確認**。Kenya・Tanzania の政府提供保険は金額**未確認** | 確認済み＋未確認 |
| ツアー・体験 | Chobe のボート・ゲームドライブ等は#38の現地費に含む | 同左 | 潜水：リーフ2本＋ギア＋リーフ税 USD140＝**22,147円**、4本なら USD270＝**42,711円**（第6章） | 140×158.19、270×158.19 | 確認済み（2026年価格） |
| 保険 | **未確認**（旅行保険は未調査）。Kenya・Tanzania の政府提供保険も別途 | 同左 | 同左（潜水の保険条件も未確認） | — | **未確認** |
| 予備日 | 3日分（標準）の宿・食は現地費の1日平均×3日として別途見積もる。単価未確認のため金額は**未確認** | 3日分（同） | 4日分（同） | 予備日数は第7章 | **未確認** |

- **確認できた範囲の合計（参考）**：ビザ（A7 25,310〜29,265円／B9 41,129〜45,084円／A7＋Moz 32,745〜36,700円）＋潜水（A7＋Moz のみ 22,147〜42,711円）＋Kasane→CPT 参考運賃（約60,500円）。**これ以外（MNL→NBO、国別の宿・食、バス運賃の円換算、保険、予備日）が未確認のため、総額は算出していない**。
- 日数が増えるほど宿・食・予備日が増える。B9 と A7＋Moz は標準で30日を超えるので、費用面でも1か月計画に不利（定性的な推計）。

---

## 9. Google Maps 検索リンク

名称は一般に使われる呼び名。国境はポスト名が現地で異なる場合がある。

| 場所 | リンク |
|---|---|
| Rusumo 国境（Rwanda↔Tanzania） | [Rusumo Border Post](https://www.google.com/maps/search/?api=1&query=Rusumo%20Border%20Post) |
| Kazungula 国境（Zambia／Zimbabwe／Botswana） | [Kazungula Border Post](https://www.google.com/maps/search/?api=1&query=Kazungula%20Border%20Post) |
| Victoria Falls Bridge（Zambia↔Zimbabwe） | [Victoria Falls Bridge](https://www.google.com/maps/search/?api=1&query=Victoria%20Falls%20Bridge) |
| Victoria Falls | [Victoria Falls](https://www.google.com/maps/search/?api=1&query=Victoria%20Falls) |
| Songwe 国境（Tanzania↔Malawi。名称は一般知識） | [Songwe Border Post](https://www.google.com/maps/search/?api=1&query=Songwe%20Border%20Post%20Malawi%20Tanzania) |
| Mchinji 国境（Malawi↔Zambia。名称は一般知識） | [Mchinji Border](https://www.google.com/maps/search/?api=1&query=Mchinji%20Border%20Post%20Malawi) |
| Kosi Bay 国境（South Africa↔Mozambique） | [Kosi Bay Border Post](https://www.google.com/maps/search/?api=1&query=Kosi%20Bay%20Border%20Post) |
| Ponta do Ouro | [Ponta do Ouro](https://www.google.com/maps/search/?api=1&query=Ponta%20do%20Ouro%20Mozambique) |
| Gozo Azul（潜水ショップ） | [Gozo Azul Diving](https://www.google.com/maps/search/?api=1&query=Gozo%20Azul%20Diving%20Ponta%20do%20Ouro) |
| Chobe 国立公園 | [Chobe National Park](https://www.google.com/maps/search/?api=1&query=Chobe%20National%20Park) |
| Livingstone | [Livingstone Zambia](https://www.google.com/maps/search/?api=1&query=Livingstone%20Zambia) |
| Maputo | [Maputo](https://www.google.com/maps/search/?api=1&query=Maputo%20Mozambique) |

---

## 10. 未確認・後続タスクと調査ログ

### 10.1 Issue #44 受入条件の達成状況

| 受入条件 | 状態 | 備考 |
|---|---|---|
| A7／B9／C の日別2〜3ルート | **達成**（A7、B9、A7＋Moz。第7章） | すべて候補。B9＋Moz の日別表は作っていない |
| EATV vs 個別を実際の最初の入国国と申請経路で比較。Kenya 入国当局へ確認 | **一部達成** | 比較は第4.1。**Kenya 入国当局への照会は未達**（外部送信は承認なしに行わない） |
| KAZA vs Zimbabwe 単独＋Zambia 免除を往復回数別に比較 | **達成**（第4.2） | |
| Tanzania・Malawi・Mozambique・Botswana・Eswatini・South Africa の要件・費用・申請時間・国境発給を公式確認 | **一部達成** | Tanzania・Malawi・South Africa・Mozambique は公式確認。**Botswana・Eswatini は公式サイト接続不可で未達**。申請所要時間・国境発給の可否は多くが未確認 |
| 航空券（日本発／マニラ発）とバス日程、国境通過可否、チケット窓口の再照合 | **一部達成** | バスの一部は確認（第5章）。**航空券の再照合は未達**。国境通過可否は未確認 |
| Mozambique ダイビング（2／4本、ギア、ボート、海況、生物、日数）＋Maputo／Eswatini 接続の費用 | **一部達成** | 料金・アクセス・日数は第6章。海況・生物・ソロ条件・Maputo／Eswatini 接続の費用は未確認 |
| 7／9／10か国の項目別総予算（二重計上なし） | **一部達成**（式と分類のみ） | 未確認項目が多く、総額は**未算出**（第8章） |
| 大型動物サファリの重複回避 | **達成**（Chobe に集約。第2章・第7章） | |
| 独立レビュー、個人情報の除去、PR提出 | **人手レビュー待ち** | 個人情報は含めていない。main への直接書込みなし |

### 10.2 Issue の数値と公式ページの食い違い

| 項目 | Issue の記載 | 今回の確認 |
|---|---|---|
| Premierline Mwanza→Mbeya | 約19h、特定日の例、87,000 TZS | ページは検索フォームのみで、取得日の便は「No trips found」。**再現できず（未確認）** |
| Malawi の料金 | USD50 と75が併存 | 公式オンライン料金表は Single USD75／Transit USD50。FCDOの到着時は USD50。**併存の理由は「到着時」と「オンライン」の別料金と読める**が、日本旅券への適用は未確認 |
| Mozambique の事前登録 | 大使館は48時間前の事前登録、旧ニュースに停止注記 | 大使館本文に停止注記は**見つからず**。政府ポータルは日本を ETA 表に掲載、FCDOは5営業日前申請。3出典で手続き名・期限が異なる |
| DAN | 最低18時間、日程は24時間以上 | 合意勧告は単回12時間・複数日18時間。24時間は DAN の簡略な提案として同ページに記載。飛行向けの勧告 |
| Gozo Azul | 2本＋ギア＋税＝USD140 | **一致**（100＋30＋10＝140、22,147円）。シリンダー・ウエイトの別料金の扱いは未確認 |
| ANAC | Kosi Bay 8:00〜17:00、673km、4WD | **一致**。4WD推奨は国境付近でなく宿泊地周辺の砂道。Maputo 経由の3〜4時間も記載あり |
| Zimbabwe | 単独 USD30 | **一致**。複数入国 USD55 の表記は Issue に無い |
| KAZA | USD50 | **一致**。窓口料金表は手数料込み USD50.50 |
| Kenya EATV | 大使館 TEMPORARILY UNAVAILABLE／政府 COMING SOON | **一致** |
| Rwanda 単独 USD50 | USD50 | 公式料金ページを取得できず**未確認** |
| 新規（Issue に無い） | — | Uganda の黄熱病証明が2026-10-02付で不要に。Kenya・Tanzania は政府提供の旅行保険が必須（FCDO）。FCDOはKenya・Uganda・Rwanda・Tanzania にエボラ関連の入国時スクリーニングを記載 |

### 10.3 後続タスク

1. Kenya 入国当局へ EATV の Kenya 初入国・eTA 追加の要否を照会（送信は承認後）。
2. Kigali→Rusumo→Mwanza、Dar es Salaam→Mbeya、Mbeya→Malawi→Zambia の運行会社と時刻を特定し、実日付で接続を検証。
3. Botswana・Eswatini・Rwanda の日本旅券要件と料金を公式（大使館 gov 等）で再確認。
4. 航空（MNL→NBO、Kasane／JNB／Maputo→CPT）を日付指定で再取得。
5. Mozambique の ETA 要否・金額・所要を2027年直前にポータルで確認し、潜水の保険・器材（シリンダー込みか）を確認。
6. 外務省の危険情報を、サイトが復旧した時点で全国分を再取得。
7. 保険（旅行・潜水・政府提供保険）と、国別の宿・食の単価を調査し、費用を再算出。

### 10.4 調査ログ（2026-10-18）

- 方法：公式ページを直接取得（各25秒以内のタイムアウト、失敗ページは再試行せず）。WebSearch は使っていない。
- 取得成功：[Kenya eTA 資格画面](https://extern.api.etakenya.go.ke/eligibility)、[Kenya 駐日大使館](https://www.kenyarep-jp.com/en/eta/)（証明書チェーンの検証に失敗するため、本文の読み取りのみ検証なしで取得）、[Uganda EATV](https://immigration.go.ug/services/east-african-tourist-visa)、[Uganda Tourist Visa](https://immigration.go.ug/services/tourist-visa)、[Uganda 免除国](https://immigration.go.ug/services/visa-exempt-countries)、[Rwanda 特別枠査証](https://www.migration.gov.rw/our-services/visa-issued-under-special-arrangement)、[Tanzania eVisa ガイドライン](https://visa.immigration.go.tz/guidelines)、[Malawi 料金](https://www.immigration.gov.mw/visa-fees)、[Malawi 査証種別](https://www.immigration.gov.mw/types-of-malawi-visa)、[Zambia KAZA](https://www.zambiaimmigration.gov.zm/kaza-univisa/)、[Zambia 免除国](https://www.zambiaimmigration.gov.zm/nationals-who-dont-require-visa/)、[Zambia 料金表](https://www.zambiaimmigration.gov.zm/for-residents/pricing-page/)、[Zimbabwe 料金](https://www.zimimmigration.gov.zw/?page_id=6958)、[南アフリカ DHA](https://www.dha.gov.za/index.php/immigration-services/exempt-countries)、[駐日モザンビーク大使館](https://embamoc.jp/visas)、[Mozambique ポータル](https://evisa.gov.mz/Home)、[FCDO Mozambique](https://www.gov.uk/foreign-travel-advice/mozambique/entry-requirements)（および各国のFCDO入国要件とAPIの更新日）、[Gozo-Azul](https://gozo-azul.co.za/scuba-diving/)、[ANAC](https://www.anac.gov.mz/en/parques/ponta-do-ouro/)、[DAN](https://dan.org/health-medicine/health-resource/health-safety-guidelines/guidelines-for-flying-after-diving/)、[Modern Coast 路線一覧](https://moderncoastltd.com/routes)、[Modern Coast Nairobi–Kampala](https://moderncoastltd.com/routes/nairobi-to-kampala)、[Premierline](https://premierline.co.tz/bus-tickets/mwanza-to-mbeya)、[African Bus](https://www.africanbus.com/tickets)。
- 取得失敗：rome2rio（HTTP 403）、gov.bw（証明書エラー）、gov.sz（タイムアウト）、外務省 anzen.mofa.go.jp（保守ページ）、Uganda／Rwanda／Tanzania の旧URL（404。別URLで取得）、Rwanda の査証料金（公式の個別料金ページ未特定。PDFは取得したが本文を読み取れず）。
- 個人情報・アフィリエイト用パラメータ付きURLは含めていない。
