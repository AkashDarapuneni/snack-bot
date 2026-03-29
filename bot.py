import os
import requests
from bs4 import BeautifulSoup

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
        # 1. Get the page
        response = requests.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Get all text and clean it
        all_text = soup.get_text(separator=' ')
        
        # 3. Check if it's still the "Waiting" screen
        if "Cravings? Hold on!" in all_text:
            print("Status: Waiting for update.")
            return

        # 4. Extract the snack list
        # We look for the common snack items usually served at Tulips
        # This is a 'Safety Net' search
        keywords = ["Biscuits", "tea", "milk", "Samosa", "Puff", "Chat", "Mysore Bajji"]
        found_items = []
        
        for word in keywords:
            if word.lower() in all_text.lower():
                found_items.append(word.capitalize())

        # 5. Format the message
        if found_items:
            snack_str = ", ".join(found_items)
            message = f"🥨 *TULIPS HOSTEL UPDATE*\n\n✅ *Today's Snack:* {snack_str}\n\n🔗 [Open Portal]({URL})"
        else:
            # If keywords fail, just send the raw text from the middle of the page
            message = f"🥨 *SNACK UPDATE:* The menu has been updated! Check here: {URL}"

        send_telegram(message)
        print("Success: Message sent to Telegram.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_snacks()
