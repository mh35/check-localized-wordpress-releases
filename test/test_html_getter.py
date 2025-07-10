"""Test for html_getter module."""

import os
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Self

from check_localized_wordpress_releases.html_getter import fetch_html


TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), "assets", "en_releases.html")


class TestHTTPRequestHandler(BaseHTTPRequestHandler):
    """Test HTTP request handler for serving dummy HTML."""

    def do_GET(self: Self) -> None:
        """Handle GET request."""
        with open(TEST_FILE_PATH, "rb") as fp:
            content = fp.read()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_HEAD(self: Self) -> None:
        """Handle HEAD request."""
        with open(TEST_FILE_PATH, "rb") as fp:
            content = fp.read()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()


def run_server(server: HTTPServer) -> None:
    """Run server.

    Args:
        server(HTTPServer): HTTP server
    """
    server.serve_forever()


def test_fetch_html() -> None:
    """Test fetch_html fuction."""
    server = HTTPServer(('127.0.0.1', 28080), TestHTTPRequestHandler)
    with ThreadPoolExecutor() as executor:
        executor.submit(run_server, server)
        res = fetch_html("http://127.0.0.1:28080/")
        try:
            assert res.attrib["lang"] == "en-US"
        finally:
            server.shutdown()
