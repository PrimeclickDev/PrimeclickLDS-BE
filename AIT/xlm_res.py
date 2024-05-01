
def intro_response(audio1):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    # response += '<Say voice="man">'
    # response += "Welcome to Primeclick Autoleads voice call demo. Please press 1 to continue and 2 to quit."
    # response += '</Say>'
    # response += '<Play url="https://autoleads.s3.eu-north-1.amazonaws.com/Confirmation.mp3">'
    response += '<Play url={audio}>'
    response += '</Play>'
    response += '</GetDigits>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    response += '</Record>'
    response += '</Response>'
    return response


def positive_flow(audio2):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    # response += '<Play url="https://autoleads.s3.eu-north-1.amazonaws.com/Positive.mp3">'
    response += '<Play url={audio2}>'
    response += '</Play>'
    # response += '<Say voice="man">'
    # response += 'Thank you for showing interest in our product. Will be in touch!'
    # response += '</Say>'
    response += '</Response>'
    return response

def negative_flow(audio3):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    # response += '<Play url="https://autoleads.s3.eu-north-1.amazonaws.com/negative.mp3">'
    response += '<Play url={audio3}>'
    response += '</Play>'
    # response += '<Say voice="man">'
    # response += 'Alright! We will keep your record incase we have offers that you may be interested in in the future'
    # response += '</Say>'
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