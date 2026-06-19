import http.server
import json
import os
import urllib.parse

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
PORT = 8000

# ── Ensure data.json exists ──────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Request handler ──────────────────────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        # Suppress noisy request logs; only print errors
        pass

    def send_json(self, code, obj):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # GET /data?key=some_key  →  { value: <stored value or null> }
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/data':
            params = urllib.parse.parse_qs(parsed.query)
            key = params.get('key', [None])[0]
            if not key:
                return self.send_json(400, {'error': 'missing key'})
            data = load_data()
            self.send_json(200, {'value': data.get(key, None)})

        else:
            # Serve static files (HTML, CSS, JS, etc.)
            super().do_GET()

    # POST /data  body: { key, value }  →  { ok: true }
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/data':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                return self.send_json(400, {'error': 'invalid JSON'})

            key = payload.get('key')
            if not key:
                return self.send_json(400, {'error': 'missing key'})

            data = load_data()

            if payload.get('delete') is True:
                data.pop(key, None)
            else:
                data[key] = payload.get('value')

            save_data(data)
            self.send_json(200, {'ok': True})

        else:
            self.send_json(404, {'error': 'not found'})


if __name__ == '__main__':
    # Make sure data.json exists on first run
    if not os.path.exists(DATA_FILE):
        save_data({})
        print(f'  Created data.json')

    server = http.server.HTTPServer(('localhost', PORT), Handler)
    print(f'')
    print(f'  Planner running →  http://localhost:{PORT}/index.html')
    print(f'  Press Ctrl+C to stop.')
    print(f'')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped.')
