import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()
EMAIL = os.getenv("MEETUP_EMAIL")
PASSWORD = os.getenv("MEETUP_PASSWORD")

# Configuration paths
GROUPS_FILE = "config/groups.txt"
LOG_FILE = "logs/rsvp_log.txt"

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
    """Logs into Meetup using credentials from .env file"""
    print("[INFO] Navigating to Meetup login page...")

    driver.get("https://www.meetup.com/login/")
    wait = WebDriverWait(driver, 10)

    try:
        # Locate and enter email
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(EMAIL)

        # Locate and enter password
        password_input = wait.until(EC.presence_of_element_located((By.ID, "current-password")))
        password_input.send_keys(PASSWORD)

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
        login_button.click()

        # Wait for login success by checking redirected URL
        # wait.until(EC.url_contains("/home"))

        print("[SUCCESS] Logged in successfully!")
        logging.info("Login successful.")
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        logging.error(f"Login failed: {e}")
        driver.quit()
        exit()

def load_group_events():
    """Reads event IDs from groups.txt"""
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
    """RSVPs to an event using its event ID with debug logging"""
    event_url = f"https://www.meetup.com/hsrmeetups/events/{event_id}/"
    print(f"[INFO] Attempting RSVP for event: {event_url}")
    logging.info(f"Attempting RSVP for event: {event_url}")

    driver.get(event_url)
    wait = WebDriverWait(driver, 15)  # Increased wait time for slow loading

    try:
        print("[DEBUG] Waiting for the RSVP button to be present on the page...")
        rsvp_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/main/div[4]/div/div/div[2]/div/div[2]/button")
        ))
        print("[DEBUG] RSVP button found on the page!")

        print("[DEBUG] Scrolling to the RSVP button to make sure it's visible...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", rsvp_button)
        print("[DEBUG] Scrolling complete.")

        print("[DEBUG] Waiting for the RSVP button to become clickable...")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/main/div[4]/div/div/div[2]/div/div[2]/button")
        ))
        print("[DEBUG] RSVP button is now clickable!")

        print("[DEBUG] Clicking the RSVP button...")
        rsvp_button.click()
        print(f"[SUCCESS] Successfully RSVP’d to event {event_id}!")
        logging.info(f"Successfully RSVP’d to event {event_id}")

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
