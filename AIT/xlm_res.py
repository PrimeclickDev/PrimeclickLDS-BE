# def intro_response(audio1):
def intro_response(): #testing
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    # response += f'<Play url="{audio1}">'
    # response += '</Play>'
    response += '<Say voice="man">'
    response += "Welcome to Autoleads. We are happy to have you here. Please press 1 to proceed"
    response += '</Say>'
    response += '</GetDigits>'
    response += '</Response>'
    return response


# def positive_record(audio2):
def positive_record():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callbackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'
    # response += f'<Play url="{audio2}">'
    # response += '</Play>'
    response += '<Say voice="man">'
    response += "At the beep please start talking."
    response += '</Say>'
    response += '</Record>'
    response += '</Response>'
    return response


# def thank_you(audio3):
def thank_you(status="success", recording_url=""):
    response = '<?xml version="1.0"?>'
    response += '<Response>'

    # Add the status and recording_url to the response
    response += f'<Status>{status}</Status>'
    response += f'<RecordingUrl>{recording_url}</RecordingUrl>'

    # Original response content
    response += '<Say voice="man">'
    response += "Thank you very much."
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