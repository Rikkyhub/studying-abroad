# 現地の食事・スーパー・日常の食費（バギオ／ケープタウン）

- 確認日: 2026-10-17（価格はすべてこの日にオンラインで確認した表示価格。2027年の価格ではない）
- Issue: [#5 食費・外食・スーパー・日本食](https://github.com/Rikkyhub/studying-abroad/issues/5)
- 前提: 1人分。バギオ 2027-02-06〜05-01（PINES、平日寮食付き、12週）。ケープタウン 2027-05-31〜07-23頃（8週、自炊前提、住居は未確定）。
- 為替（参考）: 1 ZAR ≈ 9.57円、1 PHP ≈ 2.51円（open.er-api.com、2026-10-16 00:02 UTC 更新）。円換算は概算で、2027年のレートではない。
- 既存資料 `research/food-and-living.md`（2026-10-16）の再検証: 「PINESの週末食は要確認」を、エージェントの記載で確認した（下記）。「仮の単価で月額を埋めない」という方針は引き継ぎ、取得できなかった品目は未確認とした。既存資料と矛盾する点はなかった。

## 1. 要点（結論と確度）

| # | 結論 | 確度 |
|---|---|---|
| 1 | PINES の寮食は**平日（祝日を含む）3食が料金に含まれる**。**週末の食事は含まれない**。週末食は金曜17時までにポータルで申し込むと **1食 PHP179**（ポイント払い）。**土曜の朝食は全員無料**、**日曜の朝食は PHP100 の申込制**。平日の食事は2週間単位でキャンセルでき、1食 PHP179 が返金される（最初の2週間は不可。再申請の手数料は2週間分 PHP500／4週以上 PHP800）。 | 中（エージェント hub1234.com の記載のみ。学校公式と philschools.jp では確認できなかった） |
| 2 | バギオの週末外食: foodpanda の Lechon House のデリバリー価格で、ご飯付きの1皿が **PHP301〜410**（掲載割引後 PHP256〜349）。Good Taste、Oh My Gulay、Café by the Ruins、Hill Station、日本食店のメニュー価格は**取得できず未確認**。 | 低〜中 |
| 3 | ケープタウンのスーパーは、PnP・Checkers・Shoprite・Woolworths の4社とも**オンライン価格を取得できた**（PnP は API、Checkers と Shoprite は商品ページの JSON-LD、Woolworths は検索 API）。主要品目の価格帯はほぼ同じで、Woolworths が1〜5割ほど高い。 | 高（表示価格。地域や店舗で変わることがある） |
| 4 | **週1回の買物リスト（1人・自炊中心）は約 R773／週**（PnP 価格、下記 4.2）。月額は **約 R3,355（約3.2万円）**。8週間で約 R6,184（約5.9万円）。 | 中（品目と量は仮定。単価は実際の価格） |
| 5 | 外食の単価（Nando's 公式メニュー API）: 1/4 Chicken + 付け合わせ1品 **R75**、Chicken Burger + 付け合わせ **R99**、1/2 Chicken + 付け合わせ **R129**。着席型の店（Spur、Ocean Basket など）の価格は取得できず未確認。 | 高（Nando's）／未確認（その他） |
| 6 | 日本食材: Woolworths で Kikkoman 醤油 500ml R118、白味噌 200g R69.99、寿司米 1kg R79.99、海苔 28g R105.99、寿司 9〜10個 R139.99。PnP では寿司米 1kg R47.99、Yutaka の有機味噌 300g R189.99。**Wing Hing などアジア系の店の所在地と価格は未確認**（検索がレート制限で失敗）。 | 中 |
| 7 | デリバリー: Mr D には「Service Fee（かご金額で変わる）」があり、TakealotMORE 会員は無料、無料配達は最低 R150（レストラン）／R350（食料品）から。Uber Eats の手数料の**南ア向けの金額は未確認**。 | 中 |

## 2. 詳細表

### 2.1 PINES の寮食（エージェントの記載）

| 項目 | 内容 | 出典 |
|---|---|---|
| 平日 | 平日（祝日を含む）は3食が料金に含まれる。5階ダイニングでビュッフェ形式。混雑するため昼食は2交代。学生証をタッチして受け取る | hub1234（準公式） |
| 週末 | 週末の食事は料金に含まれない。金曜17時までにポータルで申し込むと 1食 PHP179（ポイント払い）。土曜の朝食は無料、日曜の朝食は PHP100 の申込制 | 同上 |
| 返金 | 平日の食事は2週間単位でキャンセルでき、1食 PHP179 が返金される。最初の2週間は不可。再申請の手数料は2週間分 PHP500、4週以上 PHP800 | 同上 |
| 体調不良時 | おかゆなど別の食事に対応 | 同上 |
| 洗濯（参考） | 洗濯と乾燥で PHP150、どちらか一方なら PHP100 | 同上 |
| 立地 | SM City Baguio まで車で約8分（3.0km）、Session Road まで約7分（2.8km）。タクシーの初乗りは PHP50 | 同上 |

※ philschools.jp/school/pines/ を取得したところ、IELTS 校舎の統合に関するニュース記事が表示され、食事の記載はなかった。PINES 公式サイトの規定は確認できていない。

### 2.2 バギオの外食（価格を確認できたもの）

foodpanda「Lechon House – Baguio」の公開ページ（デリバリー価格。PHP、1品あたり、2026-10-17）

| 品目 | 価格 | 掲載割引後 |
|---|---|---|
| Lechon Belly with Rice | 410 | 348.5 |
| Hungarian Sausage (1pc) With Egg, Mixed Veggies & Rice | 301 | 255.85 |
| Lechon Kawali | 321 | 272.85 |
| Crispy Sisig with Egg | 394 | 334.9 |
| Pakbet | 221 | 187.85 |
| Plain Rice | 32 | 27.2 |
| Ice Tea | 70 | 59.5 |
| Bottled Water 500ml | 30 | 25.5 |
| Ube Cake | 260 | 221 |

※ デリバリーアプリの価格は店頭より高く設定されることがある（一般論で、この店については未確認）。foodpanda はその後のアクセスで "Access denied" になり、他の店は取得できなかった。

バギオ市の foodpanda 一覧ページ（取得できた48店）には、Good Taste、Oh My Gulay、Café by the Ruins、Hill Station、日本食店はいずれも載っていなかった。一覧に載らないことは、店が存在しない根拠にはならない。

指定されたローカル料理（pinikpikan、etag、strawberry taho、ube jam）と、それを出す店や価格は**未確認**（6章参照）。**口コミ情報は今回は一切使っていない。**

### 2.3 バギオのスーパー
SM City Baguio、Puregold、Baguio Public Market は、価格・営業情報ともに**未確認**。距離は 2.1 の hub1234 の記載（SM まで車で約8分）のみ。

### 2.4 ケープタウンのスーパー価格（2026-10-17、ZAR、税込の表示価格）

| 品目 | PnP（店舗コード WC21） | Checkers | Shoprite | Woolworths |
|---|---|---|---|---|
| 米 2kg | Excella Parboiled 34.99／Tastic 44.99 | Housebrand Parboiled 26.99／Tastic 44.99 | Ritebrand Parboiled 28.99 | Parboiled Long Grain 41.99 |
| 食パン 700g | Albany Superior White 17.99 | Albany Superior White 18.99 | SASKO Premium 19.99 | White Sandwich 21.99 |
| スパゲッティ 500g | No Name 16.99 | Mr. Pasta 16.99 | Ritebrand 14.99 | Spaghetti Pasta 22.99 |
| 鶏胸肉 | No Name Chicken Breast Fillet 1.5kg（冷凍）99.99／PnP Skinless Chicken Fillet Breast 12 Pack 約2kg 159.98 | 調べた生・冷凍の各商品が在庫切れで価格なし | County Fair 在庫切れ | Skinless Chicken Breast Fillets 約900g 125.54 |
| 牛ひき肉 | PnP Beef Mince 138.99/kg、Ground Beef 400g 54.99 | Beef Mince (300–500g) 129.99（kg単価表示） | 同 129.99 | Lean Beef Mince 500g 74.99 |
| 卵 18個 | Eggs for Africa Medium 49.99／PnP Large 64.99 | Nulaid Large 59.99／Housebrand 64.99 | Nulaid 在庫切れ | Free Range Large 91.99 |
| 牛乳 2L | Clover Full Cream 29.99 | Clover Fresh Full Cream 37.99 | 在庫切れ | Fresh Full Cream 38.99 |
| プレーンヨーグルト 1kg | PnP Full Cream 39.99 | Crystal Valley Low Fat 36.99 | 在庫切れ | Greek Style 77.99 |
| 玉ねぎ 2kg | PnP Onions 69.99 | Onions 59.99 | Onions 59.99 | Brown Onions 82.99 |
| トマト 1kg | PnP English Tomatoes 34.99 | Tomatoes 1kg 34.99（在庫切れ表示） | 在庫切れ | Salad Tomatoes 34.99 |
| じゃがいも 2kg | PnP All Purpose 48.99 | Boil & Roast 49.99 | 在庫切れ | Medium Potatoes 54.99 |
| にんじん 1kg | PnP Carrots 14.99 | Large Carrots 16.99 | 在庫切れ | Large Carrots 16.99 |
| バナナ | PnP Bananas Box 1.2kg 42.99 | Bananas 1.2kg 39.99 | 同 39.99 | Bananas Tray 1.2kg 48.99 |
| りんご 1.5kg | PnP Fuji 32.99 | Top Red 39.99 | 在庫切れ | Seasonal Apples 33.99 |
| ひまわり油 2L | Sunfoil 84.99／No Name Cooking Oil 66.99 | 調べた商品が在庫切れ | Ritebrand 87.99 | Sunflower Oil 84.99 |
| 塩 1kg | No Name Iodated 14.49 | Housebrand 13.99 | Ritebrand 13.99 | Cerebos 25.99 |
| 醤油 | Kikkoman 500ml 154.99／Vital Original 500ml 84.99 | Kikkoman 150ml 129.99 | 未取得 | Kikkoman Traditional 500ml 118.00 |
| オートミール 1kg | No Name Live Well Quick Oats 39.99 | Housebrand Rolled Oats 36.99 | Ritebrand Oats 36.99 | Rolled Oats 47.99 |
| インスタントコーヒー 200g | PnP 100% Pure 119.99 | Jacobs Krönung 204.99 | 未取得 | Nescafé Classic 129.99 |
| ルイボスティー 80袋 | PnP Rooibos 39.99 | Housebrand 37.99 | Ritebrand 37.99 | Rooibos Tagless 56.99 |
| 水 5L | PnP Still Spring 28.99／Cape Aqua 23.99 | aQuellé 29.99 | aQuellé 31.99 | Still Spring 29.99 |
| 冷凍ミックス野菜 | No Name 900g 40.99 | 調べた商品が在庫切れ | Ritebrand 900g 在庫切れ | Diced Vegetable Mix 1kg 64.99 |
| インスタント麺 | Indomie Mi Goreng 85g 7.99 | — | — | — |

注:
- 「在庫切れ」は、配達エリアを指定しない状態のオンライン在庫の表示。店頭に置いていないという意味ではない。Checkers の JSON-LD では、在庫切れの商品は価格 0 と表示される。
- PnP は店舗コード WC21（Western Cape 系と推定）の価格。WC01 でも同じ価格だった。店舗名は API から特定できなかった。
- ケープタウンの水道水は飲用可とされることが多いが、今回は公式情報を確認していない（未確認）。水は買物リストに入れているが、外してもよい。

### 2.5 日本食・アジア食材（オンライン価格、ZAR）

| 品目 | 店 | 価格 |
|---|---|---|
| Kikkoman Traditional Soy Sauce 500ml | Woolworths | 118.00 |
| Kikkoman Soy Sauce 500ml | PnP | 154.99 |
| Miso Tasty White Miso Paste 200g | Woolworths | 69.99 |
| Hikari Karu-Mu Koji Miso Paste 375g | Woolworths | 99.99 |
| Yutaka Organic Miso 300g | PnP | 189.99 |
| Asian Sushi Rice 1kg | Woolworths | 79.99 |
| Paddy Sushi Rice 1kg | PnP | 47.99 |
| Asian Sushi Nori 28g | Woolworths | 105.99 |
| Our Sushi Stacker & Rose Selection 9 Pcs | Woolworths | 139.99 |
| Our Sushi Salmon Roses 6 pk | Woolworths | 109.99 |
| PnP Sushi Salmon Rose Combo 8 Pieces | PnP | 89.99 |

Wing Hing などアジア系スーパーの店舗名・所在地・価格は**未確認**。参考までに検索リンクを載せる（存在は確認していない）。
- Wing Hing Cape Town（検索リンク）: https://www.google.com/maps/search/?api=1&query=Wing+Hing+Cape+Town
- Asian supermarket Cape Town（検索リンク）: https://www.google.com/maps/search/?api=1&query=Asian+supermarket+Cape+Town

### 2.6 外食単価（Nando's 南ア公式メニュー API、default メニュー、ZAR）

| メニュー | 価格 |
|---|---|
| 1/4 Chicken + any Single Side | 75 |
| 1/4 Chicken, Single Chips & Nando's Roll | 85 |
| Chicken Burger + any Single Side | 99 |
| Chicken Wrap + any Single Side | 110 |
| 1/2 Chicken + any Single Side | 129 |
| Avo & Halloumi Boujee Bowl with Pulled Chicken | 95 |
| PERi-PERi Chips (Single) | 36 |

※ default メニューの価格。店舗やデリバリーでは変わることがある。飲み物とチップは含まない。

### 2.7 デリバリー手数料

| サービス | 確認できた内容 | 金額 |
|---|---|---|
| Mr D | Service Fee は「かごの金額によって変わる」。TakealotMORE 会員は Service Fee が無料。会員の無料配達は最低注文額がレストラン R150、食料品 R350。初回注文は配達無料のクーポンあり。デリバリー用に価格を上げる店もある。PnP の食料品は1注文45点まで | 具体的な金額の記載なし（未確認） |
| Uber Eats | ヘルプに載っている手数料の種類は Service Fee、Delivery Fee、Small Order Fee、Busy Area Fee など。取得したページは日本向けの内容とみられ、南アの金額は書かれていない | 未確認 |
| Checkers Sixty60 | 配達料 | 未確認（サイトの API が 403） |

### 2.8 買い物の安全
- 外務省 海外安全ホームページの南アフリカの頁（危険情報、安全対策基礎データ）は、今回のURL推定で取得できなかった（未確認）。次回は https://www.anzen.mofa.go.jp/ から「南アフリカ」を開いて確認する。
- 現時点の方針（推奨で、出典の確認はまだ）: 夜間と人通りの少ない道を歩かない。重い荷物を持つ買物は配車アプリ（Uber、Bolt）か Sixty60 などの配達を使う。スマホを路上で出さない。住居が決まったら、最寄り店までの道を昼に下見する。

## 3. 実行可否の判定

| 項目 | 判定 |
|---|---|
| バギオで平日に寮食だけで過ごすこと | 可（3食付き。エージェント情報） |
| バギオの週末に寮食を使うこと | 可（PHP179/食、金曜17時の締切までに申込） |
| ケープタウンで自炊すること | 可。4大チェーンとも主食、たんぱく源、野菜を R15〜R160 で買える。住居にキッチンがあることが前提（未確定） |
| ケープタウンで日本食材を確保すること | 可（醤油、味噌、寿司米、海苔は Woolworths や PnP にある）。割高なので、少量を日本から持って行くのも選択肢 |

## 4. 費用試算

### 4.1 バギオ（週末食、12週）
週末は約12回（2027-02-06 は土曜、05-01 も土曜。土曜13回・日曜12回のうち、到着日と出発日の扱いで変わる）。土曜の朝食は無料。

| ケース | 計算 | 合計 |
|---|---|---|
| 低: 週末は寮食のみ | 土曜の昼・夜 2食 + 日曜の朝・昼・夜（朝 PHP100、昼夜 PHP179×2）= 179×2 + 100 + 179×2 = PHP816/週 × 12 | PHP9,792（約2.5万円） |
| 標準: 週末の半分を外食 | 寮食で週 PHP408（816×0.5）+ 外食3食×PHP350（Lechon House のご飯付き1皿＋飲み物 ≒ PHP301〜410＋30〜70）≒ PHP1,458/週 × 12 | PHP17,496（約4.4万円） |
| 高: 週末は全部外食＋カフェ | 外食5食×PHP450 + 日曜朝 PHP100 + カフェ等 PHP300（未確認の仮置き）= PHP2,650/週 × 12 | PHP31,800（約8.0万円） |

※ 外食単価は foodpanda の1店舗の価格を基準にしている（確度は低い）。カフェの PHP300 は根拠のない仮置きなので、COST では未確認の注記を付けた。平日のおやつや飲み物は含まない。

### 4.2 ケープタウン: 週1回の買物リスト（1人、自炊中心、PnP 価格）

| 品目 | 商品 | 週の量 | 単価 R | 週額 R |
|---|---|---|---|---|
| 米 | Excella Rice Parboiled 2kg | 1/2袋（1kg） | 34.99 | 17.50 |
| パン | Albany Superior White 700g | 1斤 | 17.99 | 17.99 |
| パスタ | No Name Spaghetti 500g | 1袋 | 16.99 | 16.99 |
| 鶏胸肉 | No Name Chicken Breast Fillet 1.5kg（冷凍） | 1袋（約1.5kg） | 99.99 | 99.99 |
| 牛ひき肉 | PnP Ground Beef 400g | 1パック | 54.99 | 54.99 |
| 卵 | Eggs for Africa Medium 18 | 1パック | 49.99 | 49.99 |
| 牛乳 | Clover Full Cream 2L | 1本 | 29.99 | 29.99 |
| ヨーグルト | PnP Full Cream Plain 1kg | 1個 | 39.99 | 39.99 |
| 玉ねぎ | PnP Onions 1kg | 1袋 | 38.99 | 38.99 |
| トマト | PnP English Tomatoes 1kg | 1袋 | 34.99 | 34.99 |
| じゃがいも | PnP All Purpose 2kg | 1/2袋 | 48.99 | 24.50 |
| にんじん | PnP Carrots 1kg | 1袋 | 14.99 | 14.99 |
| バナナ | PnP Bananas Box 1.2kg | 1箱 | 42.99 | 42.99 |
| りんご | PnP Fuji 1.5kg | 1袋 | 32.99 | 32.99 |
| 冷凍野菜 | No Name Mixed Vegetables 900g | 1袋 | 40.99 | 40.99 |
| オートミール | No Name Quick Oats 1kg | 1/2袋 | 39.99 | 20.00 |
| 水 | Cape Aqua Still Water 5L | 2本 | 23.99 | 47.98 |
| インスタント麺 | Indomie Mi Goreng 85g | 3個 | 7.99 | 23.97 |
| 小計（生鮮・主食） | | | | 649.82 |
| 調味料など（8週で按分） | 油 Sunfoil 2L 84.99、塩 14.49、醤油 Vital 500ml 84.99、コーヒー 200g 119.99、ルイボス 80袋 39.99、Kikkoman 500ml 154.99 = 499.44 ÷ 8週 | | | 62.43 |
| 味噌など日本食材（8週で按分） | 白味噌 200g（Woolworths 69.99）×2 + 寿司米 1kg（PnP 47.99）= 187.97 ÷ 8 | | | 23.50 |
| 予備（量の変動、5%） | 735.75 × 0.05 | | | 36.79 |
| **週額** | | | | **約 R773** |

- 月額（30.4日 ÷ 7 = 4.34週）: 773 × 4.34 ≒ **R3,355（約3.2万円）**
- 8週間: 773 × 8 ≒ **R6,184（約5.9万円）**
- 安いケース（Checkers/Shoprite のプライベートブランドに替え、水を買わない）: 週 R650 程度（約 -16%、計算は概算）。高いケース（Woolworths で買う）: 主な品目で 1.2〜1.5倍なので週 R1,000 程度（係数 1.3 を掛けた概算）。

### 4.3 ケープタウンの3ケース（8週間、1人）

| ケース | 計算 | 8週合計 R | 円換算 |
|---|---|---|---|
| A 自炊中心 | R773/週 × 8 | 6,184 | 約5.9万円 |
| B 自炊 + 外食週2回 | 自炊を2食分減らす R773 −（2食 × 約R25 の食材費）= R723/週 + 外食2回 × R110（Nando's の Wrap + Side）+ 飲み物 R30 × 2 = R220 + 60 → R1,003/週 × 8 | 8,024 | 約7.7万円 |
| C 外食多め | 自炊 R450/週（朝食と一部）+ 外食7回 × R140（Nando's の 1/2 Chicken + Side R129 程度＋飲み物）= R980 + デリバリー2回分の手数料（未確認のため仮に計上しない）→ R1,430/週 × 8 | 11,440＋手数料 | 約11万円＋α |

※ 「1食あたりの食材費 R25」は 4.2 の週額 ÷ 約30食で出した概算（773 ÷ 30 ≒ 26）。チップ（一般に10〜15%とされるが、出典は未確認）と酒類は含まない。

## 5. 未確認事項（理由）

| 項目 | 理由 |
|---|---|
| PINES 公式の食事規定、2027年の週末食の価格 | 公式サイトを取得しておらず、philschools.jp にも記載がなかった。hub1234 の1件だけで、裏付けがない |
| Good Taste、Oh My Gulay、Café by the Ruins、Hill Station、Session Road の店、バギオの日本食店とカフェのメニュー価格 | 公式サイトの推定URLに接続できなかった。hillstation.com.ph は JS リダイレクトのみ。foodpanda は2回目以降 403/Access denied。GrabFood は位置情報なしでは検索結果が0件 |
| pinikpikan、etag、strawberry taho、ube jam を出す店と価格 | 検索エンジン（Brave）がレート制限（429）で使えなかった |
| SM City Baguio、Puregold、Public Market の価格 | 時間切れのため、取得まで進めなかった |
| Wing Hing などアジア系スーパーの所在地と価格 | 検索が 429。公式サイトも特定できなかった |
| Spur、Ocean Basket、Kauai、Steers などの価格 | メニューページに価格がなかった（JS で読み込むかアプリ専用）。McDonald's は 403、KFC は接続できなかった |
| Uber Eats と Sixty60 の南アでの手数料の金額 | 公開ページに金額がない |
| 外務省の南アフリカの安全情報 | URL 推定で取得できなかった。トップページから辿って確認する必要がある |
| ケープタウンの水道水が飲めるか | 公式情報を確認していない |
| 住居のキッチン設備 | 住居が未確定 |

## 6. 問い合わせ先・文案

PINES（またはエージェント）宛て:
> 2027年2月6日入学予定の者です。寮食について確認させてください。(1) 平日3食が料金に含まれ、週末は1食179ペソの申込制という理解で合っていますか。2027年も同じ料金ですか。(2) 土曜の朝食が無料、日曜の朝食が100ペソという点は2027年も同じですか。(3) 週末の申込締切と支払い方法（ポイントのチャージ方法）を教えてください。(4) アレルギーや体調不良の際、どのように対応していただけますか。

ケープタウンの住居先宛て（確定後）:
> Could you confirm the kitchen facilities (fridge, stove/oven, microwave, kettle, cookware, utensils), whether the kitchen is shared, and the nearest supermarket and a safe way to get there?

## 7. 出典一覧

| URL | 種別 | 確認日 | 適用年度 | 確認内容 |
|---|---|---|---|---|
| https://www.hub1234.com/philippines/baguio/pines-main | 準公式（留学エージェント） | 2026-10-17 | 2026年時点の掲載 | 寮食の範囲、週末 PHP179、土曜朝食無料、日曜朝食 PHP100、キャンセル返金、洗濯料金、距離 |
| https://philschools.jp/school/pines/ | 準公式（エージェント） | 2026-10-17 | 2026-10-04 の記事 | 食事の記載なし（IELTS 校舎の統合ニュースのみ） |
| https://www.foodpanda.ph/restaurant/r1dl/lechon-house-baguio | 準公式（デリバリーアプリ） | 2026-10-17 | 2026 | 2.2 のメニュー価格（PHP） |
| https://www.foodpanda.ph/city/baguio | 準公式 | 2026-10-17 | 2026 | 掲載48店（指定の店は載っていない） |
| https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search（POST, storeCode=WC21） | 公式（PnP の商品検索 API） | 2026-10-17 | 2026 | 2.4/2.5 の PnP 価格 |
| https://www.checkers.co.za/product/...（各商品ページの JSON-LD。例: checkers-housebrand-parboiled-white-rice-2kg-10158755EA） | 公式 | 2026-10-17 | 2026 | 2.4 の Checkers 価格 |
| https://www.shoprite.co.za/product/...（例: ritebrand-parboiled-medium-grain-white-rice-2kg-10130255EA） | 公式 | 2026-10-17 | 2026 | 2.4 の Shoprite 価格 |
| https://ac.cnstrc.com/search/...?key=key_tw9hKe0fkfgEf36D（Woolworths サイトが使う検索 API）、https://www.woolworths.co.za/prod/Food/Deli-Entertaining/Entertaining-Platters/Our-Sushi-Salmon-Combo/_/A-6009226866340（商品ページで価格が一致することを確認） | 公式 | 2026-10-17 | 2026 | 2.4/2.5 の Woolworths 価格 |
| https://api.nandos.co.za/api/v2/pack/menu/default | 公式（Nando's SA） | 2026-10-17 | 2026 | 2.6 のメニュー価格 |
| https://www.mrd.com/help/faqs | 公式 | 2026-10-17 | 2026 | Mr D の Service Fee と最低注文額 |
| https://help.uber.com/en/ubereats/restaurants/article/what-fees-may-apply-to-my-order?nodeId=65d229e2-a2b4-4fa0-b10f-b36c9546cf55 | 公式（ただし日本向けとみられる） | 2026-10-17 | 2026 | 手数料の種類 |
| https://open.er-api.com/v6/latest/JPY | 参考（為替API） | 2026-10-17 | 2026-10-16 | ZAR、PHP の円換算 |

## 8. 調査ログ

検索（Brave の `search.brave.com/search?q=`。HTTP コード）
- 200 `PINES baguio weekend meal 179`
- 200 `hub1234 PINES 週末 食事 179`
- 429 `philschools PINES 週末 食事`、429 `PINES international academy weekend meal fee 179 pesos`、429 `philschools.jp PINES 料金 食事 週末`、429 `PINES Baguio official site weekend meals`、429 `philschools.jp PINES 週末 食事 179ペソ`
- 202（結果なし）DuckDuckGo html/lite `philschools PINES 週末 食事`、`PINES baguio weekend meal`。Bing は結果を抽出できなかった
- 200 `checkers.co.za Tastic Rice 2kg price`
- 429 `Nando's South Africa menu prices quarter chicken R`
- 429→200 `Uber Eats fees explained service fee small order fee delivery fee`
- 429 `Wing Hing supermarket Cape Town Asian`、429 `Japanese grocery Cape Town miso natto shop`
- 一括検索（12件中、確認時点で 1〜4件目は 429。5件目 `H&M South Africa stores...` のみ 200。その後の `Wing Hing Cape Town Asian supermarket address`、`Japanese food store Cape Town miso tofu`、`Good Taste restaurant Baguio menu prices`、`Oh My Gulay Baguio menu price`、`Cafe by the Ruins Baguio menu price`、`Hill Station Baguio menu price` は結果を確認できず、未確認扱い）

取得（主なもの）
- 404 https://hub1234.com/pines/ → 200 https://www.hub1234.com/philippines/baguio/pines-main
- 200 https://philschools.jp/school/pines/
- 404 https://www.checkers.co.za/search/all?q=rice、404 https://www.shoprite.co.za/search/all?q=rice、200（JS のみ）https://www.checkers.co.za/search?q=rice
- 403 https://www.checkers.co.za/api/catalogue/get-products-filter（POST）
- 200 Checkers と Shoprite の sitemap（seq_product-sitemap_00〜02）から商品URLを抽出 → 商品ページ約60件を取得（200）
- 200 https://www.pnp.co.za/main-L46UXSRH.js → PnP の検索 API を特定。GET は 400、POST + storeCode=WC21 で 200。GP21/GA21/KZ21 は 400、WC01/WC10 は 200
- 200 https://www.woolworths.co.za/cat?Ntt=rice（価格は含まれない）、301 /server/searchCategory、200 cnstrc.com の JS → 検索キーを特定 → ac.cnstrc.com を約40回検索（200）
- 200 https://www.nandos.co.za/eat/menu（JS）→ 200 api.nandos.co.za/api/v2/pack/menu/default、404 store.nandos.co.za
- 200 spur.co.za/menu（価格なし）、200 oceanbasket.com/za/menu（価格なし）、200 kauai.co.za/menu（価格なし。WebFetch でも確認）、200 steers.co.za/menu（価格なし）、403 mcdonalds.co.za/menu、000 kfc.co.za/menu
- 406 uber.com/za/en/eats/how-it-works（WebFetch では 404）、404 mrd.com/faq → 200 mrd.com/help/faqs（WebFetch）、200 uber.com/za/en/deliver（顧客向けの手数料なし）
- 200 foodpanda.ph/city/baguio、404 foodpanda.ph/city/baguio-city、200 → 2回目以降 "Access denied"（Lechon House）。GrabFood の検索結果は0件（WebFetch）。WebFetch で foodpanda は 403
- 000（接続不可）cafebytheruins.com、goodtastebaguio.com、ohmygulay.com、hillstationbaguio.com。200 hillstation.com.ph（リダイレクトのみ）
- 404 anzen.mofa.go.jp/info/pcsafetymeasure_136.html、200 pcsafetymeasure_174.html（南アではなかった）
- 200 open.er-api.com（為替）
