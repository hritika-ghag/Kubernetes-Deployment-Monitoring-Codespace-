#!/usr/bin/env python3
"""
Tiny HTTP app using only Python stdlib.
Endpoints:
  /         -> returns a greeting
  /ping     -> returns JSON-like ok
  /healthz  -> returns healthy (used by probes)
  /metrics  -> returns simple Prometheus-format metrics
Listens on port 8080 by default.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import threading

HOST = "0.0.0.0"
PORT = 8080

# Simple in-memory metrics (not persistent across restarts)
_metrics_lock = threading.Lock()
_metrics = {
    "requests_total": 0,
    "errors_total": 0,
    "last_request_latency_seconds": 0.0
}

class SimpleHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        start = time.time()
        try:
            if self.path == "/" or self.path.startswith("/?"):
                self._ok_text("Hello from my zero-dependency K8s test app!")
            elif self.path == "/ping":
                self._ok_json({"status": "ok"})
            elif self.path == "/healthz":
                self._ok_text("healthy")
            elif self.path == "/metrics":
                self._ok_text(self._render_metrics(), content_type="text/plain; version=0.0.4")
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"not found")
                with _metrics_lock:
                    _metrics["errors_total"] += 1
                return
        except Exception:
            with _metrics_lock:
                _metrics["errors_total"] += 1
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"internal error")
            return
        finally:
            latency = time.time() - start
            with _metrics_lock:
                _metrics["requests_total"] += 1
                _metrics["last_request_latency_seconds"] = latency

    def log_message(self, format, *args):
        # reduce noise in stdout — still useful to see basic logs in container
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

    def _ok_text(self, text, content_type="text/plain; charset=utf-8"):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _ok_json(self, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _render_metrics(self):
        # Manual Prometheus text exposition (very small subset)
        with _metrics_lock:
            reqs = _metrics["requests_total"]
            errs = _metrics["errors_total"]
            lat = _metrics["last_request_latency_seconds"]
        lines = [
            "# HELP myk8sapp_requests_total Total requests received by the app",
            "# TYPE myk8sapp_requests_total counter",
            f"myk8sapp_requests_total {reqs}",
            "# HELP myk8sapp_errors_total Total errors encountered",
            "# TYPE myk8sapp_errors_total counter",
            f"myk8sapp_errors_total {errs}",
            "# HELP myk8sapp_last_request_latency_seconds Latency of last request in seconds",
            "# TYPE myk8sapp_last_request_latency_seconds gauge",
            f"myk8sapp_last_request_latency_seconds {lat:.6f}",
            ""
        ]
        return "\n".join(lines)

def run():
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f"Starting server at http://{HOST}:{PORT}  (endpoints: /, /ping, /healthz, /metrics)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        server.server_close()

if __name__ == "__main__":
    run()
