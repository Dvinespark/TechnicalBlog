#  This file will hold all the necessary db actions that need to be performed
from config import db_connection_string, db_credentials
import pymongo


class MongoDB:
    """
    Base class for initializing mongo db access parameters
    """
    def __init__(self):
        self._initialize_connection_parameters()
        try:
            self.mongo_client = pymongo.MongoClient(self.connection_string)
            self._db = self.mongo_client[self.database_name]
        except Exception as e:
            print(f"Could not connect to the string -> {self.connection_string}")
            pass

    def _initialize_connection_parameters(self):
        # get connection strings from some setting files
        self.connection_string = db_connection_string
        self.database_name = db_credentials["db_name"]
        self.mongo_client = None
        self.db_collection = None

    def get_collection(self, collection_name=None):
        return self._db[collection_name]