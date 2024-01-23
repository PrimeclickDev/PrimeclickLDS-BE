import http.client
import json

conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com")
authorization_token = '75dd75c756479ec0b8a148986fd6247e-c712fc66-6d27-4e46-b372-5b12fe56ae1d'

payload = json.dumps({
    "name": "Collect digits",
    "description": "Collect user input and follow default branches",
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
            "playFromUrl": "https://od.lk/s/NTZfMjc5MDk2NThf/ivr_audio4.mp3"
        },

        {
            "collectInto": "myVariable",
            "options": {
                "maxInputLength": 1,
                "timeout": 10,
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
                        "playFromUrl": "https://od.lk/s/NTZfMjc5MDkwNjJf/ivr_audio2.mp3"
                    }
                ],
                "2": [
                    {
                        "playFromUrl": "https://od.lk/s/NTZfMjc5MDkxMjVf/ivr_audio3.mp3"
                    }
                ],
                "__default": [
                    {
                        "say": "You pressed some other key or didn't press any key"
                    }
                ]
            },
            "switch": "myVariable"
        }
    ]
})

headers = {
    'Authorization': 'App ' + authorization_token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

conn.request("POST", "/voice/ivr/1/scenarios", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
