# database/mongodb.py
import pymongo
import pandas as pd

class MongoDB:
    def __init__(self, connection_string = 'mongodb://localhost:27017', database_name = 'rs_db'):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        collection = self.db[collection_name]  
        cursor = collection.find({})
        df = pd.DataFrame(list(cursor))
        return df
