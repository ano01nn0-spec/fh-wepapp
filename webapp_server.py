#!/usr/bin/env python3
"""
Minimal web server to serve the Telegram Mini App (index.html) on Railway.
Railway sets the PORT environment variable automatically.
"""
import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    response = send_from_directory(BASE_DIR, "index.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
