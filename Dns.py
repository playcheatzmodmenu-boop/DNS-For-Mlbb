from flask import Flask, request, render_template_string, redirect, url_for, session
import secrets
import string
import socket
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATABASE_KEYS = {
    "ADMIN-MASTER-KEY": True
}

# Listahan ng 3 NextDNS configurations na pagpipilian
DNS_POOL = [
    {
        "profile_id": "5717aa",
        "dot_quic": "5717aa.dns.nextdns.io",
        "doh_url": "https://dns.nextdns.io/5717aa"
    },
    {
        "profile_id": "5bf32b",
        "dot_quic": "5bf32b.dns.nextdns.io",
        "doh_url": "https://dns.nextdns.io/5bf32b"
    },
    {
        "profile_id": "6c527e",
        "dot_quic": "6c527e.dns.nextdns.io",
        "doh_url": "https://dns.nextdns.io/6c527e"
    }
]

def get_fastest_dns():
    best_dns = DNS_POOL[0]
    lowest_ping = float('inf')

    for dns in DNS_POOL:
        total_time = 0
        success_count = 0
        # Susubukan natin mag-connect nang 2 beses para makuha ang average ping
        for _ in range(2):
            try:
                start_time = time.time()
                # Port 443 para sa DoT/HTTPS check
                sock = socket.create_connection((dns["dot_quic"], 443), timeout=1.5)
                sock.close()
                latency = (time.time() - start_time) * 1000 # convert to ms
                total_time += latency
                success_count += 1
            except Exception:
                pass
        
        if success_count > 0:
            avg_ping = total_time / success_count
            if avg_ping < lowest_ping:
                lowest_ping = avg_ping
                best_dns = dns
        
    return best_dns

# ----------------- ADMIN LOGIN (For Panel) -----------------
@app.route("/panel-login", methods=["GET", "POST"])
def panel_login():
    error = ""
    if request.method == "POST":
        admin_pass = request.form.get("password", "")
        if admin_pass == "slider123":
            session['admin_logged'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "Invalid panel password!"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Admin Panel Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { 
    background: #0d1117; 
    color: white; 
    font-family: 'Segoe UI', Arial, sans-serif; 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
}
.box { 
    background: #161b22; 
    border: 1px solid #30363d; 
    border-radius: 16px; 
    padding: 35px; 
    width: 100%; 
    max-width: 400px; 
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    text-align: center; 
}
h2 { color: #58a6ff; margin-bottom: 20px; font-size: 22px; }
input { 
    width: 100%; 
    padding: 14px; 
    background: #0d1117; 
    border: 1px solid #30363d; 
    border-radius: 8px; 
    color: white; 
    font-size: 16px; 
    margin-bottom: 20px; 
    text-align: center; 
    outline: none;
    transition: border 0.3s;
}
input:focus { border-color: #58a6ff; }
button { 
    background: #da3633; 
    color: white; 
    border: none; 
    padding: 14px; 
    border-radius: 8px; 
    font-weight: bold; 
    cursor: pointer; 
    width: 100%; 
    font-size: 16px; 
    transition: background 0.3s;
}
button:hover { background: #f85149; }
.error { color: #ff5555; font-size: 14px; margin-bottom: 15px; background: rgba(255,85,85,0.1); padding: 10px; border-radius: 6px; border: 1px solid rgba(255,85,85,0.3); }
</style>
</head>
<body>
<div class="box">
    <h2>Admin Password</h2>
    <form method="POST">
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <input type="password" name="password" placeholder="Enter password" required autocomplete="off">
        <button type="submit">Access Panel</button>
    </form>
</div>
</body>
</html>
""", error=error)

# ----------------- ADMIN PANEL (Key Generator) -----------------
@app.route("/panel", methods=["GET", "POST"])
def admin_panel():
    if not session.get('admin_logged'):
        return redirect(url_for('panel_login'))

    msg = ""
    if request.method == "POST":
        chars = string.ascii_uppercase + string.digits
        key_part1 = ''.join(secrets.choice(chars) for _ in range(4))
        key_part2 = ''.join(secrets.choice(chars) for _ in range(4))
        new_key = f"DNS-{key_part1}-{key_part2}"
        
        DATABASE_KEYS[new_key] = True
        msg = f"Generated: {new_key}"

    keys_list_html = ""
    for k, status in DATABASE_KEYS.items():
        st_label = '<span style="color:#00ff99;">Active</span>' if status else '<span style="color:#ff5555;">Used</span>'
        keys_list_html += f"<li style='margin-bottom: 8px;'><b>{k}</b> — {st_label}</li>"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Admin Key Panel</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background:#0d1117; color:white; font-family:'Segoe UI', Arial, sans-serif; padding:20px; display:flex; justify-content:center; align-items:center; min-height:100vh; }
.box { background:#161b22; border:1px solid #30363d; border-radius:16px; padding:30px; width:100%; max-width:600px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
h2 { color:#58a6ff; margin-bottom: 20px; }
button { background:#238636; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; cursor:pointer; width: 100%; font-size: 16px; transition: background 0.3s; }
button:hover { background:#2ea043; }
.key-box { background:#0d1117; padding:12px; border:1px solid #30363d; border-radius:8px; font-family:monospace; color:#00ff99; margin-top:15px; font-size: 15px; text-align: center; }
ul { padding-left: 20px; line-height: 1.6; margin-top: 10px; max-height: 250px; overflow-y: auto; }
</style>
</head>
<body>
<div class="box">
    <h2>Key Generator Panel</h2>
    <form method="POST">
        <button type="submit">+ Generate New Key</button>
    </form>
    {% if msg %}
        <div class="key-box">{{ msg }}</div>
    {% endif %}
    
    <h3 style="color:#c9d1d9; margin-top:25px; font-size: 16px;">Generated Keys History:</h3>
    <ul>
        {{ keys_list_html | safe }}
    </ul>
</div>
</body>
</html>
""", msg=msg, keys_list_html=keys_list_html)

# ----------------- LOGIN PAGE (For Users) -----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        user_key = request.form.get("key", "").strip()
        
        if user_key in DATABASE_KEYS and DATABASE_KEYS[user_key] == True:
            DATABASE_KEYS[user_key] = False # 1-time use only
            session['authorized_key'] = user_key
            return redirect(url_for('dns_dashboard'))
        else:
            error = "Invalid key, already expired, or already used!"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>NextDNS - Secure Access</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { 
    background: #0d1117; 
    color: white; 
    font-family: 'Segoe UI', Arial, sans-serif; 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
}
.box { 
    background: #161b22; 
    border: 1px solid #30363d; 
    border-radius: 16px; 
    padding: 40px 30px; 
    width: 90%; 
    max-width: 420px; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    text-align: center; 
}
.logo-icon {
    font-size: 36px;
    margin-bottom: 10px;
}
h2 { 
    color: #ffffff; 
    font-size: 22px; 
    margin-bottom: 8px; 
}
p.subtitle {
    color: #8b949e;
    font-size: 14px;
    margin-bottom: 25px;
}
input { 
    width: 100%; 
    padding: 14px 16px; 
    background: #0d1117; 
    border: 1px solid #30363d; 
    border-radius: 8px; 
    color: #00ff99; 
    font-size: 16px; 
    font-family: monospace;
    letter-spacing: 1px;
    margin-bottom: 20px; 
    text-align: center; 
    outline: none;
    transition: all 0.3s ease;
}
input:focus { 
    border-color: #00ff99; 
    box-shadow: 0 0 8px rgba(0, 255, 153, 0.2);
}
button { 
    background: #1f6feb; 
    color: white; 
    border: none; 
    padding: 14px; 
    border-radius: 8px; 
    font-weight: bold; 
    cursor: pointer; 
    width: 100%; 
    font-size: 16px; 
    transition: background 0.3s, transform 0.1s;
}
button:hover { background: #388bfd; }
button:active { transform: scale(0.98); }
.error { 
    color: #ff5555; 
    font-size: 13px; 
    background: rgba(255, 85, 85, 0.1); 
    border: 1px solid rgba(255, 85, 85, 0.3); 
    padding: 10px; 
    border-radius: 6px; 
    margin-bottom: 20px; 
}
</style>
</head>
<body>
<div class="box">
    <div class="logo-icon">🛡️</div>
    <h2>Enter Access Key</h2>
    <p class="subtitle">Please enter your key to get the DNS setup</p>
    <form method="POST">
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <input type="text" name="key" placeholder="DNS-XXXX-XXXX" required autocomplete="off">
        <button type="submit">Access DNS</button>
    </form>
</div>
</body>
</html>
""", error=error)

# ----------------- DNS DASHBOARD (One-time view) -----------------
@app.route("/dashboard")
def dns_dashboard():
    if 'authorized_key' not in session:
        return redirect(url_for('login'))
    
    session.pop('authorized_key', None)

    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        user_ip = request.remote_addr

    # Piliin ang pinakamabilis na DNS base sa ping test para sa user na ito
    fastest = get_fastest_dns()
    profile_id = fastest["profile_id"]
    dot_quic = fastest["dot_quic"]
    doh_url = fastest["doh_url"]

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>NextDNS Device Setup</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background:#0d1117; color:white; font-family:'Segoe UI', Arial, sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; padding:20px; }
.box { background:#161b22; border:1px solid #30363d; border-radius:16px; padding:30px; width:100%; max-width:600px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
.status-box { background: rgba(255,85,85,0.1); border: 1px solid rgba(255,85,85,0.3); padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #ff5555; font-size: 14px; line-height: 1.5; font-weight: bold; text-align: center; }
h2 { color:#58a6ff; margin-bottom: 5px; font-size: 22px; }
.label { font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: bold; margin-top: 15px; letter-spacing: 0.5px; }
.value { font-size: 15px; font-family: monospace; color: #00ff99; background: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid #30363d; word-break: break-all; margin-top: 5px; }
</style>
</head>
<body>

<div class="box">
    <h2>Private Dns Protection</h2>
    <p style="color: #8b949e; font-size: 13px; margin-bottom: 20px;">ViP Access Only (Optimized Lowest Ping)</p>
    
    <div class="status-box">
        ⚠️ WARNING: If you reload or press the back button, this access will be gone! Copy it immediately.
    </div>

    <div class="label">Generated Profile ID</div>
    <div class="value">{{ profile_id }}</div>

    <div class="label">DNS-over-TLS/QUIC</div>
    <div class="value">{{ dot_quic }}</div>

    <div class="label">DNS-over-HTTPS</div>
    <div class="value">{{ doh_url }}</div>
</div>

</body>
</html>
""", user_ip=user_ip, profile_id=profile_id, dot_quic=dot_quic, doh_url=doh_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
