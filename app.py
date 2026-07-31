import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from test_agent import generate_dummy_items

DATA_FILE = Path(__file__).with_name("data.json")


class ItemHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/items":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        try:
            items = generate_dummy_items()

            if not isinstance(items, list):
                raise ValueError("The JSON file must contain a list of items")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(items).encode("utf-8"))
        except Exception as exc:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(("127.0.0.1", 8000), ItemHandler)
    print("API running at http://127.0.0.1:8000/items")
    server.serve_forever()


if __name__ == "__main__":
    main()
