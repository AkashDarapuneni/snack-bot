import os
import requests
import re

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(api_url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_snacks():
    try:
        # 1. Fetch the website
        response = requests.get(URL, timeout=15)
        html_content = response.text

        # 2. Check for the "Waiting" state
        if "Cravings? Hold on!" in html_content:
            print("Snacks not updated yet.")
            return

        # 3. Extract snack name
        # We look for the text that appears between 'Sunday, March 29, 2026' and 'Updated at'
        # Or we grab the most prominent text that isn't a UI element
        snack_pattern = re.search(r'2026(.*?)Updated at', html_content, re.DOTALL | re.IGNORECASE)
        
        if snack_pattern:
            snack_name = snack_pattern.group(1).strip()
            # Clean up any HTML tags if they exist
            snack_name = re.sub('<[^<]+?>', '', snack_name).strip()
        else:
            # Fallback: Just look for common snack words or the largest text block
            snack_name = "New Snack Available (Check Site)!"

        # 4. Final Notification
        message = (
            f"🥨 *TULIPS BOYS HOSTEL UPDATE*\n\n"
            f"✅ *Today's Snack:* {snack_name}\n\n"
            f"🔗 [Open Snack Portal]({URL})"
        )
        send_telegram(message)
        print(f"Success! Found: {snack_name}")

    except Exception as e:
        print(f"Script Error: {e}")

if __name__ == "__main__":
    get_snacks()
