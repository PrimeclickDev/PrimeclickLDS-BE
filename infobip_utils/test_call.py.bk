import http.client
import json
from backend import settings


def start_call_recording(call_id):
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
    authorization_token = settings.INFOBIP_AUTH_TOKEN
    payload = {
        "enabled": True,
        # Replace this with your recording URL
        "recordingUrl": "https://your-recording-url",
        "recordingChannel": "ALL",  # You can specify 'INBOUND', 'OUTBOUND', or 'ALL'
        "stopOnDTMF": True  # Optionally, you can specify to stop recording on DTMF input
    }
    headers = {
        'Authorization': 'App ' + authorization_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    conn.request(
        "POST", f"/voice/ivr/1/calls/{call_id}/recordings", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    print(data)
    conn.close()


def call(audio1=None, audio2=None, audio3=None):
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
    authorization_token = settings.INFOBIP_AUTH_TOKEN
    payload = json.dumps({
        "name": "Collect Digits",
        "description": "Collect user input and follow default branches for better user experience",
        "script": [
            {
                "request": "https://requestb.in/12345",
                "options": {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/json"
                    },
                    "body": {
                        "payload": "${to} finished the IVR."
                    }
                }
            },

            {
                "playFromUrl": audio1
            },

            {
                "collectInto": "myVariable",
                "options": {
                    "maxInputLength": 1,
                    "timeout": 15,
                    "sendToReports": "ALWAYS",
                    "mappedValues": {
                        "1": "pressed one",
                        "2": "pressed two"
                    }
                }
            },

            {
                "case": {
                    "1": [
                        {
                            "playFromUrl": audio2
                        }
                    ],
                    "2": [
                        {
                            "playFromUrl": audio3
                        }
                    ],
                    "__default": [
                        {
                            "say": "You pressed some other key or didn't press any key yet. Kindly press one or two"
                        }
                    ]
                },
                "switch": "myVariable"
            },

        ]
    })

    headers = {
        'Authorization': 'App ' + authorization_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    conn.request("POST", "/voice/ivr/1/scenarios", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    print(data)
    response_data = json.loads(data)
    scenario_id = response_data.get('id')
    # Start call recording after call initiation
    start_call_recording(response_data['callId'])
    conn.close()
    return scenario_id
