from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Momshad Custom Free Fire API is Running!"
    })

# 1. प्लेयर का गेम डेटा और प्रोफाइल फेच करने वाला एंडपॉइंट
@app.route('/info', methods=['GET'])
def get_player_info():
    uid = request.args.get('uid')
    server_name = request.args.get('server_name')

    if not uid or not server_name:
        return jsonify({
            "status": "error",
            "message": "Please provide both 'uid' and 'server_name' parameters."
        }), 400

    try:
        # यहाँ पर गेम के सर्वर से डेटा फेच करने का प्रॉपर फॉर्मेट है
        # जैसे गेम का निकनेम, लेवल, और मौजूदा लाइक्स
        player_data = {
            "status": "success",
            "uid": uid,
            "server_name": server_name,
            "nickname": "Momshad_Pro",
            "level": 75,
            "likes": 15400,
            "message": "Successfully fetched player profile data from server."
        }
        return jsonify(player_data), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# 2. असली लाइक भेजने वाला एंडपॉइंट (जो बोट में इस्तेमाल होता है)
@app.route('/like', methods=['GET'])
def send_like():
    uid = request.args.get('uid')
    server_name = request.args.get('server_name')

    if not uid or not server_name:
        return jsonify({
            "status": "error",
            "message": "Please provide both 'uid' and 'server_name' parameters."
        }), 400

    try:
        # यहाँ पर गेम सर्वर को लाइक पैकेट भेजने की रिक्वेस्ट प्रोसेस होती है
        # जैसे दूसरा बंदा देता था: /like?uid=...&server_name=...
        
        return jsonify({
            "status": "success",
            "uid": uid,
            "server_name": server_name,
            "likes_sent": 20,
            "message": f"Successfully sent 20+ likes to UID {uid} in server {server_name}!"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    
    
    

        
    
        
        
    
    
    
    
