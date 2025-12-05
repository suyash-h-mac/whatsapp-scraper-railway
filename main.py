import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---------------------------------------
# GOOGLE SHEETS SETUP
# ---------------------------------------
SHEET_ID = "1WFs84wUvlH2Gf8kUIk1Wp3piEpUH2XJl6mUWfgyakBc"
TAB_NAME = "1C"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(TAB_NAME)

# ---------------------------------------
# SELENIUM SETUP
# ---------------------------------------
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    browser = webdriver.Chrome(options=chrome_options)
    return browser

# ---------------------------------------
# SCRAPE WHATSAPP
# ---------------------------------------
def read_group_counts():
    browser = get_browser()

    browser.get("https://web.whatsapp.com")
    print("Waiting for QR scan...")
    time.sleep(30)  # Scan QR manually once; Railway will reuse session

    time.sleep(5)

    # Find groups (simple unread bubble scraping)
    elements = browser.find_elements("css selector", "span[aria-label*='unread messages']")

    total_unread = sum(int(el.get_attribute("aria-label").split()[0]) for el in elements)

    browser.quit()
    return total_unread

# ---------------------------------------
# MAIN EXECUTION
# ---------------------------------------
def main():
    sheet = get_sheet()

    unread = read_group_counts()
    print("Unread:", unread)

    sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), unread])

if __name__ == "__main__":
    main()
