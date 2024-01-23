import http.client
import json
from datetime import datetime, timedelta

conn = http.client.HTTPSConnection("8g4mnr.api.infobip.com")
authorization_token = '75dd75c756479ec0b8a148986fd6247e-c712fc66-6d27-4e46-b372-5b12fe56ae1d'


def arrange_nums(qrst):
    nums = [{"to": num} for num in qrst]
    return nums


def launch(nums):
    # Calculate the time 5 minutes from now
    # send_at_time = datetime.now() - timedelta(minutes=58)
    send_at_time = datetime.now() + timedelta(minutes=2)
    send_at_formatted = send_at_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    print(str(send_at_formatted))

    payload = json.dumps({
        "messages": [
            {
                "scenarioId": "5707A84265B0AE452827A78D01A29BD6",
                "from": "12172814794",
                "destinations": nums,
                "notifyUrl": "https://coral-app-kajof.ondigitalocean.app/call-report/",
                "notifyContentType": "application/json",
                "callbackData": "DLR callback data",
                "validityPeriod": 720,
                "sendAt": send_at_formatted,
                "retry": {
                    "minPeriod": 1,
                    "maxPeriod": 5,
                    "maxCount": 5
                },
                "record": False,
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
                        "TUESDAY",
                        "WEDNESDAY",
                    ]
                }
            }
        ]
    })

    headers = {
        'Authorization': 'App ' + authorization_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    conn.request("POST", "/voice/ivr/1/messages", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    # return data


# nummber_queryset = ["2348034489360", "2347083955292", "2348166590317"]
# nums = arrange_nums(nummber_queryset)
# launch(nums)
