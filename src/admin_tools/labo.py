"""Services éphémères locaux : vrais échanges HTTP/SMTP, données simulées."""

import json
import socket
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from aiosmtpd.controller import Controller

from admin_tools.chemins import DONNEES


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path)
        if route.path == "/machines":
            data = (DONNEES / "machines.html").read_bytes()
            status, content_type = 200, "text/html; charset=utf-8"
        elif route.path == "/geo":
            ip = parse_qs(route.query).get("ip", [""])[0]
            data = json.dumps(
                {"status": "success", "country": "Pays fictif", "city": "Ville témoin", "query": ip}
            ).encode()
            status, content_type = 200, "application/json"
        elif route.path == "/absent":
            data = b'{"status":"fail"}'
            status, content_type = 200, "application/json"
        elif route.path == "/invalide":
            data, status, content_type = b"pas du JSON", 200, "application/json"
        else:
            data, status, content_type = b"indisponible", 503, "text/plain"
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # Accès HTTP ordinaires, pas des avertissements masqués.


@contextmanager
def serveur_http():
    serveur = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=serveur.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{serveur.server_port}"
    finally:
        serveur.shutdown()
        serveur.server_close()
        thread.join(timeout=3)


class Capture:
    def __init__(self):
        self.messages = []

    async def handle_DATA(self, server, session, envelope):
        self.messages.append(envelope.content)
        return "250 Message capturé dans le laboratoire"


@contextmanager
def serveur_smtp():
    capture = Capture()
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    controleur = Controller(capture, hostname="127.0.0.1", port=port)
    controleur.start()
    try:
        yield port, capture
    finally:
        controleur.stop()
