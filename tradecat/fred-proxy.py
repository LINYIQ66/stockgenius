#!/usr/bin/env python3
"""Simple FRED CSV proxy - returns JSON without API key"""
import json, sys, urllib.request, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

SERIES_MAP = {
    'FEDFUNDS': {'name': '联邦基金利率', 'unit': '%'},
    'CPIAUCSL': {'name': 'CPI', 'unit': ''},
    'UNRATE': {'name': '失业率', 'unit': '%'},
    'GDP': {'name': 'GDP', 'unit': '十亿美元'},
    'T10Y2Y': {'name': '10Y-2Y利差', 'unit': '%'},
    'DCOILWTICO': {'name': 'WTI原油', 'unit': '美元/桶'},
    'VIXCLS': {'name': 'VIX', 'unit': ''},
    'DEXCHUS': {'name': 'USD/CNY', 'unit': ''},
    'WM2NS': {'name': 'M2货币供应', 'unit': '十亿美元'},
    'ICSA': {'name': '初请失业金', 'unit': '千人'},
    'CSUSHPINSA': {'name': '房价指数', 'unit': ''},
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        series_id = params.get('series_id', [''])[0].upper()
        if series_id not in SERIES_MAP:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Unknown series'}).encode())
            return
        try:
            url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10)
            lines = resp.read().decode().strip().split('\n')
            observations = []
            for line in lines[1:]:  # skip header
                parts = line.split(',')
                if len(parts) == 2 and parts[1] != '.':
                    observations.append({'date': parts[0], 'value': parts[1]})
            meta = SERIES_MAP[series_id]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'series_id': series_id,
                'name': meta['name'],
                'unit': meta['unit'],
                'observations': observations[-1:]  # latest only
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        pass  # suppress logs

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8945
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'FRED proxy on :{port}')
    server.serve_forever()
