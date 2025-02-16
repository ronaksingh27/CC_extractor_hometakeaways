import requests
import json
import time
from bs4 import BeautifulSoup

# Configuration
MEETUP_USERNAME = "ronaksingh2708@gmail.com"
MEETUP_PASSWORD = "Borosil@55"
GROUPS = ["mumbai-weekend-events", "group2"]  # List of groups to auto-RSVP
LOGIN_URL = "https://secure.meetup.com/login/"
BASE_URL = "https://www.meetup.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

session = requests.Session()


def login():
    """Logs in to Meetup.com"""
    print("Attempting to log in...")
    response = session.get(LOGIN_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("meta", {"name": "next_csrf"})["content"]

    # print(soup)
    print(csrf_token)
    
    payload = {
        "email": MEETUP_USERNAME,
        "password": MEETUP_PASSWORD,
        "next": "/",
        "csrf": csrf_token,
    }

    # print(payload)
    
    login_response = session.post(LOGIN_URL, data=payload, headers=HEADERS)
    # print(login_response)
    
    if( login_response.status_code == 200 ):
        print("Login successfull")
    else :
        print("Login failed")

    return login_response.status_code == 200



def find_events(group):
    """Finds upcoming events for a specific group."""
    print(f"Searching events for group: {group}")
    url = f"{BASE_URL}{group}/events/"

    print(url)
    response = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # print(soup)
    print(response)
    print(soup.find_all("a",href=True))
    
    for link in soup.find_all("a", href=True):
        if "/events/" in link["href"]:
            events.append(link["href"])
    
    print(f"Found {len(events)} events for group: {group}")
    return events


def rsvp_event(event_url):
    """RSVPs to a given event."""
    print(f"Attempting to RSVP for event: {event_url}")
    response = session.get(event_url, headers=HEADERS)
    print(event_url)

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("meta", {"name": "next_csrf"})["content"]
    print(csrf_token)

    event_id = event_url.split("/")[-2]
    rsvp_url = f"{event_url}/rsvp" 

    print(event_id,rsvp_url)
    
    payload = json.dumps({"response": "yes"})
    headers = {
        "Content-Type": "application/json",
        "Csrf-Token": csrf_token,
    }
    
    rsvp_response = session.post(rsvp_url, data=payload, headers=headers)
    success = rsvp_response.status_code == 200
    print(f"RSVP {'successful' if success else 'failed'} for event: {event_url}")
    return success


if __name__ == "__main__":
    if login():
        for group in GROUPS:
            events = find_events(group)
            for event in events:
                if rsvp_event(event):
                    print(f"Successfully RSVP'd to {event}")
                time.sleep(5)  # Avoid rate limiting
    else:
        print("Login failed.")
