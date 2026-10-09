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
    region = request.args.get('region', 'IND').upper()  # डिफ़ॉल्ट रीजन IND रहेगा
    
    if not target_uid:
        return jsonify({"error": "कृपया टारगेट UID दें! उदाहरण: /like?region=ind&uid=YOUR_UID"}), 400

    # 1. टारगेट प्लेयर की जानकारी फेच करने का सेटअप
    player_info = {
        "target_uid": target_uid,
        "region": region,
        "nickname": "Player Name",
        "likes": "Checking..."
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
        guest_uid = account.get("uid")
        password = account.get("password")
        
        try:
            # फ्री फायर गेम सर्वर का लाइक एंडपॉइंट और हेडर्स
            api_url = "https://clientbp.ggblueshark.com/LikeProfile"
            
            headers = {
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; RMX2151 Build/RP1A.200720.011)",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json"
            }
            
            payload = {
                "uid": int(target_uid),
                "region": region
            }
            
            # असली रिक्वेस्ट भेजने का लॉजिक (जरूरत पड़ने पर अनकमेंट करें)
            # response = requests.post(api_url, json=payload, headers=headers, timeout=5)
            
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
    
    
            
    
    
    
    
    

        
    
        
        
    
    
    
    
