# バギオ週末観光（2〜4月）と季節・雨天代替

- 確認日：2026-10-17／[Issue #4](https://github.com/Rikkyhub/studying-abroad/issues/4)
- 前提：**匿名モデルケース**（大人1名、平日は語学学校、週末の土日だけ動ける）。起点はバギオ市中心部の **Burnham Park**（公開の観光地。個人の滞在先・学校は起点にしない）。
- 料金は**大人1名・入場料のみ**（交通・飲食は別）。**現地通貨（PHP）のまま**記載し、円換算はしない（[sources.md](sources.md) のとおり本資料では換算しない。参考レートは 各地域ページの「通貨と円換算」（[バギオ](../areas/baguio.md)・[アフリカ周遊](../areas/africa.md)・[ケープタウン](../areas/capetown.md)） にある）。
- 「2027年」と書いていない料金・時間は、すべて**取得時点（2026年）の掲示値**。2027年の価格・営業時間を保証しない。

## 0. 表記ルール

| 区分 | 意味 |
|---|---|
| 公式 | 市・州・政府機関・事業者の公式サイト／公式APIで確認 |
| 口コミ | Wikivoyage など共同編集・ブログ。公式ではない |
| 推計（OSRM） | OpenStreetMap の経路計算（車、渋滞・休憩・乗り継ぎなし）。**公式の所要時間ではない** |
| 未確認 | 取得できなかった、または根拠がない |

料金は次の3つを混ぜない：①**一般（旅行者）料金**、②**外国人料金**（区分がある場合）、③**現地居住者向け料金・キャンペーン**（旅行者には適用しない。参考としてのみ記載）。

## 1. 要点

| # | 結論 | 根拠・確度 |
|---|---|---|
| 1 | 市内の主要施設の料金はバギオ市公式の予約サイト **Baguio VISITA** のAPIで確認できた（2026-10-17 取得）。Botanical Garden **110**、Mines View **20**、Tam-awan **60**、BenCab **200**、Igorot Stone Kingdom **100**、Sky Ranch **50**、Mirador **100**、他は **0**（PHP） | 公式。ただし**外国人／居住者の区分、学生割引の有無は表示なし** |
| 2 | Botanical Garden の**住民無料措置**（BLISTT圏の住民対象、Ordinance No. 62 s.2025、6か月間）は **2026年1月末で終了**。そもそも旅行者には適用されない | 報道（Daily Tribune 2026-02-18）。金額の記載なし |
| 3 | 2〜4月は乾季。PAGASA 平年値（1991–2020）で降雨日数（1mm以上）は **2月3日・3月5日・4月8日**、5月は18日。雷雨日数は2月1日・3月3日・4月9日 | 公式（PAGASA） |
| 4 | **2027年の聖週間**は 3/21（枝の主日）〜3/28（復活祭）。聖木曜 3/25・聖金曜 3/26。バス・宿が混む。**2027年の祝日指定は大統領布告が未発表** | 日付は計算値。祝日は未確認 |
| 5 | **Panagbenga（花祭り）2027 の日程は未発表**。公式サイト panagbenga.com は「Launching Soon」表示のまま。2026年の日程を2027年に当てはめない | 公式サイトで未発表を確認 |
| 6 | 日帰りの現実的な範囲は**片道2時間以内（推計）**の市内・La Trinidad・Tuba・Mt. Ulap。Sagada・La Union は**1泊2日**、Banaue/Batad は**夜行利用で金曜夜発**が前提、Vigan は週末では非推奨 | 時間はOSRM推計。バス時刻の公式確認は Banaue（Ohayami 21:00）のみ |

## 2. 市内（Baguio VISITA 公式データ）

出典：[Baguio VISITA Park Tickets](https://visita.baguio.gov.ph/park-tickets) が使う公開API `https://api-booking.baguio.visita.ph/api/parks`（2026-10-17 取得、16件）。料金は大人1名の登録値。**外国人料金・居住者料金の区分は無い**ため①一般料金として扱う。営業時間はAPIの `openingHours` 原文（午前/午後の表記がなく曖昧なものは「表記が曖昧」と注記）。

距離・時間は Burnham Park（16.4121, 120.5933）からの**OSRM推計**（車）。

| 施設 | 料金 PHP（2026登録値） | 営業時間（VISITA原文） | Burnham Parkから（推計） | 雨天 | 地図 |
|---|---|---|---|---|---|
| Burnham Park | 0（ボートは別料金・未確認） | 表記なし | 起点 | △ | [Maps](https://www.google.com/maps/search/?api=1&query=Burnham+Park+Baguio) |
| Baguio Cathedral | 0 | 「6:00-7:00」（曖昧） | 1.2km／5分 | ○（屋内） | [Maps](https://www.google.com/maps/search/?api=1&query=Baguio+Cathedral) |
| Sky Ranch | 50（乗り物別・未確認） | 「10:00-10:00」（曖昧） | 1.3km／5分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Sky+Ranch+Baguio) |
| Ili-Likha Artists Village | 0 | 「10:00-9:00」（曖昧） | 1.3km／5分 | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Ili-Likha+Artists+Village+Baguio) |
| Baguio Botanical Garden | 110 | 6:00am–6:00pm | 3.1km／9分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Baguio+Botanical+Garden) |
| The Mansion | 0 | 「9:00-3:00」 | 4.2km／12分 | △（外観のみ） | [Maps](https://www.google.com/maps/search/?api=1&query=The+Mansion+Baguio) |
| Wright Park | 0（乗馬は別料金・未確認） | 「1:30-6:00」（曖昧） | 4.3km／12分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Wright+Park+Baguio) |
| Camp John Hay | 0（個別施設は別料金） | 「8:00-7:00」 | 4.6km／12分 | △ | [Maps](https://www.google.com/maps/search/?api=1&query=Camp+John+Hay+Baguio) |
| Mines View Park | 20 | 「6:00-8:00」（曖昧） | 5.2km／15分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Mines+View+Park+Baguio) |
| Bell Church（La Trinidad） | 0 | 「6:00-5:00」 | 2.9km／8分 | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Bell+Church+La+Trinidad) |
| Tam-awan Village | 60 | 「7:00-8:00」（曖昧） | 3.9km／10分 | △（ギャラリー） | [Maps](https://www.google.com/maps/search/?api=1&query=Tam-awan+Village+Baguio) |
| Igorot Stone Kingdom | 100 | 「7:00-6:00」 | 4.4km／12分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Igorot+Stone+Kingdom+Baguio) |
| BenCab Museum（Tuba） | 200 | 「9:00-6:00」 | 6.4km／16分 | ◎（屋内） | [Maps](https://www.google.com/maps/search/?api=1&query=BenCab+Museum) |
| Strawberry Farm（La Trinidad） | 0（イチゴ狩りは別料金・未確認） | 「8:00-6:00」 | 7.3km／16分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Strawberry+Farm+La+Trinidad+Benguet) |
| Lion's Head（Kennon Rd） | 0 | 「6:00-6:00」 | 8.1km／21分 | × | [Maps](https://www.google.com/maps/search/?api=1&query=Lion%27s+Head+Kennon+Road+Baguio) |
| Mirador Heritage & Eco-Spirituality Park | 100 | 「6:00-6:00」 | 未計算（APIに座標なし） | × | [Maps](https://www.google.com/maps/search/?api=1&query=Mirador+Heritage+Eco-Spirituality+Park+Baguio) |

- **Botanical Garden**：市の告知「入場料引き上げ」ページ（main.baguio.gov.ph）は JavaScript 表示で本文を取得できず、値上げ額・適用日は**未確認**。VISITA の 110 を採用。
- **現地居住者向けキャンペーン（③、旅行者には適用しない）**：Botanical Garden の BLISTT 住民向け無料措置（2026年1月末終了）。
- タクシー料金：**公式（LTFRB）の運賃表は未確認**。口コミ（Wikivoyage、年度不明）では初乗り PHP35＋100mごとに PHP1.50。

## 3. 日帰り・1泊2日

距離・時間は Burnham Park からの **OSRM推計**（車、渋滞・休憩なし）。山岳道路のバスは推計より大幅に長い。

| 目的地 | 車の推計 | 公共交通（出典区分） | 主な費用（PHP・出典区分・年度） | 予約・手続 | 判定 | 地図 |
|---|---|---|---|---|---|---|
| Mt. Ulap（Itogon） | 22km／約45分 | ジープニー・タクシー（運賃**未確認**） | 登録料・ガイド料**未確認** | ガイド要否も**未確認** | 日帰り可（料金要確認） | [Maps](https://www.google.com/maps/search/?api=1&query=Mt+Ulap+Ampucao+Itogon) |
| Kabayan | 84km／約1.8時間 | バス・バン・ジープニー（口コミ） | 一部施設は寄付制（口コミ） | 未確認 | 日帰りは長い。1泊推奨 | [Maps](https://www.google.com/maps/search/?api=1&query=Kabayan+Benguet) |
| La Union（San Juan） | 85km／約2時間 | バス・バン（運賃・時刻**未確認**） | サーフレッスン料金**未確認**（口コミの値は2010年で古く不採用） | 不要 | 日帰りまたは1泊2日 | [Maps](https://www.google.com/maps/search/?api=1&query=Urbiztondo+Beach+San+Juan+La+Union) |
| Sagada | 140km／約2.9時間 | GL Trans／Lizardo Trans、6:00〜13:00に複数便、約6時間、**PHP220**、**聖金曜は1便のみ**（口コミ：Wikivoyage） | 登録・環境料 **100**（口コミ、2025年6月時点）、洞窟の連結ツアー 1名 **800**（口コミ、年度不明） | 到着後に町の観光案内所で登録。洞窟はガイド同行 | **1泊2日なら可** | [Maps](https://www.google.com/maps/search/?api=1&query=Sagada+Municipal+Tourism+Office) |
| Mt. Pulag | Kabayan方面 | チャーター、またはツアー | **2026/2027年の入山料は公式で未確認** | DENR の許可・オリエンテーション・診断書が必要とする情報（口コミ、2015年） | ツアー利用の1泊2日。要確認事項が多い | [Maps](https://www.google.com/maps/search/?api=1&query=Mt+Pulag+DENR+Visitor+Center+Ambangeg) |
| Banaue／Batad | 187km／約3.7時間 | **Ohayami Bus がバギオ（Governor Pack Rd）21:00発**（公式：Ifugao州） | 料金**未確認**（公式に記載なし） | Batad は徒歩 | **金曜夜発の夜行＋1泊**なら可 | [Maps](https://www.google.com/maps/search/?api=1&query=Batad+Rice+Terraces) |
| Vigan | 230km／約4時間 | バス会社・運賃**未確認** | 未確認 | 不要 | 週末では非推奨 | [Maps](https://www.google.com/maps/search/?api=1&query=Calle+Crisologo+Vigan) |

- Victory Liner（公式）：オンライン予約は First Class・Royal Class のみ。**2026-10-17〜10-19 はQRコード式発券への移行でオンライン・事前予約を停止**（当日窓口販売は継続）との告知。2027年の予約方法は再確認する。

### 週末の日帰り・1泊2日が成立する条件

- **日帰り**：①片道が推計2時間以内、②帰りの便・配車が日没前後に確保できる、③所属先（学校・寮）の門限・外出規則に収まる、④晴天（山・展望地）または屋内中心の雨天案がある。→ 市内・La Trinidad・Tuba・Mt. Ulap が該当。La Union は帰りの便が確認できるまで「条件付き」。
- **1泊2日**：①所属先の**外泊許可**が得られる、②土曜朝に出発し日曜午後に帰着できる便がある（Sagada は口コミ上 6:00〜13:00発・約6時間）、③**聖週間（2027-03-21〜28）とPanagbenga の大型週末を避ける**か事前予約する、④天候による道路状況（4月以降は雷雨が増える）を前日に確認する。
- **夜行併用**：Banaue/Batad は金曜21:00発（公式）で土曜朝着、日曜に戻る行程。金曜夜に出られることが前提。

## 4. 季節（2〜4月）

**PAGASA 気候平年値（1991–2020、Baguio City 観測所、標高1,510m）**（公式PDF）

| 月 | 降水量 mm | 降雨日数（≥1mm） | 雷雨日数 | 最高 ℃ | 最低 ℃ |
|---|---|---|---|---|---|
| 2月 | 23.7 | 3 | 1 | 23.7 | 13.4 |
| 3月 | 50.5 | 5 | 3 | 24.8 | 14.5 |
| 4月 | 99.5 | 8 | 9 | 25.5 | 15.9 |
| （参考）5月 | 340.0 | 18 | 18 | 24.7 | 16.4 |

- 平年値であり**2027年の予報ではない**。4月は雷雨日が増えるため、山歩きは午前中に終える計画にする。

**イベント（開催年を混同しない）**

| 期間 | 内容 | 2027年の扱い |
|---|---|---|
| 例年2月〜3月上旬 | Panagbenga（花祭り）。2026年の開催実績は報道あり | **未発表。2027年の開催日は確定していない** |
| 2027-03-21〜28 | 聖週間（計算値） | 日付は確実。祝日指定は未発表 |

**雨天代替**：BenCab Museum（200、屋内）、Tam-awan のギャラリー（60）、Ili-Likha（0）、Baguio Cathedral（0）、市場での食べ歩き（費用は推計）。

## 5. モデルコース（推計を含む。1名、PHP）

入場料は VISITA の2026年登録値。交通・飲食は**推計**（根拠となる公式運賃なし）。

- **日帰りA「アートと先住民文化」（雨でも成立）**：Burnham Park → BenCab → Tam-awan → Igorot Stone Kingdom → 市場で夕食。入場料 200＋60＋100＝**360**（公式値の合計）。交通・飲食は推計で 1,000〜2,500。
- **日帰りB「山と農園」（晴天日）**：早朝 Mt. Ulap → 午後 La Trinidad（Strawberry Farm 0、Bell Church 0）。Ulap の登録・ガイド料が**未確認**のため合計は算出しない。
- **1泊2日「Sagada」**：バス 220×2＝440＋登録料 100＋洞窟ツアー 800＝**1,340**（いずれも口コミ値の合計）。宿・飲食は**未確認**（公式価格なし）。

## 6. 未確認事項

| 項目 | 理由 |
|---|---|
| VISITA料金が外国人にも同額か・学生割引 | APIに区分がない |
| Botanical Garden の値上げ額・適用日 | 市の告知が JavaScript 表示で取得できず、報道にも金額なし |
| Mt. Pulag・Mt. Ulap の入山料・ガイド料・予約方法（2027年） | DENR関係サイトが 403／名前解決不可。公式ページ未発見 |
| Sagada の公式料金 | 町の公式サイトが再構築中。口コミ値で代用 |
| La Union・Vigan 行きのバス会社・運賃・時刻、Ohayami の運賃 | 公式時刻・運賃表を取得できず |
| Panagbenga 2027、2027年の祝日 | 未発表 |
| タクシー公式運賃（LTFRB） | 未取得 |
| 所属先の外泊・門限規則 | 個別に確認する事項（本資料には記載しない） |

**問い合わせ文案（送信していない）**
- DENR-CAR（Mt. Pulag）：*Could you tell me the current fees for foreign visitors, the reservation procedure and lead time, orientation schedule, and medical certificate requirements for a weekend hike in Feb–Apr 2027?*
- Sagada Municipal Tourism Office：*What are the 2027 registration/environmental fee and cave guide rates for foreign visitors, and are there special arrangements during Holy Week?*

## 7. 調査ログ（2026-10-17）

- **方針**：2026-10-16〜17 の旧ブランチ（`origin/research/4-sightseeing`）の記述を出発点に、主要な料金・時間を公式サイトで再取得。個人の滞在先・学校・費用合計は削除し、起点を公開の観光地に変更。
- **検索クエリ（旧調査、2026-10-16〜17）**：「visita baguio park tickets entrance fee botanical garden」（Brave、成功）、「Baguio Botanical Garden entrance fee P100 tourists 2026 ordinance」（captcha）、「Mt Pulag entrance fee DENR 2026」系6種（Brave・DDG・Bing・Mojeek・Yahoo、すべて失敗）、「Panagbenga 2026 schedule grand street dance float parade」（captcha）。今回（2026-10-17）は検索エンジンを使わず公式ドメインに直接アクセス。
- **取得成功（今回）**：`https://api-booking.baguio.visita.ph/api/parks`（curl、16件）、`https://pubfiles.pagasa.dost.gov.ph/pagasaweb/files/cad/CLIMATOLOGICAL%20NORMALS%20(1991-2020)/BAGUIO.pdf`（WebFetch で保存したPDFを読取）、`https://ifugao.gov.ph/getting-here/`、`https://mountainprovince.gov.ph/the-province/getting-here/`（バギオ発の具体情報なし）、`https://www.victoryliner.com/`、`https://panagbenga.com/`（Launching Soon）、`https://tribune.net.ph/2026/02/18/residents-now-must-pay-for-baguio-botanical-garden`（WebFetch）、`https://en.wikivoyage.org/w/index.php?title=Sagada&action=raw`、`https://router.project-osrm.org/table/v1/driving/...`（距離・時間）。
- **失敗**：PAGASA PDF の WebFetch 本文抽出（バイナリのため。保存PDFの読取で代替）。旧調査での失敗：newsinfo.inquirer.net・mb.com.ph・pia.gov.ph・bmb.gov.ph・car.denr.gov.ph/mt-pulag（403）、mtpulag.denr.gov.ph（DNS）、banaue.gov.ph・benguet.gov.ph（接続不可）、main.baguio.gov.ph（JavaScript で本文なし）、sagada.gov.ph（再構築中）。
- **計算**：復活祭の日付（2027-03-28）は計算アルゴリズムによる。
