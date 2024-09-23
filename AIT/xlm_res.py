# def intro_response(audio1):
def intro_response(content1): #testing
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="8" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    # response += f'<Play url="{audio1}">'
    # response += '</Play>'
    # response += '<Say voice="man">'
    # response += f"{content1}"
    # response += '</Say>'
    if content1.endswith(('.mp3', '.wav', '.ogg')):  # Simple check for audio file extensions
        response += f'<Play>{content1}</Play>'  # Play audio if it's an audio link
    else:
        response += f'<Say voice="man">{content1}</Say>'
    response += '</GetDigits>'
    response += '</Response>'
    return response


# def positive_record(audio2):
def positive_record(content2):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="20" trimSilence="true" playBeep="true" callbackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    # response += f'<Play url="{audio2}">'
    # response += '</Play>'
    # response += '<Say voice="man">'
    # response += f"{content2}"
    # response += '</Say>'
    if content2.endswith(('.mp3', '.wav', '.ogg')):  # Simple check for audio file extensions
        response += f'<Play>{content2}</Play>'  # Play audio if it's an audio link
    else:
        response += f'<Say voice="man">{content2}</Say>'
    response += '</Record>'
    response += '</Response>'
    return response


def thank_you(content3):
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    if content3.endswith(('.mp3', '.wav', '.ogg')):  # Simple check for audio file extensions
        response += f'<Play>{content3}</Play>'  # Play audio if it's an audio link
    else:
        response += f'<Say voice="man">{content3}</Say>'
    # response += f'<Play url="{audio3}">'
    # response += '</Play>'
    # response += f'<Say voice="man">{content3}</Say>'
    response += '</Response>'
    return response



def handle_inbound():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += "Thank you for calling Autoleads. Our customer support will be in touch. Thanks again!"
    response += '</Say>'
    response += '</Response>'
    return response


# def record_call():
#     response = '<?xml version="1.0"?>'
#     response += '<Response>'
#     response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callBackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
#     response += '</Record>'
#     response += '</Response>'
#     return response