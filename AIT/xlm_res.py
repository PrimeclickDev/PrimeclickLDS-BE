def intro_response():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    response += '<Say voice="man">'
    response += "Welcome to Primeclick Autoleads voice demo. Please press 1 to continue and 2 to quit."
    response += '</Say>'
    # response += '<Play url="https://jolly-heisenberg-meninsky.at-internal.com/jocofullinterview41.mp3">'
    # response += '</Play>'
    response += '</GetDigits>'
    response += '</Record>'
    response += '</Response>'
    return response


def positive_flow():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += 'Thank you for showing interest in our product. Will be in touch!'
    response += '</Say>'
    response += '</Response>'
    return response

def negative_flow():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += 'Alright! We will keep your record incase we have offers that you may be interested in in the future'
    response += '</Say>'
    response += '</Response>'
    return response


def record_call():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    # response += '<Say voice="woman">'
    # response += 'Press the pound sign to end the recording'
    # response += '</Say>'
    response += '</Record>'
    response += '</Response>'
    return response