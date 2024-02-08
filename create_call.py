import http.client
import json

from backend import settings

# audio1 = "https://od.lk/s/NTZfMjc5MDM4Nzhf/Primeclick%20%281%29.mp3"
# audio2 = "https://od.lk/s/NTZfMjc5MDkwNjJf/ivr_audio2.mp3"
# audio3 = "https://od.lk/s/NTZfMjc5MDkxMjVf/ivr_audio3.mp3"


def call(audio1=None, audio2=None, audio3=None):
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
    authorization_token = settings.INFOBIP_AUTH_TOKEN
    # authorization_token = '39f8e3641d7d8e85305a419fc4f79415-795ee287-c1f2-4e4a-861b-0fb8f0a571c8'
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

    conn.request("POST", "/voice/ivr/1/scenarios",
                 payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    print(data)
    print(settings.INFOBIP_AUTH_TOKEN)
    response_data = json.loads(data)

    scenario_id = response_data.get('id')
    # print("Scenario ID:", scenario_id)
    return scenario_id

    conn.close()
