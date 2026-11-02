# 現地の食事・スーパー・外食の一般料金（バギオ／ケープタウン）

- 調査設計：2026-10-16／価格の確認日：**2026-10-17**／[Issue #5](https://github.com/Rikkyhub/studying-abroad/issues/5)
- 対象：語学学校の寮に滞在する人（バギオ）と、自炊できる住居に滞在する人（ケープタウン）を想定した、**一般向けの価格比較**。個人の支払額・契約内容・予約内容は載せない（[公開データ方針](../docs/05-public-data-policy.md)、[#16](https://github.com/Rikkyhub/studying-abroad/issues/16)）。
- 価格はすべて **2026-10-17 にオンラインで見た表示価格**で、2027年の価格ではない。店舗・地域・在庫・キャンペーンによって変わる。
- 円換算はしない（[sources.md](sources.md) のとおり、換算レートは採用していない）。
- 第4章の3パターンは**匿名モデルの試算**で、特定の人の実際の支出ではない。

## 1. 要点

| # | 結論 | 確度 |
|---|---|---|
| 1 | PINES（バギオ）の食事条件：紹介会社 hub1234 の掲載では、平日（祝日を含む）の3食が料金に含まれ、週末は申込制で1食 PHP179。**学校公式の資料では確認できていないため要確認**。 | 要確認（準公式1件のみ） |
| 2 | バギオの外食・スーパーの価格：今回は取得できず**未確認**。デリバリーアプリ（foodpanda）は 403 で表示されなかった。 | 未確認 |
| 3 | ケープタウンの4大スーパー（Pick n Pay、Checkers、Shoprite、Woolworths）は、オンラインの表示価格を取得できた。主食・卵・野菜は3社でほぼ同じ価格帯で、Woolworths は品目によって1〜5割ほど高い。 | 高（表示価格） |
| 4 | 外食：Nando's（南ア公式メニュー API の default メニュー）は 1/4 Chicken＋Single Side が R75、1/2 Chicken＋Single Side が R129。そのほかのチェーンはメニューに価格がなく**未確認**。 | 高（Nando's）／未確認（その他） |
| 5 | 日本食材：醤油・味噌・寿司米・海苔は Woolworths と Pick n Pay のオンライン価格を確認できた。アジア系食材店の所在地と価格は**未確認**。 | 中 |
| 6 | デリバリー：Mr D の Service Fee は「かごの金額によって変わる」と公式 FAQ にあるが、金額は書かれていない。Uber Eats と Checkers Sixty60 の南アの手数料は**未確認**。 | 中／未確認 |

## 2. バギオ（寮食中心）

### 2.1 PINES の食事条件（要確認）

**学校公式の資料では確認できていない。** 以下は紹介会社 hub1234 の掲載（準公式、2026-10-17 確認、適用年度の記載なし）。2027年の条件として扱わない。

| 項目 | hub1234 の掲載内容 | 状態 |
|---|---|---|
| 平日 | 平日（祝日を含む）の3食は寮費に含まれる。5階のダイニングでビュッフェ形式 | 要確認 |
| 週末 | 週末の食事は料金に含まれない。金曜17時までにポータルで申し込むと1食 PHP179（ポイントから支払い） | 要確認 |
| 土曜・日曜の朝食 | 土曜の朝食は全員無料。日曜の朝食は PHP100 の申込制 | 要確認 |
| 平日食のキャンセル | 2週間単位でキャンセルでき、1食 PHP179 が返金される（最初の2週間は不可）。再申請の手数料は2週間分 PHP500、4週以上 PHP800 | 要確認 |
| 体調不良時 | おかゆなど別の食事を用意 | 要確認 |
| 立地 | SM City Baguio まで車で約8分（3.0km）、徒歩35〜40分 | 要確認 |

- PINES 公式サイト（pinesacademy.com）は 403（ボット判定）で、取得できなかった。2024年3月のアーカイブ（施設・寮のページ）には食堂の写真だけがあり、食事の回数や料金は載っていなかった。
- philschools.jp の PINES のページ（2026-10-04 の記事）には、食事の記載がなかった。
- 学校の規定を直接確認するまで、**週末の食費は「要確認」**とし、金額を確定させない。

### 2.2 バギオの外食・スーパー（未確認）

- 外食：foodpanda の店舗ページは 403（Access denied）で、今回は価格を確認できなかった。PR #14 の版に載っていた foodpanda の価格は、再確認できていないので載せない。
- スーパー（SM City Baguio、Puregold、Baguio Public Market）：価格・営業時間ともに**未確認**。
- 地元料理（pinikpikan、strawberry taho など）を出す店と価格：**未確認**。口コミ情報は使っていない。

## 3. ケープタウン（自炊中心）

### 3.1 表示価格の条件

| 店 | 取得方法 | 地域・店舗 | 税 | 配送 |
|---|---|---|---|---|
| Pick n Pay（PnP） | 公式サイトの商品検索 API | 店舗コード **WC21** の価格（Western Cape 内の店舗と推定。店舗名は特定できなかった） | 表示価格。VAT（15%）込みかどうかはサイト上の表記を確認していない | 含まない |
| Checkers | 公式サイトの商品ページ（JSON-LD） | 配達エリアを指定しない状態のオンライン価格 | 同上 | 含まない（Sixty60 の配達料は未確認） |
| Shoprite | 公式サイトの商品ページ（JSON-LD） | 同上 | 同上 | 含まない |
| Woolworths | 公式サイトが使う検索 API | **地域によって価格が3通りある**（API の p10／p30／p60）。どの地域に当たるかは未確認。価格が違う品目は幅で示した | 同上 | 含まない |

共通：確認日 2026-10-17、通貨 ZAR、適用年度は2026年時点の表示価格（2027年は未確認）、1商品あたりの価格。「在庫切れ」は、オンラインの表示であり、店頭に置いていないという意味ではない。

### 3.2 主な食品の価格（ZAR、容量は商品名のとおり）

| 品目 | PnP（WC21） | Checkers | Shoprite | Woolworths |
|---|---|---|---|---|
| 米 2kg | Excella Parboiled 34.99／Tastic 44.99 | Housebrand Parboiled 26.99 | Ritebrand Parboiled 28.99 | Parboiled Long Grain 41.99 |
| 食パン 700g | Albany Superior White 17.99 | Albany Superior White 18.99 | SASKO Premium White 19.99 | White Sandwich 21.99 |
| スパゲッティ 500g | No Name 16.99 | Mr. Pasta 16.99 | Ritebrand 14.99 | Spaghetti Pasta 22.99 |
| 鶏胸肉 | No Name Chicken Breast Fillet 1.5kg 99.99 | 未再確認 | 未再確認 | Skinless Chicken Breast Fillets 平均900g 125.54 |
| 牛ひき肉 | PnP Ground Beef 400g 54.99 | 未再確認 | 未再確認 | Lean Beef Mince 500g 74.99 |
| 卵 18個 | Eggs for Africa Medium 49.99／PnP Large 64.99 | Nulaid Large 59.99 | 未再確認 | Free Range Large 91.99 |
| 牛乳 2L | Clover Full Cream 29.99 | Clover Fresh Full Cream 37.99 | 未再確認 | Fresh Full Cream 38.99〜40.99 |
| ヨーグルト 1kg | PnP Full Cream Plain 39.99 | 未再確認 | 未再確認 | 未再確認 |
| 玉ねぎ 2kg | PnP Onions 69.99（1kg 38.99） | Onions 59.99 | Onions 54.99〜59.99（商品コード2種） | Brown Onions 79.99〜82.99 |
| トマト 1kg | PnP English Tomatoes 34.99 | Tomatoes 34.99（在庫切れ表示） | 未再確認 | Salad Tomatoes 34.99 |
| じゃがいも 2kg | PnP All Purpose 48.99 | Boil & Roast 49.99 | 未再確認 | 未再確認 |
| にんじん 1kg | PnP Carrots 14.99 | Large Carrots 16.99 | 未再確認 | 未再確認 |
| バナナ 1.2kg | PnP Bananas Box 42.99 | Bananas 39.99 | Bananas 39.99 | Bananas Tray 46.99〜48.99 |
| りんご 1.5kg | PnP Fuji 32.99 | Top Red 39.99 | 未再確認 | 未再確認 |
| ひまわり油 2L | Sunfoil 84.99／No Name 89.99 | 未再確認 | Ritebrand 87.99 | Sunflower Oil 84.99 |
| 塩 1kg | No Name Iodated 14.49 | Housebrand Iodated Coarse 13.99 | Ritebrand 13.99 | 未再確認 |
| オーツ 1kg | No Name Live Well Quick Cooking 39.99 | Housebrand Rolled Oats 36.99 | Ritebrand Oats 36.99 | Rolled Oats 47.99 |
| 水 5L | Cape Aqua Still 23.99 | aQuellé Still 29.99 | 未再確認 | 未再確認 |
| 冷凍ミックス野菜 | No Name 900g 40.99 | 未再確認 | 未再確認 | 未再確認 |
| インスタント麺 | Indomie Mi Goreng 85g 7.99 | — | — | — |
| インスタントコーヒー 200g | PnP 100% Pure 119.99 | 未再確認 | 未再確認 | 未再確認 |
| ルイボスティー 80袋 | PnP Rooibos 39.99 | 未再確認 | 未再確認 | 未再確認 |

- 「未再確認」は、今回の再検証で価格を取り直していない品目。PR #14 の版の値は引き継いでいない。
- PnP の No Name Sunflower Oil 2L は、PR #14 の版の R66.99 から R89.99 に変わっていた。
- **ケープタウン市の上水道は通常、飲用可能**：市の[水質公式ページ](https://www.capetown.gov.za/family-and-home/residential-utility-services/residential-water-and-sanitation-services/water-quality/)はSANS 241:2015に基づく定期検査を公表（2026-10-24確認、掲載の最新四半期は2026年4〜6月）。ただし[2026-05-16の市の注意喚起](https://www.capetown.gov.za/media-and-news/use-less-water-as-severe-weather-impacts-water-treatment-operations/)では、濁り・変色があれば煮沸し市へ報告するよう案内。**個々の宿泊施設の配管・貯水槽、局所的な断水・汚染、2027年の状況までは保証しない**。ボトル水の費用モデルは、宿泊先と現地の水質情報が確認できるまで変更しない。

### 3.3 日本食・アジア食材（ZAR）

| 品目 | 店 | 価格 |
|---|---|---|
| Kikkoman Traditional Soy Sauce 500ml | Woolworths | 118.00（通常価格の表示 143.99） |
| Kikkoman Soy Sauce 500ml | PnP | 154.99 |
| Kikkoman Soya Sauce 500ml／Soy Sauce 150ml | Checkers | 159.99／129.99 |
| Vital Original Soy Sauce 500ml | PnP | 84.99 |
| Miso Tasty White Miso Paste 200g | Woolworths | 69.99 |
| Hikari Karu-Mu Koji Miso Paste 375g | Woolworths | 99.99 |
| Yutaka Organic Miso 300g | PnP | 189.99 |
| Asian Sushi Rice 1kg | Woolworths | 79.99 |
| Paddy Sushi Rice 1kg | PnP | 47.99 |
| Asian Sushi Nori 28g | Woolworths | 105.99 |
| Our Sushi Salmon Combo（個数の表示なし） | Woolworths | 139.99 |
| Our Sushi Salmon Roses 6 pk | Woolworths | 109.99 |
| PnP Sushi Salmon Rose Combo 8 Pieces | PnP | 89.99 |

アジア系食材店（Wing Hing など）の所在地と価格は**未確認**。

### 3.4 外食（Nando's 南ア公式メニュー API、default メニュー、ZAR）

| メニュー | 価格 |
|---|---|
| 1/4 Chicken + any Single Side | 75 |
| 1/4 Chicken, Single Chips & Nando's Roll | 85 |
| Chicken Burger + any Single Side | 99 |
| Chicken Wrap + any Single Side | 110 |
| 1/2 Chicken + any Single Side | 129 |

- default メニューの価格（API の値はセント単位。例：7500 → R75）。店舗やデリバリーでは変わることがある。飲み物・チップは含まない。
- Spur、Ocean Basket、Kauai、Steers などは、PR #14 の調査時にメニューページに価格がなく、今回も再取得していない（未確認）。

### 3.5 デリバリー手数料

| サービス | 確認できた内容（2026-10-17） | 金額 |
|---|---|---|
| Mr D（公式 FAQ） | Service Fee はかごの金額によって変わる。TakealotMORE 会員は Service Fee なし。会員の無料配達の最低注文額はレストラン R150、食料品 R350。初回注文の配達無料クーポンあり。デリバリー用に価格を上げる店もある | Service Fee・配達料の金額は**未確認** |
| Uber Eats | 南アの手数料の金額 | 未確認（再取得していない） |
| Checkers Sixty60 | 配達料 | 未確認 |

## 4. 匿名モデルの試算：ケープタウンの食費3パターン（1人、8週間）

**これは匿名モデルのシミュレーションで、特定の人の実際の支出や支払額ではない。** 品目と量は仮定で、単価は 3.2〜3.4 の 2026-10-17 の表示価格を使った。配達料・チップ・酒類は含めていない。

### 4.1 週1回の買物リスト（PnP WC21 の価格）

| 品目 | 商品 | 週の量 | 単価 R | 週額 R |
|---|---|---|---|---|
| 米 | Excella Rice Parboiled 2kg | 1/2袋 | 34.99 | 17.50 |
| パン | Albany Superior White 700g | 1斤 | 17.99 | 17.99 |
| パスタ | No Name Spaghetti 500g | 1袋 | 16.99 | 16.99 |
| 鶏胸肉 | No Name Chicken Breast Fillet 1.5kg | 1袋 | 99.99 | 99.99 |
| 牛ひき肉 | PnP Ground Beef 400g | 1パック | 54.99 | 54.99 |
| 卵 | Eggs for Africa Medium 18個 | 1パック | 49.99 | 49.99 |
| 牛乳 | Clover Full Cream 2L | 1本 | 29.99 | 29.99 |
| ヨーグルト | PnP Full Cream Plain 1kg | 1個 | 39.99 | 39.99 |
| 玉ねぎ | PnP Onions 1kg | 1袋 | 38.99 | 38.99 |
| トマト | PnP English Tomatoes 1kg | 1袋 | 34.99 | 34.99 |
| じゃがいも | PnP All Purpose 2kg | 1/2袋 | 48.99 | 24.50 |
| にんじん | PnP Carrots 1kg | 1袋 | 14.99 | 14.99 |
| バナナ | PnP Bananas Box 1.2kg | 1箱 | 42.99 | 42.99 |
| りんご | PnP Fuji 1.5kg | 1袋 | 32.99 | 32.99 |
| 冷凍野菜 | No Name Mixed Vegetables 900g | 1袋 | 40.99 | 40.99 |
| オーツ | No Name Live Well Quick Cooking Oats 1kg | 1/2袋 | 39.99 | 20.00 |
| 水 | Cape Aqua Still Water 5L | 2本 | 23.99 | 47.98 |
| インスタント麺 | Indomie Mi Goreng 85g | 3個 | 7.99 | 23.97 |
| 小計 | | | | 649.82 |
| 調味料・飲料（8週で按分） | Sunfoil 2L 84.99＋塩 1kg 14.49＋Vital 醤油 500ml 84.99＋コーヒー 200g 119.99＋ルイボス 80袋 39.99＝344.45 ÷ 8 | | | 43.06 |
| 日本食材（8週で按分） | Woolworths 白味噌 200g 69.99＋PnP 寿司米 1kg 47.99＝117.98 ÷ 8 | | | 14.75 |
| 予備（5%） | 707.63 × 0.05 | | | 35.38 |
| **週額** | | | | **約 R743** |

### 4.2 3パターン

| パターン | 計算 | 週額 R | 8週 R |
|---|---|---|---|
| A 自炊中心 | 4.1 の週額 | 743 | 5,944 |
| B 自炊＋外食週2回 | 743（自炊は減らさない控えめな計算）＋ Nando's Chicken Wrap + Side R110 × 2 | 963 | 7,704 |
| C 外食多め | 自炊を A の6割（743 × 0.6 ≒ 446）＋ Nando's 1/2 Chicken + Side R129 × 7 | 1,349 | 10,792 |

- 外食の単価は Nando's の1チェーンだけを基準にしている。着席型の店や飲み物を含めると上がる（金額は未確認）。
- 住居にキッチン（冷蔵庫・コンロなど）があることが A・B の前提。住居の設備は住居ごとに確認する。

## 5. 未確認事項

| 項目 | 理由 |
|---|---|
| PINES の食事条件（平日3食、週末 PHP179、土日の朝食、キャンセル規定）と2027年の適用 | 学校公式サイトが 403。アーカイブにも食事の規定がなかった。紹介会社1件の掲載のみ |
| バギオの外食・スーパーの価格 | foodpanda が 403。スーパーは調べられなかった |
| Woolworths の3つの価格区分がどの地域に当たるか | API に地域名がない |
| PnP の店舗コード WC21 の店舗名 | API から特定できなかった |
| 表示価格の VAT の扱い | サイト上の表記を確認していない |
| Checkers・Shoprite の一部品目（鶏胸肉・牛ひき肉など） | 今回は再取得していない |
| Nando's 以外の外食価格 | メニューに価格がない（PR #14 の調査時）。今回は再取得していない |
| Mr D・Uber Eats・Sixty60 の手数料の金額 | 公開ページに金額がない、または再取得していない |
| ケープタウンの水道水・買物の安全 | 市の配水水質は公式資料で確認（2026-10-24）。ただし宿泊先の配管・貯水槽、個別の水質警報、2027年の状況は未確認。買物時の治安・移動は #8 で別途確認 |

## 6. 問い合わせの文案（送信はしていない）

学校宛て：
> 2027年に入学を検討している者です。寮の食事について確認させてください。(1) 平日3食が料金に含まれ、週末は1食179ペソの申込制という理解で合っていますか。2027年も同じ料金ですか。(2) 土曜・日曜の朝食の扱いを教えてください。(3) 週末の申込締切と支払い方法を教えてください。(4) アレルギーや体調不良の際の対応を教えてください。

## 7. 調査ログ（2026-10-17）

WebSearch はこの環境では使えなかった（API エラー）。そのため、各社の公式サイトと API を直接取得した。

| 結果 | URL・内容 |
|---|---|
| 200 | https://www.hub1234.com/philippines/baguio/pines-main（WebFetch。PINES の食事条件の掲載を再確認） |
| 200 | https://philschools.jp/school/pines/（食事の記載なし。2026-10-04 の記事） |
| 403 | https://pinesacademy.com/ と https://www.pinesacademy.com/（WebFetch と curl。ボット判定） |
| 200 | Wayback CDX（pinesacademy.com/*）→ 2024-03-18 の eng/classroom_main?nav=cafeteria と eng/dorm_main を取得。食堂の写真の見出しだけで、食事の回数・料金はなかった。web.archive.org は WebFetch では取得できなかった |
| 200（別サイト） | https://www.pinesedu.com/、https://www.pinesglobal.com/（PINES 校とは無関係） |
| 000 | https://pines.ph/（接続できず） |
| 403 | https://www.foodpanda.ph/restaurant/r1dl/lechon-house-baguio（WebFetch と curl） |
| 200 | https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search（POST、storeCode=WC21、query パラメータ。約27語を検索） |
| 403→200 | Checkers の商品ページは WebFetch では 403、curl では 200。https://www.checkers.co.za/sitemap.xml → seq_product-sitemap_00〜02 から商品URLを抽出し、JSON-LD の価格を取得 |
| 200／500 | Shoprite の seq_product-sitemap_00〜01 は 200、02 は 500。商品ページは 200 |
| 200 | https://ac.cnstrc.com/search/...（Woolworths の検索 API、約17語）。Woolworths の商品ページ（Our Sushi Salmon Combo）は WebFetch で価格が表示されなかった |
| 200 | https://api.nandos.co.za/api/v2/pack/menu/default（WebFetch では名前と価格を対応付けられず、curl で取得して商品IDで照合） |
| 200 | https://www.mrd.com/help/faqs（WebFetch） |
| 未実施 | Uber Eats、Sixty60、Spur・Ocean Basket ほかのメニュー、外務省の安全情報、バギオのスーパー（時間の都合で今回は再取得していない） |
