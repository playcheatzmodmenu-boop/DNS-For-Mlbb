from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<title>NextDNS Setup Reader</title>
<style>
body {
    background:#0d1117;
    color:white;
    font-family:Arial, sans-serif;
    padding:20px;
}
.box {
    background:#161b22;
    border:1px solid #30363d;
    border-radius:12px;
    padding:20px;
    max-width:600px;
    margin:auto;
}
h2 {
    color:#00ff99;
    margin-top: 0;
}
.section-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #58a6ff;
}
.section-desc {
    font-size: 14px;
    color: #8b949e;
    margin-bottom: 15px;
}
.item-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
}
.label {
    font-size: 12px;
    color: #8b949e;
    text-transform: uppercase;
    font-weight: bold;
    margin-bottom: 4px;
}
.value {
    font-size: 15px;
    font-family: monospace;
    color: #c9d1d9;
    word-break: break-all;
}
</style>
</head>
<body>

<div class="box">
    <h2>Endpoints</h2>
    <div class="section-desc">Set up NextDNS with this profile using one of the endpoints below.</div>

    <div class="item-card">
        <div class="label">ID</div>
        <div class="value">1165b4</div>
    </div>

    <div class="item-card">
        <div class="label">DNS-over-TLS/QUIC</div>
        <div class="value">1165b4.dns.nextdns.io</div>
    </div>

    <div class="item-card">
        <div class="label">DNS-over-HTTPS</div>
        <div class="value">https://dns.nextdns.io/1165b4</div>
    </div>

    <div class="item-card">
        <div class="label">IPv6</div>
        <div class="value">2a07:a8c0::1165b4<br>2a07:a8c1::1165b4</div>
    </div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
