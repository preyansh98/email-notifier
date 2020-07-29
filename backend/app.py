from flask import Flask, request, jsonify
from gauth_module import setup_gmail_api_auth
import json
import base64
app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# process webhook from cloud pubsub
@app.route('/cloud/webhook/', methods=['POST'])
def post_placeholder():
    req_data = request.get_json()
    notif_payload = req_data['message']['data']
    
    decoded = base64.b64decode(notif_payload).decode('utf-8')
    resp_data = json.loads(decoded)
    
    email_address = resp_data['emailAddress']
    history_id = resp_data['historyId']

    # get gmail service
    service = setup_gmail_api_auth(SCOPES)

    # get email history
    all_history = get_user_history(email_address, history_id)

    if all_history is not None:
        new_messages = all_history[0]['messagesAdded']
        process_new_messages(new_messages)

    return { 'status' : 'success' }, 200

@app.route('/')
def index():
    return "<h1>Welcome to this server</h1>"

def get_user_history(email_address, history_id):
    try:
        history = (service.users().history().list(userId=email_address,
                                                    startHistoryId=history_id,
                                                    historyTypes="messageAdded")
                            .execute())

        changes = history['history'] if 'history' in history else []
    
        # append all possible results
        while 'nextPageToken' in history:
            page_token = history['nextPageToken']
            history = (service.users().history().list(userId=user_id,
                                            startHistoryId=start_history_id,
                                            historyTypes='messageAdded',
                                            pageToken=page_token).execute())
            changes.extend(history['history'])

        return changes
    
    except errors.HttpError as error:    
        print 'An error occurred: %s' % error
        return None

def process_new_messages(new_messages):
    #todo
    print(new_messages)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)