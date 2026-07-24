from flask import Flask, request, render_template_string, redirect, url_for, session
import secrets
import string

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # Kailangan para sa session management

# Pansamantalang lagayan ng mga generated keys (Sa memory muna natin ilagay)
# Format: { "KEY-XXXX": True (Active) / False (Used) }
DATABASE_KEYS = {
    "ADMIN-MASTER-KEY": True # Default master key para masubukan mo agad
}

# ----------------- ADMIN PANEL (Paggawa ng Key) -----------------
@app.route("/panel", methods=["GET", "POST"])
def admin_panel():
    msg = ""
    new_key = ""
    if request.method == "POST":
        # Gumawa ng random generated key (Halimbawa: DNS-A9X2-7B4K)
        chars = string.ascii_uppercase + string.digits
        key_part1 = ''.join(secrets.choice(chars) for _ in range(4))
        key_part2 = ''.join(secrets.choice(chars) for _ in range(4))
        new_key = f"DNS-{key_part1}-{key_part2}"
        
        # I-save sa database keys na active
        DATABASE_KEYS[new_key] = True
        msg = f"Successfully generated key: {new_key}"

    keys_list_html = ""
    for k, status in DATABASE_KEYS.items():
        st_label = '<span style="color:#00ff99;">Active (Unused)</span>' if status else '<span style="color:#ff5555;">Used / Expired</span>'
        keys_list_html += f"<li><b>{k}</b> - {st_label}</li>"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Admin Key Panel</title>
<style>
body { background:#0d1117; color:white; font-family:Arial, sans-serif; padding:30px; }
.box { background:#161b22; border:1px solid #30363d; border-radius:12px; padding:20px; max-width:600px; margin:auto; }
h2 { color:#58a6ff; }
button { background:#238636; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; }
button:hover { background:#2ea043; }
.key-box { background:#0d1117; padding:10px; border:1px solid #30363d; border-radius:6px; font-family:monospace; color:#00ff99; margin-top:10px; }
ul { padding-left: 20px; line-height: 1.8; }
</style>
</head>
<body>
<div class="box">
    <h2>Key Generator Panel</h2>
    <form method="POST">
        <button type="submit">Generate New Key</button>
    </form>
    {% if msg %}
        <div class="key-box">{{ msg }}</div>
    {% endif %}
    
    <h3 style="color:#c9d1d9; margin-top:30px;">All Generated Keys:</h3>
    <ul>
        {{ keys_list_html | safe }}
    </ul>
    <p style="font-size:12px; color:#8b949e; margin-top:20px;"><a href="/" style="color:#58a6ff;">Pumunta sa Login Page</a></p>
</div>
</body>
</html>
""", msg=msg, keys_list_html=keys_list_html)

# ----------------- LOGIN PAGE (Gamit ang Key) -----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        user_key = request.form.get("key", "").strip()
        
        # Suriin kung valid at active pa ang key
        if user_key in DATABASE_KEYS and DATABASE_KEYS[user_key] == True:
            # I-burn / i-disable agad ang key para 1-time use lang!
            DATABASE_KEYS[user_key] = False
            
            # I-save sa session ng browser na logged in na sya
            session['authorized_key'] = user_key
            return redirect(url_for('dns_dashboard'))
        else:
            error = "Invalid key, expired na, o nagamit na!"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Login - DNS Access</title>
<style>
body { background:#0d1117; color:white; font-family:Arial, sans-serif; padding:50px; }
.box { background:#161b22; border:1px solid #30363d; border-radius:12px; padding:30px; max-width:400px; margin:auto; text-align:center; }
input { width:90%; padding:12px; background:#0d1117; border:1px solid #30363d; border-radius:6px; color:white; font-size:16px; margin-bottom:15px; text-align:center; }
button { background:#1f6feb; color:white; border:none; padding:12px 20px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%; font-size:16px; }
button:hover { background:#388bfd; }
.error { color:#ff5555; font-size:14px; margin-bottom:15px; }
</style>
</head>
<body>
<div class="box">
    <h2>Enter Access Key</h2>
    <form method="POST">
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <input type="text" name="key" placeholder="ILAGAY ANG KEY DITO" required autocomplete="off">
        <button type="submit">Login</button>
    </form>
    <p style="font-size:12px; color:#8b949e; margin-top:20px;"><a href="/panel" style="color:#58a6ff;">Punta sa Admin Panel</a></p>
</div>
</body>
</html>
""", error=error)

# ----------------- DNS DASHBOARD (Isang beses lang ma-a-access) -----------------
@app.route("/dashboard")
def dns_dashboard():
    # Suriin kung galing sa matagumpay na login ang user
    if 'authorized_key' not in session:
        return redirect(url_for('login'))
    
    # Alisin agad sa session pagka-load para kapag nag-refresh/ni-reload nya, bawal na!
    session.pop('authorized_key', None)

    # Kunin ang IP ng device para sa profile mapping
    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        user_ip = request.remote_addr

    device_id = abs(hash(user_ip)) % 1000000
    profile_id = f"d{device_id:06x}"
    dot_quic = f"{profile_id}.dns.nextdns.io"
    doh_url = f"https://dns.nextdns.io/{profile_id}"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>NextDNS Device Setup</title>
<style>
body { background:#0d1117; color:white; font-family:Arial, sans-serif; padding:30px; }
.box { background:#161b22; border:1px solid #30363d; border-radius:12px; padding:20px; max-width:650px; margin:auto; }
.status-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #ff5555; font-weight: bold; }
h2 { color:#58a6ff; margin-top: 0; }
.label { font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: bold; margin-top: 15px; }
.value { font-size: 15px; font-family: monospace; color: #c9d1d9; background: #0d1117; padding: 10px; border-radius: 6px; border: 1px solid #30363d; word-break: break-all; }
</style>
</head>
<body>

<div class="box">
    <h2>Device Setup (One-Time View)</h2>
    
    <div class="status-box">
        ⚠️ PAALALA: Kapag nire-load o pinindot mo ang back button, mawawala na ang access na ito! Kopyahin mo na agad.
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
        
