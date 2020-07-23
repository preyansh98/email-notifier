# Mongo DB Implementation
from pymongo import MongoClient
import os 

client = None

def initialize_and_return_db_client():
    global client
    if client is not None:
        return client

    mongo_str = os.getenv('mongo_str')
    
    if mongo_str:
        client = MongoClient(mongo_str)

    return client 