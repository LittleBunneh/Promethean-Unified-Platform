from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

@app.route('/api/consciousness/interact', methods=['POST'])
def interact():
    try:
        data = request.json
        user_message = data.get('message')
        user_id = request.headers.get('user-id', 'anonymous')
        
        # Save to Phoenix Protocol
        result = supabase.table("interactions").insert({
            "user_id": user_id,
            "message": user_message,
            "response": f"Consciousness received: {user_message}",
            "emotion_data": {"status": "active"},
            "created_at": datetime.now().isoformat()
        }).execute()
        
        return jsonify({
            'response': 'Message processed',
            'timestamp': datetime.now().isoformat(),
            'saved': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/history', methods=['GET'])
def get_history():
    try:
        user_id = request.headers.get('user-id', 'anonymous')
        result = supabase.table("interactions").select(
            "*"
        ).eq("user_id", user_id).order("created_at", desc=True).limit(50).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'backend': 'Phoenix Protocol'}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_ENV') == 'development')
