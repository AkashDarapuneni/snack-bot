import requests
from bs4 import BeautifulSoup
import os

# Secrets from GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def get_snack_details():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Check if the "Wait" message is still there
        page_text = soup.get_text()
        if "Cravings? Hold on!" in page_text:
            print("Snacks not updated yet.")
            return

        # 2. Extract specific snack names
        # We target the <main> tag from your screenshot and look for headings or bold text
        main_content = soup.find('main')
        found_snacks = []

        if main_content:
            # Most likely the snack name is in an <h2>, <h3>, or a <span> with text
            for item in main_content.find_all(['h2', 'h3', 'p']):
                text = item.get_text().strip()
                # We skip generic text like the date or "Today's Evening Snack"
                if text and len(text) > 1 and "Snack" not in text and "2026" not in text:
                    found_snacks.append(f"• {text}")

        # 3. Format and Send
        if found_snacks:
            # This creates the list of actual snacks (e.g., Biscuits, Tea)
            snack_list = "\n".join(found_snacks)
            message = (
                f"🥨 *NEW SNACK UPLOADED!*\n\n"
                f"✅ *Today's Menu:*\n{snack_list}\n\n"
                f"🔗 [Open Website]({URL})"
            )
        else:
            # Fallback if we can't find specific tags
            message = f"🥨 *Snacks are updated!* Check the site for details: {URL}"
            
        send_telegram_message(message)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_snack_details()
