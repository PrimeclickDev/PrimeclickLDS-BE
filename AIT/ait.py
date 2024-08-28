import requests
from backend import settings

def make_voice_call(nums, camp_id):
    from business.models import Campaign, Lead
    url = 'https://voice.africastalking.com/call'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': settings.AIT_API_KEY
    }

    try:
        campaign = Campaign.objects.get(id=camp_id)
        print("----------CAMPAIGN HERE_________", campaign)
    except Campaign.DoesNotExist:
        print(f"Campaign with id {camp_id} does not exist.")
        return

    # Convert list of numbers to a comma-separated string
    numbers_str = ",".join(nums)

    payload = {
        'username': settings.AIT_USERNAME,
        'to': numbers_str,  # List of numbers as a comma-separated string
        'from': "+2347080629896",
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code in [200, 201]:
            print(f"Call initiated successfully for {numbers_str}")
            session_id = response.json().get('entries', [{}])[0].get('sessionId')
            if session_id:
                for num in nums:
                    lead = Lead.objects.filter(campaign=campaign, phone_number=num).first()
                    if lead:
                        lead.session_id = session_id
                        lead.save()
                        print(f"Session ID {session_id} saved for {num}")
        else:
            print(f"Failed to initiate calls. Status code:", response.status_code)
    except requests.RequestException as e:
        print(f"Encountered an error while making the calls: {e}")
