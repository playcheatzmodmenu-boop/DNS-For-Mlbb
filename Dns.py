from flask import Flask
import requests

app = Flask(__name__)

NEXTDNS = "https://my.nextdns.io/1165b4/setup"

@app.route("/")
def index():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(NEXTDNS, headers=headers, timeout=30)
        result = response.text

        return f"""<!DOCTYPE html>
<html>
<head>
<title>NextDNS Reader</title>
</head>
<body style="background:#0d1117; color:white; font-family:Arial; padding:30px;">
<div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:20px; max-width:900px; margin:auto;">
<h2 style="color:#00ff99;">NextDNS Setup Result</h2>
<pre style="white-space:pre-wrap; font-size:16px; line-height:1.5;">{result}</pre>
</div>
</body>
</html>"""

    except Exception as e:
        return f"<h2>Error</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
