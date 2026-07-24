from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(name)

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

            # hintayin ang React/JS render
            page.wait_for_timeout(5000)

            content = page.locator("body").inner_text()

            browser.close()

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>NextDNS Extractor</title>
        <style>
        body {{
            font-family: Arial;
            background:#111;
            color:#0f0;
            padding:20px;
        }}
        pre {{
            white-space:pre-wrap;
        }}
        </style>
        </head>

        <body>
        <h2>NextDNS Setup</h2>
        <pre>{content}</pre>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h2>Error</h2>
        <pre>{e}</pre>
        """


if name == "main":
    app.run(
        host="0.0.0.0",
        port=5000
    )