import http.client
import json

from backend import settings


def call_delete():
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com")
    authorization_token = settings.INFOBIP_AUTH_TOKEN

    payload = json.dumps({
        "id": "E56E44C8D256532D129440995F66548F"
    })

    headers = {
        'Authorization': 'App ' + authorization_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("DELETE", "/voice/ivr/1/scenarios/{id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    conn.close()
