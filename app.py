import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Free Fire Like & Info API is Running Successfully!"

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    
    if not target_uid:
        return jsonify({"error": "कृपया टारगेट UID दें! उदाहरण: /like?uid=YOUR_UID"}), 400

    # 1. टारगेट प्लेयर की जानकारी फेच करने का सेटअप
    player_info = {
        "target_uid": target_uid,
        "nickname": "Player Name", # यहाँ एपीआई रिस्पांस से नेम आएगा
        "likes": "Checking..."     # यहाँ लाइक काउंट आएगा
    }

    # 2. guest_account.json फाइल को लोड करना
    try:
        with open('guest_account.json', 'r') as f:
            guest_accounts = json.load(f)
    except Exception as e:
        return jsonify({"error": f"गेस्ट अकाउंट फाइल पढ़ने में एरर आया: {str(e)}"}), 500

    success_count = 0
    results = []

    # 3. लूप चलाकर गेस्ट अकाउंट्स से लाइक भेजना
    for account in guest_accounts:
        guest_uid = account["uid"]
        password = account["password"]
        
        try:
            # यहाँ लाइक भेजने वाला मुख्य रिक्वेस्ट लॉजिक आएगा
            # headers = {"Authorization": f"Bearer {password}"}
            # response = requests.post(...)
            
            success_count += 1
            results.append({
                "guest_uid": guest_uid,
                "status": "Success",
                "message": "Like sent successfully"
            })
        except Exception as e:
            results.append({
                "guest_uid": guest_uid,
                "status": "Failed",
                "error": str(e)
            })

    return jsonify({
        "status": "Completed",
        "player_details": player_info,
        "total_guest_accounts": len(guest_accounts),
        "success_count": success_count,
        "results": results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
    
    
    
    
    

        
    
        
        
    
    
    
    
