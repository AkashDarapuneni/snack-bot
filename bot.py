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
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 1. Go to URL
            page.goto(URL, wait_until="networkidle")
            
            # 2. Check for "Waiting" state immediately
            if "Cravings? Hold on!" in page.content():
                print("Status: Still waiting for snacks.")
                return

            # 3. CRITICAL STEP: Wait for the snack text to appear
            # We wait for the element that contains the date or snack name
            # This ensures Firebase has finished loading
            page.wait_for_selector("main", timeout=15000)
            
            # Give it 2 extra seconds just to be safe for slow connections
            page.wait_for_timeout(2000)

            # 4. Extract text from the main container
            # We look for the h1/h2 tags where "Biscuits tea milk" usually sits
            snack_text = page.locator("main").inner_text()
            
            # 5. Clean the data
            lines = [line.strip() for line in snack_text.split('\n') if line.strip()]
            
            # Filter out UI noise (Dates, "Updated at", etc.)
            ignore_list = ["Sunday", "March", "2026", "Updated", "Verified", "Snack"]
            final_items = [l for l in lines if not any(word in l for word in ignore_list)]

            if final_items:
                menu = "\n".join([f"• {item}" for item in final_items])
                message = (
                    f"🥨 *TULIPS BOYS HOSTEL UPDATE*\n\n"
                    f"✅ *Today's Menu:*\n{menu}\n\n"
                    f"🔗 [Open Portal]({URL})"
                )
                send_telegram(message)
                print(f"Success! Sent: {menu}")
            else:
                # If we found the page updated but couldn't parse the words
                send_telegram(f"🥨 *SNACK UPDATE:* Menu is updated! View here: {URL}")

            browser.close()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    get_snacks()
