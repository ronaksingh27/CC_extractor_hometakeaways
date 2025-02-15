import os
import logging
import time
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random

def setup_driver():
    """Initialize Chrome WebDriver with anti-detection settings"""
    print("[INFO] Setting up Chrome WebDriver...")

    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"  # Correct Chromium path
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Hides automation
    options.add_argument("--incognito")  # Use incognito mode
    options.add_argument("--disable-extensions")  # Prevent extension detection
    options.add_argument("--disable-popup-blocking")  # Avoid pop-ups blocking actions
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hide automation flag
    options.add_experimental_option("useAutomationExtension", False)

    # Randomize user-agent to avoid detection
    user_agent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ])
    options.add_argument(f"user-agent={user_agent}")

    service = Service("/usr/bin/chromedriver")  # Ensure correct driver path
    driver = webdriver.Chrome(service=service, options=options)

    # Remove `navigator.webdriver` flag to prevent detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Remove additional fingerprints
    driver.execute_script("""
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});
    """)

    print("[SUCCESS] WebDriver initialized!")
    return driver

def human_like_delay():
    """Randomized delay to simulate human browsing"""
    time.sleep(random.uniform(2, 5))  # Wait 2-5 seconds

def move_mouse_randomly(driver):
    """Simulates human-like random mouse movement"""
    actions = webdriver.ActionChains(driver)
    for _ in range(random.randint(3, 7)):
        x_offset = random.randint(-50, 50)
        y_offset = random.randint(-50, 50)
        actions.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.1, 0.3))


def login(driver):
    """Logs into Meetup using credentials from .env file"""
    print("[INFO] Navigating to Meetup login page...")

    driver.get("https://www.meetup.com/login/")

    # human_like_delay()  # Simulate human behavior
    # move_mouse_randomly(driver)  # Simulate mouse movement

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

        time.sleep(5)
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

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

def rsvp_to_event(driver, event_id):
    """RSVPs to an event using its event ID with debug logging"""
    event_url = f"https://www.meetup.com/mumbai-weekend-events/events/{event_id}/"
    print(f"[INFO] Attempting RSVP for event: {event_url}")
    logging.info(f"Attempting RSVP for event: {event_url}")

    driver.get(event_url)
    wait = WebDriverWait(driver, 15)  # Increased wait time for slow loading

    try:
        print("[DEBUG] Waiting for the RSVP button to be present on the page...")
        rsvp_button =  wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='attend-irl-btn']")  # Using data-testid
        ))
        print(f"[DEBUG] RSVP button found! Text: '{rsvp_button.text}'")

        print("[DEBUG] Scrolling to the RSVP button to make sure it's visible...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", rsvp_button)
        print("[DEBUG] Scrolling complete.")

        print("[DEBUG] Waiting for the RSVP button to become clickable...")
        wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='attend-irl-btn']")  # Using data-testid
        ))
        print("[DEBUG] RSVP button is now clickable!")

        print("[DEBUG] Attempting to click the RSVP button...")
        try:
            #rsvp_button.click()
            
            # print("[SUCCESS] RSVP button clicked successfully!")
            print("[DEBUG] Clicking Attend button via JavaScript...")
            driver.execute_script("arguments[0].style.border='3px solid red'; arguments[0].style.backgroundColor='yellow';", rsvp_button)
        except:
            print("[WARNING] Normal click failed, using JavaScript click...")
            driver.execute_script("arguments[0].click();", rsvp_button)

        print("[DEBUG] Waiting for redirection to RSVP confirmation page...")
        time.sleep(20)  # Allow time for redirection

        # Verify if URL contains "/rsvp"
        current_url = driver.current_url
        print(f"[DEBUG] Current URL: {current_url}")

        if "rsvp" in current_url:
            print("[SUCCESS] RSVP confirmed! Booking successful.")
            logging.info(f"RSVP successful for event {event_id}")
        else:
            print("[ERROR] RSVP failed! No confirmation page detected.")
            logging.error(f"RSVP failed for event {event_id}")


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
