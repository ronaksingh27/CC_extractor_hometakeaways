import requests

# Configuration
RSVP_URL = "https://www.meetup.com/gql2"

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

def rsvp_event(event_id, venue_id="27533193"):
    """RSVPs to a Meetup event."""
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
    
    response = session.post(RSVP_URL, headers=HEADERS, json=payload)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

if __name__ == "__main__":
    rsvp_event("305939343")  # Replace with your event ID
