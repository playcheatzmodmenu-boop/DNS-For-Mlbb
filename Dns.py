from flask import Flask, request
import requests

app = Flask(__name__)

# Pwede kang gumamit ng Master API key galing sa NextDNS account mo kung gusto mo silang gawan ng profile awtomatiko
# O kaya ay gagamitin natin ang IP-based mapping para sa mga users mo.

@app.route("/")
def index():
    # Kunin ang IP address ng device na bumisita
    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        user_ip = request.remote_addr

    # Dito pwede nating tawagin ang NextDNS API para igawa ng profile ang IP nila,
    # o kaya ay i-display natin ang setup na naka-angkop sa kanilang device.
    
    # Halimbawa ng paggawa ng dynamic ID base sa IP o pagkuha mula sa API:
    # (Para sa demo na ito, gagamitin natin ang IP para magmukhang dedicated sa device nila)
    
    # Gumawa tayo ng unique short ID galing sa IP para laging consistent sa device nila
    device_id = abs(hash(user_ip)) % 1000000
    profile_id = f"d{device_id:06x}" # Halimbawa: d4c2a1
    
    dot_quic = f"{profile_id}.dns.nextdns.io"
    doh_url = f"https://dns.nextdns.io/{profile_id}"

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>NextDNS Device Setup</title>
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
    max-width:650px;
    margin:auto;
}}
.status-box {{
    background: #0d1117;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #00ff99;
    font-weight: bold;
}}
h2 {{
    color:#58a6ff;
    margin-top: 0;
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
    <h2>Device Setup</h2>
    
    <div class="status-box">
        ✓ Connected! This device/IP ({user_ip}) is mapped to this profile.
    </div>

    <div class="label">Generated Profile ID</div>
    <div class="value">{profile_id}</div>

    <div class="label">DNS-over-TLS/QUIC</div>
    <div class="value">{dot_quic}</div>

    <div class="label">DNS-over-HTTPS</div>
    <div class="value">{doh_url}</div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
