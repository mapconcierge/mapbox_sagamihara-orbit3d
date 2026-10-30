#!/bin/sh
# OSM (Overpass API) から相模原キャンパス周辺の highway を取得して raw/ に保存する。
# bbox は s,w,n,e (WGS84 / EPSG:4326)。データ © OpenStreetMap contributors (ODbL)
BBOX="${BBOX:-35.558,139.393,35.575,139.413}"
curl -sS --fail -G "https://overpass-api.de/api/interpreter" \
  -A "furuhashi-lab-orbit3d/0.1 (research; taichi@gs.gsc.aoyama.ac.jp)" \
  -H "Accept: */*" \
  --data-urlencode "data=[out:json][timeout:60];way[\"highway\"]($BBOX);out geom tags;" \
  -o raw/osm_highways_raw.json
