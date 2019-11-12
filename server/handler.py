from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):

    CONTENT_TYPE_HEADER = "Content-Type"
    CONTENT_TYPE_JSON = "application/json"

    def do_GET(self):
        return self.send_error(404)

    def do_POST(self):
        return self.send_error(404)

    def get_server(self):
        return self.server

    def clean_path(self) -> str:
        if self.path.startswith("/"):
            return self.path[1:]
        return self.path
