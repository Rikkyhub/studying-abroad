# route_points.csv

`data/route_points.csv` を表にした閲覧用のページです（21行 × 13列）。正本は CSV で、このファイルは `python3 scripts/build_html.py` が生成します。手で編集しないでください。

| id | name_ja | name_en | iata_or_code | country | lat | lon | kind | note | maps_query | world_pos | africa_pos | provisional |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MNL | マニラ | Manila Ninoy Aquino International Airport | MNL | フィリピン | 14.5086 | 121.0194 | airport | 出発地。各ルートはマニラ発として描く（バギオからマニラへの国内移動は描かない） | Ninoy Aquino International Airport | br | none | N |
| BAGUIO | バギオ | Baguio City |  | フィリピン | 16.4023 | 120.5960 | city | 留学地。マニラの北約200kmにあるためマニラ印に重ねて示す | Baguio City Philippines | tr | none | N |
| BKK | バンコク | Bangkok Suvarnabhumi Airport | BKK | タイ | 13.6900 | 100.7501 | airport | 乗継地は未確認。資料の例示（BKK/KUL/SIN等）から仮置き（ルートA） | Suvarnabhumi Airport | t | none | Y |
| KUL | クアラルンプール | Kuala Lumpur International Airport | KUL | マレーシア | 2.7456 | 101.7099 | airport | 乗継地は未確認。資料の例示から仮置き（ルートC） | Kuala Lumpur International Airport | bl | none | Y |
| SIN | シンガポール | Singapore Changi Airport | SIN | シンガポール | 1.3644 | 103.9915 | airport | 乗継地は未確認。資料の例示から仮置き（ルートD・E） | Singapore Changi Airport | br | none | Y |
| DXB | ドバイ | Dubai International Airport | DXB | アラブ首長国連邦 | 25.2532 | 55.3657 | airport | 湾岸の乗継地は未確認。Issue記載の候補から仮置き（ルートB） | Dubai International Airport | t | tl | Y |
| NBO | ナイロビ | Nairobi Jomo Kenyatta International Airport | NBO | ケニア | -1.3192 | 36.9278 | airport | A・Eの拠点。ケニア入国はeTA | Jomo Kenyatta International Airport | tl | tl | N |
| SERENGETI | セレンゲティ | Serengeti National Park |  | タンザニア | -2.3333 | 34.8333 | park | 北部サファリの候補地 | Serengeti National Park | dot | l | N |
| NGORONGORO | ンゴロンゴロ | Ngorongoro Conservation Area |  | タンザニア | -3.1667 | 35.5833 | park | 北部サファリの候補地 | Ngorongoro Conservation Area | dot | bl | N |
| ADD | アディスアベバ | Addis Ababa Bole International Airport | ADD | エチオピア | 8.9779 | 38.7993 | airport | 空港乗継のみ。市内滞在・北部は対象外 | Addis Ababa Bole International Airport | t | r | N |
| TNR | アンタナナリボ | Antananarivo Ivato International Airport | TNR | マダガスカル | -18.7969 | 47.4788 | airport | マダガスカルの玄関口。入国条件は要確認 | Ivato International Airport Antananarivo | r | r | N |
| DAR | ダルエスサラーム | Dar es Salaam Julius Nyerere International Airport | DAR | タンザニア | -6.8781 | 39.2026 | airport | Cの東アフリカ側の起点 | Julius Nyerere International Airport | r | r | N |
| LUN | ルサカ | Lusaka Kenneth Kaunda International Airport | LUN | ザンビア | -15.3308 | 28.4526 | airport | DARからの航空の到着地 | Kenneth Kaunda International Airport | dot | tl | N |
| LIVINGSTONE | リビングストン | Livingstone |  | ザンビア | -17.8419 | 25.8543 | city | ビクトリアフォールズのザンビア側の町 | Livingstone Zambia | dot | l | N |
| VICFALLS | ビクトリアフォールズ | Victoria Falls |  | ジンバブエ | -17.9243 | 25.8572 | border | ザンビア側との間は橋の国境（リビングストンに隣接） | Victoria Falls Bridge border post | dot | br | N |
| CHOBE | チョベ | Chobe National Park Kasane |  | ボツワナ | -17.7978 | 25.1500 | park | カズングラ国境の近く。野生動物と国境の渋滞に注意 | Chobe National Park | dot | bl | N |
| JNB | ヨハネスブルグ | Johannesburg O.R. Tambo International Airport | JNB | 南アフリカ | -26.1392 | 28.2460 | airport | 南アの玄関口。Cの終点 | O.R. Tambo International Airport | tl | tr | N |
| CPT | ケープタウン | Cape Town International Airport | CPT | 南アフリカ | -33.9715 | 18.6021 | airport | 終点（A・B・E）。第2か国留学の候補地 | Cape Town International Airport | l | l | N |
| KRUGER | クルーガー | Kruger National Park |  | 南アフリカ | -23.9900 | 31.5500 | park | 資料の地図リンクに掲載。どのルートにも入れていない | Kruger National Park | dot | r | N |
| MRU | モーリシャス | Mauritius Sir Seewoosagur Ramgoolam International Airport | MRU | モーリシャス | -20.4302 | 57.6836 | airport | 接続・費用は未確認（ルートD） | Sir Seewoosagur Ramgoolam International Airport | dot | tr | N |
| SEZ | セーシェル | Seychelles International Airport | SEZ | セーシェル | -4.6743 | 55.5218 | airport | 接続・費用は未確認（ルートD） | Seychelles International Airport | dot | tr | N |
