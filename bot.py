import requests
from bs4 import BeautifulSoup
import os

# These variables are pulled from GitHub Secrets for security
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram_message(text):
    """Sends a formatted message to your Telegram Channel."""
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")

def get_snack_details():
    """Scrapes the website for updated snack info."""
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We check the full text of the page first
        page_text = soup.get_text()

        # If the update hasn't happened yet, do nothing
        if "Cravings? Hold on!" in page_text:
            print("Snacks not updated yet. Checking again later...")
            return

        # If updated, we find the snack name
        # Based on your screenshots, snacks are likely inside <h2> or <h3> tags
        snacks = []
        for header in soup.find_all(['h1', 'h2', 'h3']):
            name = header.get_text().strip()
            if name and "Cravings" not in name:
                snacks.append(f"• {name}")

        if snacks:
            snack_list = "\n".join(snacks)
            message = f"🥨 *TULIPS BOYS HOSTEL: SNACK UPDATE*\n\n✅ *Today's Menu:*\n{snack_list}\n\n🔗 [View on Website]({URL})"
            send_telegram_message(message)
        else:
            send_telegram_message(f"🥨 *Snacks are updated!* Check the site for details: {URL}")

    except Exception as e:
        print(f"Error scraping website: {e}")

if __name__ == "__main__":
    get_snack_details()
