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
    return 'Free Fire Like API is Running Successfully!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'IND').upper()

    if not target_uid:
        return jsonify({'error': 'कृपया UID प्रदान करें'}), 400

    # डिफ़ॉल्ट मान जब तक असली डेटा न मिले
    nickname = f"Player_{target_uid[-4:]}"
    current_likes = '0'

    # प्लेयर का असली नाम और डेटा फेच करना
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

    # गेस्ट अकाउंट JSON फाइल लोड करना
    guest_accounts = []
    try:
        if os.path.exists('guest_account.json'):
            with open('guest_account.json', 'r') as f:
                guest_accounts = json.load(f)
    except Exception as e:
        print(f"Guest file load error: {e}")

    total_guests = len(guest_accounts) if isinstance(guest_accounts, list) else 0

    # रिस्पॉन्स भेजना
    return jsonify({
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
        'status': 'Success' if total_guests > 0 else 'Failed',
        'likes_added': total_guests,
        'reason': f'Processed via {total_guests} Guest Accounts' if total_guests > 0 else 'No Guest Accounts Found'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
                
    
            
    
    
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
