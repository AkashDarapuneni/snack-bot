import os
from requests_html import HTMLSession

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram_message(text):
    import requests
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def get_snack_details():
    session = HTMLSession()
    try:
        response = session.get(URL)
        # This is the magic part: it runs the JavaScript on the page
        # sleep=2 gives the React app 2 seconds to load the snacks
        response.html.render(sleep=2)

        # Check for the 'waiting' text in the rendered HTML
        if "Cravings? Hold on!" in response.html.text:
            print("Still waiting for update...")
            return

        # Find all snack names (usually in h2 or h3 in these types of apps)
        # Based on your screen, we'll look for headings inside the <main> tag
        snacks = response.html.find('main h2, main h3, main p')
        
        found_list = []
        for s in snacks:
            name = s.text.strip()
            # Filter out dates or generic titles
            if name and "Snack" not in name and "2026" not in name:
                found_list.append(f"• {name}")

        if found_list:
            final_menu = "\n".join(found_list)
            msg = f"🥨 *SNACK UPDATE!*\n\n✅ *Today's Menu:*\n{final_menu}\n\n🔗 [Open Site]({URL})"
            send_telegram_message(msg)
        else:
            # If no specific tags found, send a general alert
            send_telegram_message(f"🥨 *Snacks are updated!* Check the site: {URL}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_snack_details()
