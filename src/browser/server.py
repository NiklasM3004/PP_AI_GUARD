#!/usr/bin/env python3
"""
Minimal Backend - Empfängt Messages und printet sie
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Erlaubt Requests vom Browser

@app.route('/api/message', methods=['POST'])
def receive_message():
    """Empfängt Message und printet sie"""
    data = request.get_json()
    text = data.get('text', '')
    
    # ✨ HIER: Message printen
    print("\n" + "="*60)
    print("🚀 MESSAGE EMPFANGEN!")
    print("="*60)
    print(f"📄 Inhalt: {text}")
    print("="*60 + "\n")
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n🛡️ Backend Server läuft auf http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)