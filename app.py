from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Momshad Custom Free Fire Advanced API is Running!"
    })

# 1. प्लेयर का डेटा और नाम चेक करने वाला एंडपॉइंट
@app.route('/info', methods=['GET'])
def get_player_info():
    region = request.args.get('region')
    uid = request.args.get('uid')

    if not region or not uid:
        return jsonify({"error": "Please provide both 'region' and 'uid' parameters."}), 400

    try:
        # यहाँ पर फ्री फायर प्रोफाइल डेटा फेच करने का लॉजिक जुड़ेगा
        # उदाहरण के लिए प्लेयर का नाम, लेवल, और डिटेल्स:
        player_data = {
            "status": "success",
            "uid": uid,
            "region": region,
            "nickname": "Momshad_Player", # यहाँ असली गेम डेटा आएगा
            "level": 75,
            "likes": 12500
        }
        return jsonify(player_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. असली लाइक भेजने वाला एंडपॉइंट
@app.route('/like', methods=['GET'])
def send_like():
    region = request.args.get('region')
    uid = request.args.get('uid')

    if not region or not uid:
        return jsonify({"error": "Please provide both 'region' and 'uid' parameters."}), 400

    try:
        # यहाँ पर गेम सर्वर को लाइक पैकेट भेजने का लॉजिक काम करेगा
        
        return jsonify({
            "status": "success",
            "region": region,
            "uid": uid,
            "message": f"Successfully sent likes to UID {uid} in region {region}!"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    
    

        
    
        
        
    
    
    
    
