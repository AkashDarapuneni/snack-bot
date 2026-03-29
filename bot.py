import os
import requests

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
# This is the actual data source for the Tulips Hostel portal
DATA_URL = "https://klu-snack-update.vercel.app/data.json" 

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def get_snacks():
    try:
        # 1. Get the raw data directly
        response = requests.get(DATA_URL, timeout=10)
        data = response.json()

        # 2. Check if snacks are "Waiting" or "Ready"
        # Most of these KLU portals use a status flag
        if data.get("status") == "waiting" or "Cravings" in str(data):
            print("Snacks not updated yet.")
            return

        # 3. Get the snack name from the data file
        # It is usually under a key like 'name', 'snack', or 'items'
        snack_name = data.get("snackName") or data.get("items") or data.get("name")
        
        if not snack_name:
            # If the JSON format is different, we try to grab the first value
            snack_name = list(data.values())[0]

        # 4. Send the message
        message = (
            f"🥨 *TULIPS BOYS HOSTEL: SNACK ALERT*\n\n"
            f"✅ *Today's Menu:* {snack_name}\n\n"
            f"🔗 [Open Portal](https://klu-snack-update.vercel.app)"
        )
        send_telegram(message)
        print(f"Success! Notified about: {snack_name}")

    except Exception as e:
        # If the JSON trick fails, we use a simple text search as backup
        print("JSON failed, trying text backup...")
        r = requests.get("https://klu-snack-update.vercel.app")
        if "Biscuits" in r.text or "Tea" in r.text:
            send_telegram(f"🥨 *SNACK UPDATE:* Biscuits, Tea, Milk are ready!")

if __name__ == "__main__":
    get_snacks()
