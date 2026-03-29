import requests
from bs4 import BeautifulSoup
import os

# These come from your GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
TARGET_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_to_telegram(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": TARGET_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def check_website():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This looks for the text on the page
        page_text = soup.get_text()

        # If "Cravings" is NOT there, it means they updated the snack!
        if "Cravings? Hold on!" not in page_text:
            # We try to grab the snack name from the H2 tag
            snack_element = soup.find('h2')
            snack_name = snack_element.text.strip() if snack_element else "New Snack Available!"
            
            message = f"🥨 *SNACK UPDATE!*\n\n✅ Today's Menu: *{snack_name}*\n🔗 [Open Website]({URL})"
            send_to_telegram(message)
            print("Message sent to channel!")
        else:
            print("Still waiting for update...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_website()
