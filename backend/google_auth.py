import flask
import requests
import logging
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from pymongo import MongoClient
from db import initialize_and_return_db_client
from urllib.error import HTTPError

# Statics

CLIENTSECRETS_LOCATION = 'creds/client_secret.json'
REDIRECT_URI = 'http://localhost:5000/oauth-callback'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
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

  authorization_url = flow.authorization_url(
    #Need offline access for job processing
    access_type = 'offline',
  )[0]

  return authorization_url


# Callback, Exchange code for token
def get_credentials_on_callback():

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENTSECRETS_LOCATION,
      scopes=SCOPES
      )

  flow.redirect_uri = REDIRECT_URI

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  auth_code = flask.request.args.get('code')
  email = get_credentials_internal(auth_code, "state")[0]
  return email


# Get Creds for API Requests
def get_credentials_for_API(email_address):
  if user_credentials_exist(email_address) is False:
    # redirects to initialize_google_auth which will do callback etc and save into session. 
    return flask.redirect('oauth-start')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **get_credentials_from_db(email_address))

  # save them back to session
  store_credentials_in_db(email_address, credentials_to_dict(credentials))

#### DB IMPLEMENTATIONS

def user_credentials_exist(email_address):
  user_doc_count = creds_collection.count_documents({'email_address':email_address}, limit = 1)
  return user_doc_count != 0 

def store_credentials_in_db(email_address, credentials_dict):
  if user_credentials_exist(email_address):
    creds_collection.find_one_and_update({'email_address':email_address}, {'credentials': credentials_dict})
    return

  entry = {'email_address':email_address, 'credentials':credentials_dict}
  creds_collection.insert_one(entry)

# needs to return in a dict form.
def get_credentials_from_db(email_address):
  if user_credentials_exist(email_address) is False:
    return None

  entry = creds_collection.find_one({'email_address':email_address})
  return entry['credentials']

def del_credentials_from_db(email_address):
  creds_collection.delete_one({'email_address':email_address})

### Revoke/Delete Access/Other Utils

def revoke(email_address):
  if user_credentials_exist(email_address) is False:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
      **get_credentials_from_db(email_address))

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


def clear_credentials(email_address):
  if user_credentials_exist(email_address) is False:
    del_credentials_from_db(email_address)
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())


## CALLBACK HELPERS

def get_credentials_internal(authorization_code, state):
  """Retrieve credentials using the provided authorization code."""
  email_address = ''
  try:
    credentials = exchange_code(authorization_code)
    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    if credentials.refresh_token is not None:
      store_credentials_in_db(email_address, credentials_to_dict(credentials))
      return email_address, credentials
    else:
      credentials = get_credentials_from_db(email_address)
      if credentials and credentials['refresh_token'] is not None:
        return email_address, credentials
  except CodeExchangeException as error:
    logging.error('An error occurred during code exchange.')
    # If none is available, redirect the user to the authorization URL.
    error.authorization_url = get_authorization_url(email_address, state)
    raise error
  except NoUserIdException:
    logging.error('No user ID could be retrieved.')
  # No refresh token has been retrieved.
  authorization_url = get_authorization_url(email_address, state)
  raise NoRefreshTokenException(authorization_url)


def exchange_code(authorization_code):
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.redirect_uri = REDIRECT_URI
  try:
    credentials = flow.step2_exchange(authorization_code)
    return credentials
  except FlowExchangeError as error:
    logging.error('An error occurred: %s', error)
    raise CodeExchangeException(None)


def get_user_info(credentials):
  user_info_service = googleapiclient.discovery.build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    # pylint: disable=maybe-no-member
    user_info = user_info_service.userinfo().get().execute()
  except HTTPError as e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info
  else:
    raise NoUserIdException()

def get_authorization_url(email_address, state):
  flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
  flow.params['access_type'] = 'offline'
  flow.params['approval_prompt'] = 'force'
  flow.params['user_id'] = email_address
  flow.params['state'] = state
  return flow.step1_get_authorize_url(REDIRECT_URI)

class GetCredentialsException(Exception):
  """Error raised when an error occurred while retrieving credentials."""

class CodeExchangeException(GetCredentialsException):
  """Error raised when a code exchange has failed."""

class NoRefreshTokenException(GetCredentialsException):
  """Error raised when no refresh token has been found."""

class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""



#Util Functions

def credentials_to_dict(credentials):
  return {'token': credentials.access_token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': list(credentials.scopes)}

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