import requests
import json
import time
from bs4 import BeautifulSoup
import re
import json

# Configuration
MEETUP_USERNAME = "ronaksingh2708@gmail.com"
MEETUP_PASSWORD = "Borosil@55"
GROUPS = ["mumbai-weekend-events", "group2"]  # List of groups to auto-RSVP
LOGIN_URL = "https://www.meetup.com/gql"
RSVP_URL = "https://www.meetup.com/gql2"
BASE_URL = "https://www.meetup.com/"

# Session setup
session = requests.Session()

# Set cookies manually
session.cookies.set("memberid", "467065603")
session.cookies.set("isspooner", "false")
session.cookies.set("meetup_session", "bbb84a01-5e9e-4768-87f7-d317246882d9")
session.cookies.set("__meetup_auth_access_token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0NjcwNjU2MDMiLCJuYmYiOjE3Mzk3MDc2NjMsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJyZWZyZXNoX3Rva2Vuc19jaGFpbl9pZCI6ImI0YTQxNTE2LTdhYWMtNGVhZi04NDIwLWE2ZWJmMDc4OGY4OCIsImV4cCI6MTczOTcxMTI2MywiaWF0IjoxNzM5NzA3NjYzLCJqdGkiOiJmNjQwZjI2YS1iY2QwLTQxYWItYmQ1Ny1iZjg5ZDIyYWViNTIifQ._grdxPlZ0fiz9BHu7etCdf7ZmQ50Rnh1LHF9iOLuM4omUau5Y6J4EeOvADP7iGd7HalH2yjrV-vi9iRxE2cg6Q")
session.cookies.set("__meetup_auth_refresh_token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0NjcwNjU2MDMiLCJhY2Nlc3NfdG9rZW5faWQiOiJmNjQwZjI2YS1iY2QwLTQxYWItYmQ1Ny1iZjg5ZDIyYWViNTIiLCJuYmYiOjE3Mzk3MDc2NjMsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJhY2Nlc3NfdG9rZW5fZXhwaXJhdGlvbl90aW1lX3NlY29uZHMiOjE3Mzk3MTEyNjMsInJlZnJlc2hfdG9rZW5zX2NoYWluX2lkIjoiYjRhNDE1MTYtN2FhYy00ZWFmLTg0MjAtYTZlYmYwNzg4Zjg4IiwiZXhwIjoxNzcxMjQzNjYzLCJpYXQiOjE3Mzk3MDc2NjMsImp0aSI6IjEyMjFhZTM3LTljNmUtNGIxZS1iY2Y4LWI3NmVjZDZkYzJmYSJ9.w999nsrt1yXxkK9QryWKQK86-svhtM-8WkXZgDkoWWAUbK29FVXYd-T3HpeAF8WEMFyi9_87OdLtar02ebDVDw")
session.cookies.set("meetup_language", "language")

# Headers
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
}

def find_events(group):
    """Finds upcoming events for a specific group."""
    print(f"Searching events for group: {group}")
    url = f"{BASE_URL}{group}/events/"

    print("url: ",url)
    
     # Retry mechanism for handling failed requests
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200 and len(response.text) > 100000:
                print("response text length , ",len(response.text))
                # print(response.text)
                print("breaking the loop , status code 200")
                break  # Successful response, exit loop
            else:
                print(f"Attempt {attempt + 1}: Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: Request failed - {e}")
        
        time.sleep(10)  # Wait before retrying
    else:
        print("Failed to fetch events after multiple attempts.")
        return []


    soup = BeautifulSoup(response.text, "html.parser")
    events = []


    # print(soup)
    # print("response : ",response)
    time.sleep(10)
    # print(soup.find_all("a",href=True))
    
    for link in soup.find_all("a", href=True):
        if "/events/" in link["href"]:
            events.append(link["href"])
    
    print(f"Found {len(events)} events for group: {group}")
    return events



def extract_event_venue_ids(page_html):
    """Extracts eventId and venueId from the event page."""
    """Extracts eventId from the event page using XPath."""
    try:
        # Parse the HTML using lxml
        tree = html.fromstring(page_html)
        
        # Extract the text from the second script tag
        script_content = tree.xpath('/html/body/script[2]/text()')
        print(script_content)

        if not script_content:
            print("No script tag found at the given XPath.")
            return None
        
        script_text = script_content[0]

        # Parse JSON inside the script tag
        json_data = json.loads(script_text)

        # Extract eventId
        event_id = json_data.get("props", {}).get("pageProps", {}).get("event", {}).get("id")

        #venue id
        venue_id = json_data.get("props", {}).get("pageProps", {}).get("event", {}).get("venue", {}).get("id")


        print(f"Extracted Event ID: {event_id}")
        print(f"Extracted Venue id {venue_id}")
        return event_id,venue_id
    except Exception as e:
        print(f"Error extracting eventId: {e}")
        return None,None


    

def rsvp_event(event_url):
    """RSVPs to a given event."""
    print(f"Attempting to RSVP for event: {event_url}")
    response = session.get(event_url, headers=HEADERS)
    print(event_url)

    soup = BeautifulSoup(response.text, "html.parser")
    # print("response ",response.text)

    event_id,venue_id, = extract_event_venue_ids(response.text)
    
    

    payload = {
        "operationName": "rsvpToEvent",
        "extensions": {
            "persistedQuery": {
            "version": 1,
            "sha256Hash": "a503eca5efa7aa3924f5397b743f53304da7b2fcf393c105ca466f8b31f6cbd3"
            }
        },
        "variables": {
            "input": {
            "eventId": event_id,
            "response": "YES",
            "proEmailShareOptin": False,
            "venueId": venue_id,
            "eventPromotionId": "0"
            }
        }
     }
    
    print("payload : ",payload)
    
    rsvp_response = session.post(RSVP_URL, headers=HEADERS, json=payload)
    print(f"Response Status Code: {rsvp_response.status_code}")
    print(f"Response Text: {rsvp_response.text}")

    return rsvp_response.status_code == 200
    



if __name__ == "__main__":
    for group in GROUPS:
        events = find_events(group)
        for event in events:
            if rsvp_event(event):
                print(f"Successfully RSVP'd to {event}")
            time.sleep(5)  # Avoid rate limiting

