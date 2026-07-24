from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

NEXTDNS = "https://my.nextdns.io/1165b4/setup"

@app.route("/")
def index():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            )
            page = browser.new_page()
            page.goto(NEXTDNS, wait_until="networkidle", timeout=60000)
            
            # Hintayin mag-load ang mismong laman gamit ang JavaScript
            page.wait_for_timeout(5000)
            
            result = page.locator("body").inner_text()
            browser.close()

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
    
