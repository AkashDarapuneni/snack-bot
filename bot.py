import os
import requests
from requests_html import HTMLSession

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def get_snacks():
    # Adding a User-Agent makes the request look like a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    session = HTMLSession()
    try:
        r = session.get(URL, headers=headers)
        # Wait 5 seconds for React to inject the snack names
        r.html.render(sleep=5, timeout=20)

        # 1. Check if the "Wait" message is gone
        if "Cravings? Hold on!" in r.html.text:
            print("Snacks not yet uploaded.")
            return

        # 2. Find snack names specifically inside the <main> section
        main_content = r.html.find('main', first=True)
        if not main_content:
            print("Could not find main content.")
            return

        # Get all headings and paragraphs
        elements = main_content.find('h1, h2, h3, p')
        found_snacks = []
        
        for el in elements:
            name = el.text.strip()
            # Logic: Skip dates (2026), generic titles, and short noise
            if name and len(name) > 2 and "Snack" not in name and "2026" not in name:
                found_snacks.append(f"• {name}")

        # 3. Send if we found items
        if found_snacks:
            # Use set() to remove any duplicate names found
            unique_snacks = list(dict.fromkeys(found_snacks))
            menu = "\n".join(unique_snacks)
            msg = f"🥨 *TULIPS HOSTEL: SNACK ALERT*\n\n✅ *Today's Menu:*\n{menu}\n\n🔗 [Open Website]({URL})"
            send_telegram(msg)
            print("Success! Message sent.")
        else:
            print("Site updated but no snack names extracted.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_snacks()
