# def intro_response(audio1):
def intro_response(): #testing
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    # response += f'<Play url="{audio1}">'
    # response += '</Play>'
    response += '<Say voice="woman">'
    response += "Welcome to Voice Memo. Press 1 followed by the pound sign. Press 2 followed by the pound sign to exit."
    response += '</Say>'
    response += '</GetDigits>'
    response += '</Response>'
    return response


def positive_record(audio2):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callbackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    response += f'<Play url="{audio2}">'
    response += '</Play>'
    response += '</Record>'
    response += '</Response>'
    return response


def thank_you(audio3):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += f'<Play url="{audio3}">'
    response += '</Play>'
    response += '</Response>'
    return response


# def record_call():
#     response = '<?xml version="1.0"?>'
#     response += '<Response>'
#     response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
#     response += '</Record>'
#     response += '</Response>'
#     return response