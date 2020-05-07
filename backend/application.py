from flask import Flask, request, Response
from pymongo import MongoClient
from google_auth import get_credentials
import json
import os

# Initiate application
application = Flask(__name__)

# Database
#mongo_str = os.getenv('mongostr')
mongo_str = "mongodb+srv://admin:adminpassword@email-notifier-db-snhkt.azure.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(mongo_str)
profile_collection = client['notifier-db']['profiles']

# Define classes
class UserProfile():
    name = ""
    gmail = ""
    emails = set()

    def __init__(self, name, gmail, emails): 
        self.name = name
        self.gmail = gmail
        self.emails = set(emails) 

# Globals

user_creds = dict()

# ENDPOINTS-------------------------------------------------

# User Endpoints
@application.route('/create-profile', methods=['POST'])
def create_profile_and_run_job():
    req_data = request.get_json()
    
    name = req_data['name']
    gmail = req_data['gmail']
    emails = req_data['emails']

    

    return  {'token': str(name)}, 200 

@application.route('/', methods=['GET'])
def say_hello():
    return {'message':'hello'}, 200


# OAuth Callback

# Let state identify the user
@application.route('/oauth-callback', methods=['GET'])
def oauth_callback(): 
    oauth_code = request.args['code']
    state = request.args['state']
    credentials = get_credentials(oauth_code, state, client)
    user_creds[state] = credentials
    
# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)