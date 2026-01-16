from flask import Flask, request, jsonify
import time
from datetime import datetime
import os

app = Flask(__name__)

servers = []
MAX_SERVERS = 50

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive", "count": len(servers)}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json() or {}
        if 'jobId' in data:
            clean = {
                "jobId": data.get("jobId"),
                "players": data.get("players", 0),
                "timestamp": data.get("timestamp", int(time.time())),
                "hasRare": data.get("hasRare", False),
                "rareName": data.get("rareName"),
                "rareRate": data.get("rareRate")
            }
            servers.append(clean)
            if len(servers) > MAX_SERVERS:
                servers.pop(0)
            return jsonify({"status": "ok"}), 200
        return jsonify({"status": "ignored"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/servers', methods=['GET'])
def get_servers():
    return jsonify({
        "servers": servers,
        "count": len(servers),
        "last_updated": datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
