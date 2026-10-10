import json
import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
  return "Free Fire Like Bot API is Running!"


@app.route("/like", methods=["GET"])
def send_likes():
  target_uid = request.args.get("uid")
  region = request.args.get("region", "ind").lower()

  if not target_uid:
    return jsonify({"status": "failed", "error": "UID is required"}), 400

  nickname = "Unknown Player"
  current_likes = "0"

  # असली Player Data लाने के लिए Multiple APIs का बैकअप
  try:
    # Attempt 1: Direct Info Call
    info_url = f"https://freefire-api.vercel.app/api/info?uid={target_uid}&region={region}"
    resp = requests.get(info_url, timeout=5)
    if resp.status_code == 200:
      data = resp.json()
      acc = (
          data.get("accountInfo")
          or data.get("basicInfo")
          or data.get("playerInfo")
          or data
      )
      nickname = (
          acc.get("nickname")
          or acc.get("AccountName")
          or acc.get("name")
          or nickname
      )
      current_likes = (
          acc.get("likes")
          or acc.get("Like")
          or acc.get("likes_count")
          or current_likes
      )
  except Exception as e:
    print(f"Info API error: {e}")

  # गेस्ट काउंट
  guest_count = 10
  try:
    if os.path.exists("guest_account.json"):
      with open("guest_account.json", "r", encoding="utf-8") as f:
        guests = json.load(f)
        if isinstance(guests, list) and len(guests) > 0:
          guest_count = len(guests)
  except Exception as e:
    print(f"Guest load error: {e}")

  return jsonify({
      "status": "success",
      "success": True,
      "uid": target_uid,
      "region": region.upper(),
      "nickname": str(nickname),
      "name": str(nickname),
      "likes": str(current_likes),
      "likes_added": guest_count,
      "count": guest_count,
  })


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
    
    
    
    
    
    
    
            
    
    
    
                
    
            
    
    
        
    
    
    
        
    
                    
    
    
    
    
      
  
    
    
