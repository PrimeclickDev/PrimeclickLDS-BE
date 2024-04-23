import requests


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
username = "pmba"
api_key = "85f8738d5a557dd54d5c54cd124b518ad568fc02c9309f402e9953c30d03504a"
from_number = "+2347080629896"
to_numbers = ["+2348120148527"]

make_voice_call(username, api_key, from_number, to_numbers)



def intro_response():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    # response += '<GetDigits numDigits="1" finishOnKey="#" timeout="15" callbackUrl="http://something.com">'
    response += '<Say voice="man">'
    response += "Welcome to Primeclick Autoleads voice demo. We are still working on this. Thanks for your patience."
    response += '</Say>'
    # response += '<Play url="https://od.lk/s/NTZfMjg0MzYwNjdf/Confirmation%20final.m4a">'
    # response += '</Play>'
    # response += '</GetDigits>'
    response += '</Response>'
    return response