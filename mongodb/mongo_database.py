from mongodb.mongo_collection import MongoCollection


class MongoDatabase(object):

    def __init__(self, mongo_client, database_name: str):
        self.database = mongo_client.client[database_name]

    def get_collection(self, collection_name: str) -> MongoCollection:
        return MongoCollection(self, collection_name)
