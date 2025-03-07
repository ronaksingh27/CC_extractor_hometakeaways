import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re
import time

session = requests.Session()
output_file="rehydration.json"


# # Set headers (including User-Agent to mimic a real browser)
# session.headers.update({
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
# })

# Headers
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
}

# Load environment variables from .env file
load_dotenv()

# Set cookies (from environment variables)
cookies = {
    "JSESSIONID": os.getenv("JSESSIONID"),
    "li_at": os.getenv("LI_AT"),
    "bscookie": os.getenv("BSCOOKIE"),
    "bcookie": os.getenv("BCOOKIE"),
    "lidc": os.getenv("LIDC"),
    "timezone": os.getenv("TIMEZONE"),
    "liap": os.getenv("LIAP"),
}

# Set cookies into the session
session.cookies.update(cookies)

# Optional: Set csrf-token (often derived from JSESSIONID)
csrf_token = cookies['JSESSIONID'].strip('"').replace('ajax:', '')  # Extract only the numeric part if needed
session.headers.update({
    "csrf-token": f"ajax:{csrf_token}"
})


def response_text():
    raw_json = "Unkown"
    response = session.get("https://www.linkedin.com/mynetwork/",headers=HEADERS,timeout=10)

    if( len(response.text) < 400000 ):
        response = session.get("https://www.linkedin.com/mynetwork/",headers=HEADERS,timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the <script> tag by its ID
    rehydrate_script = soup.find("script", {"id": "rehydrate-data"})

    if rehydrate_script:
        script_content = rehydrate_script.string

        # Extract the JSON part (strip away the `window.__como_rehydration =` part)
        match = re.search(r'window\.__como_rehydration__\s*=\s*(\[[^\n]+)', script_content)
        
        if match:
            raw_json = match.group(1)

            # Handle any trailing garbage (sometimes the script might have extra after the array)
            raw_json = raw_json.strip().rstrip(';')

            # Optional: Replace escape sequences if needed (depends on data cleanliness)
            raw_json = raw_json.replace(r'\u0026', '&').replace(r'\\"', '"')

            try:
                # parsed_data = json.loads(raw_json)

                # Now you can pretty print or process it further
                # print(json.dumps(parsed_data, indent=2))
                # Ensure file exists (this is redundant in Python since 'w' mode creates it anyway, but adding for clarity)
                # if not os.path.exists(output_file):
                #     open(output_file, 'w').close()

                # # Save the raw JSON string directly to file (as-is, without parsing)
                # with open(output_file, "w", encoding="utf-8") as f:
                #     f.write(raw_json)

                # print(f"Saved raw JSON to {output_file}")

                return raw_json

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                with open("rehydration.json","w",encoding="utf-8") as f:
                    json.dump(raw_json,f,indent=2,ensure_ascii=False)
                print(raw_json)  # For debugging
        else:
            print("Could not locate window.__como_rehydration in script")
    else:
        print("rehydrate-data script not found")
    return raw_json


def get_unique_payloads():
    data = response_text()

    # Regex to match payloads that contain all required fields in any order
    required_fields = [
        "inviteeUrn",
        "nonIterableProfileId",
        "renderMode",
        "firstName",
        "lastName",
        "isDisabled",
        "connectionState",
    ]


    # Extract payload
    payload_matches = re.findall(r'"payload\\"\s*:\s*({.*?{.*?}.*?}.*?}.*?})', data)

    print(f"Total payloads found: {len(payload_matches)}")

    # # Print each payload
    # for index, payload in enumerate(payload_matches, start=1):
    #     print(f"Payload {index}:")
    #     print(payload)
    #     print("-" * 50)

    # print(payload_matches)

    unique_payloads = set()

    for payload_str in payload_matches:
        try:
           
            
            payload_json = ""
            try:
                unescaped_payload = payload_str.encode('utf-8').decode('unicode_escape')
                print(unescaped_payload)
                payload_json = json.loads(unescaped_payload)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")



            # Check if it matches the required structure
            if all(field in payload_json for field in required_fields):
                # Add JSON string to set for automatic deduplication

                print(json.dumps(payload_json, indent=2))
                # payload_json["connectionState"]

                payload_as_str = json.dumps(payload_json, sort_keys=True)
                print(payload_as_str)
                # print(payload_as_str)
                unique_payloads.add(payload_as_str)

        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

    if unique_payloads:
        print(f"✅ Found {len(unique_payloads)} unique valid payloads matching the required format.\n")

        return unique_payloads
        # for i, payload_str in enumerate(unique_payloads, start=1):
        #     payload = json.loads(payload_str)  # Convert back to dict for pretty printing
            # print(f"Payload {i}:")
            # print(json.dumps(payload, indent=2))
            # print("-" * 50)
    else:
        print("❌ No valid payloads found matching the required format.")

    return unique_payloads


# Function to create payload for each profile
def create_payload(profile):
    base_payload = {
        "requestId": "com.linkedin.sdui.requests.mynetwork.addaAddConnection",
        "serverRequest": {
            "$type": "proto.sdui.actions.core.ServerRequest",
            "requestId": "com.linkedin.sdui.requests.mynetwork.addaAddConnection",
            "payload": profile,
            "requestedStates": [],
            "requestedArguments": {
                "$type": "proto.sdui.actions.requests.RequestedArguments",
                "payload": profile,
                "requestedStateKeys": []
            },
            "onClientRequestFailureAction": {
                "actions": [
                    {
                        "$type": "proto.sdui.actions.core.SetState",
                        "value": {
                            "$type": "proto.sdui.actions.core.SetState",
                            "stateKey": "",
                            "stateValue": "",
                            "state": {
                                "$type": "proto.sdui.State",
                                "stateKey": "",
                                "key": {
                                    "$type": "proto.sdui.StateKey",
                                    "value": profile["connectionState"],
                                    "key": {
                                        "$type": "proto.sdui.Key",
                                        "value": {
                                            "$case": "id",
                                            "id": profile["connectionState"]
                                        }
                                    },
                                    "namespace": ""
                                },
                                "value": {
                                    "$case": "stringValue",
                                    "stringValue": "Connect"
                                },
                                "isOptimistic": False
                            },
                            "isOptimistic": False
                        }
                    },
                    {
                        "$type": "proto.sdui.actions.core.SetState",
                        "value": {
                            "$type": "proto.sdui.actions.core.SetState",
                            "stateKey": "",
                            "stateValue": "",
                            "state": {
                                "$type": "proto.sdui.State",
                                "stateKey": "",
                                "key": {
                                    "$type": "proto.sdui.StateKey",
                                    "value": profile["isDisabled"],
                                    "key": {
                                        "$type": "proto.sdui.Key",
                                        "value": {
                                            "$case": "id",
                                            "id": profile["isDisabled"]
                                        }
                                    },
                                    "namespace": ""
                                },
                                "value": {
                                    "$case": "booleanValue",
                                    "booleanValue": False
                                },
                                "isOptimistic": False
                            },
                            "isOptimistic": False
                        }
                    }
                ]
            },
            "isStreaming": False,
            "rumPageKey": ""
        },
        "states": [],
        "requestedArguments": {
            "$type": "proto.sdui.actions.requests.RequestedArguments",
            "payload": profile,
            "requestedStateKeys": [],
            "states": []
        }
    }

    return base_payload


def get_payloads():
    temp = []
    linkedin_payloads = get_unique_payloads()

    # Parse them into proper dictionaries
    profiles = [json.loads(profile) for profile in linkedin_payloads]

    # Generate payloads
    for profile in profiles:
        payload = create_payload(profile)
        print(json.dumps(payload, indent=4))
        temp.append(payload)  # <-- append the actual object, not stringified JSON
        print(f"Saved raw JSON to {output_file}")

    # Clear the file (optional if you want to reset file every time)
    open(output_file, 'w').close()

    # Write as proper JSON array
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(temp, f, indent=4)  # <-- This will format as a clean JSON array


    with open(output_file,'r',encoding='utf-8') as f:
        payloads = json.load(f)

    return temp

LINKEDIN_URL = "https://www.linkedin.com/flagship-web/rsc-action/actions/server-request?sduiid=com.linkedin.sdui.requests.mynetwork.addaAddConnection"

def connect():

    payloads = get_payloads()

    # Loop through all payloads and send POST request for each
    for payload in payloads:
        response = session.post(LINKEDIN_URL,headers=HEADERS, json=payload)

        # Print response for each request
        print(f"Sent request for: {payload.get('serverRequest', {}).get('requestedArguments', {}).get('payload', {}).get('firstName', 'Unknown')}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        print("-" * 50)

        if( response.status_code == 400 ):
            response = session.post(LINKEDIN_URL,headers=HEADERS, json=payload)
            # Print response for each request
            print(f"Sent request for: {payload.get('serverRequest', {}).get('requestedArguments', {}).get('payload', {}).get('firstName', 'Unknown')}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            print("-" * 50)

        names.add(payload.get('serverRequest', {}).get('requestedArguments', {}).get('payload', {}).get('firstName', 'Unknown'))
    print("✅ All requests sent.")


names = set()

for i in range(10):
    print(f"for {i+1}th round")
    time.sleep(2)
    connect()

print(len(names))
print(names)