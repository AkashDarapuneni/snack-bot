import os
import requests
from requests_html import HTMLSession

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def get_snack_details():
    session = HTMLSession()
    try:
        response = session.get(URL)
        # Give React 3 seconds to load the snacks
        response.html.render(sleep=3)

        # Check if the "Hold on" message is still visible
        if "Cravings? Hold on!" in response.html.text:
            print("Snacks not updated yet.")
            return

        # Find the snack names. We target text inside the <main> tag
        main_content = response.html.find('main', first=True)
        found_snacks = []

        if main_content:
            # We look for h2, h3, or paragraphs that contain snack names
            items = main_content.find('h2, h3, p')
            for item in items:
                name = item.text.strip()
                # Skip the date and generic titles
                if name and len(name) > 2 and "Snack" not in name and "2026" not in name:
                    found_snacks.append(f"• {name}")

        if found_snacks:
            snack_list = "\n".join(found_snacks)
            message = (
                f"🥨 *NEW SNACK UPLOADED!*\n\n"
                f"✅ *Today's Menu:*\n{snack_list}\n\n"
                f"🔗 [Open Website]({URL})"
            )
            send_telegram_message(message)
        else:
            print("Could not find specific snack names, though site is updated.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_snack_details()
