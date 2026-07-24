from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    # Kunin ang IP address ng user na pumunta sa site mo (kahit nasa Render pa yan)
    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        user_ip = request.remote_addr

    # Pwede nating gawan ng unique ID o DNS endpoint base sa IP nila
    # Halimbawa, gagamitin natin ang IP nila para sa custom DNS view
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Custom DNS Setup</title>
<style>
body {{
    background:#0d1117;
    color:white;
    font-family:Arial, sans-serif;
    padding:30px;
}}
.box {{
    background:#161b22;
    border:1px solid #30363d;
    border-radius:12px;
    padding:20px;
    max-width:600px;
    margin:auto;
}}
h2 {{
    color:#00ff99;
}}
.label {{
    font-size: 12px;
    color: #8b949e;
    text-transform: uppercase;
    font-weight: bold;
    margin-top: 15px;
}}
.value {{
    font-size: 15px;
    font-family: monospace;
    color: #c9d1d9;
    background: #0d1117;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #30363d;
    word-break: break-all;
}}
</style>
</head>
<body>

<div class="box">
    <h2>Linked IP DNS Setup</h2>
    <p>Awtomatikong nakita ang iyong IP at naka-link sa profile na ito.</p>

    <div class="label">Your Linked IP Address</div>
    <div class="value">{user_ip}</div>

    <div class="label">Your Custom DNS-over-HTTPS (DoH)</div>
    <div class="value">https://dns.yoursite.com/profile-{user_ip.replace('.', '-')}</div>

    <div class="label">Your Assigned DNS Server / IP</div>
    <div class="value">103.247.36.36 (Sample Resolver)</div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
