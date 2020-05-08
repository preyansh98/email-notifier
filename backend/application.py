from flask import Flask, request, Response, redirect
from pymongo import MongoClient
from google_auth import *
from db import initialize_and_return_db_client
import json
import os

# Initiate application
application = Flask(__name__)

# Database
client = initialize_and_return_db_client()
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


# OAuth Routes

# OAuth init
@application.route('/oauth-start', methods = ['GET'])
def init_oauth():
    auth_url = initialize_google_oauth()
    return redirect(auth_url)

# OAuth Callback
# Let state identify the user
@application.route('/oauth-callback', methods=['GET'])
def oauth_callback(): 
    email = get_credentials_on_callback()
    r_uri = "oauth-complete/email="+email
    return redirect(r_uri,code=302)
    
# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)