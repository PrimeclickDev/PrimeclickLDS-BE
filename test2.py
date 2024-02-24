import http.client
import json
conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=15)
authorization_token = ""

payload = json.dumps({
    "name": "Capture speech",
    "description": "Capture users speech and branch the call based on the spoken words.",
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
            "say": "Hello, this is Austin from primeclick. Would you like to continue with the purchase?"
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

conn.request("POST", "/voice/ivr/1/scenarios", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
