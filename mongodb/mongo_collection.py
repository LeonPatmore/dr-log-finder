class MongoCollection(object):

    def __init__(self, mongo_database, collection_name: str):
        self.collection = mongo_database.database[collection_name]

    def insert(self, document: dict):
        self.collection.insert_one(document)

    def query(self, filter_: dict, sanitise: bool=False) -> list:
        result_list = list(self.collection.find(filter=filter_))
        if sanitise is True:
            for result in result_list:
                del result['_id']
        return result_list

    def create_index(self, index: str):
        self.collection.create_index(index)
