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
    try:
        campaign = Campaign.objects.get(id=camp_id)
        print("----------CAMPAIGN HERE_________", campaign)
    except Campaign.DoesNotExist:
        print(f"Campaign with id {camp_id} does not exist.")
        return session_ids

    for num in nums:
        payload = {
            'username': settings.AIT_USERNAME,
            'to': num,
            'from': "+2347080629896",
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code in [200, 201]:
                print(f"Call initiated successfully for {num}")
                try:
                    session_id = response.json().get('entries', [{}])[0].get('sessionId')
                    if session_id:
                        if campaign.call_session_id:
                            print(f"Existing call session ID: {campaign.call_session_id}")
                        else:
                            campaign.call_session_id = str(session_id)
                            campaign.save()
                            print("New session ID saved to campaign:", campaign.call_session_id)
                        # session_ids.append(session_id)
                    else:
                        print(f"No session ID found in the response for {num}")
                except (IndexError, KeyError, TypeError) as e:
                    print(f"Failed to extract sessionId from response for {num}: {e}")
                    continue
            else:
                print(f"Failed to initiate call for {num}. Status code:", response.status_code)
        except requests.RequestException as e:
            print(f"Encountered an error while making the call for {num}: {e}")

    return session_ids
