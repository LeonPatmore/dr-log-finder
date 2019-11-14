import threading
from http.server import HTTPServer
from time import sleep

from configuration.configuration import Configuration
from file_searcher.file_searcher import FileSearcher
from logger.logger import logger
from mongodb.mongo_client import MongoClient
from server.handler import Handler


class Server(HTTPServer):

    def __init__(self, configuration: Configuration, handler: Handler = None):
        super().__init__((configuration.get_property("server.host"),
                          configuration.get_property("server.port")),
                         handler)
        self.file_searcher = FileSearcher(True, False)
        self.running = False
        self.dr_collection = MongoClient(configuration.get_property("mongo.host"),
                                         (int)(configuration.get_property("mongo.port")))\
            .get_database(configuration.get_property("mongo.database")) \
            .get_collection(configuration.get_property("mongo.collection.drs"))
        self.dr_collection.create_index("messageId")
        self.dr_path = configuration.get_property("dr.path")

    def start(self):
        if self.running:
            raise SystemError("Can not start server since it is already running!")
        self.running = True
        threading.Thread(target=self._schedule_refresh_drs).start()
        self.serve_forever()

    def safe_insert(self, json):
        if 'messageId' in json and len(self.get_json_with_id(json['messageId'])) == 0:
            self.dr_collection.insert(json)

    def get_json_with_id(self, uuid: str) -> list:
        self._refresh_drs()
        return self.dr_collection.query({"messageId": uuid}, True)

    def _refresh_drs(self):
        files = self.file_searcher.get_files_by_regex(self.dr_path)
        for file in files:
            jsons = self.file_searcher.file_to_jsons(file)
            for json in jsons:
                self.safe_insert(json)

    def _schedule_refresh_drs(self):
        while self.running:
            logger.info("Running DR refresh!")
            self._refresh_drs()
            sleep(10)
