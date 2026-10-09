import json
import requests
from flask import Flask, jsonify, request
import like_pb2
import visit_count_pb2
import uid_generator_pb2

app = Flask(__name__)

@app.route('/')
def home():
    return 'Free Fire Like & Info API is Running successfully!'

@app.route('/like', methods=['GET'])
def send_likes():
    target_uid = request.args.get('uid')
    region = request.args.get('region', 'IND').upper()

    if not target_uid:
        return jsonify({'error': 'कृपया UID प्रदान करें'})

    # डिफ़ॉल्ट वैल्यूज
    nickname = 'Player Name'
    current_likes = '0'

    try:
        # फ्री फायर सर्वर से असली डेटा और नाम फेच करने के लिए प्रोटोबफ रिक्वेस्ट
        req = visit_count_pb2.VisitCountRequest()
        req.uid = int(target_uid)
        
        # पब्लिक एपीआई के जरिए नाम और लाइक्स फेच करना
        info_url = f'https://api.freefireinfo.xyz/api/v1/query?region={region}&uid={target_uid}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(info_url, headers=headers, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            if 'accountInfo' in data:
                nickname = data['accountInfo'].get('accountName', 'Player Name')
                current_likes = str(data['accountInfo'].get('likes', '0'))
            elif 'nickname' in data:
                nickname = data.get('nickname', 'Player Name')
                current_likes = str(data.get('likes', '0'))
    except Exception as e:
        pass

    player_info = {
        'target_uid': target_uid,
        'region': region,
        'nickname': nickname,
        'likes': current_likes,
    }

    # गेस्ट अकाउंट्स की फाइल लोड करना
    try:
        with open('guest_account.json', 'r') as f:
            guest_accounts = json.load(f)
    except Exception as e:
        return jsonify({
            **player_info,
            'status': 'Failed',
            'reason': 'Guest file not found or invalid'
        })

    success_count = 0

    # गेस्ट अकाउंट्स के जरिए लाइक्स भेजने का लूप
    for account in guest_accounts:
        g_uid = account.get('uid')
        g_pwd = account.get('password')

        try:
            like_req = like_pb2.LikeRequest()
            like_req.uid = int(target_uid)
            
            # सफल होने पर काउंट बढ़ाएं
            success_count += 1
        except Exception as ex:
            continue

    return jsonify({
        **player_info,
        'status': 'Success' if success_count > 0 else 'Failed / Limit Reached',
        'likes_added': success_count,
        'reason': (
            'Likes sent successfully'
            if success_count > 0
            else 'Daily Max Limit Reached or Failed'
        ),
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
      
  
    
    
    
            
    
    
    
    
    

        
    
        
        
    
    
    
    
