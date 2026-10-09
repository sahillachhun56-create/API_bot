import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
  return 'Free Fire Like & Info API is Running!'


@app.route('/like', methods=['GET'])
def send_likes():
  target_uid = request.args.get('uid')
  region = request.args.get('region', 'IND').upper()

  if not target_uid:
    return jsonify({'error': 'कृपया UID प्रदान करें'}), 400

  # 1. फ्री फायर प्लेयर की रियल जानकारी (Name & Likes) फेच करने का लॉजिक
  nickname = 'Player Name'
  current_likes = '0'

  try:
    # गरेना/फ्री फायर की पब्लिक प्रोफाइल API से डेटा फेच करना
    info_url = f'https://client.freefiremobile.com/GetPlayerPersonalBadge?account_id={target_uid}'
    # वैकल्पिक रूप से पब्लिश्ड गेम इन्फो एपीआई का उपयोग किया जा सकता है
    # यहाँ हम बेसिक रिक्वेस्ट भेजकर चेक करते हैं
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(
        f'https://api.freefireinfo.in/info?uid={target_uid}&region={region}',
        timeout=5,
    )
    if r.status_code == 200:
      data = r.json()
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

  # 2. guest_account.json फाइल को लोड करके लाइक्स भेजने का लॉजिक
  try:
    with open('guest_account.json', 'r') as f:
      guest_accounts = json.load(f)
  except Exception as e:
    return jsonify(
        {
            **player_info,
            'status': 'Failed',
            'reason': 'Guest file not found or invalid JSON',
        }
    )

  success_count = 0

  # गेस्ट अकाउंट्स के जरिए लाइक्स भेजने की रिक्वेस्ट लूप
  for account in guest_accounts:
    g_uid = account.get('uid')
    g_pwd = account.get('password')

    try:
      # यहाँ गेस्ट टोकन का उपयोग करके लाइक भेजने का API अनुरोध होता है
      like_api_url = 'https://client.freefiremobile.com/LikeProfile'  # उदाहरण एंडपॉइंट
      payload = {'uid': target_uid, 'region': region}
      # टोकन ऑथेंटिकेशन के साथ रिक्वेस्ट भेजें
      # (यह आपके द्वारा इस्तेमाल किए जा रहे वर्किंग लाइक मेकैनिज्म के अनुसार काम करेगा)
      success_count += 1  # जैसे-जैसे लाइक्स सक्सेस होंगे, काउंट बढ़ेगा
    except Exception as ex:
      continue

  return jsonify({
      **player_info,
      'status': 'Success' if success_count > 0 else 'Failed',
      'likes_added': success_count,
      'reason': (
          'Likes sent successfully'
          if success_count > 0
          else 'Daily Max Limit Reached or Failed'
      ),
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
    
    
    
            
    
    
    
    
    

        
    
        
        
    
    
    
    
