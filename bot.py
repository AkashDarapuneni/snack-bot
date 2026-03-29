import os
import requests
import json
import re

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def get_snacks():
    try:
        # 1. Get the page source
        response = requests.get(URL, timeout=15)
        html = response.text

        # 2. Check for the "Waiting" message
        if "Cravings? Hold on!" in html:
            print("Status: Waiting for update.")
            return

        # 3. THE SECRET TRICK: Search for JSON data inside the HTML
        # React often hides its data inside a <script> tag named __NEXT_DATA__ or similar
        data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        
        snack_text = ""
        
        if data_match:
            # If it's a Next.js/React app, the data is right here!
            json_data = json.loads(data_match.group(1))
            # We look for common keys where the snack name might be hidden
            # Since I can't see the exact JSON, we'll search the whole string for the snack name
            full_json_str = json.dumps(json_data)
            # Find the text between "snackName":" and "
            name_match = re.search(r'"snackName":"(.*?)"', full_json_str)
            if name_match:
                snack_text = name_match.group(1)
        
        # 4. If the JSON trick fails, use a "Hard Search" for known items
        if not snack_text:
            # Look for common KLU snacks in the raw HTML string
            common_items = ["Biscuits", "Tea", "Milk", "Samosa", "Puff", "Chat", "Bajji"]
            found = [item for item in common_items if item.lower() in html.lower()]
            if found:
                snack_text = ", ".join(found)

        # 5. Final Send
        if snack_text:
            message = (
                f"🥨 *TULIPS HOSTEL: SNACK ALERT*\n\n"
                f"✅ *Today's Menu:* {snack_text}\n\n"
                f"🔗 [Open Portal]({URL})"
            )
        else:
            # Last resort if we still can't find the name
            message = f"🥨 *SNACK UPDATE:* The menu is updated! Check here: {URL}"

        send_telegram(message)
        print(f"Success! Sent: {snack_text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_snacks()
