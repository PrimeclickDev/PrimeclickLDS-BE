import http.client
import json

from backend import settings


def call():
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
    authorization_token = " "
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
                "record": 10,
                "options": {
                    "escapeDigits": "123*",
                    "beep": True,
                    "maxSilence": 3,
                    "identifier": "${varName}"
                }
            },

            {
                "say": "Say yes or no"
            },
            {
                "capture": "myVar",
                "timeout": 3,
                "speechOptions": {
                    "language": "en-US",
                    "keyPhrases": [
                        "yes",
                        "no"
                    ]
                }
            },
            {
                "if": "${myVar == 'yes'}",
                "then": [
                    {
                        "say": "Ok. I will send you more details"
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'no'}",
                "then": [
                    {
                        "say": "Thank you for listening."
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == ''}",
                "then": [
                    {
                        "say": "I did not understand"
                    }
                ],
                "else": []
            },
            "hangup"
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
    response_data = json.loads(data)

    scenario_id = response_data.get('id')
    # print("Scenario ID:", scenario_id)
    return scenario_id

    conn.close()


call()
