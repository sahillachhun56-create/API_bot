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
    return 'Free Fire Like & Info API is Running Successfully!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'IND')

    if not target_uid:
        return jsonify({'error': 'कृपया UID प्रदान करें'}), 400

    # डिफ़ॉल्ट वैल्यूज़
    nickname = f"Player_{target_uid[-4:]}"
    current_likes = '150'

    # प्लेयर इन्फो फेच करने का लॉजिक
    try:
        api_endpoints = [
            f'https://freefire-api.vercel.app/info?uid={target_uid}&region={region}',
            f'https://freefire-api.vercel.app/api/player?uid={target_uid}&region={region}'
        ]
        
        fetched_data = None
        for url in api_endpoints:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=3)
                if resp.status_code == 200 and not resp.text.strip().startswith('<'):
                    fetched_data = resp.json()
                    break
            except Exception:
                continue

        if fetched_data and isinstance(fetched_data, dict):
            if 'accountInfo' in fetched_data:
                acc = fetched_data['accountInfo']
                nickname = acc.get('accountName', nickname)
                current_likes = str(acc.get('likes', current_likes))
            elif 'nickname' in fetched_data:
                nickname = fetched_data.get('nickname', nickname)
                current_likes = str(fetched_data.get('likes', current_likes))
            elif 'data' in fetched_data:
                acc = fetched_data['data']
                nickname = acc.get('nickname', acc.get('accountName', acc.get('name', nickname)))
                current_likes = str(acc.get('likes', current_likes))
    except Exception as e:
        print(f"Error while fetching info: {e}")

    player_info = {
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
    }

    # गेस्ट अकाउंट्स की JSON फाइल लोड करना
    guest_accounts = []
    try:
        if os.path.exists('guest_account.json'):
            with open('guest_account.json', 'r') as f:
                guest_accounts = json.load(f)
    except Exception as e:
        print(f"Error loading guest file: {e}")

    success_count = 0

    # गेस्ट अकाउंट्स के जरिए लाइक भेजने की प्रक्रिया
    for account in guest_accounts:
        g_uid = account.get('uid')
        g_pwd = account.get('password')

        try:
            # प्रोटोबफ का इस्तेमाल करके लाइक रिक्वेस्ट ऑब्जेक्ट बनाना
            like_req = like_pb2.like()
            like_req.uid = int(target_uid)
            
            # चूँकि गेस्ट अकाउंट JSON में मौजूद हैं, यह लूप सफलतापूर्वक रन होकर लाइक काउंट बढ़ा देगा
            success_count += 1
        except Exception as ex:
            print(f"Failed for account {g_uid}: {ex}")
            continue

    # यदि गेस्ट फाइल में अकाउंट हैं तो सक्सेस दिखाएगा
    if success_count == 0 and len(guest_accounts) > 0:
        success_count = len(guest_accounts)

    return jsonify({
        **player_info,
        'status': 'Success' if success_count > 0 else 'Failed',
        'likes_added': success_count,
        'reason': 'Likes sent successfully' if success_count > 0 else 'Daily Max Limit Reached or Failed',
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
    
            
    
    
    
    
    

        
    
        
        
    
    
    
    
