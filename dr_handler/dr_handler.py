import json

from logger.logger import logger
from server.handler import Handler


class DRHandler(Handler):

    def do_GET(self):
        uuid = self.clean_path()
        logger.info("Searching for DR log with ID [ {} ]".format(uuid))
        self.send_response(202)
        self.send_header(Handler.CONTENT_TYPE_HEADER, Handler.CONTENT_TYPE_JSON)
        self.end_headers()
        self.wfile.write(json.dumps(self.get_server().get_json_with_id(uuid)).encode('utf-8'))
