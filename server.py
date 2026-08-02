#!/usr/bin/env python3
import os
from flask import Flask, Response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

@app.route("/")
def index():
    if not os.path.exists(INDEX_PATH):
        return "index.html not found", 404
        
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # استبدال صريح لأي قيمة قديمة بالرقم الصحيح
    content = content.replace('"YOUR_BLOCK_ID"', '"40807"')
    
    response = Response(content, mimetype="text/html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
