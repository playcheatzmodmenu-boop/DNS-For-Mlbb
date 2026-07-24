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

            page.wait_for_timeout(5000)

            text = page.locator("body").inner_text()

            browser.close()

        return f"""
        <html>
        <body>
        <h2>NextDNS Result</h2>
        <pre>{text}</pre>
        </body>
        </html>
        """

    except Exception as e:
        return f"<pre>{e}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
