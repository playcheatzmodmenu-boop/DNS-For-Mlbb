from flask import Flask
import requests

app = Flask(__name__)

NEXTDNS = "https://my.nextdns.io/1165b4/setup"

@app.route("/")
def index():
    try:
        # Nilagyan natin ng User-Agent para magmukhang galing sa totoong browser ang request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(NEXTDNS, headers=headers, timeout=30)
        result = response.text

        # Kung sakaling nagbalik ito ng HTML, pwede nating ipalabas sa pre tag
        # o kaya naman ay diretso nang basahin ng backend mo nang hindi nakikita ng iba ang link.
        html_content = f"""<!DOCTYPE html>
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
<h2>NextDNS Setup Data (Hidden Fetch)</h2>
<pre>{result}</pre>
</div>
</body>
</html>"""
        return html_content

    except Exception as e:
        return f"""
        <h2>Error</h2>
        <pre>{e}</pre>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    padding:30px;
}
.box {
    background:#161b22;
    border:1px solid #30363d;
    border-radius:12px;
    padding:20px;
    max-width:900px;
    margin:auto;
}
h2 {
    color:#00ff99;
}
pre {
    white-space:pre-wrap;
    font-size:16px;
    line-height:1.5;
}
</style>
</head>
<body>
<div class="box">
<h2>NextDNS Setup Result</h2>
<pre>""" + result + """</pre>
</div>
</body>
</html>"""
        return html_content

    except Exception as e:
        return f"""
        <h2>Error</h2>
        <pre>{e}</pre>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
