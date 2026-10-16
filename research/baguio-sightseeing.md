# バギオ週末観光（2〜4月）と季節・雨天代替

- 確認日: 2026-10-17
- Issue: [#4 バギオ・ケープタウン週末観光と季節/雨天代替案](https://github.com/Rikkyhub/studying-abroad/issues/4)
- 前提: 日本国籍の社会人1名。2027-02-06（土）〜05-01（土）に PINES International Academy（スピーキングキャンパス、3 Ignacio Villamor St., Brgy. Lualhati, Baguio City。既存資料 `research/philippines-pines.md` の記載）に在籍。週末だけ動ける。
- 優先: 珍しい郷土料理、自然・山、写真、動物、体験。
- 通貨: PHP（参考: 1 PHP ≒ 2.51 円。open.er-api.com、2026-10-16 更新値）。
- 数字には特記のない限り「大人1名」「入場料のみ（交通・飲食は別）」を前提とする。
- 既存資料 `research/baguio-sightseeing.md`（2026-10-16 版）を再検証した。The Mansion の入場無料・9:00–15:00 は VISITA API でも同じ値だった（下表）。料金未確定だった他の施設は今回埋めた。

---

## 1. 要点（結論と確度）

| # | 結論 | 確度 |
|---|---|---|
| 1 | 市内の主要施設の料金と営業時間は、市の公式予約サイト Baguio VISITA のデータ（API `api-booking.baguio.visita.ph/api/parks`）で確認できた。Botanical Garden **110**、Mines View **20**、Tam-awan **60**、BenCab **200**、Igorot Stone Kingdom **100**、Sky Ranch **50**、Mirador **100**。Burnham Park、Wright Park、The Mansion、Camp John Hay、Strawberry Farm、Bell Church、Lion's Head は **0（無料）**（PHP、2026年の登録値） | 高（公式）。ただし「観光客料金か」「学生割引の有無」は表示がなく未確認 |
| 2 | PINES は Wright Park・The Mansion・Botanical Garden まで約 0.6〜1.1km、Mines View まで約 2km。徒歩圏で、半日あれば回れる | 中（OSRM の道路距離。所要時間は渋滞なしの計算値） |
| 3 | 2〜4月は乾季。PAGASA の平年値（1991–2020）では降雨日数が **2月3日・3月5日・4月8日**。5月（18日）から雨季に入る。**週末観光に最も向いた時期**で、雨天代替が必要になる日は少ない | 高（公式） |
| 4 | **2027年の聖週間**: 枝の主日 3/21、聖木曜 3/25、聖金曜 3/26、聖土曜 3/27、復活祭 3/28（計算値）。この前後はバスや宿が混み、Sagada 行きは聖金曜に減便するという記述もある（Wikivoyage） | 日付は高（計算）、休日の扱いは未確認（2027年の大統領布告が未発表） |
| 5 | Panagbenga は例年2月の1か月間で、3月上旬の最初の日曜ごろが最終日（Wikipedia の一般的な説明）。2026年はスポンサー関連のイベントが 2/28〜3/8 に開かれた（SunStar の記事）。**2027年の日程は未発表で、確定していない** | 中 |
| 6 | 1泊2日なら **Sagada**（片道約6時間、バス PHP220。環境・登録料 PHP100。洞窟はガイド必須）が、希望（山・洞窟・郷土料理・写真）に最も合う。Banaue/Batad や Vigan は片道4時間以上かかり、1泊2日では移動が多い。週末に行くなら金曜夜発が前提 | 中（料金は Wikivoyage の2025〜26年の記載。公式では未確認） |
| 7 | **Mt. Pulag** は DENR の許可、必須オリエンテーション、診断書（2015年以降）が必要。**2026年の入山料は公式資料で確認できなかった**。個人手配は難しく、ツアーの利用を推奨 | 低（料金は未確認） |
| 8 | **PINES の外泊・門限ルールは未確認**。1泊2日の計画は、学校の外泊許可を前提に組んでいる | — |

---

## 2. 詳細表

### 2-1. 市内（Baguio VISITA 公式データ）

出典: [Baguio VISITA Park Tickets](https://visita.baguio.gov.ph/park-tickets) が使う公開 API `https://api-booking.baguio.visita.ph/api/parks`（確認日 2026-10-17。各レコードの更新日は 2026-07〜10）。料金は大人1名あたりの PHP の登録値。距離と時間は PINES（16.4136, 120.6177）からの道路距離を OSRM で計算したもの（車で渋滞なし）。

| 施設 | 料金 PHP | 営業時間（VISITA 表記） | PINES から | 推奨手段 | 希望との相性 | 地図 |
|---|---|---|---|---|---|---|
| The Mansion | 0 | 9:00–15:00 | 0.6km／2分 | 徒歩約10分 | 写真（正門） | [検索リンク](https://www.google.com/maps/search/?api=1&query=The+Mansion+Baguio) |
| Wright Park | 0（乗馬は別料金、未確認） | 「1:30-6:00」（表記が曖昧） | 0.7km／2分 | 徒歩約10分 | 動物（乗馬）、松並木の写真 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Wright+Park+Baguio) |
| Baguio Botanical Garden | 110 | 6:00–18:00 | 1.1km／3分 | 徒歩約15分 | 自然、イゴロット様式の小屋 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Baguio+Botanical+Garden) |
| Mines View Park | 20 | 「6:00-8:00」（表記が曖昧） | 2.0km／6分 | タクシーまたは徒歩約30分 | 眺望、日の出 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Mines+View+Park+Baguio) |
| Camp John Hay | 0（個別施設は別料金） | 8:00–19:00 | 2.8km／8分 | タクシー | 松林の散策 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Camp+John+Hay+Baguio) |
| Baguio Cathedral | 0 | 6:00–19:00 | 3.0km／8分 | タクシー、または Session Road から徒歩 | 写真 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Baguio+Cathedral) |
| Sky Ranch | 50（乗り物は別料金、未確認） | 10:00–22:00 | 3.1km／8分 | タクシー | — | [検索リンク](https://www.google.com/maps/search/?api=1&query=Sky+Ranch+Baguio) |
| Ili-Likha Artists Village | 0 | 10:00–21:00 | 3.1km／9分 | タクシー | アート、軽食 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Ili-Likha+Artists+Village+Baguio) |
| Burnham Park | 0（ボートは別料金、未確認） | 表記なし | 3.6km／11分（直線約2.6km） | 徒歩約35〜50分（推定）またはタクシー | 湖、ボート | [検索リンク](https://www.google.com/maps/search/?api=1&query=Burnham+Park+Baguio) |
| Session Road／Baguio Public Market | 0 | 未確認 | 約3〜4km（推定） | タクシー | **郷土料理・市場**（Good Shepherd のウベジャムなどは Wikivoyage の情報） | [検索リンク](https://www.google.com/maps/search/?api=1&query=Baguio+City+Public+Market) |
| Tam-awan Village | 60 | 「7:00-8:00」（表記が曖昧） | 7.0km／19分 | タクシー | **コルディリェラの伝統家屋、工芸体験** | [検索リンク](https://www.google.com/maps/search/?api=1&query=Tam-awan+Village+Baguio) |
| Igorot Stone Kingdom | 100 | 7:00–18:00 | 7.5km／21分 | タクシー（Tam-awan の近く） | 写真 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Igorot+Stone+Kingdom+Baguio) |
| Strawberry Farm（La Trinidad） | 0（イチゴ狩りは別料金、未確認） | 8:00–18:00 | 9.5km／22分 | タクシーまたはジープニー | 体験、ご当地スイーツ | [検索リンク](https://www.google.com/maps/search/?api=1&query=Strawberry+Farm+La+Trinidad+Benguet) |
| BenCab Museum（Tuba） | 200 | 9:00–18:00 | 9.7km／26分 | タクシー | **雨天代替（屋内）**、アート | [検索リンク](https://www.google.com/maps/search/?api=1&query=BenCab+Museum) |
| Bell Church（La Trinidad） | 0 | 6:00–17:00 | 5.0km／14分 | タクシー | 写真 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Bell+Church+La+Trinidad) |
| Lion's Head（Kennon Rd） | 0 | 6:00–18:00 | 10.7km／27分 | タクシー | 写真 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Lion%27s+Head+Kennon+Road+Baguio) |
| Mirador Heritage & Eco-Spirituality Park | 100 | 6:00–18:00 | 未計算 | タクシー | 眺望 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Mirador+Heritage+Eco-Spirituality+Park+Baguio) |

- **Botanical Garden の料金**: 市の発表に「入場料引き上げ」の告知がある（main.baguio.gov.ph。JavaScript で表示するページのため本文は取得できず）。Daily Tribune（2026-02-18、報道）によると、BLISTT 圏の住民向け6か月間の無料措置（Ordinance No. 62 s.2025）が2026年1月末で終了した。報道には金額の記載がない。現時点では VISITA の登録値 110 を採用する。
- **タクシー料金の目安**: 初乗り PHP35（500m まで）＋100m ごとに PHP1.50。Wikivoyage の記載（口コミ／準公式、年度不明）で、LTFRB の公式資料では未確認。例として PINES→BenCab（9.7km）は 35＋(9.2km÷0.1km)×1.5 ≒ **PHP173**、PINES→Burnham（3.6km）は ≒ **PHP82**（計算値で、渋滞時の待ち時間料金は含まない）。1日チャーター（8〜9時間）は **PHP1,800–2,000**（Wikivoyage）。

### 2-2. 日帰り・1泊2日

距離と時間は PINES からの OSRM 計算値（車、渋滞なし、休憩なし）。実際のバスはさらに時間がかかる。

| 目的地 | 距離／車の目安 | 公共交通（出典） | 主な費用（PHP） | ガイド・予約 | 判定 | 地図 |
|---|---|---|---|---|---|---|
| **Mt. Ulap**（Ampucao, Itogon） | 18km／約35分 | ジープニーまたはタクシー（料金は未確認） | 登録料・ガイド料は**未確認** | 現地でガイド必須とする情報が多いが、公式では未確認 | 日帰りで可。料金は要確認 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Mt+Ulap+Ampucao+Itogon) |
| **Sagada**（Mountain Province） | 138km／約2.9時間（バスは約6時間） | GL Trans／Lizardo Trans が 6:00〜13:00 に複数便、**PHP220**、約6時間。聖金曜は1便のみ（Wikivoyage、2026-05 編集） | 登録・環境料 **100**（2025年6月時点）。Sumaging と Lumiang をつなぐ洞窟ツアー（2〜3時間）は1名 **800**、1名追加ごとに +400。Echo Valley のロッククライミングは 200（いずれも Wikivoyage） | 洞窟はガイド必須。到着後、町の観光案内所で登録と短いオリエンテーションを受ける | **1泊2日なら可**。土曜早朝に出て日曜午後に戻る。往復12時間 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Sagada+Municipal+Tourism+Office) |
| **Mt. Pulag**（Kabayan, Ambangeg 登山道） | Kabayan まで 78km／約1.7時間。Ranger Station までは3〜4時間（PinoyMountaineer） | チャーターのジープ、またはバスとバイクタクシー | 2015年の参考値: 登録料 225、ガイド料 500（1〜5名）。**2026年の料金は未確認** | DENR の Visitor Center での**必須オリエンテーション**と**診断書**が必要（2015年以降。PinoyMountaineer 2015-12-03 更新）。予約制 | 1泊2日（ツアー推奨）。料金と予約方法は要確認 | [検索リンク](https://www.google.com/maps/search/?api=1&query=Mt+Pulag+DENR+Visitor+Center+Ambangeg) |
| **Kabayan**（ミイラの洞窟） | 78km／約1.7時間 | バス・バン・ジープニーあり（Wikivoyage） | 一部の施設は無料・寄付制（Wikivoyage、2026-08 編集） | 未確認 | 日帰りは可能だが長い。Pulag と組み合わせると良い | [検索リンク](https://www.google.com/maps/search/?api=1&query=Kabayan+Benguet) |
| **Banaue／Batad** の棚田 | Banaue まで 186km／約3.7時間 | Ohayami Bus がバギオ（Governor Pack Rd）を **21:00発**（Ifugao 州政府の公式ページ） | Batad の環境・遺産料 **50**、Banaue→Batad のジープニー 200（2024年5月）。いずれも Wikivoyage | Batad は徒歩のみ。ガイドは任意（約400） | 夜行0泊＋1泊、または2泊なら可。**金曜夜発の0泊2日案** | [検索リンク](https://www.google.com/maps/search/?api=1&query=Batad+Rice+Terraces) |
| **Vigan**（世界遺産の街並み） | 227km／約4時間 | バス会社と運賃は**未確認**（Wikivoyage はマニラ発の情報のみ） | 未確認 | 不要 | 1泊2日。移動の負担が大きい | [検索リンク](https://www.google.com/maps/search/?api=1&query=Calle+Crisologo+Vigan) |
| **La Union（San Juan）** のサーフィン | 86km／約2時間 | バス・バンの運賃は**未確認** | サーフレッスン PHP200／時（**2010年の古い値**。現行料金は未確認） | 不要 | 日帰り、または1泊2日で可。シーズンは11〜4月（Wikivoyage） | [検索リンク](https://www.google.com/maps/search/?api=1&query=Urbiztondo+Beach+San+Juan+La+Union) |

### 2-3. 季節（2〜4月）

**PAGASA 気候平年値（1991–2020、Baguio City 観測所、標高 1,510m）**

| 月 | 降水量 mm | 降雨日数 | 最高気温 ℃ | 最低気温 ℃（Wikipedia 経由、PAGASA） |
|---|---|---|---|---|
| 2月 | 23.7 | 3 | 23.7 | 13.4 |
| 3月 | 50.5 | 5 | 24.8 | 14.5 |
| 4月 | 99.5 | 8 | 25.5 | 15.9 |
| （参考）5月 | 340.0 | 18 | 24.7 | — |

- 4月後半からは雷雨が出始める。朝晩は約13〜16℃と冷えるため、上着が必要。

**イベントと混雑**

| 期間 | 内容 | 2027年の確度 |
|---|---|---|
| 2月の1か月間 | Panagbenga（花祭り）。例年2/1〜3月最初の日曜ごろ（Wikipedia）。2026年はスポンサー関連のイベントが 2/28〜3/8（SunStar の記事）。大きなパレードは最終週末あたり | **未確定**。市・財団の正式発表を待つ |
| 2027-03-21〜03-28 | 聖週間（枝の主日〜復活祭）。3/25 聖木曜、3/26 聖金曜は例年祝日 | 日付は計算値で確実。祝日指定は未発表 |

- 混雑対策: パレードの週末と聖週間は、Session Road や Burnham 周辺、バスの予約が非常に混む。Victory Liner は Royal Class と First Class だけがオンライン予約でき、他の等級は当日にターミナルで購入する（同社サイトの告知、2026-10）。
- 雨天時の代替: BenCab Museum（屋内）、Tam-awan のギャラリー、Ili-Likha、Public Market での食べ歩き、Good Shepherd Convent での買い物。

---

## 3. 実行可否の判定

| 候補 | 判定 | 理由 |
|---|---|---|
| 市内（徒歩とタクシー） | **可** | 公式料金を確認済み。近距離 |
| Mt. Ulap 日帰り | **条件付きで可** | 距離は近い。登録料・ガイド・受付時間が未確認 |
| La Trinidad（イチゴ・Bell Church） | **可** | 公式データで無料を確認。体験料金のみ未確認 |
| Sagada 1泊2日 | **条件付きで可** | バス片道6時間。学校の外泊許可が必要。聖週間は避ける |
| Mt. Pulag | **条件付き（ツアー推奨）** | 診断書とオリエンテーションが必須。2026年の料金は未確認 |
| Banaue／Batad | **条件付きで可** | 夜行バスの0泊2日、または2泊が必要 |
| Vigan | **可能だが非推奨** | 片道4時間以上で、交通情報も未確認 |
| La Union | **条件付きで可** | 運賃とレッスン料が未確認 |

---

## 4. モデルコースと費用試算（1名、PHP）

※ 交通費と飲食費は推測を含む見積。入場料は VISITA の登録値（2026年）。

### 日帰りA「アートと先住民文化」（雨でも成立）
PINES → Botanical Garden（徒歩）→ The Mansion・Wright Park（徒歩）→ タクシーで BenCab → Tam-awan → Igorot Stone Kingdom → Public Market で夕食 → 帰着

- 入場料: 110＋0＋200＋60＋100 = **470**
- タクシー: 低 4区間×約150 = 600 ／ 標準 800 ／ 高 チャーター 2,000
- 飲食: 低 400 ／ 標準 600 ／ 高 1,000
- **合計: 低 470＋600＋400 = 1,470 ／ 標準 470＋800＋600 = 1,870 ／ 高 470＋2,000＋1,000 = 3,470**

### 日帰りB「山と農園」（晴天日）
早朝に Mt. Ulap を歩く（Ampucao 側から入る）→ 午後に La Trinidad の Strawberry Farm と Bell Church → 夜は Session Road

- 入場料: Ulap の登録・ガイド料は**未確認**のため、仮に 0〜1,000（推測）。Strawberry 0、Bell Church 0
- 交通: タクシー・ジープニーで 500〜1,500（推測）
- 飲食・イチゴ狩り: 500〜1,000（推測）
- **合計: 低 0＋500＋500 = 1,000 ／ 標準 500＋1,000＋700 = 2,200 ／ 高 1,000＋1,500＋1,000 = 3,500**

### 1泊2日A「Sagada：洞窟・Echo Valley・山の町」
土曜 6:00 頃にバスでバギオを出発 → 昼過ぎに Sagada 着、登録 → Echo Valley とハンギング・コフィン → 宿泊 → 日曜朝に洞窟ツアー → 昼のバスでバギオへ戻る（夜着）

- バス: 220×2 = 440
- 登録・環境料: 100
- 洞窟ツアー（1名参加時）: 800（他の旅行者と組めば1人あたりは下がる）
- 宿: 低 800 ／ 標準 1,500 ／ 高 2,500（推測。公式価格は未確認）
- 飲食: 低 800 ／ 標準 1,200 ／ 高 1,500
- 現地のジープニー・ガイド: 低 0 ／ 標準 300 ／ 高 600
- **合計: 低 440＋100＋800＋800＋800＋0 = 2,940 ／ 標準 440＋100＋800＋1,500＋1,200＋300 = 4,340 ／ 高 440＋100＋800＋2,500＋1,500＋600 = 5,940**

### 1泊2日B「La Union：海とサーフィン体験」
土曜朝にバスで San Juan へ → 午後にサーフィンのレッスン → 宿泊 → 日曜に再度サーフィンと海鮮 → 夕方にバギオへ戻る

- バス: 片道 150〜300 と仮定、往復 300〜600（推測）
- レッスン: 2回×（500〜1,000）= 1,000〜2,000（推測。2010年の PHP200／時は古いので採用しない）
- 宿: 1,000〜3,000（推測）
- 飲食: 800〜1,500
- **合計: 低 300＋1,000＋1,000＋800 = 3,100 ／ 標準 450＋1,500＋2,000＋1,100 = 5,050 ／ 高 600＋2,000＋3,000＋1,500 = 7,100**

（参考）Mt. Pulag はツアー料金を調べられなかったため、試算していない。

---

## 5. 費用まとめ
12週間で「日帰り4回＋1泊2日2回」とした場合の目安:
- 低: 日帰り 4×1,470 = 5,880、1泊 2,940＋3,100 = 6,040 → **11,920**
- 標準: 4×2,000 = 8,000、4,340＋5,050 = 9,390 → **17,390**
- 高: 4×3,500 = 14,000、5,940＋7,100 = 13,040 → **27,040**

---

## 6. 未確認事項（理由つき）

| 項目 | 理由 |
|---|---|
| Mt. Pulag の2026年の入山料・予約窓口・人数上限 | mtpulag.denr.gov.ph は DNS で解決できず、bmb.gov.ph と car.denr.gov.ph/mt-pulag は 403。DENR-CAR の Citizen's Charter 2026（PDF）にも記載がない。検索エンジンも captcha で使えなかった |
| Mt. Ulap の登録料・ガイド料 | 公式ページが見つからず、検索もブロックされた |
| Sagada の現行料金（公式） | sagada.gov.ph が「rebuilding」の表示。Wikivoyage（2025〜26年）の値で代用した |
| バギオ発 La Union・Vigan のバス会社と運賃、Victory Liner の運賃 | 公式サイトの時刻・運賃表は予約フォームの奥にあり、取得できなかった |
| Panagbenga 2027 の日程 | 公式サイト panagbenga.com は「Launching Soon」の表示で、正式発表はまだない |
| 2027年の祝日（聖週間） | 大統領布告が未発表 |
| VISITA の料金が観光客向けか、学生割引があるか | API にその項目がない |
| Botanical Garden の値上げ額 | 市の告知ページが JavaScript で表示されるため本文を取得できず、報道にも金額がない |
| PINES の外泊許可・門限 | pinesacademy.com が 403。既存資料にも記載がない |
| タクシーの公式料金（LTFRB） | 確認できず、Wikivoyage の値で代用した |

---

## 7. 問い合わせ先と文案（送信はしていない）

- **PINES（学校）**: 「週末に1泊2日で Sagada などへ行く場合、外泊の申請手続き、門限、週末の食事キャンセルの締切（金曜17時と聞いています）を教えてください。」
- **DENR Mt. Pulag Protected Area Office**（連絡先は未確認。DENR-CAR の代表窓口 car.denr.gov.ph の Contact Us から問い合わせる）:
  > I plan to hike Mt. Pulag (Ambangeg trail) on a weekend in Feb–Apr 2027. Could you tell me the current entrance/environmental fees for foreign visitors, the reservation procedure and lead time, orientation schedule, and medical certificate requirements?
- **Sagada Municipal Tourism Office**:
  > What are the 2027 registration/environmental fee and the cave tour guide rates for foreign visitors, and are there special arrangements during Holy Week?

---

## 8. 出典一覧

| URL | 種別 | 確認日 | 適用年度 | 確認内容 |
|---|---|---|---|---|
| https://visita.baguio.gov.ph/park-tickets および https://api-booking.baguio.visita.ph/api/parks | 公式（市） | 2026-10-17 | 2026年の登録値 | 料金・営業時間・座標 |
| https://main.baguio.gov.ph/social-bot/announcement/increase-of-entrance-fee-at-baguio-botanical-garden | 公式（市） | 2026-10-17 | 不明 | 値上げ告知の存在のみ（本文は取得できず） |
| https://tribune.net.ph/2026/02/18/residents-now-must-pay-for-baguio-botanical-garden | 報道 | 2026-10-17 | 2026 | 住民向け無料措置の終了 |
| https://pubfiles.pagasa.dost.gov.ph/pagasaweb/files/cad/CLIMATOLOGICAL%20NORMALS%20(1991-2020)/BAGUIO.pdf | 公式（PAGASA） | 2026-10-17 | 1991–2020 | 降水量・降雨日数・最高気温 |
| https://en.wikipedia.org/wiki/Baguio（気候表、出典は PAGASA） | 準公式 | 2026-10-17 | 1991–2020 | 最低気温 |
| https://ifugao.gov.ph/getting-here/ | 公式（州） | 2026-10-17 | 不明 | Ohayami のバギオ発 21:00 |
| https://mountainprovince.gov.ph/the-province/getting-here/ | 公式（州） | 2026-10-17 | 不明 | Sagada の概要、名産品 |
| https://www.victoryliner.com/ | 公式（事業者） | 2026-10-17 | 2026 | オンライン予約の範囲 |
| https://en.wikivoyage.org/wiki/Sagada ／ Batad ／ Baguio ／ Kabayan ／ San_Juan_(La_Union) ／ Mount_Pulag_National_Park | 口コミ（共同編集） | 2026-10-17 | 2010〜2026（項目ごとに記載） | 運賃・料金・タクシー料金 |
| https://www.pinoymountaineer.com/2007/09/mt-pulag-2922.html | 口コミ（ブログ） | 2026-10-17 | 2015 | Pulag の手続き・参考料金 |
| https://www.sunstar.com.ph/pampanga/bingoplus-to-multiply-the-fun-at-panagbenga-festival-2026 | 報道（スポンサー記事） | 2026-10-17 | 2026 | 2/28〜3/8 のイベント |
| https://www.sunstar.com.ph/davao/feature/panagbenga-2026-baguio-in-bloom | 報道 | 2026-10-17 | 2026 | パレードの開催 |
| https://en.wikipedia.org/wiki/Panagbenga_Festival | 準公式 | 2026-10-17 | 一般 | 例年の期間 |
| https://router.project-osrm.org ／ https://photon.komoot.io | 計算ツール（OSM） | 2026-10-17 | — | 距離・所要時間・座標 |
| https://open.er-api.com/v6/latest/JPY | 為替データ | 2026-10-17 | 2026-10-16 | PHP→円の換算 |

---

## 9. 調査ログ（2026-10-16〜17）

- 検索エンジン: Brave（初回の数件は成功し、その後 captcha と 429）、DuckDuckGo html/lite（ボット判定）、Bing（無関係な結果）、Mojeek（空）、Yahoo（307）、Startpage・Ecosia（結果なし／403）。**検索結果をもとにした調査は、途中から公式ドメインへの直接アクセス、Wayback CDX、各サイト内検索、Wikivoyage・Wikipedia の raw に切り替えた。**
- 実行した検索クエリ: 「visita baguio park tickets entrance fee botanical garden」（Brave、成功）、「Baguio Botanical Garden entrance fee P100 tourists 2026 ordinance」（Brave、captcha）、「Mt Pulag entrance fee DENR 2026」系の6種（Brave・DDG・Bing・Mojeek・Yahoo、すべて失敗）、「Panagbenga 2026 schedule grand street dance float parade」（Brave、captcha）、SunStar サイト内検索（panagbenga 2026／street dance／float parade／2027）。
- 取得に成功（200）: visita.baguio.gov.ph、api-booking.baguio.visita.ph/api/parks、main.baguio.gov.ph（JavaScript 表示のため本文なし）、tribune.net.ph（WebFetch）、car.denr.gov.ph のトップ・サイト内検索・記事3件・Citizen's Charter、CITIZENS-CHARTER-DENR-CAR-2026-R.pdf、PAGASA BAGUIO.pdf、ifugao.gov.ph/getting-here、mountainprovince.gov.ph、sagada.gov.ph（rebuilding 表示）、victoryliner.com、codalines.com（必要な情報なし）、panagbenga.com（Launching Soon）、sunstar.com.ph の記事4件、pinoymountaineer.com（2007/09 の記事）、Wikivoyage 8件、Wikipedia（Baguio、Panagbenga）。
- 失敗: newsinfo.inquirer.net（403）、mb.com.ph（WebFetch で 403）、pia.gov.ph（403）、pinesacademy.com（403）、bmb.gov.ph（403）、car.denr.gov.ph/mt-pulag と /protected-areas（403）、mtpulag.denr.gov.ph・pulag.denr.gov.ph（DNS）、banaue.gov.ph・benguet.gov.ph（接続できず）、pinoymountaineer 2007/05（404）、Wayback CDX の一部（Temporarily Offline）、nominatim（Access denied）。
- 計算: OSRM のテーブル・ルート検索（PINES→各地）、復活祭の日付を計算するアルゴリズム（2027年）。
