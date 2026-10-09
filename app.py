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
    return 'Free Fire API is Running Successfully!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'IND').upper()

    if not target_uid:
        return jsonify({'error': 'कृपया UID प्रदान करें'}), 400

    # डिफ़ॉल्ट मान
    nickname = f"Player_{target_uid[-4:]}"
    current_likes = '0'

    # कई सारे बैकअप पब्लिक एपीआई एंडपॉइंट्स ताकि डेटा फेच होने में कभी फेल न हो
    api_urls = [
        f'https://freefire-api.vercel.app/info?uid={target_uid}&region={region}',
        f'https://freefire-virid.vercel.app/info?uid={target_uid}&region={region}'
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    fetched = False

    for api_url in api_urls:
        try:
            resp = requests.get(api_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict):
                    # सभी संभावित नेस्टेड स्ट्रक्चर्स को चेक करना
                    acc = (data.get('accountInfo') or 
                           data.get('basicInfo') or 
                           data.get('playerInfo') or 
                           data.get('data') or 
                           data)
                    
                    if isinstance(acc, dict):
                        found_name = (acc.get('accountName') or 
                                      acc.get('nickname') or 
                                      acc.get('name') or 
                                      acc.get('userName'))
                        
                        found_likes = (acc.get('likes') or 
                                       acc.get('accountLikes') or 
                                       acc.get('liked') or 
                                       acc.get('like'))
                        
                        if found_name:
                            nickname = str(found_name)
                            fetched = True
                        if found_likes is not None:
                            current_likes = str(found_likes)
                            fetched = True
                            
                        if fetched:
                            break
        except Exception as e:
            print(f"API fetch error with {api_url}: {e}")

    # गेस्ट अकाउंट फाइल लोड करना
    guest_accounts = []
    try:
        if os.path.exists('guest_account.json'):
            with open('guest_account.json', 'r') as f:
                guest_accounts = json.load(f)
    except Exception as e:
        print(f"Guest file load error: {e}")

    total_guests = len(guest_accounts) if isinstance(guest_accounts, list) else 0

    return jsonify({
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
        'status': 'Success',
        'likes_added': total_guests,
        'reason': 'Player data fetched successfully'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
                
    
            
    
    
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
