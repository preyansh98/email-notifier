import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from pymongo import MongoClient
from db import initialize_and_return_db_client

# Statics

CLIENTSECRETS_LOCATION = 'creds/client_secret.json'
REDIRECT_URI = 'http://localhost:5000/oauth-callback'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Db Access
client = initialize_and_return_db_client()
creds_collection = client['notifier-db']['usercreds']


# Initialize GAuth Flow
def initialize_google_oauth():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENTSECRETS_LOCATION,
    SCOPES
  )
  flow.redirect_uri = REDIRECT_URI

  authorization_url, state = flow.authorization_url(
    #Need offline access for job processing
    access_type = 'offline',
    # TODO: add state to represent user id. 
    include_granted_scopes = 'true'
  )

  return authorization_url


# Callback, Exchange code for token
def get_credentials_on_callback():
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENTSECRETS_LOCATION,
      scopes=SCOPES, 
      state=state)

  flow.redirect_uri = REDIRECT_URI

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  user_id = credentials.id_token.email
  store_credentials_in_db(user_id, credentials_to_dict(credentials))

# Get Creds for API Requests
def get_credentials_for_API(user_id):
  if user_credentials_exist(user_id) is False:
    # redirects to initialize_google_auth which will do callback etc and save into session. 
    return flask.redirect('oauth-start')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **get_credentials_from_db(user_id))

  # save them back to session
  store_credentials_in_db(user_id, credentials_to_dict(credentials))

#### DB IMPLEMENTATIONS

def user_credentials_exist(user_id):
  user_doc_count = creds_collection.count_documents({'user_id':user_id}, limit = 1)
  return user_doc_count != 0 

def store_credentials_in_db(user_id, credentials_dict):
  if user_credentials_exist(user_id):
    creds_collection.find_one_and_update({'user_id':user_id}, {'credentials': credentials_dict})
    return

  entry = {'user_id':user_id, 'credentials':credentials_dict}
  creds_collection.insert_one(entry)

# needs to return in a dict form.
def get_credentials_from_db(user_id):
  if user_credentials_exist(user_id) is False:
    return None

  entry = creds_collection.find_one({'user_id':user_id})
  return entry.credentials

def del_credentials_from_db(user_id):
  creds_collection.delete_one({'user_id':user_id})

### Revoke/Delete Access/Other Utils

def revoke(user_id):
  if user_credentials_exist(user_id) is False:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
      **get_credentials_from_db(user_id))

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


def clear_credentials(user_id):
  if user_credentials_exist(user_id) is False:
    del_credentials_from_db(user_id)
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')