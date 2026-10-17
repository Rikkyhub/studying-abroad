# ケープタウン週末観光（6〜7月・冬）と雨天・強風時の代替

- 確認日：2026-10-17／[Issue #4](https://github.com/Rikkyhub/studying-abroad/issues/4)
- 前提：**匿名モデルケース**（大人1名、平日は語学学校、週末の土日だけ動ける、運転しない場合も想定）。起点は**市中心部（Company's Garden 付近）**。個人の滞在先・学校は起点にしない。
- 料金は**大人1名**、**現地通貨（ZAR）のまま**記載し、円換算はしない（[sources.md](sources.md) のとおり本資料では換算しない。参考レートは [data/fx.csv](../data/fx.csv) にある）。
- 「2027年」と書いていない料金・時間は**取得時点（2026年）の掲示値**。2027年6〜7月の価格・営業を保証しない。

## 0. 表記ルール

| 区分 | 意味 |
|---|---|
| 公式 | 政府機関・施設・事業者の公式サイト／公式CMS |
| 準公式・二次 | 観光局の記事、Wikipedia の気候表（出典は気象機関） |
| 推計（OSRM） | OpenStreetMap の経路計算（車、渋滞・駐車・待ち時間なし）。**公式の所要時間ではない** |
| 未確認 | 取得できなかった、または根拠がない |

料金は3種類を分ける：①**国際（外国人・非居住者）料金**＝本資料の試算に使う値、②**一般料金**（区分のない施設）、③**南ア居住者・SADC・アフリカ国籍・南アの学生向け料金やキャンペーン**＝旅行者には適用しない。参考としてのみ記載し、試算には使わない。

## 1. 要点

| # | 結論 | 根拠・確度 |
|---|---|---|
| 1 | **SANParks（Table Mountain NP）の保全料**は適用期間 **2025-11-01〜2026-10-31** の国際料金で Cape Point **R515**、Boulders **R245**、Newlands・Oudekraal **R200**。カードのみ。**2026-11以降（2027年6〜7月を含む期間）の料金表は未発表** | 公式（Wayback 2026-10-10 取得分。現行ページは 403） |
| 2 | SANParks は、旅券に **Study／Work などの南アのビザ・許可**が貼付された外国人に南ア居住者料金を認める。**ビザ免除（短期滞在）で入国する場合は対象外**で国際料金。本資料は国際料金で試算 | 公式。適用は入国資格次第 |
| 3 | **ケーブルカー**：大人往復 オンライン **R475**／窓口 **R530**（CMS更新 2026-08-17、有効期間の表記なし）。チケットは選択日から**7日間有効**で、オンライン購入分は期間内に返金・日付変更が可能 | 公式 |
| 4 | **年次メンテナンス運休**：2026年は **7/27〜8/9**（公式発表）。**2027年の日程は未発表**。2026年の日付を2027年に当てはめない（例年7月末〜8月上旬との傾向は2025・2026年の2例のみ） | 公式（2026年分） |
| 5 | 冬の雨：平年値（1991–2020、ケープタウン国際空港）で **6月 92.3mm・降雨日10.1日、7月 84.8mm・9.1日**（≥0.1mm）。週末2日のうち1日は雨の前提で雨天案を用意 | 二次（Wikipedia の気候表、出典 SAWS/NOAA）。風の統計は未確認 |
| 6 | 雨天・強風時は V&A／市中心部の屋内施設：Two Oceans Aquarium（大人 **R280**）、Zeitz MOCAA（**R350**、2026-09-01〜）、Iziko South African Museum（国際 **R100**、2026-04-01〜） | 公式 |
| 7 | 2026年6〜7月の観光局イベント記事は**2027年に開催される根拠ではない** | — |

## 2. 候補地（料金区分つき）

距離・時間は市中心部（-33.9268, 18.4174）からの **OSRM推計**（車）。

| 候補地 | ①国際／②一般料金（ZAR） | 適用期間 | ③居住者等（参考・不使用） | 営業／条件 | 推計 | 晴 | 雨 | 強風 | 地図 |
|---|---|---|---|---|---|---|---|---|---|
| Table Mountain Aerial Cableway | ②往復 475（オンライン）／530（窓口）、片道 300／330。学生 320（窓口のみ） | 表記なし（CMS更新 2026-08-17） | SA Senior R130 | 強風・悪天候で運休。2026年は7/27〜8/9運休 | 4.6km／10分（下部駅付近まで） | ◎ | × | × | [Maps](https://www.google.com/maps/search/?api=1&query=Table+Mountain+Aerial+Cableway+Lower+Station) |
| Cape Point | ①515 | 2025-11-01〜2026-10-31 | SA R110、SADC R225 | カードのみ、車1台ごとに支払い | 64km／71分 | ◎ | △ | △ | [Maps](https://www.google.com/maps/search/?api=1&query=Cape+Point+Table+Mountain+National+Park) |
| Boulders（ペンギン） | ①245 | 同上 | SA R55、SADC R110 | カードのみ。営業時間**未確認** | 41km／44分 | ◎ | ○ | △ | [Maps](https://www.google.com/maps/search/?api=1&query=Boulders+Penguin+Colony) |
| Kirstenbosch 植物園 | ①270（アフリカ・SADC以外の大人） | 2026–2027 | SA居住者・SADC R110、アフリカ国籍 R150、南アの学生 R60 | 冬（4〜8月）8:00–18:00、温室 9:00–17:00。Webtickets のみ、現金不可 | 12km／15分 | ◎ | △（温室） | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Kirstenbosch+National+Botanical+Garden) |
| Two Oceans Aquarium | ②大人 280 | 年度表記なし（ショップデータ更新 2026-03-31） | — | 平日 9:30–18:00、週末・祝日・学校休暇 9:00–18:00 | 4.3km／7分（V&A） | ○ | ◎ | ◎ | [Maps](https://www.google.com/maps/search/?api=1&query=Two+Oceans+Aquarium) |
| Zeitz MOCAA | ②350（Webtickets） | 2026-09-01〜 | 南ア・アフリカ国籍は窓口で R199 | 10:00–18:00（最終入場 17:30） | V&A内 | ○ | ◎ | ◎ | [Maps](https://www.google.com/maps/search/?api=1&query=Zeitz+MOCAA) |
| Iziko South African Museum | ①100 | 2026-04-01〜 | Local 大人 R60 | 9:00–17:00（冬の土日 8:30–16:00 の記載あり） | 市中心部 | ○ | ◎ | ◎ | [Maps](https://www.google.com/maps/search/?api=1&query=Iziko+South+African+Museum) |
| Robben Island | ①600（Non South Africans 大人、標準ツアー）。Walking Tour ①1,400（金〜日） | 年度表記なし | South Africans R400／R1,000 | 9:00／11:00／13:00／15:00発、約3.5時間。**欠航時の規定は未確認** | V&A | ◎ | △ | × | [Maps](https://www.google.com/maps/search/?api=1&query=Nelson+Mandela+Gateway+Robben+Island+ferry) |
| Old Biscuit Mill（Neighbourgoods Market） | 0（飲食別） | 現行掲示 | — | マーケット 土 9–15時、日 10–16時 | 4.3km／6分 | ○ | ◎ | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Old+Biscuit+Mill+Woodstock) |
| Chapman's Peak Drive | ②通行料 68（普通車） | 現行掲示 | — | **2026-10-17 取得時点で「CLOSED」表示**。落石・強風で閉鎖あり | Hout Bay 19km／21分 | ◎ | × | × | [Maps](https://www.google.com/maps/search/?api=1&query=Chapman%27s+Peak+Drive) |
| Muizenberg | 0 | — | — | サーフィンレッスン料金**未確認** | 27km／28分 | ○ | × | △ | [Maps](https://www.google.com/maps/search/?api=1&query=Muizenberg+Beach) |
| Hermanus（鯨） | 陸上観察 0。船 ②大人 1,500（rack rate） | 年度表記なし | — | 船は 7:00／9:00／12:00／14:00／16:00発（天候次第）、2時間。鯨は6〜11月に沿岸滞在（事業者説明、遭遇保証なし） | 120km／97分 | ◎ | △ | ×（船） | [Maps](https://www.google.com/maps/search/?api=1&query=Hermanus+New+Harbour) |
| Franschhoek Wine Tram | ②Hop-on Hop-off 350（試飲別） | **2026-11-01 から値上げ予告** | — | 冬季の運行日**未確認** | 76km／57分 | ◎ | ○ | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Franschhoek+Wine+Tram) |
| Stellenbosch | 農園ごと（**未確認**） | — | — | — | 55km／45分 | ◎ | ○ | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Stellenbosch+town+centre) |
| Aquila Private Game Reserve | ②早朝 From 1,995／午後 From 2,365／4x4終日 From 2,895。送迎 From 1,180（日帰り） | 送迎は 2025-11-01〜2026-10-31 | — | 早朝 7:00–11:00、終日 9:00–16:30 | 186km／約2.5時間 | ◎ | △ | ○ | [Maps](https://www.google.com/maps/search/?api=1&query=Aquila+Private+Game+Reserve) |

- **観光局の居住者限定プロモーション**（南アIDを持つ居住者向けの割引料金など）は③に当たり、旅行者向け料金に転記しない。

### 移動手段

| 手段 | 料金（ZAR） | 区分 | 備考 |
|---|---|---|---|
| MyCiTi バス | myconnect カード R40。1日パス 130、3日パス 290、7日パス 420 | 公式 | 現金不可 |
| 配車アプリ・ケープ半島ツアー | **未確認** | — | 運転しない場合の主手段。事業者の公式料金を特定できず |

## 3. 週末の日帰り・1泊2日が成立する条件

- **日帰り（市内・半島）**：①当日朝に**ケーブルカー運行状況・Chapman's Peak の開通状況**を公式で確認、②運転しない場合は配車アプリかツアーを確保（料金は未確認）、③日没が早い冬は明るいうちに戻る、④雨・強風なら屋内案（V&A・市中心部）に差し替え。Cape Point・Boulders は推計片道1時間前後で日帰り可。
- **日帰り（遠方）**：Aquila（推計片道約2.5時間）は**送迎付きツアー**（迎えは早朝）が前提。
- **1泊2日**：Hermanus（推計97分）・ワイン地方（推計45〜57分）は日帰りも可能だが、船の欠航（海況）や試飲後の移動を考えると1泊が安全。条件は①**宿と交通の事前確保**、②船ツアーは**天候次第で中止**になるため予備日（日曜）を残す、③所属先の外泊規則に収まること。
- **ケーブルカー**：2027年の年次運休日程が未発表のため、**6月〜7月中旬の晴天・弱風日に優先**して入れる。チケットは7日間有効・オンライン購入分は日付変更／返金可。

## 4. 冬の天候統計

**ケープタウン国際空港 1991–2020 平年値**（Wikipedia「Cape Town」気候表、出典 SAWS／NOAA）

| 月 | 降水量 mm | 降雨日数（≥0.1mm） | 平均最高 ℃ | 平均最低 ℃ | 日照（月） |
|---|---|---|---|---|---|
| 6月 | 92.3 | 10.1 | 18.2 | 8.1 | 175.9h |
| 7月 | 84.8 | 9.1 | 17.9 | 7.4 | 197.0h |

- 観光局の「冬は11〜20℃、月10〜11日程度の雨」（2026-10-16 取得時の記載）は季節説明であり**2027年の予報ではない**。今回（2026-10-17）は同ページが 403 で再取得できなかった。
- **風の統計は未確認**（SAWS は JavaScript 表示で取得不可）。

## 5. モデルコース（推計を含む。1名、ZAR）

入場料は公式掲示値（①または②）。交通・飲食は**推計**のため合計には含めない。

- **晴天日**：ケーブルカー往復 475（オンライン）＋ Kirstenbosch 270 ＝ **745**（公式値の合計）。
- **雨天日**：Two Oceans Aquarium 280 ＋ Zeitz MOCAA 350 ＋ Iziko SA Museum 100 ＝ **730**。交通は MyCiTi（カード 40＋1日パス 130＝170、公式）。
- **半島（晴天・弱風）**：Cape Point 515 ＋ Boulders 245 ＝ **760**（2025-11〜2026-10 の料金。2027年は改定の可能性）。ツアー・配車料金は未確認。
- **1泊2日 Hermanus**：船 1,500（rack rate、年度表記なし）。交通・宿は未確認。
- **Aquila 日帰り**：4x4終日 From 2,895 ＋ 送迎 From 1,180 ＝ **From 4,075**（送迎料金は2026-10-31まで有効）。

## 6. 未確認事項

| 項目 | 理由 |
|---|---|
| SANParks の 2026-11〜2027-10 料金 | 未発表（現行表は 2026-10-31 まで） |
| 2027年のケーブルカー年次運休・冬の運行時間 | 未発表 |
| ケーブルカー学生料金を語学学校の学生証で使えるか | 公式に条件記載なし（窓口のみ） |
| Boulders の営業時間 | SANParks 現行ページが 403 |
| Robben Island の欠航時規定・料金の有効年度 | サイトに記載なし |
| 配車アプリ・ケープ半島ツアー・料理教室・サーフィンレッスンの料金 | 公式ページを特定できず |
| Wine Tram の2027年料金・冬季運行日 | 2026-11-01 の値上げ後の額が未掲載 |
| 風の統計 | SAWS 取得不可 |
| 2027年冬のイベント | 未発表。2026年記事は根拠にしない |

**問い合わせ文案（送信していない）**
- Table Mountain Aerial Cableway：*Could you tell me the 2027 annual maintenance closure dates and the June–July operating hours? Is the student rate available with a private language school student card?*
- SANParks：*When will the conservation fees for 1 Nov 2026–31 Oct 2027 be published?*
- Robben Island Museum：*What is the refund/reschedule policy when ferries are cancelled due to weather?*

## 7. 調査ログ（2026-10-17）

- **方針**：旧ブランチ（`origin/research/4-sightseeing`、2026-10-16〜17）の記述を出発点に、主要な料金・時間を公式サイトで再取得。個人の在籍予定・学校・起点・費用合計を削除し、起点を市中心部に変更。費用は入場料の公式値の合計だけを示し、推計の交通・飲食は合計に入れない形に改めた。
- **検索**：旧調査では Brave・DuckDuckGo・Bing・Mojeek・Yahoo が captcha／429／無関係な結果で使えず。今回は検索エンジンを使わず公式ドメインに直接アクセス。
- **取得成功（今回）**：`https://cms.tablemountain.net/api`（GraphQL：ticketTypes、maintenance／refund 検索）、`https://www.tablemountain.net/our-blog/table-mountain-aerial-cableway-announces-2026-annual-maintenance-shutdown-dates`（WebFetch）、`https://www.tablemountain.net/our-blog/how-does-table-mountain-cableways-ticketing-work`（WebFetch）、`http://web.archive.org/web/20261010190236/https://www.sanparks.org/parks/table-mountain/rates-entry-fees`、`https://www.sanbi.org/gardens/kirstenboch/visitor-information/information/`、`https://zeitzmocaa.museum/plan-your-visit/`、`https://www.iziko.org.za/visit/`、`https://www.robben-island.org.za/`、`https://www.aquarium.co.za/visit-us/plan-your-trip`、`https://shop.aquarium.co.za/`（埋め込みデータ）、`https://theoldbiscuitmill.co.za/visitor-info/`、`https://www.myciti.org.za/en/myconnect-fares/multi-day-packages/`、`https://www.myciti.org.za/en/myconnect-fares/get-your-myconnect-card/`、`https://winetram.co.za/`、`https://www.chapmanspeakdrive.co.za/tariff/standard.html`、`https://aquilasafari.com/day-trip-safaris/`、`https://aquilasafari.com/transport/`、`https://www.hermanus-whale-cruises.co.za/trip.php`、`https://www.hermanus-whale-cruises.co.za/whales.php`、`https://en.wikipedia.org/w/index.php?title=Cape_Town&action=raw`、`https://router.project-osrm.org/table/v1/driving/...`。
- **失敗**：`https://www.sanparks.org/parks/table-mountain/rates-entry-fees`（403）、`http://web.archive.org/cdx/search/cdx?...`（Temporarily Offline。availability API で代替）、`https://www.capetown.travel/the-best-time-of-year-to-visit-cape-town/`・`/100-things-to-do-in-winter-in-cape-town/`（403）、CMS の `ticketTypesEntries` 直接クエリ（エラー。`entries(section:)` で代替）。旧調査での失敗：waterfront.co.za（429）、weathersa.co.za（JavaScript 表示）、robben-island.org.za/tickets（404）。
