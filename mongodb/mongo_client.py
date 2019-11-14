import pymongo

from mongodb.mongo_database import MongoDatabase


class MongoClient(object):

    def __init__(self, host: str, port: int):
        self.client = pymongo.MongoClient(self.get_mongo_db_uri(host, port))

    @staticmethod
    def get_mongo_db_uri(host: str, port: int) -> str:
        return "mongodb://{}:{}/".format(host, port)

    def get_database(self, database_name) -> MongoDatabase:
        return MongoDatabase(self, database_name)
