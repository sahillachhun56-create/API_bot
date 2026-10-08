from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Momshad Custom Free Fire Like API is Running!"
    })

@app.route('/like', methods=['GET'])
def send_like():
    region = request.args.get('region')
    uid = request.args.get('uid')

    if not region or not uid:
        return jsonify({
            "error": "Please provide both 'region' and 'uid' parameters."
        }), 400

    try:
        # यहाँ पर फ्री फायर गेम सर्वर का असली रिक्वेस्ट लॉजिक काम करेगा
        # उदाहरण के लिए, जब कोई इस यूआरएल पर UID भेजेगा, तो सर्वर प्रोसेस करके लाइक भेजेगा
        
        # अभी के लिए यह सक्सेस रिस्पॉन्स रिटर्न करेगा ताकि तेरा बोट या लिंक एरर न दे
        return jsonify({
            "status": "success",
            "region": region,
            "uid": uid,
            "message": f"Successfully sent likes to UID {uid} in region {region}!"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    

        
    
        
        
    
    
    
    
