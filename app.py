from flask import Flask, jsonify, request

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
        return jsonify({"error": "Please provide both 'region' and 'uid' parameters."}), 400
    
    return jsonify({
        "status": "success",
        "message": f"Successfully sent likes to UID {uid} in region {region}!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    

        
    
        
        
    
    
    
    
