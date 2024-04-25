import requests
from dotenv import load_dotenv
from backend.settings import AIT_API_KEY, AIT_USERNAME
import os
load_dotenv()

def make_voice_call(username, api_key, from_number, to_numbers):
    url = 'https://voice.africastalking.com/call'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': api_key
    }
    
    payload = {
        'username': username,
        'to': ','.join(to_numbers),
        'from': from_number,
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201 or response.status_code == 200:
            print("Call initiated successfully")
            # Print the response data
            print("Response data:", response.json())
            # print("Response data:", response.json()['entries'][0]['sessionId'])
        else:
            print("Failed to initiate call. Status code:", response.status_code)
    except Exception as e:
        print("Encountered an error while making the call:", str(e))


# Example usage with your provided numbers
username = os.getenv("AIT_USERNAME")
# username = AIT_USERNAME
api_key = os.getenv("AIT_API_KEY")
# api_key = AIT_API_KEY
from_number = "+2347080629896"
to_numbers = ["+2348120148527", "+2348166590317"]

make_voice_call(username, api_key, from_number, to_numbers)