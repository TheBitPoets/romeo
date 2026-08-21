import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"status": "ok"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

server = HTTPServer(("127.0.0.1", 0), Handler)
thread = threading.Thread(target=server.handle_request)
thread.start()
with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/status") as response:
    assert response.status == 200
    assert json.load(response)["status"] == "ok"
thread.join()
server.server_close()
print("HTTP 200 OK")
