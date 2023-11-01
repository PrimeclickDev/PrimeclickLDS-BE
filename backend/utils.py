import requests

from .settings import SENDCHAMP_API_KEY 

def send_email(to_email, otp):
    sendchamp_url = 'https://api.sendchamp.com/api/v1/verification/create'

    headers = {
        'Authorization': f'Bearer {SENDCHAMP_API_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        "channel": "email",
        "sender": "PrimeClick Media",
        "token_type": "numeric",
        "token_length": 4,
        "expiration_time": 5,
        "customer_email_address": to_email,
        "customer_mobile_number": "",
        "meta_data": {},
        "token": otp
    }

    response = requests.request('POST', sendchamp_url, headers=headers, json=payload)
    #     response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    #     return response.json()  # Response data if needed
    # except requests.exceptions.RequestException as e:
    #     # Handle request exceptions (e.g., network errors)
    #     print(f"SendChamp API request failed: {e}")
    #     return None
