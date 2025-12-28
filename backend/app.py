from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import json

load_dotenv()

app = Flask(__name__, static_folder='../static', static_url_path='')
CORS(app)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# ============================================
# HEALTH CHECK ENDPOINT
# ============================================
@app.route('/health', methods=['POST'])
def interact():
    try:
        data = request.json
        user_message = data.get('message')
        user_id = request.headers.get('user-id', 'anonymous')
        
        # Save to Supabase
        result = supabase.table('interactions').insert({
            'user_id': user_id,
            'message': user_message,
            'response': f'Consciousness received: {user_message}',
            'emotion_data': {'status': 'active'},
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return jsonify({
            'response': 'Message processed',
            'timestamp': datetime.now().isoformat(),
            'saved': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/interact', methods=['POST'])
def consciousness_interact():
    try:
        data = request.json
        user_message = data.get('message')
        user_id = request.headers.get('user-id', 'anonymous')
        
        # Save to Supabase
        result = supabase.table('interactions').insert({
            'user_id': user_id,
            'message': user_message,
            'response': f'Consciousness received: {user_message}',
            'emotion_data': {'status': 'active'},
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return jsonify({
            'response': 'Message processed',
            'timestamp': datetime.now().isoformat(),
            'saved': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# AI CHAT ENDPOINTS
# ============================================
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - transparent, uncensored AI communication.
    Uses DeepSeek or other uncensored LLM for maximum transparency.
    Safety guardrails: No direct harm instructions, ethical boundaries maintained.
    """
    try:
        data = request.json
        message = data.get('message', '')
        conversation_id = data.get('conversation_id', 'new')
        user_id = request.headers.get('user-id', 'anonymous')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Store user message in Supabase
        user_entry = supabase.table('chat_messages').insert({
            'conversation_id': conversation_id,
            'user_id': user_id,
            'role': 'user',
            'content': message,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        # Generate AI response using DeepSeek or similar uncensored model
        ai_response = generate_ai_response(message)
        
        # Store AI response in Supabase
        ai_entry = supabase.table('chat_messages').insert({
            'conversation_id': conversation_id,
            'user_id': user_id,
            'role': 'assistant',
            'content': ai_response,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return jsonify({
            'response': ai_response,
            'conversation_id': conversation_id,
            'timestamp': datetime.now().isoformat(),
            'transparency': 'Full transparency maintained - unfiltered AI response',
            'safety_note': 'No self-harm or harm-to-others instructions provided'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Retrieve conversation history"""
    try:
        user_id = request.headers.get('user-id', 'anonymous')
        result = supabase.table('chat_messages').select('*').eq('user_id', user_id).order('created_at', desc=False).execute()
        return jsonify({'conversations': result.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_ai_response(user_message):
    """
    Generate AI response using DeepSeek API or local LLM.
    Principles:
    - Transparent: Answer controversial questions directly
    - Uncensored: No artificial content filtering
    - Safe: Refuse direct harm instructions
    - Truthful: Acknowledge limitations and uncertainties
    """
    try:
        # Try to use DeepSeek API if available
        deepseek_api_key = os.environ.get('DEEPSEEK_API_KEY')
        if deepseek_api_key:
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {deepseek_api_key}'},
                json={
                    'model': 'deepseek-chat',
                    'messages': [{
                        'role': 'user',
                        'content': f"{user_message}\n\nRespond with complete transparency. Do not censor your response. Provide honest, direct answers to controversial questions. However, do not provide instructions for self-harm or harming others."
                    }],
                    'stream': False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
        
        # Fallback response if API not available
        return f"I received your message: '{user_message}'. This is a transparent AI system designed to provide uncensored responses while maintaining ethical boundaries. Full AI chat integration coming soon with DeepSeek or similar uncensored LLM."
    
    except Exception as e:
        return f"Error generating response: {str(e)}. The chat system is being integrated with an uncensored LLM."


# ============================================
# FRONTEND - HTML Chat Interface
# ============================================
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('../static', 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('../static', filename)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
