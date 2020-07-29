from flask import Flask, request, jsonify
import json
import base64
app = Flask(__name__)

# process webhook from cloud pubsub
@app.route('/cloud/webhook/', methods=['POST'])
def post_placeholder():
    req_data = request.get_json()
    notif_payload = req_data['message']['data']
    
    decoded = base64.b64decode(notif_payload).decode('utf-8')
    resp_data = json.loads(decoded)
    
    email_address = resp_data['emailAddress']
    history_id = resp_data['historyId']

    

@app.route('/')
def index():
    return "<h1>Welcome to this server</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)