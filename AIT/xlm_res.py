def intro_response(audio1):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    response += f'<Play url="{audio1}">'
    response += '</Play>'
    response += '</GetDigits>'
    # response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    response += '</Record>'
    response += '</Response>'
    return response


def positive_flow(audio2):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += f'<Play url="{audio2}">'
    response += '</Play>'
    response += '</Response>'
    return response


def negative_flow(audio3):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += f'<Play url="{audio3}">'
    response += '</Play>'
    response += '</Response>'
    return response


def record_call():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    response += '</Record>'
    response += '</Response>'
    return response
