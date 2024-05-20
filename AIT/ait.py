import requests
from dotenv import load_dotenv
from backend import settings 
import os
load_dotenv()

def make_voice_call(nums, camp_id):
    from business.models import Campaign
    url = 'https://voice.africastalking.com/call'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': settings.AIT_API_KEY
    }

    session_ids = []

    for num in nums:
        payload = {
            'username': settings.AIT_USERNAME,
            'to': num,
            'from': "+2347080629896",
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 201 or response.status_code == 200:
                print(f"Call initiated successfully for {num}")
                session_id = response.json()['entries'][0]['sessionId']
                session_ids.append(session_id)
            else:
                print(f"Failed to initiate call for {num}. Status code:", response.status_code)
        except Exception as e:
            print("Encountered an error while making the call for", num, ":", str(e))

    campaign = Campaign.objects.get(id=camp_id)
    campaign.call_session_id = session_ids[0]
    campaign.save()
    
    return session_ids
