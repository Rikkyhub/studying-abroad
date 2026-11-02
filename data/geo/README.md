# 地図の元データ（data/geo）

`scripts/build_maps.py` が読む国境ポリゴン。ビルド時にネットワークは使いません。

| ファイル | 内容 | 用途 |
|---|---|---|
| `countries-110m.json` | 国境 1:110m（TopoJSON） | 世界地図 |
| `countries-50m.json` | 国境 1:50m（TopoJSON） | アフリカ地図（海岸線が細かい） |

- 取得元：npm パッケージ [world-atlas](https://github.com/topojson/world-atlas) **2.0.2**（`https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json` ほか）
- 元データ：[Natural Earth](https://www.naturalearthdata.com/)（パブリックドメイン）。world-atlas のパッケージ自体は ISC ライセンス。
- 更新する場合は上記URLから取り直してこのフォルダに置き、`py scripts/build_maps.py` を実行する。国境線は各国の公式な主張を表すものではなく、概念図としての利用に限る。
