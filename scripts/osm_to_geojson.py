"""raw/osm_highways_raw.json (Overpass out geom) -> processed/campus_paths.geojson
CRS: 入出力とも WGS84 (EPSG:4326)、座標順は [lon, lat]。変換なし。
オーバーレイ対象: Mapbox 標準スタイルで描かれにくい細道 (footway/path/pedestrian/steps/cycleway/track)
と service、および access=private の全道路。
データ © OpenStreetMap contributors (ODbL)
"""
import json, sys

BBOX = (139.393, 35.558, 139.413, 35.575)  # w,s,e,n
DETAIL = {"footway", "path", "pedestrian", "steps", "cycleway", "track", "service"}
KEEP = ("highway", "name", "access", "foot", "surface", "service", "footway", "tunnel", "bridge", "indoor", "layer")

raw = json.load(open("raw/osm_highways_raw.json"))
feats, skipped = [], {"short": 0, "oob": 0, "not_target": 0, "indoor": 0}
for e in raw["elements"]:
    t = e.get("tags", {})
    if not (t.get("highway") in DETAIL or t.get("access") == "private"):
        skipped["not_target"] += 1
        continue
    if t.get("indoor"):  # 屋内通路は地図オーバーレイから除外
        skipped["indoor"] += 1
        continue
    coords = [[p["lon"], p["lat"]] for p in e.get("geometry", [])]
    if len(coords) < 2:
        skipped["short"] += 1
        continue
    if any(not (BBOX[0] <= x <= BBOX[2] and BBOX[1] <= y <= BBOX[3]) for x, y in coords):
        # bbox を少しはみ出す way は許容 (Overpass は bbox 交差 way を全長で返す)。極端値のみ除外
        if any(not (130 < x < 145 and 30 < y < 40) for x, y in coords):
            skipped["oob"] += 1
            continue
    props = {k: t[k] for k in KEEP if k in t}
    props["osm_id"] = e["id"]
    feats.append({"type": "Feature", "properties": props, "geometry": {"type": "LineString", "coordinates": coords}})

out = {"type": "FeatureCollection", "features": feats,
       "metadata": {"source": "OpenStreetMap via Overpass API", "license": "ODbL",
                    "attribution": "© OpenStreetMap contributors", "crs": "EPSG:4326",
                    "osm_base": raw.get("osm3s", {}).get("timestamp_osm_base")}}
json.dump(out, open("processed/campus_paths.geojson", "w"), ensure_ascii=False, separators=(",", ":"))
# file:// で index.html を直接開くと fetch(GeoJSON) が CORS で失敗するため、<script> で読める JS 版も出力する
with open("processed/campus_paths.js", "w") as f:
    f.write("// 自動生成: scripts/osm_to_geojson.py / © OpenStreetMap contributors (ODbL)\nwindow.CAMPUS_PATHS = ")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

from collections import Counter
print("input ways:", len(raw["elements"]), "-> output features:", len(feats), "skipped:", skipped)
print(Counter(f["properties"]["highway"] for f in feats).most_common())
print("access=private:", sum(1 for f in feats if f["properties"].get("access") == "private"))
xs = [c[0] for f in feats for c in f["geometry"]["coordinates"]]; ys = [c[1] for f in feats for c in f["geometry"]["coordinates"]]
print("bbox:", round(min(xs), 5), round(min(ys), 5), round(max(xs), 5), round(max(ys), 5))
