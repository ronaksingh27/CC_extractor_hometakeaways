import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load environment variables
load_dotenv()

EMAIL = os.getenv("MEETUP_EMAIL")
PASSWORD = os.getenv("MEETUP_PASSWORD")

GROUPS_FILE = "config/groups.txt"  # Updated path for event IDs
LOG_FILE = "logs/rsvp_log.txt"  # Log file path

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def setup_driver():
    """Initialize Selenium WebDriver for ARM-based Ubuntu"""
    print("[INFO] Setting up the Chrome WebDriver...")
    
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"  # Ensure correct Chromium path
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # Optional: Run headless

    service = Service("/usr/bin/chromedriver")  # Ensure correct driver path
    driver = webdriver.Chrome(service=service, options=options)

    print("[SUCCESS] WebDriver initialized!")
    return driver

def login(driver):
    """Logs into Meetup using credentials from the .env file"""
    print("[INFO] Navigating to Meetup login page...")

    driver.get("https://www.meetup.com/login/")
    time.sleep(2)

    print("[INFO] Entering login credentials...")
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    login_button.click()

    time.sleep(5)  # Wait for login
    print("[SUCCESS] Logged in successfully!")

def load_group_events():
    """Reads event IDs from config/groups.txt"""
    print(f"[INFO] Loading event IDs from {GROUPS_FILE}...")

    if not os.path.exists(GROUPS_FILE):
        print(f"[ERROR] File not found: {GROUPS_FILE}")
        logging.error("groups.txt file not found!")
        return []

    with open(GROUPS_FILE, "r") as file:
        event_ids = [line.strip() for line in file if line.strip()]

    print(f"[SUCCESS] Loaded {len(event_ids)} event IDs.")
    return event_ids

def rsvp_to_event(driver, event_id):
    """RSVPs to an event using its event ID"""
    event_url = f"https://www.meetup.com/hsrmeetups/events/{event_id}/"
    print(f"[INFO] Attempting RSVP for event: {event_url}")
    logging.info(f"Attempting RSVP for event: {event_url}")

    driver.get(event_url)
    time.sleep(3)

    try:
        rsvp_button = driver.find_element(By.XPATH, "//button[contains(text(),'Attend')]")
        rsvp_button.click()
        print(f"[SUCCESS] Successfully RSVP’d to event {event_id}!")
        logging.info(f"Successfully RSVP’d to event {event_id}")
        time.sleep(2)
    except Exception as e:
        print(f"[ERROR] Failed to RSVP for event {event_id}: {e}")
        logging.error(f"Failed to RSVP for event {event_id}: {e}")

def run_bot():
    """Main function to run the Meetup auto-RSVP bot"""
    print("[INFO] Starting Meetup auto-RSVP bot...")

    driver = setup_driver()
    login(driver)

    event_ids = load_group_events()

    for event_id in event_ids:
        rsvp_to_event(driver, event_id)

    print("[INFO] Closing the browser...")
    driver.quit()
    print("[SUCCESS] Meetup auto-RSVP bot finished!")

if __name__ == "__main__":
    run_bot()
