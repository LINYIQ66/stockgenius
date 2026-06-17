#!/bin/bash
OUT="/var/www/html/tradecat/fred-data.json"
echo '{"series":{' > "$OUT.tmp"
FIRST=1

fetch_series() {
  local sid=$1
  local url="https://fred.stlouisfed.org/graph/fredgraph.csv?id=$sid&cosd=2025-01-01"
  local csv=$(curl -s --max-time 15 "$url" 2>/dev/null)
  if [ -n "$csv" ]; then
    local last=$(echo "$csv" | tail -1)
    local date=$(echo "$last" | cut -d, -f1)
    local value=$(echo "$last" | cut -d, -f2)
    if [ "$value" != "." ] && [ -n "$value" ]; then
      if [ $FIRST -eq 0 ]; then echo ',' >> "$OUT.tmp"; fi
      echo "\"$sid\":{\"value\":\"$value\",\"date\":\"$date\"}" >> "$OUT.tmp"
      FIRST=0
    fi
  fi
}

for sid in DFF CPIAUCSL UNRATE GDP T10Y2Y DCOILWTICO VIXCLS DEXCHUS M2SL ICSA CSUSHPINSA; do
  fetch_series "$sid"
  sleep 1
done

echo '}}' >> "$OUT.tmp"
mv "$OUT.tmp" "$OUT"
echo "Done: $(wc -c < "$OUT") bytes"
