import http.client
import json
from datetime import datetime, timedelta
from backend import settings


conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com", timeout=30)
authorization_token = settings.INFOBIP_AUTH_TOKEN


def launch(nums, scenario_id):
    send_at_time = datetime.now() + timedelta(minutes=2)
    day_of_week = send_at_time.strftime("%A").upper()
    send_at_formatted = send_at_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    print(str(send_at_formatted))
    print(str(day_of_week))

    payload = json.dumps({
        "messages": [
            {
                "scenarioId": scenario_id,
                "from": "2347080631313",
                "destinations": nums,
                "notifyUrl": "https://coral-app-kajof.ondigitalocean.app/call-report/",
                "notifyContentType": "application/json",
                "callbackData": "DLR callback data",
                "validityPeriod": 720,
                "sendAt": send_at_formatted,
                "retry": {
                    "minPeriod": 10,
                    "maxPeriod": 10,
                    "maxCount": 3
                },
                "record": True,
                "deliveryTimeWindow": {
                    "from": {
                        "hour": 0,
                        "minute": 30
                    },
                    "to": {
                        "hour": 23,
                        "minute": 59
                    },
                    "days": [

                        day_of_week

                    ]
                },
                "callTimeout": 90
            }
        ]
    })

    headers = {
        'Authorization': 'App ' + authorization_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        conn.request("POST", "/voice/ivr/1/messages", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response_data = json.loads(data)
        print(response_data)
    except Exception as e:
        print(f"Error: {e}")

    conn.close()



