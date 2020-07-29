from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/cloud/webhook/', methods=['POST'])
def post_placeholder():
    req_data = request.get_json()
    print(req_data)
    return {'status' : 'success'}, 200   

@app.route('/')
def index():
    return "<h1>Welcome to this server</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)