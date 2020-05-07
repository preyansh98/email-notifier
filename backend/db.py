# Mongo DB Implementation
from pymongo import MongoClient
import os 

client = None

def initialize_and_return_db_client():
    if client is not None:
        return client

    mongo_str = "mongodb+srv://admin:adminpassword@email-notifier-db-snhkt.azure.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(mongo_str)

    return client 