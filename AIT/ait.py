import requests
from dotenv import load_dotenv
from backend import settings 
import os
load_dotenv()

def make_voice_call(to_numbers):
    url = 'https://voice.africastalking.com/call'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': settings.AIT_API_KEY
    }
    
    payload = {
        'username': settings.AIT_USERNAME,
        'to': to_numbers,
        'from': "+2347080629896",
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201 or response.status_code == 200:
            print("Call initiated successfully")
            # print(payload['to'])
            # Print the response data
            print("Response data:", response.json())
            return response.json()['entries'][0]['sessionId']
        else:
            print("Failed to initiate call. Status code:", response.status_code)
    except Exception as e:
        print("Encountered an error while making the call:", str(e))


# Example usage with your provided numbers
# username = os.getenv("AIT_USERNAME")
# username = settings.AIT_USERNAME
# api_key = os.getenv("AIT_API_KEY")
# api_key = settings.AIT_API_KEY
# from_number = "+2347080629896"
# to_numbers = ["+2348120148527", "+2348166590317", "+2349027538937"]

# make_voice_call(username, api_key, from_number, to_numbers)