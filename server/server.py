import threading
from http.server import HTTPServer
from time import sleep

from configuration.configuration import Configuration
from file_searcher.file_searcher import FileSearcher
from logger.logger import logger
from server.handler import Handler


class Server(HTTPServer):

    def __init__(self, configuration: Configuration, handler: Handler = None):
        super().__init__((configuration.get_property("server.host"),
                          configuration.get_property("server.port")),
                         handler)
        self.configuration = configuration
        self.file_searcher = FileSearcher()
        self.running = False

    def start(self):
        if self.running:
            raise SystemError("Can not start server since it is already running!")
        self.running = True
        threading.Thread(target=self._dummy_get).start()
        self.serve_forever()

    def get_json_with_id(self, uuid: str) -> list:
        final_jsons = list()
        files = self.file_searcher.get_files_by_regex(self.configuration.get_property("dr.path"))
        for file in files:
            final_jsons.extend(self._search_jsons_for_id(self.file_searcher.file_to_jsons(file), uuid))
        return final_jsons

    @staticmethod
    def _search_jsons_for_id(jsons: list, uuid: str) -> list:
        final_jsons = list()
        for json in jsons:
            if "messageId" in json and json['messageId'] == uuid:
                final_jsons.append(json)
        return final_jsons

    def _dummy_get(self):
        while self.running:
            logger.info("Running dummy get to refresh!")
            self.get_json_with_id("random_id")
            sleep(10)
