from flask import Flask
import requests

app = Flask(__name__)

NEXTDNS = "https://my.nextdns.io/1165b4/setup"

@app.route("/")
def index():
    try:
        # Kunin ang buong nilalaman ng site gamit ang requests
        response = requests.get(NEXTDNS, timeout=30)
        result = response.text

        return f"""
<!DOCTYPE html>
<html>

<head>
<title>NextDNS Reader</title>
<style>
body {{
    background:#0d1117;
    color:white;
    font-family:Arial;
    padding:30px;
}}
.box {{
    background:#161b22;
    border:1px solid #30363d;
    border-radius:12px;
    padding:20px;
    max-width:900px;
    margin:auto;
}}
h2 {{
    color:#00ff99;
}}
pre {{
    white-space:pre-wrap;
    font-size:16px;
    line-height:1.5;
}}
</style>
</head>

<body>
<div class="box">
<h2>NextDNS Setup Result</h2>
<pre>
{result}
</pre>
</div>
</body>

</html>
"""

    except Exception as e:
        return f"""
        <h2>Error</h2>
        <pre>{e}</pre>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
