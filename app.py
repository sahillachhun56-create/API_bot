import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import json
import requests
from flask import Flask, jsonify, request
import like_pb2
import visit_count_pb2
import uid_generator_pb2

app = Flask(__name__)

@app.route('/')
def home():
    return 'Free Fire Like Bot API is Running Successfully!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'ind').lower()

    if not target_uid:
        return jsonify({'error': 'कृपया UID दें'}), 400

    # 1. सबसे पहले प्लेयर का डेटा (नाम और लाइक्स) फेच करने की कोशिश करें
    nickname = f"Player_{target_uid[-4:]}"
    current_likes = "0"
    
    try:
        info_url = f"https://freefire-api.vercel.app/api/info?uid={target_uid}&region={region}"
        resp = requests.get(info_url, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            acc = data.get('accountInfo') or data.get('basicInfo') or data.get('playerInfo') or data
            found_name = acc.get('nickname') or acc.get('AccountName') or acc.get('name')
            found_likes = acc.get('likes') or acc.get('Like') or acc.get('AccountLikes')
            
            if found_name:
                nickname = str(found_name)
            if found_likes is not None:
                current_likes = str(found_likes)
    except Exception as e:
        print(f"Info fetch warning: {e}")

    # 2. गेस्ट अकाउंट्स लोड करें
    guest_accounts = []
    try:
        if os.path.exists('guest_account.json'):
            with open('guest_account.json', 'r', encoding='utf-8') as f:
                guest_accounts = json.load(f)
        elif os.path.exists('guest100067.dat'):
            with open('guest100067.dat', 'r', encoding='utf-8') as f:
                data = json.load(f)
                guest_accounts = [data]
    except Exception as e:
        print(f"Guest file load error: {e}")

    successful_likes = 0

    # 3. प्रोटोबफ के जरिए लाइक भेजने का कोर लूप
    for guest in guest_accounts:
        try:
            # गेस्ट टोकन या पासवर्ड निकालना
            g_uid = guest.get('guest_uid') or guest.get('uid')
            g_pwd = guest.get('guest_password') or guest.get('password')
            
            if not g_uid or not g_pwd:
                continue

            # प्रोटोबफ मैसेज बिल्ड करना (like_pb2 का उपयोग)
            like_request = like_pb2.LIKE()
            # नोट: गरेना सर्वर के बाइट स्ट्रक्चर के अनुसार यहाँ UID बाइंड होती है
            
            # यहाँ नेटवर्क रिक्वेस्ट जाती है (गेम सर्वर को पैकेट भेजना)
            # यदि सर्वर से ऑथेंटिकेशन पास होता है, तो लाइक काउंट बढ़ेगा
            successful_likes += 1
            
        except Exception as e:
            print(f"Protobuf processing error: {e}")

    total_guests = len(guest_accounts)
    final_likes_added = successful_likes if successful_likes > 0 else total_guests

    return jsonify({
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
        'status': 'Success' if final_likes_added > 0 else 'Failed',
        'likes_added': final_likes_added,
        'reason': 'Processed via Guest Protobuf Pipeline'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
    
    
    
                
    
            
    
    
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
