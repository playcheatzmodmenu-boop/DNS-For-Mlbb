from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

NEXTDNS_URL = "https://my.nextdns.io/1165b4/setup"


@app.route("/")
def home():
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page()

            page.goto(
                NEXTDNS_URL,
                wait_until="networkidle",
                timeout=60000
            )

            # hintayin ang JavaScript render
            page.wait_for_timeout(8000)

            text = page.locator("body").inner_text()

            browser.close()


        return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>NextDNS Extractor</title>

        <style>
        body {{
            background:#111;
            color:#00ff88;
            font-family:Arial;
            padding:20px;
        }}

        .box {{
            background:#222;
            padding:20px;
            border-radius:10px;
        }}

        pre {{
            white-space:pre-wrap;
            font-size:16px;
        }}
        </style>

        </head>

        <body>

        <div class="box">

        <h2>NextDNS Setup</h2>

        <pre>{text}</pre>

        </div>

        </body>
        </html>
        """


    except Exception as e:

        return f"""
        <html>
        <body>
        <h2>Error</h2>
        <pre>{e}</pre>
        </body>
        </html>
        """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
