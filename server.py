#!/usr/bin/env python3
import os
import re
import requests
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()


def validate_router_name(router_name: str) -> tuple[str, str]:
    raw = router_name.strip()
    clean = re.sub(r'^(fh[_\-]?|Fh[_\-]?)', '', raw, flags=re.IGNORECASE).strip().lower()

    if not clean or len(clean) != 6 or not all(c in '0123456789abcdef' for c in clean):
        raise ValueError("Invalid format. Router name must contain 6 hex characters.")

    return clean, f"Fh_{clean}"


def generate_fiberhome_password(clean_hex: str) -> str:
    """FiberHome Password Generation Algorithm"""
    char_map = {
        '0': 'f', '1': 'e', '2': 'd', '3': 'c',
        '4': 'b', '5': 'a', '6': '9', '7': '8'
    }
    converted = "".join(char_map.get(c, c) for c in clean_hex)
    return f"wlan{converted}"


@app.route("/")
def index():
    if not os.path.exists(INDEX_PATH):
        return "index.html not found", 404
        
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    response = Response(content, mimetype="text/html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/api/verify", methods=["POST"])
def verify():
    """استقبال تأكيد مشاهدة الإعلان وإرسال كلمة السر للتلغرام مباشرة"""
    try:
        data = request.get_json() or {}
        router_name = data.get("name", "")
        chat_id = data.get("chat_id")

        if not router_name or not chat_id:
            return jsonify({"error": "Missing name or chat_id"}), 400

        clean_hex, full_network_name = validate_router_name(router_name)
        password = generate_fiberhome_password(clean_hex)

        if BOT_TOKEN:
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            text = (
                f"🎉 **Ad Watch Verified!**\n\n"
                f"📌 **Network:** `{full_network_name}`\n"
                f"🔑 **Password:** `{password}`"
            )
            requests.post(telegram_url, json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }, timeout=10)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error in /api/verify: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
