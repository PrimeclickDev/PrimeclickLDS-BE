import http.client
import json

from backend import settings


def call(audio1=None, audio2=None, audio3=None):
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
    # authorization_token = settings.INFOBIP_AUTH_TOKEN
    authorization_token = "4b1929b91cac7612bb23d8265e60fd97-8e2143f5-de79-42e7-b15d-1b5280f70a07"
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
                "record": 3,
                "options": {
                    "escapeDigits": "123*",
                    "beep": False,
                    "maxSilence": 10,
                    "identifier": "${callRecord}"
                }
            },

            {
                "playFromUrl": audio1
            },
            {
                "capture": "myVar",
                "timeout": 3,
                "speechOptions": {
                    "language": "en-US",
                    "keyPhrases": [
                        "yes", "interested", "no", "not interested", "ok",
                        "sure", "absolutely", "of course", "sure why not?"
                        "Count me in", "Please do", "No", "Not interested",
                        "No, thank you", "I'm not interested", "I'm afraid not", "Absolutely not",
                    ]
                },
                "dtmfOptions": {
                    "maxInputLength": 1
                }
            },
            {
                "if": "${myVar == 'yes' || myVar == '1'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'interested'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'sure, why not?'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'sure'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'of course'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'absolutely'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'ok'}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'no' || myVar == '2'}",
                "then": [
                    {
                        "playFromUrl": audio3
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'not interested' || myVar == '2'}",
                "then": [
                    {
                        "playFromUrl": audio3
                    }
                ],
                "else": []
            },
            {
                "if": "${myVar == 'sorry' || myVar == '2'}",
                "then": [
                    {
                        "playFromUrl": audio3
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
    # print(data)
    response_data = json.loads(data)

    scenario_id = response_data.get('id')
    print("Scenario ID:", scenario_id)
    return scenario_id

    conn.close()


call("https://od.lk/s/NTZfMjg0MzYwNjdf/Confirmation%20final.m4a",
     "https://od.lk/s/NTZfMjg0MzYwNzhf/Positive%20repsonse..m4a", "https://od.lk/s/NTZfMjg0MzYwOTJf/negative%20response.m4a")
