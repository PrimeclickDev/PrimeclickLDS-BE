import http.client
import json

from backend import settings


def call_delete():
    conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com")
    authorization_token = settings.INFOBIP_AUTH_TOKEN
    # authorization_token = '75dd75c756479ec0b8a148986fd6247e-c712fc66-6d27-4e46-b372-5b12fe56ae1d'

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
