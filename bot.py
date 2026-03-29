import os
import requests
from playwright.sync_api import sync_playwright

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
URL = "https://klu-snack-update.vercel.app"

def send_telegram(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

def get_snacks():
    with sync_playwright() as p:
        try:
            # Launch browser in headless mode (no window)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Go to the site and wait for the network to stop loading
            page.goto(URL, wait_until="networkidle")
            
            # 1. Check if the "Wait" message is there
            if "Cravings? Hold on!" in page.content():
                print("Status: Still waiting for snacks.")
                return

            # 2. Wait for the snack card to appear (The white box in your screenshot)
            # We wait up to 10 seconds for the text to change from 'Loading' to actual snacks
            page.wait_for_timeout(5000) 

            # 3. Target the specific area where "Biscuits tea milk" is written
            # Based on your screenshot, it's inside the main container
            snack_element = page.locator("main") 
            full_text = snack_element.inner_text()

            # 4. Clean up the text
            # We remove the date and the "Updated at" time to keep just the snacks
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            # Usually, the snack names are the largest text or follow the date
            # We filter out known UI words
            bad_words = ["Sunday", "March", "2026", "Updated", "Verified", "students", "Evening Snack"]
            final_snacks = [l for l in lines if not any(word in l for word in bad_words)]

            if final_snacks:
                snack_result = "\n".join([f"• {s}" for s in final_snacks])
                message = (
                    f"🥨 *TULIPS BOYS HOSTEL: SNACK ALERT*\n\n"
                    f"✅ *Today's Menu:*\n{snack_result}\n\n"
                    f"🔗 [Open Portal]({URL})"
                )
                send_telegram(message)
                print(f"Success! Sent: {snack_result}")
            else:
                # Fallback if text extraction is tricky
                send_telegram(f"🥨 *SNACK UPDATE:* The menu is updated! Check here: {URL}")

            browser.close()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    get_snacks()
