from flask import Flask, request, Response, redirect
from pymongo import MongoClient
from google_auth import *
from multiprocessing import Process
from job_handler import run_jobs
from db import initialize_and_return_db_client
import json, os, threading

# Initiate application
application = Flask(__name__)

# Database
client = initialize_and_return_db_client()
profile_collection = client['notifier-db']['profiles']

# Define classes
class UserProfile():
    name = ""
    phone = ""
    gmail = ""
    emails = set()
    options_call = False
    options_sms = False

    def __init__(self, name, phone, gmail, emails, options_call, options_sms): 
        self.name = name
        self.phone = phone
        self.gmail = gmail
        self.emails = set(emails) 
        self.options_call = options_call
        self.options_sms = options_sms

    def validate_profile(self):
        return (len(self.name) > 0 and len(self.phone) > 0 and len(self.gmail) > 0
                and len(self.emails) > 0 and (self.options_call or self.options_sms))

# Globals

user_creds = dict()
FRONTEND_URI = "http://localhost:3000"

# ENDPOINTS-------------------------------------------------

# User Endpoints
@application.route('/create-profile', methods=['POST'])
def create_profile_and_run_job():
    req_data = request.get_json()
    
    name = req_data['name']
    phone = req_data['phone']
    gmail = req_data['gmail']
    emails = req_data['emails']
    options_sms = req_data['options']['sms']
    options_call = req_data['options']['call']

    profile = UserProfile(name,phone,gmail, emails, options_call,options_sms)
    
    if profile.validate_profile() is False:
        return {"error" : "Profile is not valid"}, 400

    status = ''
    # status = start_job(profile)

    return  {'status': status}, 200 

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
    # r_uri = "oauth-complete/email="+email
    r_uri = FRONTEND_URI+"/oauth-complete?email="+email
    return redirect(r_uri,code=302)
    
# Run server
def start_web_server():
    application.run(debug=True)
    
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    web_server_process = Process(target = start_web_server)
    job_process = Process(target = run_jobs)

    web_server_process.start()
    job_process.start()
