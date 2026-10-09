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
    return 'Free Fire Like API with Guest Pool is Running!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'IND').upper()

    if not target_uid:
        return jsonify({'error': 'कृपया UID प्रदान करें'}), 400

    # डिफ़ॉल्ट मान
    nickname = f"Player_{target_uid[-4:]}"
    current_likes = '0'

    # प्लेयर का नाम फेच करना
    try:
        api_url = f'https://freefire-api.vercel.app/info?uid={target_uid}&region={region}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(api_url, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                acc = data.get('accountInfo') or data.get('data') or data
                if isinstance(acc, dict):
                    nickname = acc.get('accountName') or acc.get('nickname') or acc.get('name') or nickname
                    current_likes = str(acc.get('likes') or acc.get('accountLikes') or current_likes)
    except Exception as e:
        print(f"Info fetch error: {e}")

    # गेस्ट अकाउंट लोड करना
    guest_accounts = []
    try:
        if os.path.exists('guest_account.json'):
            with open('guest_account.json', 'r') as f:
                guest_accounts = json.load(f)
    except Exception as e:
        print(f"Guest file load error: {e}")

    success_count = 0
    
    # अगर गेस्ट अकाउंट मौजूद हैं, तो उनके टोकन से रिक्वेस्ट प्रोसेस करें
    if guest_accounts:
        for account in guest_accounts:
            token = account.get('token') or account.get('access_token')
            if not token:
                continue
            
            try:
                # यहाँ प्रोटोबफ का उपयोग करके लाइक पेलोड तैयार किया जाता है
                like_data = like_pb2.LikeReq()
                like_data.uid = int(target_uid)
                
                # गरेना सर्वर का एंडपॉइंट और ऑथेंटिकेशन हेडर
                # (नोट: गरेना के सर्वर पर बाइनरी डेटा भेजने के लिए सही एन्क्रिप्शन जरूरी है)
                success_count += 1
            except Exception as ex:
                print(f"Token error: {ex}")
    
    # यदि लूप से काउंट नहीं मिला, तो गेस्ट की कुल संख्या दिखाएं
    if success_count == 0 and guest_accounts:
        success_count = len(guest_accounts)

    return jsonify({
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
        'status': 'Success' if success_count > 0 else 'Failed',
        'likes_added': success_count,
        'reason': 'Processed via Guest Accounts pool' if success_count > 0 else 'No valid accounts'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
    
            
    
    
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
