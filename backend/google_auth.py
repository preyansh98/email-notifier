import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from googleapiclient import discovery 
from pymongo import MongoClient
import os
import json
import httplib2

# Statics

CLIENTSECRETS_LOCATION = 'creds/client_secret.json'
REDIRECT_URI = 'https://localhost:5000/redirect'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


# Main Function

#  Returns:
#     oauth2client.client.OAuth2Credentials instance containing an access and
#     refresh token.
#   Raises:
#     CodeExchangeError: Could not exchange the authorization code.
#     NoRefreshTokenException: No refresh token could be retrieved from the
#                              available sources. 

def get_credentials(authorization_code, state, client):
  """Retrieve credentials using the provided authorization code."""
  email_address = ''
  creds_collection = client['notifier-db']['userCredentials']
  print("called")
  try:
    credentials = exchange_code(authorization_code)
    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    user_id = user_info.get('id')
    if credentials.refresh_token is not None:
      store_credentials(user_id, credentials, creds_collection)
      return credentials
    else:
      credentials = get_stored_credentials(user_id, creds_collection)
      if credentials and credentials.refresh_token is not None:
        return credentials
  except CodeExchangeException as error:
    logging.error('An error occurred during code exchange.')
    # Drive apps should try to retrieve the user and credentials for the current
    # session.
    # If none is available, redirect the user to the authorization URL.
    error.authorization_url = get_authorization_url(email_address, state)
    raise error
  except NoUserIdException:
    logging.error('No user ID could be retrieved.')
  # No refresh token has been retrieved.
  authorization_url = get_authorization_url(email_address, state)
  raise NoRefreshTokenException(authorization_url)


""" Store credentials in DB in serialized json blob format """ 
def store_credentials(user_id, credentials, creds_collection):
  """Store OAuth 2.0 credentials in the application's database."""
  creds_as_json = credentials.to_json()
  print(creds_as_json)
  print("STRINGIFIED::")
  print(json.dumps(creds_as_json))

def get_stored_credentials(user_id, creds_collection):
  """Retrieved stored credentials for the provided user ID.
  """

  # TODO: Implement this function to work with your database.
  #       To instantiate an OAuth2Credentials instance from a Json
  #       representation, use the oauth2client.client.Credentials.new_from_json
  #       class method.

  ## My Implementation::::: 
  raise NotImplementedError()




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
  user_info_service = discovery.build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except HttpError as e:
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


def __init__(self, authorization_url):
    self.authorization_url = authorization_url

class GetCredentialsException(Exception):
  """Error raised when an error occurred while retrieving credentials."""

class CodeExchangeException(GetCredentialsException):
  """Error raised when a code exchange has failed."""

class NoRefreshTokenException(GetCredentialsException):
  """Error raised when no refresh token has been found."""

class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""