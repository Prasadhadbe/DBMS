from pymongo import MongoClient
from bson import ObjectId

class MongoDB:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, data):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def read_document(self, document_id):
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        return document

    def update_document(self, document_id, data):
        result = self.collection.update_one({"_id": ObjectId(document_id)}, {"$set": data})
        return result.modified_count

    def delete_document(self, document_id):
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count
