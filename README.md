# 相模原キャンパス 3D オービット / Sagamihara Campus 3D Orbit

## 概要 / Overview

**日本語**
青山学院大学 相模原キャンパスを Mapbox GL JS（Standard スタイル + 地形）で 3D 表示し、中心を固定したオービットカメラで回転させる Web 地図です。
Mapbox のベースマップに描かれていない私道・歩道などの小道を、OpenStreetMap（OSM）由来のデータでオーバーレイして補っています。

- 小道データ源は切り替え可能です。
  - **OpenFreeMap（既定）**: ベクタータイルを表示範囲だけリアルタイム取得（bbox の制限なし）
  - **OSM 事前取得（Overpass API）**: `processed/campus_paths.*`。取得範囲外は描画不可
- 回転速度・ピッチ・ズーム・スタイル（Standard / Standard Satellite / Satellite Streets）をパネルで変更できます。

**English**
A Mapbox GL JS 3D view of Aoyama Gakuin University's Sagamihara campus with an orbiting camera.
Footways, private roads and other small paths that the Mapbox basemap does not draw are overlaid from OpenStreetMap,
either live from OpenFreeMap vector tiles (default) or from a pre-downloaded Overpass extract.

## 使い方 / Usage

1. Mapbox の **public token（`pk.`）** を用意します（`sk.` は使わない）。
2. `config.example.js` を `config.js` にコピーしてトークンを設定します（`config.js` は `.gitignore` 済み）。
   ```js
   window.MAPBOX_TOKEN = "pk.xxxxxxxx";
   ```
   一時的には URL パラメータ `?token=pk.…` でも指定できます。
3. ローカルで開きます（`file://` でも動作しますが、HTTP サーバー経由を推奨）。
   ```sh
   python3 -m http.server 8765   # → http://127.0.0.1:8765/index.html
   ```

### 事前取得データの再生成 / Rebuilding the OSM extract

```sh
./scripts/fetch_osm_highways.sh      # Overpass API → raw/osm_highways_raw.json（BBOX 環境変数で範囲変更可）
python3 scripts/osm_to_geojson.py    # → processed/campus_paths.geojson / .js
```

- `raw/` は取得した原本、`processed/` は加工後です。元データは上書きしません。
- 座標系はすべて WGS84（EPSG:4326）、変換はありません。
- 取得日時の目安: OSM 基準時刻 2026-10-30 05:28 UTC（`processed/campus_paths.geojson` の `metadata.osm_base`）。
- 私道は OSM では `access=private` で表されます（`highway=private` という値は存在しません）。

### GitHub Pages で公開する / Deploying to GitHub Pages

`.github/workflows/pages.yml` が `main` への push で自動デプロイします。

1. リポジトリを作成して push（**公開前にトークンの URL 制限を必ず設定**）。
2. Mapbox アカウントの [Access tokens](https://account.mapbox.com/access-tokens/) で、公開用の public token に URL 制限
   `https://<user>.github.io/<repo>/*` を設定。
3. Settings → Secrets and variables → Actions に `MAPBOX_PUBLIC_TOKEN` を登録。
4. Settings → Pages → Source を **GitHub Actions** に設定。

公開ページの `config.js` からトークンは誰でも読めます。public token はそういう前提の設計ですが、URL 制限なしでは他サイトに流用されて課金される恐れがあります。

## データソース・ライセンス / Data sources & Licenses

| 対象 | ライセンス / 出典 |
|---|---|
| コード（`index.html`, `scripts/`） | CC0 1.0（`LICENSE`） |
| OSM データ（`raw/`, `processed/`） | © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), **ODbL 1.0**。利用時は帰属表示が必要（画面右下に表示） |
| ベクタータイル（小道・既定） | [OpenFreeMap](https://openfreemap.org) © [OpenMapTiles](https://www.openmaptiles.org/) / Data from OpenStreetMap |
| ベースマップ・地形・衛星画像 | © Mapbox, © OpenStreetMap, Maxar（Mapbox 利用規約に従う） |

OpenFreeMap は無料の公開サービスです。大量アクセスや商用での継続利用には向きません。

## 既知の制限・記録 / Known limitations & notes

- OpenFreeMap のタイルは最大ズーム 14 で、ズーム 17 では拡大表示のため線形がやや粗くなります。
- OpenMapTiles は元の OSM より収録する道が少なく、小さな道が欠ける場合があります。必要なら「OSM 事前取得」に切り替えてください。
- Overpass API は User-Agent / Accept ヘッダーが無いと HTTP 406 を返します（`scripts/fetch_osm_highways.sh` に反映済み）。
- `file://` で開くと GeoJSON の `fetch` が失敗するため、`processed/campus_paths.js`（`<script>` 読み込み）を併せて出力しています。
- Mapbox GL JS は v3.21.0 以降で `.pmtiles` の vector ソースを直接読めます。本プロジェクトの OpenFreeMap は XYZ 配信のため未使用です。
- 動作確認はソフトウェア描画のヘッドレス Chrome で行いました。実機 GPU・各ブラウザでの確認は未実施です。

## 著者 / Author

古橋研究室 (Furuhashi Lab), 青山学院大学 地球社会共生学部 / Aoyama Gakuin University, School of Global Studies and Collaboration

## 関連リンク / Links

- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- [Mapbox GL JS — Add a PMTiles vector source](https://docs.mapbox.com/mapbox-gl-js/example/pmtiles-vector-source/)
- [OpenFreeMap](https://openfreemap.org)
- [OpenStreetMap](https://www.openstreetmap.org)
- Medium 記事・発表資料: （未作成）
