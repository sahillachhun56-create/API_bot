from flask import Flask, request, jsonify
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import aiohttp
import requests
import json
import like_pb2
import uid_generator_pb2
import visit_count_pb2
from google.protobuf.message import DecodeError
from collections import OrderedDict
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API and Bot Server is Live!"

# Valid API keys
VALID_API_KEYS = {
    "Anurag"  # don't change warna api on nahi hogi
}

# Like limit tracking
daily_limit = 99
used_count = 0

def load_tokens(region):
    try:
        if region == "IND":
            with open("token_ind.json", "r") as f:
                tokens = json.load(f)
        elif region in {"BR", "US", "SAC", "NA"}:
            with open("token_br.json", "r") as f:
                tokens = json.load(f)
        else:
            with open("token_bd.json", "r") as f:
                tokens = json.load(f)
        return tokens
    except Exception as e:
        app.logger.error(f"Error loading tokens: {e}")
        return None

def encrypt_message(plaintext):
    try:
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(plaintext, AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        return binascii.hexlify(encrypted_message).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Error encrypting: {e}")
        return None

def create_protobuf_message(user_id, region):
    try:
        message = like_pb2.Like()
        message.uid = int(user_id)
        message.region = region
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error creating protobuf message: {e}")
        return None

async def send_request(encrypted_uid, token, region):
    try:
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; M2010J19SI Build/RP1A.200720.011)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55"
        }
        if region == "IND":
            url = "https://client.ind.freefiremobile.com/LikeProfile"
        elif region in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/LikeProfile"
        else:
            url = "https://clientbp.ggservices.com/LikeProfile"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers) as response:
                return await response.text()
    except Exception as e:
        app.logger.error(f"Exception in send_request: {e}")
        return None

async def send_multiple_requests(uid, region):
    try:
        protobuf_message = create_protobuf_message(uid, region)
        if protobuf_message is None:
            return None
        encrypted_uid = encrypt_message(protobuf_message)
        if encrypted_uid is None:
            return None
        tokens = load_tokens(region)
        if tokens is None:
            return None

        tasks = []
        for i in range(100):
            t_obj = tokens[i % len(tokens)]
            tok = t_obj['token'] if isinstance(t_obj, dict) and 'token' in t_obj else t_obj
            tasks.append(send_request(encrypted_uid, tok, region))

        results = await asyncio.gather(*tasks)
        return results
    except Exception as e:
        app.logger.error(f"Exception in send_multiple_requests: {e}")
        return None

def create_protobuf(uid):
    try:
        message = uid_generator_pb2.uid_generator()
        message.saturn_ = int(uid)
        message.garena = 1
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error creating protobuf: {e}")
        return None

def enc(uid):
    protobuf_data = create_protobuf(uid)
    if protobuf_data is None:
        return None
    return encrypt_message(protobuf_data)

def make_request(encrypt, region, token):
    try:
        if region == "IND":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalProfile"
        elif region in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalProfile"
        else:
            url = "https://clientbp.ggservices.com/GetPlayerPersonalProfile"

        edata = bytes.fromhex(encrypt)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; M2010J19SI Build/RP1A.200720.011)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55"
        }
        response = requests.post(url, data=edata, headers=headers, timeout=10)
        binary = response.content
        decoded = visit_count_pb2.Info()
        decoded.ParseFromString(binary)
        return decoded
    except DecodeError as e:
        app.logger.error(f"DecodeError: {e}")
        return None
    except Exception as e:
        app.logger.error(f"Error in make_request: {e}")
        return None

@app.route('/like', methods=['GET'])
def handle_requests():
    global used_count

    # API key check
    api_key = request.args.get("key")
    if api_key not in VALID_API_KEYS:
        result = OrderedDict([
            ("error", "Invalid or missing API key"),
            ("status", 3)
        ])
        return app.response_class(
            response=json.dumps(result),
            status=401,
            mimetype='application/json'
        )

    uid = request.args.get("uid")
    region = request.args.get("region", "IND")
    if not uid or not region:
        return jsonify({"error": "UID and region are required"}), 400

    def process_request():
        global used_count

        tokens = load_tokens(region)
        if not tokens:
            raise Exception("Failed to load tokens")

        first_token = tokens[0]
        token = first_token['token'] if isinstance(first_token, dict) and 'token' in first_token else first_token

        encrypted_uid = enc(uid)
        if encrypted_uid is None:
            raise Exception("Encryption failed")

        before = make_request(encrypted_uid, region, token)
        if before is None:
            raise Exception("Failed to get initial info")

        before_info = getattr(before, 'AccountInfo', None)
        before_like = getattr(before_info, 'Likes', 0) if before_info else 0

        asyncio.run(send_multiple_requests(uid, region))

        after = make_request(encrypted_uid, region, token)
        if after is None:
            after_like = before_like + 100
            after_info = before_info
        else:
            after_info = getattr(after, 'AccountInfo', None)
            after_like = getattr(after_info, 'Likes', before_like) if after_info else before_like

        like_given = max(after_like - before_like, 0)
        status = 1 if like_given > 0 else 0

        if status == 1:
            used_count += 1

        remaining = max(daily_limit - used_count, 0)

        nickname = getattr(after_info, 'Nickname', 'Unknown') if after_info else 'Unknown'
        level = getattr(after_info, 'Level', 0) if after_info else 0
        player_region = getattr(after_info, 'Region', region) if after_info else region
        player_uid = getattr(after_info, 'UID', uid) if after_info else uid

        result = OrderedDict([
            ("LikesGivenByAPI", like_given),
            ("LikesafterCommand", after_like),
            ("LikesbeforeCommand", before_like),
            ("PlayerNickname", nickname),
            ("Level", level),
            ("Region", player_region),
            ("UID", player_uid),
            ("status", status),
            ("daily_limit", daily_limit),
            ("used", used_count),
            ("remaining", remaining)
        ])

        return app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )

    try:
        return process_request()
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# /remain endpoint
@app.route('/remain', methods=['GET'])
def remain_info():
    global used_count

    remaining = max(daily_limit - used_count, 0)
    data = {
        "daily_limit": daily_limit,
        "remaining": remaining,
        "used": used_count,
        "reset_info": "4:00 AM IST"
    }
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
        
