import http.client
import json
from datetime import datetime, timedelta
from backend import settings


def new_call(audio1=None, audio2=None, audio3=None):
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)

    payload = json.dumps({
        "name": "Capture speech or digit",
        "description": "Capture speech or digit",
        "script": [
            {
                "record": 3,
                "options": {
                    "escapeDigits": "123*",
                    "beep": False,
                    "maxSilence": 10,
                    "identifier": "${varName}"
                }
            },
            {
                "playFromUrl": audio1
            },
            {
                "capture": "myVar",
                "timeout": 5,
                "speechOptions": {
                    "language": "en-US",
                    "maxSilence": 3,
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
                "if": "${myVar == 'yes' || myVar == '1}",
                "then": [
                    {
                        "playFromUrl": audio2
                    }
                ],
                "else": [
                    {
                        "if": "${myVar == 'no' || myVar == '2'}",
                        "then": [
                            {
                                "playFromUrl": audio2
                            }
                        ],
                        "else": [
                            {
                                "say": "I did not understand"
                            }
                        ]
                    }
                ]
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


new_call("https://od.lk/s/NTZfMjg0MzYwNjdf/Confirmation%20final.m4a",
         "https://od.lk/s/NTZfMjg0MzYwNzhf/Positive%20repsonse..m4a",
         "https://od.lk/s/NTZfMjg0MzYwOTJf/negative%20response.m4a")
