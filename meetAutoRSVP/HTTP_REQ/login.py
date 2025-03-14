import requests
import json
import time

# Configuration
MEETUP_USERNAME = "ronaksingh2708@gmail.com"
MEETUP_PASSWORD = "Borosil@55"
GROUPS = ["mumbai-weekend-events", "group2"]  # List of groups to auto-RSVP
LOGIN_URL = "https://www.meetup.com/gql"
BASE_URL = "https://www.meetup.com/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US",
    "Content-Type": "application/json",
    "Cookie": "MEETUP_BROWSER_ID=id=18b58592-302a-4c0f-bffc-32781a10eace; MEETUP_TRACK=id=12d3e1fb-f53a-471a-80ff-0cee88e235b0; cjConsent=MHxOfDB8Tnww; cjUser=27a086a8-ea86-4f09-b1f0-6eeb5fb5e63d; _scid=ZwXj-PxsaEZ8eJVIT29ALXIar3UDX7Vb; _ScCbts=%5B%5D; _sctr=1%7C1739557800000; _tt_enable_cookie=1; _ttp=YEMk43_Jc1qJDGfvMnaXaHRcL-s.tt.1; _gcl_au=1.1.1857372627.1739641507; _gid=GA1.2.412105399.1739641507; __stripe_mid=86a245ee-fd0d-4ea5-84ec-afe9f6800261baf47c; __qca=P0-189850536-1739641560322; _cc_id=a6c50584f7d81faf1cc92c55d289d9b1; panoramaId_expiry=1739727960442; panoramaId=2629bf4b20dc837a738ed6d1bd87a9fb927adfc23a79f1610e35f60bcd0b2e1e; panoramaIdType=panoDevice; SIFT_SESSION_ID=095a7d2e-20b6-4ae1-af5c-d392c7e249c0; enable_fundraising_pledge_banner_show=true; MEETUP_MEMBER_LOCATION=__typename=LocationSearch&city=Mumbai&country=in&lat=18.959999084472656&lon=72.81999969482422&name=Mumbai%252C+India%252C+meetup1&state=&timeZone=Asia%252FCalcutta&borough=&localizedCountryName=in&neighborhood=&zip=meetup1; _clck=1ohd6pg%7C2%7Cfth%7C0%7C1872; MEETUP_LANGUAGE=language=en&country=US; __Host-NEXT_MEETUP_CSRF=a6995e6a-5d61-427e-96c3-2e677fb433db; ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%2225fab9b7-2a12-1ca7-3c1e-88674bac2abb%22%2C%22c%22%3A1739641545977%2C%22l%22%3A1739696533421%7D; ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22467065603%22%2C%22c%22%3A1739641545979%2C%22l%22%3A1739696533421%7D; _scid_r=c4Xj-PxsaEZ8eJVIT29ALXIar3UDX7VbClddbw; ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%2217934613-76d6-3aa9-07a0-8acd0b1af6f4%22%2C%22e%22%3A1739698482981%2C%22c%22%3A1739696533420%2C%22l%22%3A1739696682981%7D; cto_bundle=173ZMl9UbTgyTk94NVhRV3o1dk5MUnZKbkpjOGdGSDIxcFdiaEZaakZBbDgzc3NqeWhCMGkwOUpGelZsd1pEQTI0YmJpTnFDdTk1dW0lMkZnejBSY2dLNmNUclRxMGFpczJIS21JS1pSWW5HSnVsbnNXbGlYTHpBY3BKNDd5ZyUyQjdGanFldVZpbVo1bTBPR3owb0hCbVZvVDU3RGpRJTNEJTNE; _ga=GA1.2.516834115.1739641507; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Feb+16+2025+14%3A43%3A48+GMT%2B0530+(India+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=deab6928-3207-4e1d-b517-57c8823c93bb&interactionCount=1&landingPath=NotLandingPage&groups=C0005%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false; _uetsid=533d8890ebc411ef944cf5877ac81a22; _uetvid=533d7f30ebc411ef99e24540d0d70005; _dc_gtm_UA-3226337-19=1; _ga_NP82XMKW0P=GS1.1.1739696534.4.1.1739697585.44.0.0"
}

session = requests.Session()

def login():
    """Logs in to Meetup.com"""
    print("Attempting to log in...")
    
    payload = {
        "operationName": "login",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "27c2dcd3fe18741b545abf6918eb37aee203463028503aa8b2b959dc1c7aa007"
            }
        },
        "variables": {
            "input": {
                "email": MEETUP_USERNAME,
                "password": MEETUP_PASSWORD,
                "rememberMe": True
            }
        }
    }
    
    login_response = session.post(LOGIN_URL, headers=HEADERS, json=payload)
    print(f"Response Status Code: {login_response.status_code}")
    print(f"Response Text: {login_response.text}")

    if login_response.status_code == 200:
        print("Login successful")
    else:
        print(f"Login failed: {login_response.status_code}, {login_response.text}")
    
    return login_response.status_code == 200

if __name__ == "__main__":
    if login():
        print("Logged in successfully!")
    else:
        print("Login failed.")
